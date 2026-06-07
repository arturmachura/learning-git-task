import os
import requests
from dotenv import load_dotenv

load_dotenv()

TMDB_TOKEN = os.getenv("TMDB_API_TOKEN")
TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_BASE_URL = "https://image.tmdb.org/t/p/"

MOVIE_LISTS = ["popular", "top_rated", "now_playing", "upcoming"]


def get_movies(how_many=8, list_type="popular"):
    url = f"{TMDB_BASE_URL}/movie/{list_type}"
    response = requests.get(url, params={"api_key": TMDB_TOKEN})
    response.raise_for_status()
    data = response.json()
    return data["results"][:how_many]


def get_poster_url(path, size="w342"):
    return f"{TMDB_IMAGE_BASE_URL}{size}{path}"
