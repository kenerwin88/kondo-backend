import attr


@attr.s(auto_attribs=True)
class Violation:
    name: str  # Name of violation, should match name of rule or requiredfile
    description: str  # In depth description of how to fix or why this was triggered
    type: str  # Type, RequiredFile or Rule
    detected: bool  # If true, repository DOES have this violation, if false, all is good!
    skipped: bool  # Sometimes based on settings we won't even check for this violation, if so we want to know that.
