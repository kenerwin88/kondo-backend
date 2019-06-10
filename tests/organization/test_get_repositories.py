import pytest
import responses
import json
from kondo_backend import app


@pytest.fixture
def client():
    client = app.test_client()
    app.config.from_pyfile("../kondo-backend.dev.config")
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
                    "name": "kondo-test-repo",
                    "id": "144091900",
                    "html_url": "https://github.com/kondo-io/kondo-test-repo",
                    "clone_url": "http://github.com/kondo-io/kondo-test-repo.git",
                },
                {
                    "name": "kondo-test-repo1",
                    "id": "187557873",
                    "html_url": "https://github.com/kondo-io/kondo-test-repo2",
                    "clone_url": "http://github.com/kondo-io/kondo-test-repo2.git",
                },
                {
                    "name": "kondo-test-repo2",
                    "id": "145332816",
                    "html_url": "https://github.com/kondo-io/kondo-test-repo3",
                    "clone_url": "http://github.com/kondo-io/kondo-test-repo3.git",
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
            "name": "kondo-test-repo",
            "id": "144091900",
            "url": "https://github.com/kondo-io/kondo-test-repo",
            "clone_url": "http://github.com/kondo-io/kondo-test-repo.git",
            "repo_type": "java",
        },
        {
            "name": "kondo-test-repo1",
            "id": "187557873",
            "url": "https://github.com/kondo-io/kondo-test-repo2",
            "clone_url": "http://github.com/kondo-io/kondo-test-repo2.git",
            "repo_type": "java",
        },
        {
            "name": "kondo-test-repo2",
            "id": "145332816",
            "url": "https://github.com/kondo-io/kondo-test-repo3",
            "clone_url": "http://github.com/kondo-io/kondo-test-repo3.git",
            "repo_type": "java",
        },
    ]
