import unittest
import json
from flask import Flask

from app import create_app, db
from app.models import User, BucketList, BucketListItem


class BaseTest(unittest.TestCase):
    """
    Base test to be used by each test method.
    """

    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

        db.create_all()
        self.user = User(username='damidee', password='yello')

        self.bucketlist = BucketList(name='Leggo', created_by=self.user.username)
        self.bucketlist1 = BucketList(name='See the world', created_by=self.user.username)

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
        response = self.client.post('/api/v1/bucketlists/', data={'name': 'Leggo'})
        output = (response.data)
        self.assertTrue(b'406', output)
        self.assertIn(b'A Bucketlist with the name already exists', output)

    def test_post_bucketlist_with_no_name(self):
        response = self.client.post('/api/v1/bucketlists/', data={'name': ''})
        output = (response.data)
        self.assertTrue(b'406', output)
        self.assertIn(b'The BucketList name cannot be empty', output)

    def test_for_invalid_bucketlist_id(self):
        response = self.client.get('/api/v1/bucketlists/6')
        result = response.data
        msg = response.status_code
        self.assertTrue(msg == 400)
        self.assertIn(b'Bucketlist does not exist', result)

    def test_put_bucketlist_successfully(self):
        response = self.client.put('/api/v1/bucketlists/1', data={'name': 'Leggo to ibadan'})
        output = response.status_code
        self.assertTrue(output == 201)
        bucketlist1 = BucketList.query.filter_by(name='Leggo').first()
        bucketlist2 = BucketList.query.filter_by(name='Leggo to ibadan').first()
        self.assertFalse(bucketlist1 == bucketlist2)

    def test_put_bucketlist_fail(self):
        response = self.client.put('/api/v1/bucketlists/1', data={'name': ''})
        output = response.data
        re = response.status_code
        self.assertTrue(re == 400)
        self.assertTrue(b'The Bucketlist is not updated', output)

    # def test_delete_a_bucketlist(self):
    #     response = self.client.delete('/api/v1/bucketlists/2')
    #     pass

    def test_get_a_bucketlist(self):
        response = self.client.get('/api/v1/bucketlists/1')
        result = response.status_code
        self.assertTrue(result == 200)

    def test_get_all_bucketlist(self):
        response = self.client.get('/api/v1/bucketlists/')
        result = response.status_code
        self.assertTrue(result == 200)

    def test_for_invalid_url(self):
        response = self.client.get('/api/bucketlists/')
        result = response.status_code
        self.assertTrue(result == 404)

    def test_get_all_bucketlist_items(self):
        response = self.client.get('/api/v1/bucketlists/1/items/')
        result = response.status_code
        self.assertTrue(result == 200)

    def test_post_bucketlist_item_succesfully(self):
        response = self.client.post('/api/v1/bucketlists/2/items/', data={'name': 'By 2020'})
        output = response.status_code
        self.assertTrue(output == 201)
        bucket_item = BucketListItem.query.filter_by(name='By 2020',
                                                     bucketlist_id=2).first()
        self.assertIsNotNone(bucket_item)

    def test_post_bucketlistitem_with_existing_name(self):
        response = self.client.post('/api/v1/bucketlists/1/items/', data={'name': 'To greece'})
        output = response.status_code
        self.assertTrue(output == 406)
        result = response.data
        self.assertIn(b'Bucketlist Item exists', result)

    def test_post_bucketlistitem_with_no_name(self):
        response = self.client.post('/api/v1/bucketlists/1/items/', data={'name': ''})
        output = response.status_code
        self.assertTrue(output == 406)
        result = response.data
        self.assertIn(b'BucketList Item has no name', result)

    # def test_delete_a_bucketlist_item(self):
    #     pass
    #
    def test_get_a_bucketlist_item(self):
        pass

    def test_put_bucketlist_item_fail(self):
        response = self.client.put('/api/v1/bucketlists/1/item/1', data={'name': ''})
        output = response.data
        re = response.status_code
        self.assertTrue(re == 400)
        self.assertTrue(b'The Bucketlist is not updated', output)

    # def test_put_bucketlist_successfully(self):
    #     pass


if __name__ == '__main__':
    unittest.main()
