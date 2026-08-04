from flask import Flask, jsonify, request, abort
from library import Movie, Series
from data import load_initial_data

app = Flask(__name__)

library = []
load_initial_data(library)


def find_by_id(item_id):
    return next((item for item in library if item.id == item_id), None)


def parse_int_field(body, key):
    try:
        return int(body[key])
    except (TypeError, ValueError):
        abort(400, description=f"Field '{key}' must be an integer.")


# --- Movies ---

@app.route("/api/movies", methods=["GET"])
def get_movies():
    movies = sorted(
        [item for item in library if isinstance(item, Movie)],
        key=lambda x: x.title,
    )
    return jsonify([m.to_dict() for m in movies])


@app.route("/api/movies/<int:item_id>", methods=["GET"])
def get_movie(item_id):
    item = find_by_id(item_id)
    if not item or not isinstance(item, Movie):
        abort(404)
    return jsonify(item.to_dict())


@app.route("/api/movies", methods=["POST"])
def add_movie():
    body = request.get_json()
    if not body or not all(k in body for k in ("title", "year", "genre")):
        abort(400)
    movie = Movie(body["title"], parse_int_field(body, "year"), body["genre"])
    library.append(movie)
    return jsonify(movie.to_dict()), 201


@app.route("/api/movies/<int:item_id>", methods=["DELETE"])
def delete_movie(item_id):
    item = find_by_id(item_id)
    if not item or not isinstance(item, Movie):
        abort(404)
    library.remove(item)
    return jsonify({"deleted": item_id}), 200


# --- Series ---

@app.route("/api/series", methods=["GET"])
def get_series():
    series = sorted(
        [item for item in library if isinstance(item, Series)],
        key=lambda x: (x.title, x.season, x.episode),
    )
    return jsonify([s.to_dict() for s in series])


@app.route("/api/series/<int:item_id>", methods=["GET"])
def get_series_episode(item_id):
    item = find_by_id(item_id)
    if not item or not isinstance(item, Series):
        abort(404)
    return jsonify(item.to_dict())


@app.route("/api/series", methods=["POST"])
def add_series_episode():
    body = request.get_json()
    required = ("title", "year", "genre", "season", "episode")
    if not body or not all(k in body for k in required):
        abort(400)
    episode = Series(
        body["title"], parse_int_field(body, "year"), body["genre"],
        parse_int_field(body, "season"), parse_int_field(body, "episode"),
    )
    library.append(episode)
    return jsonify(episode.to_dict()), 201


@app.route("/api/series/season", methods=["POST"])
def add_season():
    body = request.get_json()
    required = ("title", "year", "genre", "season", "episodes_count")
    if not body or not all(k in body for k in required):
        abort(400)
    added = []
    for ep in range(1, parse_int_field(body, "episodes_count") + 1):
        episode = Series(
            body["title"], parse_int_field(body, "year"), body["genre"],
            parse_int_field(body, "season"), ep,
        )
        library.append(episode)
        added.append(episode.to_dict())
    return jsonify(added), 201


@app.route("/api/series/<int:item_id>", methods=["DELETE"])
def delete_series_episode(item_id):
    item = find_by_id(item_id)
    if not item or not isinstance(item, Series):
        abort(404)
    library.remove(item)
    return jsonify({"deleted": item_id}), 200


# --- Shared ---

@app.route("/api/play/<int:item_id>", methods=["POST"])
def play(item_id):
    item = find_by_id(item_id)
    if not item:
        abort(404)
    item.play()
    return jsonify({"id": item_id, "plays": item.plays})


@app.route("/api/top", methods=["GET"])
def top_titles():
    try:
        count = int(request.args.get("count", 5))
    except ValueError:
        abort(400, description="Query parameter 'count' must be an integer.")
    content_type = request.args.get("type")

    if content_type == "movie":
        pool = [item for item in library if isinstance(item, Movie)]
    elif content_type == "series":
        pool = [item for item in library if isinstance(item, Series)]
    else:
        pool = list(library)

    top = sorted(pool, key=lambda x: x.plays, reverse=True)[:count]
    return jsonify([item.to_dict() for item in top])


@app.route("/api/search", methods=["GET"])
def search():
    query = request.args.get("q", "").lower()
    results = [item for item in library if query in item.title.lower()]
    return jsonify([item.to_dict() for item in results])


if __name__ == "__main__":
    app.run(debug=True)
