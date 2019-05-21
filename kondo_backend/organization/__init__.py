from flask import Blueprint
from flask_restplus import Api


blueprint = Blueprint("organization", __name__)
api = Api(blueprint)

# noinspection PyPep8
from . import get_orgs
