import attr


@attr.s(auto_attribs=True)
class Condition:
    condition_type: str
    condition_value: str


@attr.s(auto_attribs=True)
class RequiredFile:
    name: str
    description: str
    condition: Condition
    immutable: bool

    def has_conditions(self):
        if self.condition:
            return True
        else:
            return False
