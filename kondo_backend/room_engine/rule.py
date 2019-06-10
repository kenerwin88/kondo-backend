import logging
import os


class Rule:
    """
    A rule is part of a room, it's used for advanced checks to ensure cleanliness
    """

    def __init__(self, name, description, trigger_type, trigger_value, excluded_files, included_files):
        self.name = name
        self.description = description
        self.trigger_type = trigger_type
        self.trigger_value = trigger_value
        self.excluded_files = excluded_files
        self.included_files = included_files
