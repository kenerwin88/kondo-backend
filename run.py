from flask import Flask
import os

app = Flask(__name__)

config = {
    "development": "kondo-backend.dev.config",
    "production": "kondo-backend.prod.config",
}

# Given a code and state (random string) from github, this will return a JWT containing authentication code.
@app.route("/login/github")
def login_github(state: str, code: str) -> str:
    return "Hello, World! Test"


if __name__ == "__main__":
    app.run(debug=True)
    config_name = os.getenv("FLASK_CONFIGURATION", "production")
    app.config.from_pyfile(
        config[config_name], silent=True
    )  # instance-folders configuration
    # print(app.config["GITHUB_CLIENT_ID"])
