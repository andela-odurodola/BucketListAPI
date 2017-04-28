#!flask/bin/python3/
from flask_restful import abort, request


class CustomMessages:
    # Custom errors for the Restful API are defined here.

    def sucess_message(message):
        # Custom error message for not acceptable requests

        response = {'status': 'OK', 'message': message}
        return response

    def conflict(message):
        # Custom error message for not acceptable requests

        response = {'status': 'Not Acceptable', 'message': message}
        return response

    def bad_request(message):
        # Custom error message for bad requests

        response = {'status': 'Bad Request', 'message': message}
        return response
