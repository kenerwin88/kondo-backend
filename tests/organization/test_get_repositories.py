import pytest
import responses
import json
from kondo_backend import app


@pytest.fixture
def client():
    client = app.test_client()
    app.config.from_pyfile("../instance/kondo-backend.dev.config")
    yield client


# noinspection PyPep8
@responses.activate
def test_get_repositories(client):
    """We should get all the repositories a user has installed kondo-io on (filtered by an organization +ID).
    This test ensures that an array of repos are returned.
    """
    responses.add(
        responses.GET,
        "https://api.github.com/user/installations/898100/repositories",
        json={
            "repositories": [
                {
                    "name": "kondo-backend",
                    "id": "187411207",
                    "html_url": "http://github.com/kondo-io/kondo-backend",
                    "clone_url": "https://github.com/kondo-io/kondo-backend.git",
                },
                {
                    "name": "kondo-frontend",
                    "id": "187557873",
                    "html_url": "http://github.com/kondo-io/kondo-frontend",
                    "clone_url": "https://github.com/kondo-io/kondo-frontend.git",
                },
                {
                    "name": "devops",
                    "id": "31432529",
                    "html_url": "http://github.com/devopslibrary/devops",
                    "clone_url": "https://github.com/devopslibrary/devops.git",
                },
            ]
        },
    )

    request = client.post(
        "/repositories",
        data=dict(
            jwt="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhY2Nlc3NfdG9rZW4iOiJUZXN0VG9rZW4ifQ.12hSOYo5DTRJnrY64IvnlQGg14Qg7-JWdKPotyF3wdo",
            org_id="898100",
        ),
    )
    # noinspection PyPep8
    json_output = json.loads(request.data.decode("utf-8"))
    assert json_output == [
        {
            "name": "kondo-backend",
            "id": "187411207",
            "url": "http://github.com/kondo-io/kondo-backend",
            "clone_url": "https://github.com/kondo-io/kondo-backend.git",
            "repo_type": "flask",
            "violations": [],
        },
        {
            "name": "kondo-frontend",
            "id": "187557873",
            "url": "http://github.com/kondo-io/kondo-frontend",
            "clone_url": "https://github.com/kondo-io/kondo-frontend.git",
            "repo_type": "unknown",
            "violations": False,
        },
        {
            "name": "devops",
            "id": "31432529",
            "url": "http://github.com/devopslibrary/devops",
            "clone_url": "https://github.com/devopslibrary/devops.git",
            "repo_type": "unknown",
            "violations": False,
        },
    ]


# noinspection PyPep8
@responses.activate
def test_get_repositories_with_violations(client):
    """We should get all the repositories a user has installed kondo-io on (filtered by an organization +ID).
    This test ensures that an array of repos are returned.
    """
    responses.add(
        responses.GET,
        "https://api.github.com/user/installations/898100/repositories",
        json={
            "repositories": [
                {
                    "name": "room-terraform",
                    "id": "182435080",
                    "html_url": "http://github.com/kondo-io/room-terraform",
                    "clone_url": "https://github.com/kondo-io/room-terraform.git",
                }
            ]
        },
    )

    request = client.post(
        "/repositories",
        data=dict(
            jwt="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhY2Nlc3NfdG9rZW4iOiJUZXN0VG9rZW4ifQ.12hSOYo5DTRJnrY64IvnlQGg14Qg7-JWdKPotyF3wdo",
            org_id="898100",
        ),
    )
    # noinspection PyPep8
    json_output = json.loads(request.data.decode("utf-8"))
    assert json_output == [
        {
            "name": "room-terraform",
            "id": "182435080",
            "url": "http://github.com/kondo-io/room-terraform",
            "clone_url": "https://github.com/kondo-io/room-terraform.git",
            "repo_type": "terraform",
            "violations": [
                '{"name": "CHANGELOG.md", "description": false, "type": "requiredFile", "detected": "False", "skipped": "False"}',
                '{"name": "main.tf", "description": false, "type": "requiredFile", "detected": "False", "skipped": "False"}',
                '{"name": "outputs.tf", "description": false, "type": "requiredFile", "detected": "False", "skipped": "False"}',
                '{"name": "variables.tf", "description": false, "type": "requiredFile", "detected": "False", "skipped": "False"}',
                '{"name": "README.md", "description": false, "type": "requiredFile", "detected": "False", "skipped": "False"}',
                '{"name": "LICENSE", "description": false, "type": "requiredFile", "detected": "False", "skipped": "False"}',
                '{"name": ".pre-commit-config.yaml", "description": false, "type": "requiredFile", "detected": "False", "skipped": "False"}',
                '{"name": ".gitignore", "description": false, "type": "requiredFile", "detected": "False", "skipped": "False"}',
                '{"name": ".editorconfig", "description": false, "type": "requiredFile", "detected": "False", "skipped": "False"}',
                '{"name": "Jenkinsfile", "description": false, "type": "requiredFile", "detected": "True", "skipped": "False"}',
            ],
        }
    ]
