class Condition:
    """
    A condition is something like, unless, only_if, with a value
    """

    def __init__(self, condition_type, condition_value):
        self.condition_type = condition_type
        self.condition_value = condition_value
