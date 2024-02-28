from flask import jsonify, make_response, Response, request
import psycopg
from typing import Any, Callable, Optional
from flask_caching import Cache
import os

CONN_INFO = {'default': {
    "dbname": os.environ.get("DB_NAME"),
    "user": os.environ.get("DB_USER"),
    "password": os.environ.get("DB_PASSWORD"),
    "host": os.environ.get("DB_HOST"),
    "port": os.environ.get("DB_PORT")
}, 
'personality' : {
    "dbname": os.environ.get("PERSONALITY_DB_NAME"),
    "user": os.environ.get("PERSONALITY_DB_USER"),
    "password": os.environ.get("PERSONALITY_DB_PASSWORD"),
    "host": os.environ.get("PERSONALITY_DB_HOST"),
    "port": os.environ.get("PERSONALITY_DB_PORT")
}}

CACHE_SETTINGS = {
    "CACHE_TYPE": "RedisCache",
    "CACHE_REDIS_HOST": os.environ.get("CACHE_HOST"),
    "CACHE_REDIS_PORT": os.environ.get("CACHE_PORT"),
    "CACHE_REDIS_PASSWORD": os.environ.get("CACHE_PASSWORD"),
    "CACHE_DEFAULT_TIMEOUT": os.environ.get("CACHE_TIMEOUT")
}

# register cache
cache = Cache(config=CACHE_SETTINGS)


@cache.memoize()
def execute_query(query: str, params: Optional[dict], conn_name: Optional[str]='default') -> list[tuple]:
    with psycopg.connect(**CONN_INFO[conn_name]) as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            results = cursor.fetchall()

    conn.close()
    return results


def get_response(
    query: str,
    params: Optional[dict] = None,
    func: Callable[[tuple], Any] = lambda row: row[0],
    conn_name: Optional[str]='default'
) -> Response:
    try:
        results = execute_query(query, params, conn_name=conn_name)
        return make_response(jsonify(list(map(func, results))), 200)
    except Exception as error:
        print(f"error: {str(error)}")
        return make_response(jsonify({"error": str(error)}), 500)
