__version__ = "0.1.0"

import os
from flask import Flask
from kondo_backend import auth
from flask_restplus import Api


app = Flask(__name__)

config = {
    "development": "../kondo-backend.dev.config",
    "production": "../kondo-backend.prod.config",
}

config_name = os.getenv("FLASK_CONFIGURATION", "production")
app.config.from_pyfile(config[config_name], silent=True)

# Register Blueprints
app.register_blueprint(auth.blueprint)
api = Api(app)
