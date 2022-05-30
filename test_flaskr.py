import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import random
from app import *
from models import Movie, Review, setup_db
from blueprints import routes


DATABASE_TEST_PATH = os.getenv('DATABASE_TEST_PATH')
MANAGER_TOKEN = os.getenv('MANAGER_TOKEN')

PERMISSON = {
    'CAN_GET_REVIEWS': os.getenv('CAN_GET_REVIEWS'),
    'CAN_POST_MOVIES': os.getenv('CAN_POST_MOVIES'),
    'CAN_POST_REVIEWS': os.getenv('CAN_POST_REVIEWS'),
    'CAN_PATCH_MOVIES': os.getenv('CAN_PATCH_MOVIES'),
    'CAN_DELETE_MOVIES': os.getenv('CAN_DELETE_MOVIES'),
    'CAN_DELETE_REVIEWS': os.getenv('CAN_DELETE_REVIEWS'),
}


class MovieTestCase(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.client = self.app.test_client
        self.database_path = DATABASE_TEST_PATH

        setup_db(self.app, self.database_path)

        self.app.register_blueprint(routes)
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_movie = {
            "title": f"title {random.random()}",
            "year": "2015",
            "genre": "Action",
            "language": "American",
            "director": "director",
            "actors": "actors",
            "poster_link": "https://www.imdb.com/title/tt3316948/mediaviewer/rm2256332800/?ref_=tt_ov_i",
            "writer": "writer",
            "description": "description"
        }
        self.new_movie_1 = {"title": "",
                            "year": "2015",
                            "genre": "Action",
                            "language": "American",
                            "director": "director",
                            "actors": "actors",
                            "poster_link": "https://www.imdb.com/title/tt3316948/mediaviewer/rm2256332800/?ref_=tt_ov_i",
                            "writer": "writer",
                            "description": "description"}

        self.new_review = {
            'username': 'abc',
            'movie': 1,
            'description': 'description'
        }

        self.new_review_1 = {
            'username': f"username {random.random()}",
            'movie': 1,
            'description': 'description'
        }

        self.headers = {'Authorization': MANAGER_TOKEN}

    def tearDown(self):
        pass

    def test_create_new_movie(self):
        res = self.client().post("/movies", json=self.new_movie, headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_create_new_review(self):
        find_movie = Movie.query.all()
        self.new_review['movie'] = find_movie[0].title
        res = self.client().post("/reviews", json=self.new_review, headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_get_movies(self):
        res = self.client().get("/movies")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["movies"])
        self.assertTrue(data["total_movies"])

    def test_get_review_by_movie(self):
        res = self.client().get("/movies/1/reviews", headers=self.headers)

        self.assertEqual(res.status_code, 200)

# Error
    def test_422_if_movie_creation_not_allowed(self):
        res = self.client().post("/questions", json=self.new_movie_1)

    def test_422_if_review_creation_not_allowed(self):
        res = self.client().post("/reviews", json=self.new_review_1, headers=self.headers)

        self.assertEqual(res.status_code, 422)

    def test_422_if_get_review_by_movie_not_success(self):
        res = self.client().get("/movies/''/reviews", headers=self.headers)

        self.assertEqual(res.status_code, 404)

    def test_422_if_delete_movie_not_success(self):
        res = self.client().delete("/movies/0", headers=self.headers)

        self.assertEqual(res.status_code, 404)

    def test_422_if_delete_movie_not_success(self):
        res = self.client().delete("/reviews/0", headers=self.headers)

        self.assertEqual(res.status_code, 422)

# delete
# note: You should comment test_delete_review and test_delete_review when run the first time

    # def test_delete_review(self):
    #     find_review = Review.query.all()
    #     res = self.client().delete(
    #         "/reviews/{}".format(find_review[0].id), headers=self.headers)
    #     review = Review.query.filter(
    #         Review.id == find_review[0].id).one_or_none()

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(review, None)

    # def test_delete_review(self):
    #     find_movie = Movie.query.all()
    #     res = self.client().delete(
    #         "/movies/{}".format(find_movie[0].id), headers=self.headers)
    #     movie = Movie.query.filter(
    #         Movie.id == find_movie[0].id).one_or_none()

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(movie, None)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
