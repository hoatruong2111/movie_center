import os
from flask import abort, request, jsonify
from jinja2 import Undefined
from blueprints import routes

from auth import requires_auth

from models import Movie, Review

REVIEW_PER_PAGE = 5


PERMISSON = {
    'CAN_GET_REVIEWS': os.getenv('CAN_GET_REVIEWS'),
    'CAN_POST_MOVIES': os.getenv('CAN_POST_MOVIES'),
    'CAN_POST_REVIEWS': os.getenv('CAN_POST_REVIEWS'),
    'CAN_PATCH_MOVIES': os.getenv('CAN_PATCH_MOVIES'),
    'CAN_DELETE_MOVIES': os.getenv('CAN_DELETE_MOVIES'),
    'CAN_DELETE_REVIEWS': os.getenv('CAN_DELETE_REVIEWS'),
}


def bindReviews(reviews):
    result = []
    for review in reviews:
        item = {
            "id": review.id,
            "username": review.username,
            "movie": review.movie,
            "description": review.description,
        }
        result.append(item)
    return result


@routes.route("/movies/<int:movie_id>/reviews")
@requires_auth(PERMISSON['CAN_GET_REVIEWS'])
def get_review_by_movie(payload, movie_id):
    try:
        result = Review.query.filter(
            movie_id == Review.movie).order_by(Review.id).all()

        if result == []:
            abort(404)

        result = bindReviews(result)

        return jsonify({
            "reviews": result,
            "total_reviews": len(result),
        })
    except Exception as e:
        if e.code == 404:
            abort(404)
        abort(500)


@routes.route("/reviews", methods=['POST'])
@requires_auth(PERMISSON['CAN_POST_REVIEWS'])
def add_Review(payload):
    try:
        body = request.get_json()
        new_username = body.get("username")
        new_movie = body.get("movie")
        new_description = body.get("description")

        movie = Movie.query.filter(
            new_movie == Movie.title).first()

        review = Review(
            username=new_username,
            movie=movie.id,
            description=new_description)

        if new_username == '' or new_description == '':
            abort(422)

        review.insert()

        return jsonify(
            {
                "success": True,
                "status": 200
            }
        )

    except Exception as e:
        abort(422)


@routes.route("/reviews/<int:review_id>", methods=['DELETE'])
@requires_auth(PERMISSON['CAN_DELETE_REVIEWS'])
def delete_review(payload, review_id):
    try:
        review = Review.query.filter(
            Review.id == review_id).one_or_none()

        if review is None:
            abort(404)

        review.delete()

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
