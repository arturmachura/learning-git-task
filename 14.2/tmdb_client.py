import os
import requests
from dotenv import load_dotenv

load_dotenv()

TMDB_TOKEN = os.getenv("TMDB_API_TOKEN")
TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_BASE_URL = "https://image.tmdb.org/t/p/"

MOVIE_LISTS = ["popular", "top_rated", "now_playing", "upcoming"]


def call_tmdb_api(endpoint, **params):
    url = f"{TMDB_BASE_URL}/{endpoint}"
    params["api_key"] = TMDB_TOKEN
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def get_movies(how_many=8, list_type="popular"):
    data = call_tmdb_api(f"movie/{list_type}")
    return data["results"][:how_many]


def get_single_movie(movie_id):
    return call_tmdb_api(f"movie/{movie_id}")


def get_movie_images(movie_id):
    return call_tmdb_api(f"movie/{movie_id}/images")


def get_single_movie_cast(movie_id):
    data = call_tmdb_api(f"movie/{movie_id}/credits")
    return data["cast"]


def get_poster_url(path, size="w342"):
    return f"{TMDB_IMAGE_BASE_URL}{size}{path}"
