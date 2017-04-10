import json
import unittest
from flask import Flask

from app import create_app, db
from app.models import User

class BaseTest(unittest.TestCase):
    """
    Base test to be used by each test method.
    It enables the DRY principles to be followed.
    """

    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

        # reusable instance
        self.user = User(username='damidee', password='yello')

        # create table
        db.create_all()


    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


class TestAuthorization(BaseTest):

    def test_register_succesfully(self):
        response = self.client.post('/api/v1/auth/register', data={'username': 'dee', 'password': 'hello'})
        result = json.loads(response.get_data(as_text=True))
        output = response.status_code
        self.assertEqual("Welcome dee to the Bucketlist Service.", result['message'])
        self.assertTrue(output == 201)
        user = User.query.filter_by(username='dee').first()
        self.assertIsNotNone(user)
        self.assertIn('dee', user.username)

    def test_register_with_exisitng_username(self):
        db.session.add(self.user)
        db.session.commit()
        response = self.client.post('/api/v1/auth/register', data={'username': 'damidee', 'password': 'andela'})
        result = json.loads(response.get_data(as_text=True))
        self.assertEqual(result['message'], "The username already exist.Choose another")
        output = response.status_code
        self.assertTrue(output == 406)

    def test_register_user_with_blank_fields(self):
        response = self.client.post('/api/v1/auth/register', data={'username': '', 'password': ''})
        result = json.loads(response.get_data(as_text=True))
        output = response.status_code
        self.assertEqual("User's details cannot be empty", result['message'])
        self.assertTrue(output == 406)

    def test_login_with_valid_details(self):
        db.session.add(self.user)
        db.session.commit()
        response = self.client.post('/api/v1/auth/login', data={'username': 'damidee', 'password': 'yello'})
        result = json.loads(response.get_data(as_text=True))
        self.assertEqual("logged in successfully as damidee", result['message'])
        output = response.status_code
        self.assertTrue(output == 202)

    def test_invalid_login_details(self):
        db.session.add(self.user)
        db.session.commit()
        response = self.client.post('/api/v1/auth/login', data={'username': 'dadee', 'password': 'yello'})
        result = json.loads(response.get_data(as_text=True))
        self.assertIn("Please enter a valid username or password", result['message'])
        output = response.status_code
        self.assertTrue(output == 400)


if __name__ == '__main__':
    unittest.main()
