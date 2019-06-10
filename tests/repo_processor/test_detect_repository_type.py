from kondo_backend.room_engine import detect_repository_type, initialize_rooms
from testfixtures import LogCapture
import os


# Initialize rooms
rooms = initialize_rooms()


def test_detect_repository_type_python():
    """Ensure detector properly returns python for python project"""
    assert (
        detect_repository_type(
            os.getcwd() + "/fixtures/sample-python-project", rooms=rooms
        )
        == "flask"
    )


def test_detect_repository_type_terraform():
    """Ensure detector properly returns terraform for terraform project"""
    assert (
        detect_repository_type(
            os.getcwd() + "/fixtures/sample-terraform-project", rooms=rooms
        )
        == "terraform"
    )


def test_detect_repository_type_invalid():
    """Ensure detector properly returns False if the is invalid"""
    with LogCapture() as l:
        assert (
            detect_repository_type(os.getcwd() + "/fixtures/bad-path", rooms=rooms)
            == "Error"
        )
        l.check(
            (
                "kondo_backend.log",
                "ERROR",
                "Path passed in to detect_repository_type is invalid",
            )
        )
