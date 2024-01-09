from flask import Flask, jsonify
from flask_cors import CORS, cross_origin 
import psycopg2
from flask import request

app = Flask(__name__)
app = Flask(__name__)
cors = CORS(app)
app = Flask(__name__)
cors = CORS(app, origins="*")
app.config['CORS_HEADERS'] = 'Content-Type'

db_params = {
    'dbname': 'comp0022',
    'user': 'admin',
    'password': 'top_secret_password',
    'host': 'database',
    'port': '5432'
}

def execute_query(query):
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return result

@app.route("/")
@cross_origin()
def hello_world():
    return 'Hello, World!'

@cross_origin()
@app.route('/get-search-results', methods=['POST'])
def get_search_results():
    try:
        data = request.get_json()
        searchText = data.get('searchText', '')
        ratings = data.get('ratings', [0, 10])
        tags = data.get('tags', [])
        genres = data.get('genres', [])
        # Mock data for testing purposes
        result_data = [{
            'imageUrl': 'https://resizing.flixster.com/dV1vfa4w_dB4wzk7A_VzThWUWw8=/ems.cHJkLWVtcy1hc3NldHMvbW92aWVzLzEyZDMyYjZmLThmNzAtNDliNC1hMjFmLTA2ZWY4M2UyMjJhMi5qcGc=',
            'title': 'Server is UP',
            'rating': 5,
            'genre': 'Bar',
            'tags': ['bla'],
            'ratingsList': [1, 2, 3, 4, 5]
        } for _ in range(10)]
        return jsonify(result_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@cross_origin()
@app.route('/movies/popular', methods=['GET'])
def get_popular_movies():
    try:
        result_data = [{
            'imageUrl': 'https://resizing.flixster.com/dV1vfa4w_dB4wzk7A_VzThWUWw8=/ems.cHJkLWVtcy1hc3NldHMvbW92aWVzLzEyZDMyYjZmLThmNzAtNDliNC1hMjFmLTA2ZWY4M2UyMjJhMi5qcGc=',
            'title': 'Server is UP',
            'rating': 5,
            'genre': 'Bar',
            'tags': ['bla'],
            'ratingsList': [1, 2, 3, 4, 5]
        } for _ in range(10)]
        return jsonify(result_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@cross_origin()
@app.route('/movies/contrevertial', methods=['GET'])
def get_controvertial_movies():
    try:
        result_data = [{
            'imageUrl': 'https://resizing.flixster.com/dV1vfa4w_dB4wzk7A_VzThWUWw8=/ems.cHJkLWVtcy1hc3NldHMvbW92aWVzLzEyZDMyYjZmLThmNzAtNDliNC1hMjFmLTA2ZWY4M2UyMjJhMi5qcGc=',
            'title': 'Server is UP',
            'rating': 5,
            'genre': 'Bar',
            'tags': ['bla'],
            'ratingsList': [1, 2, 3, 4, 5]
        } for _ in range(10)]
        return jsonify(result_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@cross_origin()
@app.route('/user-skew', methods=['POST'])
def calculate_users_skew():
    try:
        data = request.get_json()
        genres = data.get('genres')
        films = data.get('films')
        users = data.get('users')

        if users and (films or genres):
            skew_result = "higher"  # Replace with your actual skew calculation
            return jsonify(skew_result)
        else:
            return jsonify({'error': 'Please provide at least one user and one film or genre.'}), 400

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@cross_origin()
@app.route('/movie-pred', methods=['POST'])
def movie_prediction():
    try:
        data = request.get_json()
        tags = data.get('tags', [])
        users = data.get('users', [])
        ratings = data.get('ratings', [0, 10])
        if tags or users or ratings:
            rating = 4.37
            return jsonify(rating)
        else:
            return jsonify({'error': 'Please provide at least one user and one film or genre.'}), 400

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@cross_origin()
@app.route('/personality-skew', methods=['POST'])
def calculate_personalities_skew():
    try:
        data = request.get_json()
        genre = data.get('genre')
        personality = data.get('personality')

        if personality and genre:
            skew_result = "higher"
            return jsonify(skew_result)
        else:
            return jsonify({'error': 'Please provide at least one user and one film or genre.'}), 400

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@cross_origin()
@app.route('/genre-autocomplete', methods=['GET'])
def genre_autocomplete():
    sample_genres = ['Action', 'Comedy', 'Drama', 'Horror', 'Science Fiction']
    try:
        # limit to five and replace with a sql query
        prefix = request.args.get('prefix', '').lower()
        matches = [genre for genre in sample_genres if genre.lower().startswith(prefix)]
        return jsonify(matches)
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@cross_origin()
@app.route('/tags-autocomplete', methods=['GET'])
def tags_autocomplete():
    # limit to five and replace with a sql query
    sample_tags = ['Adventure', 'Romance', 'Thriller', 'Fantasy', 'Mystery']
    try:
        prefix = request.args.get('prefix', '').lower()
        matches = [tag for tag in sample_tags if tag.lower().startswith(prefix)]
        return jsonify(matches)
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500
    
@cross_origin()
@app.route('/films-autocomplete', methods=['GET'])
def films_autocomplete():
    # Replace this with actual data retrieval logic from your database
    sample_films = ['Film1', 'Film2', 'Film3', 'Film4', 'Film5']
    try:
        prefix = request.args.get('prefix', '').lower()
        matches = [film for film in sample_films if film.lower().startswith(prefix)]
        return jsonify(matches)
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@cross_origin()
@app.route('/users-autocomplete', methods=['GET'])
def users_autocomplete():
    # Replace this with actual data retrieval logic from your database
    sample_users = ['User1', 'User2', 'User3', 'User4', 'User5']
    try:
        prefix = request.args.get('prefix', '').lower()
        matches = [user for user in sample_users if user.lower().startswith(prefix)]
        return jsonify(matches)
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500
    
@cross_origin()
@app.route('/personalities-autocomplete', methods=['GET'])
def personalities_autocomplete():
    # Replace this with actual data retrieval logic from your database
    sample_personalities = ['Introvert', 'Extrovert', 'Ambivert']
    try:
        prefix = request.args.get('prefix', '').lower()
        matches = [user for user in sample_personalities if user.lower().startswith(prefix)]
        return jsonify(matches)
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5555, host='0.0.0.0')
