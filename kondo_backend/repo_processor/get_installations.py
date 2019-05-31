import jwt
from datetime import datetime, timedelta
import requests
from kondo_backend import app
import os


def get_installations():
    private_key = open(app.config["GITHUB_PRIVATE_KEY"], "r+").read()

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

    r = requests.get("https://api.github.com/app/installations", headers=headers)
    installations = []
    for install in r.json():
        installations.append({"id": install["id"], "org": install["account"]["login"]})
    print(r.json())
    return installations
