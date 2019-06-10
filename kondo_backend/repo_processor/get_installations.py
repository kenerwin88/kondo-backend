import jwt
import os
from datetime import datetime, timedelta
import requests
from kondo_backend import app


def get_installations():
    """
    This function requires that a valid Github Private Key is provided.  It returns an array containing every
    single installation ID and name.  This MUST not be exposed publicly, it is only used internally for determining
    who has the application installed.  We can then use the installation IDs to get an access token later
    on, and even download all of the repos from the org for processing.

    Returns
    -------
    :rtype: list
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

    r = requests.get("https://api.github.com/app/installations", headers=headers)
    installations = []
    for install in r.json():
        installations.append(
            {"id": str(install["id"]), "org": str(install["account"]["login"])}
        )
    return installations
