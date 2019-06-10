from .condition import Condition


class RequiredFile:
    """
    A required file has a name and condition that determines whether it should be checked or not
    """

    def __init__(self, name: str, condition: Condition):
        self.name = name
        self.condition = condition

    def has_condition(self):
        if self.condition is False:
            return False
        else:
            return True

