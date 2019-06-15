import requests
from flask import request, Response, current_app
from jwt import decode
from kondo_backend.auth import api
from flask_restplus import Resource
import json
import rejson
from loguru import logger


@api.route("/repositories")
class Repository(Resource):
    @api.doc(
        params={
            "jwt": "A JWT token used for authenticating the request.",
            "org_id": "org id to filter repositories by (AKA installation_id)",
        }
    )
    @api.response(200, "Success", str)
    @api.response(401, "Authentication Error")
    def post(self) -> Response:
        """
        Given a user's JWT and the name of an organization that the user has access to, this function will return all
        repositories that the user has access to.

        Returns
        -------
        array
            Array of repositories
        """
        # Get access_token from decoded JWT passed in from frontend
        org_id = request.values["org_id"]
        decoded_jwt = decode(
            request.values["jwt"], "kondo-secret", algorithms=["HS256"]
        )
        req = requests.get(
            "https://api.github.com/user/installations/" + org_id + "/repositories",
            headers={
                "Accept": "application/vnd.github.machine-man-preview+json",
                "Authorization": "token " + decoded_jwt["access_token"],
            },
        )

        # Connect to Redis
        redis_host = current_app.config["REDIS_HOST"]
        r = rejson.Client(host=redis_host, port=6379, db=0, decode_responses=True)
        # log.info("Connected to Redis server: " + redis_host)
        repos_json = req.json()["repositories"]
        repos = []
        for repo in repos_json:
            repo_id: int = repo["id"]
            processed_repo = json.loads(r.jsonget(repo_id))

            logger.debug("JSON repo info retrieved from Redis: " + str(processed_repo))
            repos.append(
                {
                    "name": repo["name"],
                    "id": str(repo["id"]),
                    "url": repo["html_url"],
                    "clone_url": repo["clone_url"],
                    "repo_type": processed_repo["repo_type"],
                    "violations": processed_repo["violations"],
                }
            )
        return Response(json.dumps(repos), status=200, mimetype="application/json")
