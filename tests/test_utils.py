import unittest

from app import create_app, db
from app.models import User, BucketList, BucketListItem


class BaseTest(unittest.TestCase):
    """
    Base test to be used by each test method.
    The test details are loaded each time a test is being run.
    """

    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

        db.create_all()

        self.create_test_user()
        self.user = User.query.filter_by(username='damidee').first()
        self.create_bucket_list()
        self.bucket_list = BucketList.query.filter_by(name='Leggo').first()
        self.user_data = {
            'username': 'damidee',
            'password': 'yello'
        }
        self.token = self.get_login_credentials()
        self.bucketlist = BucketList(name='Leggo', created_by=self.user.id_no)
        self.bucketlist1 = BucketList(name='See the world', created_by=self.user.id_no)
        self.bucketlistitem = BucketListItem(name='To greece', done=True, bucketlist_id=self.bucket_list.id_no)

    def create_test_user(self):
        user = User.query.filter_by(username='damidee').first()
        if not user:
            test_user = User(username='damidee', password='yello')
            db.session.add(test_user)
            db.session.commit()

    def create_bucket_list(self):
        bucket_list = BucketList.query.filter_by(name='Leggo').first()
        if not bucket_list:
            test_bucketlist = BucketList(name='Leggo', created_by=self.user.id_no)
            db.session.add(test_bucketlist)
            db.session.commit()

    def get_login_credentials(self):
        login_response = self.client.post('/api/v1/auth/login', data=self.user_data)
        self.assertEqual(login_response.status_code, 200)
        user = User.query.filter_by(username='damidee').first()
        token = user.generate_auth_token()
        return token


    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
