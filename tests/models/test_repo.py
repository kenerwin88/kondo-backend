from kondo_backend.models import Repo


def test_repo_without_violations_serialized_as_json():
    """Ensure Repo can be serialized"""
    repo = Repo(
        id=1234,
        name="test_repo",
        clone_url="https://github.com/kondo-io/test_repo.git",
        description="Test",
        room_type="unknown",
        violations="False",
    )
    assert repo.to_json() == {
        "id": 1234,
        "name": "test_repo",
        "clone_url": "https://github.com/kondo-io/test_repo.git",
        "description": "Test",
        "violations": "False",
        "room_type": "unknown",
    }
