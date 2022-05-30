import os
from sqlalchemy import Column, ForeignKey, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy

DATABASE_PATH = os.getenv('DATABASE_PATH')
db = SQLAlchemy()

"""
setup_db(app)
    binds a flask application and a SQLAlchemy service
"""


def setup_db(app, database_path=DATABASE_PATH):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


class parentClass(db.Model):
    __abstract__ = True

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()


"""
Movie

"""


class Movie(parentClass):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True)
    year = db.Column(db.String(4))
    genre = db.Column(db.String(100))
    language = db.Column(db.String(100))
    director = db.Column(db.String(100))
    actors = db.Column(db.String(500))
    poster_link = db.Column(db.String(500))
    writer = db.Column(db.String(100))
    description = db.Column(db.String(500))

    def __init__(self, title, year, genre, language, director, actors, poster_link, writer, description):
        self.title = title
        self.year = year
        self.genre = genre
        self.language = language
        self.director = director
        self.actors = actors
        self.poster_link = poster_link
        self.writer = writer
        self.description = description

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'year': self.year,
            'genre': self.genre,
            'language': self.language,
            'director': self.director,
            'actors': self.actors,
            'poster_link': self.poster_link,
            'writer': self.writer,
            'description': self.description
        }


"""
Review

"""


class Review(parentClass):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    description = db.Column(db.String(500))
    username = db.Column(db.String(100))
    movie = Column(db.Integer, db.ForeignKey('movies.id', ondelete="cascade"),
                   nullable=False)

    def __init__(self, description, movie, username):
        self.description = description
        self.username = username
        self.movie = movie

    def format(self):
        return {
            'id': self.id,
            'username': self.username,
            'movie': self.movie,
            'description': self.description,
        }
