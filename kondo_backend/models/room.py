import attr
from .required_file import RequiredFile


@attr.s(auto_attribs=True)
class Rule:
    """
    A rule is part of a room, it's used for advanced checks to ensure cleanliness
    """

    name: str
    description: str
    trigger_type: str
    trigger_value: str
    excluded_files: [str]


@attr.s(auto_attribs=True)
class Detectors:
    """

    The detectors are used to see if a repo should use this room (auto detection)
    """

    file_extensions: [str]


@attr.s(auto_attribs=True)
class Room:
    """
    A room is a description of a perfect space, all clean.  This is what you want your repos to model
    """

    title: str
    required_files: [RequiredFile]
    rules: [Rule]
    detectors: Detectors
