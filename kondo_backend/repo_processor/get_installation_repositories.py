import requests
from typing import List
from kondo_backend.models import Repo


def get_installation_repositories(token: str) -> List[Repo]:
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
            Repo(
                id=repo["id"],
                name=repo["full_name"],
                clone_url=repo["clone_url"],
                description=repo["description"],
                room_type="unknown",
                violations=[],
            )
        )
    return installation_repos
