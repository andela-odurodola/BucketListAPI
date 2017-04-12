from flask import request
from flask_restful import Resource

from app.models import User
from app.common.custom_messages import CustomMessages
from app.common.helpers import login_user

class Login_User(Resource):
    """
    The Bucketlist service makes use of the Token-based Authentication.
    That is, it generates a token for the user while login.
    """

    def post(self):
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            return login_user(user), 202
        return CustomMessages.not_acceptable('Please enter a valid username or password'), 406
