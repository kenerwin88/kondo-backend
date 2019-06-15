from loguru import logger
from kondo_backend import app
from kondo_backend import git_tools
from kondo_backend.models import Room
from .room_loader import room_loader
import toml
import os


def initialize_rooms() -> [Room]:
    # Initialize  Logger
    logger.info("Initializing rooms... (Cloning, loading into memory)")

    # Load official room list from settings.toml
    settings_file = os.path.join(app.instance_path, "settings.toml")
    rooms = toml.load(settings_file)["rooms"]
    logger.debug("List of rooms loaded: " + str(rooms))

    # Room cache directory
    room_cache_directory = app.config["CACHE_DIRECTORY"] + "/rooms/"

    loaded_rooms = {}
    for room in rooms:
        room_repo_path = room_cache_directory + room

        # If repo not already cloned
        if not os.path.isdir(room):
            git_tools.clone_repository(
                clone_url=rooms[room],
                username=os.environ["GITHUB_USER"],
                password=os.environ["GITHUB_TOKEN"],
                target_dir=room_repo_path,
            )

        # Load Rooms
        loaded_rooms[room] = room_loader(path=room_repo_path)
        logger.info("Room: " + room + " loaded successfully.")
    logger.info("Room loading complete")
    return loaded_rooms
