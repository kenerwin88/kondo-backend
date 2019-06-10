from kondo_backend import app, room_engine
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

    # Initialize Room Engine
    rooms = room_engine.initialize_rooms()  # Load all the rooms into memory

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
            repo_type = room_engine.detect_repository_type(path=target_dir, rooms=rooms)
            log.debug(repo["full_name"] + " detected as " + repo_type)
            repo["repo_type"] = repo_type

            # Validate repository using room engine
            settings = {
                "CHANGELOG_DISABLED": False,
                "LICENSE_DISABLED": False,
                "PRECOMMIT_HOOKS_DISABLED": False,
                "GLOBAL_JENKINSFILE_ENABLED": True,
            }
            if repo_type == "unknown":
                log.debug(
                    "Unable to validate repo: "
                    + repo["full_name"]
                    + ", repo_type not detected"
                )
            else:
                validation_output = room_engine.validate_repo(
                    rooms[repo_type], target_dir, settings=settings
                )
                log.debug("Validation output: " + str(validation_output))

            # Update Redis
            r.hmset(repo["id"], repo)
            log.debug("Updated repo info stored in redis: " + str(repo))
