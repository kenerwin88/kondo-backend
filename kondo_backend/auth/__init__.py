from flask import Blueprint
from flask_restplus import Api


blueprint = Blueprint("auth", __name__)
api = Api(blueprint)

# noinspection PyPep8
from . import login_github
