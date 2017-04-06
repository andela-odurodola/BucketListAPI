from flask import request
from flask_restful import Resource

from app.models import User
from app.common.errors import custom_errors
from app.common.helpers import save_into_database, user_detail


class Register_User(Resource):
    """
    Since API get information from sources. There is need to authenticate users.
    Users need to register their login details.
    """

    def post(self):
        username = request.form.get('username')
        password = request.form.get('password')
        username_check = User.query.filter_by(username=username).first()
        if username and password:
            if username_check:
                return custom_errors['UserNameExists'], 406
            else:
                user_info = User(username=username, password=password)
                if save_into_database(user_info):
                    return user_detail(user_info), 201
        else:
            return custom_errors['UserDetailsEmpty'], 406
