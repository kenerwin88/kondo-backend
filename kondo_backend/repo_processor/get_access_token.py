import jwt
import os
from datetime import datetime, timedelta
import requests
from kondo_backend import app
from typing import Dict


def get_access_token(installation_id: str) -> str:
    """
    In order to authentication to a Github installation API, you have to have a token (one PER installation).  Given
    an installation ID, this function will return the token needed for later API calls and git authentication.

    Returns
    -------
    str
        Token for installation authenticaiton
        """
    private_key = open(
        os.path.join(app.instance_path, app.config["GITHUB_PRIVATE_KEY"]), "r+"
    ).read()

    payload = {
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(minutes=10),
        "iss": "30108",
    }
    encoded_jwt = jwt.encode(payload, private_key, algorithm="RS256").decode("utf-8")

    # /app/installations
    headers = {
        "Authorization": "Bearer " + encoded_jwt,
        "Accept": "application/vnd.github.machine-man-preview+json",
    }

    req = requests.post(
        "https://api.github.com/app/installations/"
        + installation_id
        + "/access_tokens",
        headers=headers,
    )

    return req.json()["token"]
    # return "token"
