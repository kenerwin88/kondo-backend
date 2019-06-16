from kondo_backend import app, room_engine
from . import get_installations, get_installation_repositories, get_access_token
from kondo_backend import git_tools
from kondo_backend.models import Repo
import rejson
from loguru import logger
import json


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
    r = rejson.Client(host=redis_host, port=6379)
    logger.info("Connected to Redis server: " + redis_host)

    # Process Every Repo
    installations = get_installations()
    for install in installations:
        auth_token = get_access_token(install["id"])

        repositories: [Repo] = get_installation_repositories(auth_token)

        for repo in repositories:
            # Clone Repos
            target_dir = app.config["CACHE_DIRECTORY"] + "/" + repo.name
            logger.debug("Cloning " + repo.name)
            git_tools.clone_repository(
                clone_url=repo.clone_url,
                username="x-access-token",
                password=auth_token,
                target_dir=target_dir,
            )

            # Detect Repository Type
            room_type = room_engine.detect_repository_type(path=target_dir, rooms=rooms)
            logger.debug(repo.name + " detected as " + room_type)
            repo.room_type = room_type

            # Validate repository using room engine
            settings = {
                "CHANGELOG_DISABLED": False,
                "LICENSE_DISABLED": False,
                "PRECOMMIT_HOOKS_DISABLED": False,
                "GLOBAL_JENKINSFILE_ENABLED": True,
            }

            # Check for violations unless room_type is unknown
            if room_type == "unknown":
                logger.debug(
                    "Unable to validate repo: " + repo.name + ", room_type not detected"
                )
                violations = "False"
            else:
                violations = room_engine.get_violations(
                    rooms[room_type], target_dir, settings=settings
                )
                logger.debug("Validation output: " + str(violations))
            repo.violations = violations
            # Update Redis
            repo_json = json.dumps(repo.to_json())
            logger.debug("Updated repo info stored in redis: " + str(repo_json))
            repo_id: int = repo.id
            r.jsonset(repo_id, rejson.Path.rootPath(), repo_json)
