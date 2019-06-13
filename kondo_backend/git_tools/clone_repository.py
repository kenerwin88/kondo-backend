from loguru import logger
import os
from git import Repo


def clone_repository(clone_url: str, username: str, password: str, target_dir: str):
    """
    Clones a git repository to a directory (with org and repo name appended), nothing more or less

    For example, https://github.com/kondo-io/kondo would be cloned to target_dir/kondo-io/kondo
    Returns path to cloned repository
    """

    # Create URL with populated username and password
    populated_url = clone_url.replace(
        "https://", "https://" + username + ":" + password + "@"
    )

    # Don't clone if it's already been cloned
    if os.path.isdir(target_dir):
        logger.info(target_dir + " folder already exists, skipping clone")
    else:
        logger.info("Cloning " + clone_url + " to " + target_dir)
        # Clone the URL
        Repo.clone_from(populated_url, target_dir, depth=1)
    return target_dir
