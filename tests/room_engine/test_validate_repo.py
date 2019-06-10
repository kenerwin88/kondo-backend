from kondo_backend.models import Room, RequiredFile, Condition
from kondo_backend.room_engine import validate_repo, room_loader


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
    violations = validate_repo(
        room=room, path="fixtures/sample-terraform-project", settings=settings
    )
    assert len(violations) == 7


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
    violations = validate_repo(
        room=room, path="fixtures/sample-terraform-project", settings=settings
    )
    assert len(violations) == 6
