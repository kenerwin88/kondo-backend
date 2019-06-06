import glob
import os
import logging


def detect_repository_type(path):
    """Return language type of a given folder/path"""
    log = logging.getLogger(__name__)
    languages = [
        {"java": [".java"]},
        {"python": [".py"]},
        {"terraform": [".tf", ".tfvars"]},
    ]
    # Check to see if path exists
    if not os.path.isdir(path):
        log.exception("Path passed in to detect_repository_type is invalid")
        return False
    file_type_count = {}
    for language in languages:
        for name, extensions in language.items():
            file_type_count[name] = 0
            for extension in extensions:
                file_type_count[name] = file_type_count[name] + len(
                    glob.glob(path + "/**/*" + extension, recursive=True)
                )
    return max(file_type_count, key=lambda key: file_type_count[key])
