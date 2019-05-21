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
def test_get_orgs(client):
    """We should get all the organizations a user has installed kondo-io on.  This test ensures that an array of orgs
    are returned, each containing an installation_id, name, and avatar.
    """
    responses.add(
        responses.GET,
        "https://api.github.com/user/installations",
        json={
            "installations": [
                {
                    "id": 932356,
                    "account": {
                        "login": "devopslibrary",
                        "avatar_url": "https://avatars3.githubusercontent.com/u/11233903?v=4",
                    },
                }
            ]
        },
        status=200,
        match_querystring=True,
    )

    request = client.post(
        "/organizations",
        data=dict(
            jwt="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhY2Nlc3NfdG9rZW4iOiJUZXN0VG9rZW4ifQ.12hSOYo5DTRJnrY64IvnlQGg14Qg7-JWdKPotyF3wdo"
        ),
    )
    # noinspection PyPep8
    json_output = json.loads(request.data.decode("utf-8"))
    assert json_output == [
        {
            "installation_id": 932356,
            "name": "devopslibrary",
            "avatar": "https://avatars3.githubusercontent.com/u/11233903?v=4",
        }
    ]
