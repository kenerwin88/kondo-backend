from kondo_backend.repo_processor import detect_repository_type
from testfixtures import LogCapture
import os


def test_detect_repository_type_python():
    """Ensure detector properly returns python for python project"""
    assert (
        detect_repository_type(os.getcwd() + "/fixtures/sample-python-project")
        == "python"
    )


def test_detect_repository_type_terraform():
    """Ensure detector properly returns terraform for terraform project"""
    assert (
        detect_repository_type(os.getcwd() + "/fixtures/sample-terraform-project")
        == "terraform"
    )


def test_detect_repository_type_invalid():
    """Ensure detector properly returns False if the is invalid"""
    with LogCapture() as l:
        assert detect_repository_type(os.getcwd() + "/fixtures/bad-path") == False
        l.check(
            (
                "kondo_backend.repo_processor.detect_repository_type",
                "ERROR",
                "Path passed in to detect_repository_type is invalid",
            )
        )
