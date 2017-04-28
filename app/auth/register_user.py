from flask import request, jsonify
from flask_restful import Resource

from app.models import User
from app.common.custom_messages import CustomMessages
from app.common.helpers import save_into_database, register_user


class Register_User(Resource):
    """
    Since API get information from sources. There is need to authenticate users.
    Users need to register their login details.
    """

    def post(self):
        username = request.form.get('username')
        password = request.form.get('password')

        if not all([username, password]):
            return CustomMessages.bad_request("User's details cannot be empty. Please specify a username and password"), 400
        username_is_taken = bool(User.query.filter_by(username=username).first())
        if username_is_taken:
            return CustomMessages.conflict('The username already exist. Choose another'), 409
        user_info = User(username=username, password=password)
        if save_into_database(user_info):
            return(register_user(user_info)), 200
        else:
            return CustomMessages.server_error('Account Creation not successfull'), 500
