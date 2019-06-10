__version__ = "0.1.0"

import os
from flask import Flask
from kondo_backend import auth, organization
from flask_restplus import Api
from flask_cors import CORS
from .log import log


app = Flask(__name__, instance_relative_config=True)
CORS(app)


config = {
    "development": "kondo-backend.dev.config",
    "production": "kondo-backend.prod.config",
}

config_name = os.getenv("FLASK_CONFIGURATION", "production")
app.config.from_pyfile(config[config_name], silent=True)

# Register Blueprints
app.register_blueprint(auth.blueprint)
app.register_blueprint(organization.blueprint)
api = Api(app)
