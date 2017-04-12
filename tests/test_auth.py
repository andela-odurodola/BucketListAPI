import json
import unittest

from app import db
from app.models import User
from tests.test_resources import BaseTest


class TestAuthorization(BaseTest):

    def test_register_succesfully(self):
        endpoint = '/api/v1/auth/register'
        credentials = {'username': 'dee', 'password': 'hello'}

        response = self.client.post(endpoint, data=credentials)
        welcome_message = json.loads(response.get_data(as_text=True)).get('message')

        self.assertEqual("Welcome dee to the Bucketlist Service.", welcome_message)
        self.assertTrue(response.status_code == 201)

    def test_register_user_persistence(self):
        endpoint = '/api/v1/auth/register'
        credentials = {'username': 'dee', 'password': 'hello'}

        self.client.post(endpoint, data=credentials)
        user = User.query.filter_by(username='dee').first()

        self.assertIsNotNone(user)
        self.assertIn('dee', user.username)

    def test_register_with_exisitng_username(self):
        db.session.add(self.user)
        db.session.commit()
        endpoint = '/api/v1/auth/register'
        credentials = {'username': 'damidee', 'password': 'andela'}

        response = self.client.post(endpoint, data=credentials)
        error_message = json.loads(response.get_data(as_text=True)).get('message')

        self.assertEqual(error_message, "The username already exist.Choose another")
        self.assertTrue(response.status_code == 406)

    def test_register_user_with_blank_fields(self):
        endpoint = '/api/v1/auth/register'
        credentials = {'username': '', 'password': ''}

        response = self.client.post(endpoint, data=credentials)
        error_message = json.loads(response.get_data(as_text=True)).get('message')

        self.assertEqual("User's details cannot be empty. Please specify a username and password", error_message)
        self.assertTrue(response.status_code == 406)

    def test_login_with_valid_details(self):
        db.session.add(self.user)
        db.session.commit()
        endpoint = '/api/v1/auth/login'
        credentials = {'username': 'damidee', 'password': 'yello'}

        response = self.client.post(endpoint, data=credentials)
        login_message = json.loads(response.get_data(as_text=True)).get('message')

        self.assertEqual("logged in successfully as damidee", login_message)
        self.assertTrue(response.status_code == 202)

    def test_invalid_login_details(self):
        db.session.add(self.user)
        db.session.commit()
        endpoint = '/api/v1/auth/login'
        credentials = {'username': 'dadee', 'password': 'yello'}

        response = self.client.post(endpoint, data=credentials)
        error_message = json.loads(response.get_data(as_text=True)).get('message')

        self.assertIn("Please enter a valid username or password", error_message)
        self.assertTrue(response.status_code == 406)


if __name__ == '__main__':
    unittest.main()
