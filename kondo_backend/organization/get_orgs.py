import requests
from flask import request, Response
from jwt import decode
from kondo_backend.auth import api
from flask_restplus import Resource
import json


@api.route("/organizations")
class Organization(Resource):
    @api.doc(params={"jwt": "A JWT token used for authenticating the request."})
    @api.response(200, "Success", str)
    @api.response(401, "Authentication Error")
    def post(self) -> Response:
        """
        Given a user's JWT, this function returns all the organizations that Kondo has been installed on (specific
        to that user).

        Returns
        -------
        array
            Array of organizations
        """
        # Get access_token from decoded JWT passed in from frontend
        decoded_jwt = decode(
            request.values["jwt"], "kondo-secret", algorithms=["HS256"]
        )
        req = requests.get(
            "https://api.github.com/user/installations",
            headers={
                "Accept": "application/vnd.github.machine-man-preview+json",
                "Authorization": "token " + decoded_jwt["access_token"],
            },
        )

        installations = req.json()["installations"]
        organizations = []
        for install in installations:
            organizations.append(
                {
                    "installation_id": install["id"],
                    "name": install["account"]["login"],
                    "avatar": install["account"]["avatar_url"],
                }
            )
        return Response(
            json.dumps(organizations), status=200, mimetype="application/json"
        )
