import pytest
import responses
from kondo_backend import app


@pytest.fixture
def client():
    client = app.test_client()
    app.config.from_pyfile("../kondo-backend.dev.config")
    yield client


# noinspection PyPep8
@responses.activate
def test_github_login(client):
    """Given the right code, the API should return a JWT"""
    responses.add(
        responses.POST,
        "https://github.com/login/oauth/access_token?accept=application%2Fjson&client_id=development_id&client_secret=development_secret&state=RandomString&code=TestValidCode",
        json={"access_token": "TestToken"},
        status=200,
        match_querystring=True,
    )

    request = client.post(
        "/login/github", data=dict(state="RandomString", code="TestValidCode")
    )
    # noinspection PyPep8
    assert (
        request.data.decode("utf-8")
        == "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhY2Nlc3NfdG9rZW4iOiJUZXN0VG9rZW4ifQ.12hSOYo5DTRJnrY64IvnlQGg14Qg7-JWdKPotyF3wdo"
    )


@responses.activate
def test_github_login_invalid_code(client):
    """Given the wrong code, the API should return an error stating as such"""
    responses.add(
        responses.POST,
        "https://github.com/login/oauth/access_token?accept=application%2Fjson&client_id=development_id&client_secret=development_secret&state=RandomString&code=TestInvalidCode",
        json={
            "error": "bad_verification_code",
            "error_description": "The code passed is incorrect or expired.",
        },
        status=200,
        match_querystring=True,
    )
    request = client.post(
        "/login/github", data=dict(state="RandomString", code="TestInvalidCode")
    )
    json_data = request.get_json()
    assert json_data["error"] == "bad_verification_code"
    assert json_data["error_description"] == "The code passed is incorrect or expired."
