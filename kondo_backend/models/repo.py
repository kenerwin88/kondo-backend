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
    repo_type: str

    def to_json(self):
        return json.dumps(
            {
                "id": self.id,
                "name": self.name,
                "clone_url": self.clone_url,
                "description": self.description,
                "violations": self.violations,
                "repo_type": self.repo_type,
            }
        )
