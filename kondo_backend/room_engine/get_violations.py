from loguru import logger
from kondo_backend.models import Violation
from kondo_backend.models import RequiredFile
import os


def get_violations(room, path, settings) -> [Violation]:
    """Analyzes a repository via a room, returns an array of violations & if found"""
    logger.info("Analyzing: " + path + " with room: " + room.title)

    violations = []

    # Analyze Required Files
    required_files: [RequiredFile] = room.required_files
    for required_file in required_files:
        detected = False
        skipped = False
        logger.debug("Checking required file: " + str(required_file))

        # Determine if we should check for the condition or skip
        if required_file.has_conditions():
            if required_file.condition.condition_type == "only_if":
                if settings[required_file.condition.condition_value]:
                    skipped = False
                else:
                    skipped = True
            if required_file.condition.condition_type == "unless":
                if settings[required_file.condition.condition_value]:
                    skipped = True
                else:
                    skipped = False

        # Check for the required file unless we've determined we need to skip checking
        if not skipped:
            if os.path.isfile(path + "/" + required_file.name):
                logger.debug(
                    "Required file: " + required_file.name + " is present in repository"
                )
                detected = False
            else:
                logger.debug(
                    "Required file: " + required_file.name + " is NOT in repository"
                )
                detected = True

        # Add the violation to the array
        violations.append(
            Violation(
                name=required_file.name,
                description=required_file.description,
                type="requiredFile",
                detected=detected,
                skipped=skipped,
            )
        )

    return violations
