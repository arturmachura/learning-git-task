import os
from dotenv import load_dotenv
from flask import Flask, render_template, request
import tmdb_client

load_dotenv()

app = Flask(__name__)


@app.context_processor
def utility_processor():
    def tmdb_image_url(path, size="w342"):
        return tmdb_client.get_poster_url(path, size)
    return {"tmdb_image_url": tmdb_image_url}


@app.route('/')
def homepage():
    list_type = request.args.get("list_type", "popular")
    if list_type not in tmdb_client.MOVIE_LISTS:
        list_type = "popular"
    movies = tmdb_client.get_movies(how_many=8, list_type=list_type)
    return render_template(
        "homepage.html",
        movies=movies,
        current_list=list_type,
        movie_lists=tmdb_client.MOVIE_LISTS,
    )


if __name__ == '__main__':
    app.run(debug=True)
