from kondo_backend import repo_processor
import pytest
import responses
from flask import app


@responses.activate
def test_get_access_token():
    responses.add(
        responses.POST,
        "https://api.github.com/app/installations/932356/access_tokens",
        json={
            "token": "v1.220533d67e5cd15a0a32890b811e72667ce6a83d",
            "expires_at": "2019-05-31T04:13:33Z",
        },
        status=200,
        match_querystring=True,
    )
    access_token = repo_processor.get_access_token.get_access_token("932356")
    assert access_token == {
        "token": "v1.220533d67e5cd15a0a32890b811e72667ce6a83d",
        "expires_at": "2019-05-31T04:13:33Z",
    }
