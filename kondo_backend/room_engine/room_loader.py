import toml
import os
import logging
from kondo_backend.models import RequiredFile, Condition, Room


def room_loader(path):
    """Parses data and returns a Room object"""
    log = logging.getLogger(__name__)

    # Import kondo.toml settings
    data = toml.load(path + "/kondo.toml")
    log.info(data)

    required_files = []
    if "required_file" in data.keys():
        for req_file in data["required_file"]:
            if "condition_type" in req_file.keys():
                condition = Condition(
                    condition_type=req_file["condition_type"],
                    condition_value=req_file["condition_value"],
                )
            else:
                condition = False
            required_files.append(
                RequiredFile(name=req_file["name"], condition=condition)
            )
    return Room(
        title=data["title"],
        required_files=required_files,
        rules=False,
        detectors=data["detectors"],
    )
