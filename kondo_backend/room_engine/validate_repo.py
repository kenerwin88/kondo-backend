import logging
import os


def validate_repo(room, path, settings):
    """Validates a repository against a room"""
    log = logging.getLogger(__name__)
    violations = []
    log.info("Validating: " + path + " with room: " + room.title)

    # Debug, show all required_files before filtering
    log.debug("Listing all required_files before filtering:")
    for rf in room.required_files:
        log.debug("Required file: " + str(rf))

    applicable_required_files = []

    # First, start with all the required_files without conditions
    applicable_required_files += list(
        filter(lambda x: (x.condition is False), room.required_files)
    )

    # Next let's work on conditionals
    required_files_with_conditions = list(
        filter(lambda x: x.condition, room.required_files)
    )
    log.debug("Required files with Conditions: " + str(required_files_with_conditions))

    # The "unless" condition
    applicable_required_files += list(
        filter(
            lambda x: (
                x.condition.condition_type == "unless"
                and settings[x.condition.condition_value] is False
            ),
            required_files_with_conditions,
        )
    )

    # Next the "only_if" condition
    applicable_required_files += list(
        filter(
            lambda x: (
                x.condition.condition_type is "only_if"
                and settings[rf.condition.condition_value] is True
            ),
            required_files_with_conditions,
        )
    )

    for required_file in applicable_required_files:
        if os.path.isfile(path + "/" + required_file.name):
            log.debug(
                "Required file: " + required_file.name + " is present in repository"
            )
        else:
            log.debug("Required file: " + required_file.name + " is NOT in repository")
            violations.append(
                "Required file: " + required_file.name + " was not found in repository."
            )
    return violations
