from kondo_backend.git_tools import clone_repository
import os


def test_clone_repository(tmp_path):
    """Ensure's that the function can clone successfully"""
    clone_path = tmp_path / "cache"
    #    clone_path.mkdir()

    clone_repository(
        clone_url="https://github.com/kondo-io/terraform-room.git",
        username=os.environ["GITHUB_USER"],
        password=os.environ["GITHUB_TOKEN"],
        target_dir=str(clone_path),
    )
    assert os.path.isfile(str(clone_path) + "/main.tf") is True


def test_clone_repository_should_skip_if_exists(tmp_path):
    """Ensure's that the function skips cloning if folder not empty"""
    clone_path = tmp_path / "cache"
    clone_path.mkdir()

    clone_repository(
        clone_url="https://github.com/kondo-io/terraform-room.git",
        username=os.environ["GITHUB_USER"],
        password=os.environ["GITHUB_TOKEN"],
        target_dir=str(clone_path),
    )
    assert os.path.isfile(str(clone_path) + "/main.tf") is False
