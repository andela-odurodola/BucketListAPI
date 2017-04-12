#!flask/bin/python3/

import unittest
import json
from flask import Flask

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

        self.user = User(username='damidee', password='yello')
        self.user_data = {'username': 'damidee',
                          'password': 'yello'}

        self.bucketlist = BucketList(name='Leggo', created_by=self.user.username)
        self.bucketlist1 = BucketList(name='See the world', created_by=self.user.username)

        self.bucketlistitem = BucketListItem(name='To greece', done=True, bucketlist_id=1)

        db.create_all()


    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


class TestResources(BaseTest):
    """
    Unit tests for each resource method such as GET, POST,
    PUT and DELETE.
    """
    def login_credentials(self):
        db.session.add(self.user)
        db.session.commit()
        login_response = self.client.post('/api/v1/auth/login', data=self.user_data)
        self.assertTrue(login_response.status_code == 202)
        user = User.query.filter_by(username='damidee').first()
        token = user.generate_auth_token()
        return token

    def test_get_bucketlist_without_login(self):
        response = self.client.get('/api/v1/bucketlists/')
        output = response.data
        self.assertEqual(response.status_code, 401)
        self.assertIn(b'Login is required', output)

    def test_post_bucketlist(self):
        response = self.client.post('/api/v1/bucketlists/', headers={'Token': self.login_credentials()}, data={'name': 'Win a Soul'})
        output = response.status_code
        self.assertTrue(output == 201)

    def test_post_bucketlist_with_existing_name(self):
        db.session.add(self.bucketlist)
        db.session.commit()
        response = self.client.post('/api/v1/bucketlists/', headers={'Token':
                                    self.login_credentials()}, data={'name': 'Leggo'})
        output = json.loads(response.get_data(as_text=True))
        self.assertTrue(response.status_code == 406)
        self.assertIn('A Bucketlist with the name already exists', output['message'])

    def test_post_bucketlist_with_no_name(self):
        response = self.client.post('/api/v1/bucketlists/', headers={'Token': self.login_credentials()}, data={'name': ''})
        output = json.loads(response.get_data(as_text=True))
        self.assertTrue(response.status_code == 406)
        self.assertIn('The BucketList name cannot be empty', output['message'])

    def test_for_invalid_bucketlist_id(self):
        db.session.add_all([self.bucketlist, self.bucketlist1])
        db.session.commit()
        response = self.client.get('/api/v1/bucketlists/6', headers={'Token': self.login_credentials()})
        output = response.data
        print(response.status_code)
        self.assertTrue(response.status_code == 400)
        self.assertIn(b'Bucketlist does not exist', output)

    def test_put_bucketlist_successfully(self):
        db.session.add(self.bucketlist)
        db.session.commit()
        response = self.client.put('/api/v1/bucketlists/1', headers={'Token': self.login_credentials()}, data={'name': 'Leggo to ibadan'})
        self.assertTrue(response.status_code == 201)
        bucketlist1 = BucketList.query.filter_by(name='Leggo').first()
        bucketlist2 = BucketList.query.filter_by(name='Leggo to ibadan').first()
        self.assertFalse(bucketlist1 == bucketlist2)

    def test_put_bucketlist_fail(self):
        response = self.client.put('/api/v1/bucketlists/1', headers={'Token': self.login_credentials()}, data={'name': ''})
        output = json.loads(response.get_data(as_text=True))
        self.assertTrue(response.status_code == 400)
        self.assertTrue('The Bucketlist is not updated', output['message'])

    def test_delete_a_bucketlist(self):
        db.session.add(self.bucketlist)
        db.session.commit()
        response = self.client.delete('/api/v1/bucketlists/1', headers={'Token': self.login_credentials()})
        self.assertTrue(response.status_code == 200)
        output = json.loads(response.get_data(as_text=True))
        self.assertTrue('BucketList has been deleted', output['message'])

    def test_get_a_bucketlist(self):
        db.session.add(self.bucketlist)
        db.session.commit()
        response = self.client.get('/api/v1/bucketlists/1', headers={'Token': self.login_credentials()})
        self.assertTrue(response.status_code == 200)
        bucketlist = BucketList.query.filter_by(id_no=1).first()
        self.assertIsNotNone(bucketlist)

    def test_get_all_bucketlist(self):
        db.session.add_all([self.bucketlist, self.bucketlist1])
        db.session.commit()
        response = self.client.get('/api/v1/bucketlists/', headers={'Token': self.login_credentials()})
        self.assertTrue(response.status_code == 200)

    def test_for_invalid_url(self):
        response = self.client.get('/api/bucketlists/', headers={'Token': self.login_credentials()})
        self.assertTrue(response.status_code == 404)

    def test_get_all_bucketlist_items(self):
        db.session.add_all([self.bucketlist, self.bucketlistitem])
        db.session.commit()
        response = self.client.get('/api/v1/bucketlists/1/items/', headers={'Token': self.login_credentials()})
        print(response.status_code)
        self.assertTrue(response.status_code == 200)

    def test_post_bucketlist_item_succesfully(self):
        db.session.add_all([self.bucketlist, self.bucketlist1, self.bucketlistitem])
        db.session.commit()
        response = self.client.post('/api/v1/bucketlists/2/items/', headers={'Token': self.login_credentials()}, data={'name': 'By 2020'})
        self.assertTrue(response.status_code == 201)
        bucket_item = BucketListItem.query.filter_by(name='By 2020',
                                                     bucketlist_id=2).first()
        self.assertIsNotNone(bucket_item)

    def test_post_bucketlistitem_with_existing_name(self):
        db.session.add_all([self.bucketlist, self.bucketlist1, self.bucketlistitem])
        db.session.commit()
        response = self.client.post('/api/v1/bucketlists/1/items/', headers={'Token': self.login_credentials()}, data={'name': 'To greece'})
        self.assertTrue(response.status_code == 406)
        result = json.loads(response.get_data(as_text=True))
        self.assertIn('Bucketlist Item exists', result['message'])

    def test_post_bucketlistitem_with_no_name(self):
        db.session.add_all([self.bucketlist, self.bucketlist1, self.bucketlistitem])
        db.session.commit()
        response = self.client.post('/api/v1/bucketlists/1/items/', headers={'Token': self.login_credentials()}, data={'name': ''})
        self.assertTrue(response.status_code == 406)
        result = json.loads(response.get_data(as_text=True))
        self.assertIn('BucketList Item has no name', result['message'])

    def test_delete_a_bucketlist_item(self):
        db.session.add_all([self.bucketlist, self.bucketlist1, self.bucketlistitem])
        db.session.commit()
        response = self.client.delete('/api/v1/bucketlists/1/items/1', headers={'Token': self.login_credentials()})
        self.assertTrue(response.status_code == 200)

    def test_get_a_bucketlist_item(self):
        db.session.add_all([self.bucketlist, self.bucketlist1, self.bucketlistitem])
        db.session.commit()
        response = self.client.get('/api/v1/bucketlists/1/items/1', headers={'Token': self.login_credentials()})
        self.assertTrue(response.status_code == 200)

    def test_put_bucketlist_item_successfully(self):
        db.session.add_all([self.bucketlist, self.bucketlist1, self.bucketlistitem])
        db.session.commit()
        response = self.client.put('/api/v1/bucketlists/1/items/1', headers={'Token': self.login_credentials()}, data={'done': True})
        self.assertTrue(response.status_code == 201)
        bucketitem1 = BucketListItem.query.filter_by(done=False).first()
        bucketitem2 = BucketListItem.query.filter_by(done=True).first()
        self.assertFalse(bucketitem1 == bucketitem2)

    def test_search_bucketlist_name(self):
        db.session.add_all([self.bucketlist, self.bucketlist1, self.bucketlistitem])
        db.session.commit()
        response = self.client.get('/api/v1/bucketlists/?q=leggo', headers={'Token': self.login_credentials()})
        self.assertTrue(response.status_code == 200)

    def test_paginate_bucketlist(self):
        db.session.add_all([self.bucketlist, self.bucketlist1, self.bucketlistitem])
        db.session.commit()
        response = self.client.get('/api/v1/bucketlists/?limit=50', headers={'Token': self.login_credentials()})
        self.assertTrue(response.status_code == 200)


class TestSerialiserMixin(BaseTest):

    def test_models_can_convert_to_dict(self):
        user_obj = self.user.to_dict()
        self.assertIsInstance(user_obj, dict)
        self.assertIsNotNone(user_obj["username"])
        self.assertIsNotNone(user_obj["password_hash"])

    def test_can_create_models_from_dict(self):
        pass

if __name__ == '__main__':
    unittest.main()
