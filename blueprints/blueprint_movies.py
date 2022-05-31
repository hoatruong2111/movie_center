import os
from flask import abort, jsonify, request
from sqlalchemy import func
from auth import requires_auth

from models import Movie
from blueprints import routes

PERMISSON = {
    'CAN_GET_REVIEWS': os.getenv('CAN_GET_REVIEWS'),
    'CAN_POST_MOVIES': os.getenv('CAN_POST_MOVIES'),
    'CAN_POST_REVIEWS': os.getenv('CAN_POST_REVIEWS'),
    'CAN_PATCH_MOVIES': os.getenv('CAN_PATCH_MOVIES'),
    'CAN_DELETE_MOVIES': os.getenv('CAN_DELETE_MOVIES'),
    'CAN_DELETE_REVIEWS': os.getenv('CAN_DELETE_REVIEWS'),
}


def bindMovies(movies):
    result = []
    for movie in movies:
        item = {
            "id": movie.id,
            "title": movie.title,
            "year": movie.year,
            "genre": movie.genre,
            "language": movie.language,
            "director": movie.director,
            "actors": movie.actors,
            "poster_link": movie.poster_link,
            "writer": movie.writer,
            'description': movie.description

        }
        result.append(item)
    return result

# get movie endpoint


@routes.route('/movies', methods=['GET'])
def get_movies():
    try:
        selection = Movie.query.all()
        movies = bindMovies(selection)

        return jsonify(
            {
                "success": True,
                "movies": movies,
                "total_movies": len(selection),
            }
        )
    except Exception as e:
        abort(422)

# add movie endpoint


@routes.route("/movies", methods=['POST'])
@requires_auth(PERMISSON['CAN_POST_MOVIES'])
def add_movie(payload):
    try:
        body = request.get_json()
        new_title = body.get("title")
        new_year = body.get("year")
        new_genre = body.get("genre")
        new_language = body.get("language")
        new_director = body.get("director")
        new_actors = body.get("actors")
        new_poster_link = body.get("poster_link")
        new_writer = body.get("writer")
        new_description = body.get("description")

        movie = Movie(
            title=new_title,
            year=new_year,
            genre=new_genre,
            language=new_language,
            director=new_director,
            actors=new_actors,
            poster_link=new_poster_link,
            writer=new_writer,
            description=new_description)

        if new_title == '':
            abort(422)

        movie.insert()

        return jsonify(
            {
                "success": True,
                "status": 200
            }
        )

    except Exception as e:
        abort(422)

# edit movie endpoint


@routes.route("/movies/<int:movie_id>", methods=['PATCH'])
@requires_auth(PERMISSON["CAN_PATCH_MOVIES"])
def update_movie(payload, movie_id):
    try:
        body = request.get_json()
        new_title = body.get("title")
        new_year = body.get("year")
        new_genre = body.get("genre")
        new_language = body.get("language")
        new_director = body.get("director")
        new_actors = body.get("actors")
        new_poster_link = body.get("poster_link")
        new_writer = body.get("writer")
        new_description = body.get("description")

        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

        # if not, send 404
        if movie.id == '':
            abort(404)

        movie.title = new_title
        movie.year = new_year
        movie.genre = new_genre
        movie.language = new_language
        movie.director = new_director
        movie.actors = new_actors
        movie.poster_link = new_poster_link
        movie.writer = new_writer
        movie.description = new_description

        movie.update()
        result = bindMovies([movie])
        return jsonify({
            "success": True,
            "drinks": result
        }
        )

    except Exception as e:
        if e.code == 404:
            abort(404)
        abort(500)

# delete movie endpoint


@routes.route("/movies/<int:movie_id>", methods=['DELETE'])
@requires_auth(PERMISSON['CAN_DELETE_MOVIES'])
def delete_movie(payload, movie_id):
    try:
        movie = Movie.query.filter(
            Movie.id == movie_id).one_or_none()

        if movie is None:
            abort(404)

        movie.delete()

        return jsonify(
            {
                "success": True,
                "msg": "deleted"
            }
        )
    except Exception as e:
        if e.code == 404:
            abort(404)
        abort(500)
