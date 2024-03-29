from .common import get_response, transform_response
from flasgger import swag_from
from flask import Blueprint, Response, request
from typing import Callable

app = Blueprint("ratings", __name__)


def movie_avg_rating(subset: bool) -> str:
    query = """
        (
            SELECT
                AVG(r.rating)
            FROM
                ratings r
            INNER JOIN
                movies m ON r.movie_id = m.movie_id
            WHERE
    """

    if subset:
        query += """
                r.user_id = ANY(%(users)s) AND
        """

    query += """
                m.title = %(movie)s
        )
    """

    return query


def user_avg_rating(subset: bool) -> str:
    query = """
        (
            SELECT
                AVG(avg_rating)
            FROM (
                SELECT
                    AVG(r.rating) AS avg_rating
                FROM
                    ratings r
    """

    if subset:
        query += """
                WHERE
                    r.user_id = ANY(%(users)s)
        """

    query += """
                GROUP BY
                    r.user_id
            )
        )
    """

    return query


def genre_avg_rating(subset: bool) -> str:
    query = """
        (
            SELECT
                AVG(r.rating)
            FROM
                ratings r
            INNER JOIN
                movies_genres mg ON r.movie_id = mg.movie_id
            WHERE
    """

    if subset:
        query += """
                r.user_id = ANY(%(users)s) AND
        """

    query += """
                mg.genre_id IN (
                    SELECT
                        mg.genre_id
                    FROM
                        movies_genres mg
                    INNER JOIN
                        movies m ON mg.movie_id = m.movie_id
                    WHERE
                        m.title = %(movie)s
                )
        )
    """

    return query


def tag_avg_rating(subset: bool) -> str:
    query = """
        (
            SELECT
                AVG(r.rating)
            FROM
                ratings r
            INNER JOIN
                movies_users_tags mut ON r.movie_id = mut.movie_id AND r.user_id = mut.user_id
            WHERE
    """

    if subset:
        query += """
                r.user_id = ANY(%(users)s) AND
        """

    query += """
                mut.tag_id IN (
                    SELECT
                        DISTINCT mut.tag_id
                    FROM
                        movies_users_tags mut
                    INNER JOIN
                        movies m ON mut.movie_id = m.movie_id
                    WHERE
                        m.title = %(movie)s
                )
        )
    """

    return query


def bias(func: Callable[[bool], str]) -> str:
    return f"""
        (
            SELECT
                COALESCE (
                    {func(False)} / {func(True)},
                    1
                )
        )
    """


@app.route("/prediction", methods=["POST"])
@swag_from(
    {
        "tags": ["Prediction"],
        "description": "Generates a prediction for a movie rating based on user, genre, and tag biases.",
        "parameters": [
            {
                "name": "movie",
                "in": "body",
                "required": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "movie": {
                            "type": "string",
                            "description": "Movie title for which the prediction is requested.",
                        },
                        "users": {
                            "type": "array",
                            "items": {"type": "integer"},
                            "description": "List of user IDs for bias calculation.",
                        },
                    },
                    "example": {"movie": "Inception", "users": [1, 2, 3]},
                },
                "description": "JSON payload containing the movie title and a list of user IDs.",
            }
        ],
        "responses": {
            200: {
                "description": "The predicted rating for the movie based on biases.",
                "examples": {
                    "application/json": {
                        "averageRating": 4.5,
                        "subsetRating": 4.2,
                        "userBias": 1.05,
                        "genreBias": 1.09,
                        "tagBias": 1,
                        "averageBias": 1.07,
                        "predictedRating": 4.494,
                    }
                },
            }
        },
    }
)
def get_prediction() -> Response:
    return transform_response(
        get_response(
            f"""
            SELECT
                {movie_avg_rating(False)} AS average_rating,
                subset_rating,
                user_bias,
                genre_bias,
                tag_bias,
                (user_bias + genre_bias + tag_bias) / 3 AS average_bias,
                subset_rating * (user_bias + genre_bias + tag_bias) / 3 AS predicted_rating
            FROM (
                SELECT
                    {movie_avg_rating(True)} AS subset_rating,
                    {bias(user_avg_rating)} AS user_bias,
                    {bias(genre_avg_rating)} AS genre_bias,
                    {bias(tag_avg_rating)} AS tag_bias
            )
            ;
            """,
            params={
                "movie": request.json.get("movie", ""),
                "users": request.json.get("users", []),
            },
            func=lambda row: {
                "averageRating": row[0],
                "subsetRating": row[1],
                "userBias": row[2],
                "genreBias": row[3],
                "tagBias": row[4],
                "averageBias": row[5],
                "predictedRating": row[6],
            },
        )
    )
