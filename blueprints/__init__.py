from flask import Blueprint
routes = Blueprint('routes', __name__)

from .blueprint_movies import *
from .blueprint_reviews import *