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
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            token = user.generate_auth_token()
            user_check = user.verify_auth_token(token)
            # return ("logged in successfuly as {}".format(user_check.username))
            return {
                'Output': 'logged in successfully as {}'.format(user_check.username),
                'Token': token
            }, 202
        return custom_errors['IncorrectLoginDetails'], 400
