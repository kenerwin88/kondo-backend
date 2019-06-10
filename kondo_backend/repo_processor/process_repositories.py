from kondo_backend import app
from . import get_installations, get_installation_repositories, get_access_token
from kondo_backend import repo_processor
from kondo_backend import git_tools
import redis
from kondo_backend import log


def process_repositories():
    """
    This is the primary entrypoint for the repo_processor.   It uses all of the other functions to discover where
    kondo has been installed, what repos each of them have, downloads them, scans them, and updates the cache with all
    necessary information for the backend API to utilize.  This function should ONLY be used for connecting all of the
    others, it shouldn't have any additional logic within.
    """
    # Connect to Redis
    redis_host = app.config["REDIS_HOST"]
    r = redis.Redis(host=redis_host, port=6379, db=0, decode_responses=True)
    log.info("Connected to Redis server: " + redis_host)

    # Process Every Repo
    installations = get_installations()
    for install in installations:
        auth_token = get_access_token(install["id"])

        repositories = get_installation_repositories(auth_token)

        for repo in repositories:
            # Clone Repos
            target_dir = app.config["CACHE_DIRECTORY"] + "/" + repo["full_name"]
            log.debug("Cloning " + repo["full_name"])
            git_tools.clone_repository(
                clone_url=repo["clone_url"],
                username="x-access-token",
                password=auth_token,
                target_dir=target_dir,
            )

            # Detect Repository Type
            repo_type = repo_processor.detect_repository_type(path=target_dir)
            log.debug(repo["full_name"] + " detected as " + repo_type)
            repo["repo_type"] = repo_type

            # Update Redis
            r.hmset(repo["id"], repo)
            log.debug("Updated repo info stored in redis: " + str(repo))
