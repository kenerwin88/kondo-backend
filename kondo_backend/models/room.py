import attr


@attr.s(auto_attribs=True)
class Condition:
    condition_type: str
    condition_value: str


@attr.s(auto_attribs=True)
class RequiredFile:
    name: str
    condition: Condition


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
    A rule is part of a room, it's used for advanced checks to ensure cleanliness
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
