from kondo_backend import log
from kondo_backend import app
import toml
import os


def initialize_rooms():
    # Initialize  Logger
    log.info("Initializing rooms... (Cloning, loading into memory)")

    # Load official room list from settings.toml
    settings_file = os.path.join(app.instance_path, "settings.toml")
    rooms = toml.load(settings_file)["rooms"]
    log.debug("List of rooms loaded: " + str(rooms))

    # rooms = {}
    # for room_repo in room_repos:
    #     target_directory = os.path.dirname(os.getcwd()) + "/cache/rooms/" + room_repo
    #
    #     # If repo not already cloned
    #     if not os.path.isdir(target_directory):
    #         clone_repository(
    #             repo_name=room_repo,
    #             user_name=user_name,
    #             token=token,
    #             target_directory=target_directory,
    #         )
    #
    #     # Load Rooms
    #     rooms[room_repo] = room_loader(path=target_directory)
    #     log.info("Room: " + room_repo + " loaded successfully.")
    # log.info("Room loading complete")
    #
    # # repositories = get_repository_list(organization, token)
    # settings = {
    #     "CHANGELOG_DISABLED": False,
    #     "LICENSE_DISABLED": False,
    #     "PRECOMMIT_HOOKS_DISABLED": False,
    #     "GLOBAL_JENKINSFILE_ENABLED": True,
    # }
    # repositories = [
    #     "traderev/tf-tr-gl",
    #     "traderev/tf-tr-gateway",
    # ]  # Hardcode so API isn't hit while developing
    # for repo in repositories:
    #     target_directory = os.path.dirname(os.getcwd()) + "/cache/repos/" + repo
    #
    #     # If repo not already cloned
    #     if not os.path.isdir(target_directory):
    #         clone_repository(
    #             repo_name=repo,
    #             user_name=user_name,
    #             token=token,
    #             target_directory=target_directory,
    #         )
    #
    #     repository_type = detect_repository_type(target_directory)
    #     room_to_use = chosen_rooms[repository_type]
    #     log.info("Room to use: " + room_to_use)
    #     validation_output = validate_repo(
    #         rooms[room_to_use], target_directory, settings=settings
    #     )
    #     print(validation_output)
