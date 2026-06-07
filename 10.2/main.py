import os
from dotenv import load_dotenv
from flask import Flask, render_template

load_dotenv()

TMDB_TOKEN = os.getenv("TMDB_API_TOKEN")

app = Flask(__name__)


@app.route('/')
def homepage():
    movies = list(range(8))
    return render_template("homepage.html", movies=movies)


if __name__ == '__main__':
    app.run(debug=True)
