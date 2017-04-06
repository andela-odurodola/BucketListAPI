from flask import request
from flask_restful import Resource

from app.models import User
from app.common.errors import custom_errors


class Login_User(Resource):
    """
    The Bucketlist service makes use of the Token-based Authentication.
    That is, it generates a token for the user while login.
    """

    def post(self):
        
