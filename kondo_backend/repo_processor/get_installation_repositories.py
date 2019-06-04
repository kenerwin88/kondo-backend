import jwt
from datetime import datetime, timedelta
import requests
from kondo_backend import app
from typing import List, Dict


def get_installation_repositories(token: str) -> List:
    """
    Given an access token, this function will return all of the repositories
    accessible within the installation.  We can then use this list to clone the repos.

    Returns
    -------
    List
        List of all repositories within installation
    """

    req = requests.get(
        "https://api.github.com/installation/repositories",
        headers={
            "Accept": "application/vnd.github.machine-man-preview+json",
            "Authorization": "token " + token,
        },
    )
    installation_repos = []
    for repo in req.json()["repositories"]:
        installation_repos.append(
            {
                "id": repo["id"],
                "full_name": repo["full_name"],
                "clone_url": repo["clone_url"],
                "description": repo["description"],
            }
        )
    return installation_repos
