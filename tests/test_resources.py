import unittest
from flask import Flask

from app import create_app, db
from app.models import User, BucketList, BucketListItem


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

        db.create_all()
        self.user = User(username='damidee', password='yello')

        self.bucketlist = BucketList(name='Leggo', created_by=self.user.username)

        self.bucketlistitem = BucketListItem(name='To greece', done=True, bucketlist_id=1)
        db.session.add_all([self.user, self.bucketlist, self.bucketlistitem])
        db.session.commit()


    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


class TestResources(BaseTest):
    # it tests for each Resource

    def test_post_bucketlist_without_login(self):
        pass

    def test_post_bucketlist_with_login(self):
        pass

    def test_post_bucketlist_with_existing_name(self):
        pass

    def test_post_bucketlist_with_no_name(self):
        pass

    def test_for_invalid_bucketlist_id(self):
        pass

    def test_for_empty_bucketlists(self):
        pass

    def test_put_bucketlist_successfully(self):
        pass

    def test_put_bucketlist_fail(self):
        pass

    def test_delete_a_bucketlist(self):
        pass

    def test_get_a_bucketlist(self):
        response = self.client.get('/api/v1/bucketlists/')
        result = response.status_code
        self.assertTrue(result == 200)

    def test_get_all_bucketlist(self):
        pass

    def test_for_invalid_url(self):
        pass

    def test_get_all_bucketlist_items(self):
        pass

    def test_post_bucketlist_item_succesfully(self):
        pass

    def test_post_bucketlistitem_with_existing_name(self):
        pass

    def test_post_bucketlistitem_with_no_name(self):
        pass

    def test_delete_a_bucketlist_item(self):
        pass

    def test_put_bucketlist_fail(self):
        pass

    def test_put_bucketlist_successfully(self):
        pass
