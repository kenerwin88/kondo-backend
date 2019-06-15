import toml
from loguru import logger
from kondo_backend.models import RequiredFile, Room, Condition


def room_loader(path):
    """Parses data and returns a Room object"""
    data = toml.load(path + "/kondo.toml")
    logger.info(data)

    required_files = []
    if "required_file" in data.keys():
        for req_file in data["required_file"]:
            # Get Conditions
            if "condition_type" in req_file.keys():
                condition = Condition(
                    condition_type=req_file["condition_type"],
                    condition_value=req_file["condition_value"],
                )
            else:
                condition = False

            # Get Description
            if "description" in req_file.keys():
                description = req_file["description"]
            else:
                logger.debug(
                    "Required file: " + req_file["name"] + " is missing a description"
                )
                description = False

            # Get Immutability
            if "immutable" in req_file.keys():
                immutable = req_file["immutable"]
            else:
                immutable = False

            required_files.append(
                RequiredFile(
                    name=req_file["name"],
                    condition=condition,
                    description=description,
                    immutable=immutable,
                )
            )
    return Room(
        title=data["title"],
        required_files=required_files,
        rules=False,
        detectors=data["detectors"],
    )
