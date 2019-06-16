import attr
import json
from kondo_backend.models import Violation, Room


@attr.s(auto_attribs=True)
class Repo:
    id: int  # Name of violation, should match name of rule or requiredfile
    name: str
    clone_url: str
    description: str
    violations: [Violation]
    room_type: str

    def to_json(self):
        if self.violations != "False":
            json_violations = []
            for v in self.violations:
                json_violations.append(v.to_json())
        else:
            json_violations = "False"
        return {
            "id": self.id,
            "name": self.name,
            "clone_url": self.clone_url,
            "description": self.description,
            "violations": json_violations,
            "room_type": self.room_type,
        }
