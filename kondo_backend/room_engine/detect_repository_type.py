import glob
import os
import logging
from kondo_backend.models import Room


def detect_repository_type(path, rooms: [Room]) -> str:
    """
    Given an array of loaded rooms, this function will scan a repository and make a best guess of what
    type of code resides within it.  This is determined by comparing and scoring the repository against every room,
    whichever one has the highest score is used as the detected repo type.
    Return language type of a given folder/path
    """
    log = logging.getLogger(__name__)

    # Check to see if path passed in exists
    if not os.path.isdir(path):
        log.exception("Path passed in to detect_repository_type is invalid")
        return "Error"
    score = {}
    for r in rooms:
        # Check for extensions (1pt per match)
        room = rooms[r]
        score[room.title] = 0
        if "file_extensions" in room.detectors:
            for extension in room.detectors["file_extensions"]:
                score[room.title] = score[room.title] + len(
                    glob.glob(path + "/**/*" + extension, recursive=True)
                )

    return max(score, key=lambda key: score[key])
