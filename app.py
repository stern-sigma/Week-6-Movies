'Basic server to respond to api calls to the database'
#pylint: disable=unused-variable
from datetime import datetime
from flask import Flask, request
from database import get_movies, get_movie_by_id, create_movie, delete_movie, get_movie_by_country


app = Flask(__name__)


def validate_sort_by(sort_by):
    '''Return if sort query is valid'''
    return sort_by in {'movie_id', 'title', 'score', 'budget', 'revenue'}


def validate_sort_order(order_by):
    '''Return if order query is valid'''
    return order_by in {'asc', 'desc'}


@app.route("/", methods=["GET"])
def endpoint_index():
    'Handles the index endpoint'
    return {"message": "Welcome to the Movie API"}, 200


@app.route("/movies", methods=["GET", "POST"])
def endpoint_get_movies(): #pylint: disable=too-many-locals,too-many-return-statements
    'Handles the movies endpoint'

    if request.method == "GET":
        sort_by = request.args.get("sort_by")
        sort_order = request.args.get("sort_order")
        search = request.args.get("search")
        print(search)
        if sort_by and not validate_sort_by(sort_by):
            return {"error": "Invalid sort_by parameter"}, 400

        if sort_order and not validate_sort_order(sort_order):
            return {"error": "Invalid sort_order parameter"}, 400

        movies = get_movies(search, sort_by, sort_order)

        if not movies:
            return {"error": "No movies found"}, 404

        return movies, 200

    data = request.json
    title = data["title"]
    release_date = data["release_date"]
    genre = data["genre"]
    overview: str = data.get("overview", "")
    status = data.get("status", "released")
    budget: int = data.get("budget", 0)
    revenue: int = data.get("revenue", 0)
    country: str = data.get("country")
    language: str = data.get("language")
    orig_title: str = data.get("orig_title")

    if not title or not release_date or not genre or not country or not language:
        return {"error": "Missing required fields"}, 400

    try:
        datetime.strptime(release_date, "%m/%d/%Y")
    except ValueError:
        return {"error": "Invalid release_date format. Please use MM/DD/YYYY"}, 400

    try:
        movie = create_movie(
            title, release_date, genre, overview, status, budget,
            revenue, country, language, orig_title)
        return {'success': True, "movie": movie}, 201
    except (TypeError, ValueError) as e:
        return {"error": str(e)}, 500


@app.route("/movies/<int:movie_id>", methods=["GET", "PATCH", "DELETE"])
def endpoint_get_movie(movie_id: int):
    'Handles the mvoies/id endpoint'
    if request.method == "GET":

        movie = get_movie_by_id(movie_id)

        if not movie:
            return {"error": "Movie not found"}, 404

        return movie, 200

    success = delete_movie(movie_id)

    if not success:
        return {"error": "Movie could not be deleted"}, 404

    return {"message": "Movie deleted"}, 200


@app.route("/countries/<string:country_code>", methods=["GET"])
def endpoint_get_movies_by_country(country_code: str):
    """Get a list of movie details by country. 
    Optionally, the results can be sorted by a specific field in ascending or descending order."""

    sort_by = request.args.get("sort_by")
    sort_order = request.args.get("sort_order")

    if not validate_sort_by(sort_by):
        return {"error": "Invalid sort_by parameter"}, 400

    if not validate_sort_order(sort_order):
        return {"error": "Invalid sort_order parameter"}, 400

    movies = get_movie_by_country(country_code, sort_by, sort_order)

    if not movies:
        return {"error": "No movies found for this country"}, 404

    return movies


if __name__ == "__main__":
    app.config['TESTING'] = True
    app.config['DEBUG'] = True
    app.run(debug=True, host="0.0.0.0", port=5000)
