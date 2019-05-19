import requests
from flask import request, current_app, Response
from jwt import encode
from kondo_backend.auth import api
from flask_restplus import Resource


@api.route("/login/github")
class Auth(Resource):
    @api.doc(
        params={
            "state": "A random string that has to match through the process, helps prevent MITM attacks.",
            "code": "A code provided by the github callback (located in the frontend)",
        }
    )
    @api.response(200, "Success", str)
    @api.response(401, "Authentication Error")
    def post(self) -> Response:
        """
        This function returns a JWT token (with the Github authentication token within the payload)

        It is meant to be called by the frontend, and the JWT is then used for authenticating to to the rest of the
        endpoints.

        You can get a code by visiting https://github.com/login/oauth/authorize?client_id=CLIENTID,  then use that to
        test via Postman or something similar.

        Returns
        -------
        str
            A JWT token containing the Github Authentication code
        """
        payload = {
            "accept": "application/json",
            "client_id": current_app.config["GITHUB_CLIENT_ID"],
            "client_secret": current_app.config["GITHUB_CLIENT_SECRET"],
            "state": request.values["state"],
            "code": request.values["code"],
        }
        req = requests.post(
            "https://github.com/login/oauth/access_token",
            params=payload,
            headers={"Accept": "application/json"},
        )

        # Return Github Error on failure
        if "error" in req.json():
            return Response(req, status=401, mimetype="application/json")

        # If successful, encode as JWT and return it
        access_token = req.json()["access_token"]
        jwt = encode({"access_token": access_token}, "kondo-secret", algorithm="HS256")
        return Response(jwt, status=200)
