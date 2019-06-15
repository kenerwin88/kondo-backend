from kondo_backend.room_engine import room_loader, get_violations
from kondo_backend.models import Violation
import json


def test_room_validation():
    """
    Ensure room validates a repository properly with basic settings
    - Should return 7 violation based on sample-terraform-project fixture
    """
    room = room_loader(path="fixtures/sample-room-terraform")
    settings = {
        "CHANGELOG_DISABLED": False,
        "LICENSE_DISABLED": False,
        "PRECOMMIT_HOOKS_DISABLED": False,
        "GLOBAL_JENKINSFILE_ENABLED": True,
    }
    violations: [Violation] = get_violations(
        room=room, path="fixtures/sample-terraform-project", settings=settings
    )
    detected_violations = list(
        filter(lambda violation: (violation.detected is True), violations)
    )
    print(detected_violations)
    assert len(detected_violations) == 8


def test_room_validation_precommit_hooks_disabled():
    """
    Ensure room validates a repository properly with basic settings
    - Should return 6 violations, because LICENSE_DISABLED is set to true
    - In other words, this checks to make sure it's reading the settings properly
    """
    room = room_loader(path="fixtures/sample-room-terraform")
    settings = {
        "CHANGELOG_DISABLED": False,
        "LICENSE_DISABLED": True,
        "PRECOMMIT_HOOKS_DISABLED": False,
        "GLOBAL_JENKINSFILE_ENABLED": True,
    }
    violations: [Violation] = get_violations(
        room=room, path="fixtures/sample-terraform-project", settings=settings
    )
    detected_violations = list(
        filter(lambda violation: (violation.detected is True), violations)
    )
    assert len(detected_violations) == 7
