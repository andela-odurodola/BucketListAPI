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

        self.user = User(username='damidee', password='yello')

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


class TestAuthorization(BaseTest):

    def test_login_with_valid_details(self):
        pass

    def test_invalid_login_details(self):
        pass

    def test_register_with_exisitng_username(self):
        pass

    def test_register_succesfully(self):
        pass

    def test_register_user_with_blank_fields(self):
        pass
