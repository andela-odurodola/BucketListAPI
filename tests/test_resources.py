#!flask/bin/python3/

import unittest
import json

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
        endpoint = '/api/v1/bucketlists/'
        credentials = {'name': 'Win a Soul'}

        response = self.client.post(endpoint, headers={'Token': self.login_credentials()}, data=credentials)

        self.assertTrue(response.status_code == 201)

    def test_post_bucketlist_with_existing_name(self):
        db.session.add(self.bucketlist)
        db.session.commit()
        endpoint = '/api/v1/bucketlists/'
        credentials = {'name': 'Leggo'}

        response = self.client.post(endpoint, headers={'Token':
                                    self.login_credentials()}, data=credentials)
        error_message = json.loads(response.get_data(as_text=True)).get('message')

        self.assertTrue(response.status_code == 406)
        self.assertIn('A Bucketlist with the name already exists', error_message)

    def test_post_bucketlist_with_no_name(self):
        endpoint = '/api/v1/bucketlists/'
        credentials = {'name': ''}

        response = self.client.post(endpoint, headers={'Token': self.login_credentials()}, data=credentials)
        error_message = json.loads(response.get_data(as_text=True)).get('message')

        self.assertTrue(response.status_code == 406)
        self.assertIn('The BucketList name cannot be empty', error_message)

    def test_for_invalid_bucketlist_id(self):
        db.session.add_all([self.bucketlist, self.bucketlist1])
        db.session.commit()
        endpoint = '/api/v1/bucketlists/6'

        response = self.client.get(endpoint, headers={'Token': self.login_credentials()})

        self.assertTrue(response.status_code == 400)
        self.assertIn(b'Bucketlist does not exist', response.data)

    def test_put_bucketlist_successfully(self):
        db.session.add(self.bucketlist)
        db.session.commit()
        endpoint = '/api/v1/bucketlists/1'
        credentials = {'name': 'Leggo to ibadan'}

        response = self.client.put(endpoint, headers={'Token': self.login_credentials()}, data=credentials)

        self.assertTrue(response.status_code == 201)

    def test_persistence_of_method_put(self):
        db.session.add(self.bucketlist)
        db.session.commit()
        endpoint = '/api/v1/bucketlists/1'
        credentials = {'name': 'Leggo to ibadan'}

        self.client.put(endpoint, headers={'Token': self.login_credentials()}, data=credentials)
        bucketlist1 = BucketList.query.filter_by(name='Leggo').first()
        bucketlist2 = BucketList.query.filter_by(name='Leggo to ibadan').first()

        self.assertFalse(bucketlist1 == bucketlist2)

    def test_put_bucketlist_fail(self):
        endpoint = '/api/v1/bucketlists/1'
        credentials = {'name': ''}
        response = self.client.put(endpoint, headers={'Token': self.login_credentials()}, data=credentials)
        error_message = json.loads(response.get_data(as_text=True)).get('message')

        self.assertTrue(response.status_code == 400)
        self.assertTrue('The Bucketlist is not updated', error_message)

    def test_delete_a_bucketlist(self):
        db.session.add(self.bucketlist)
        db.session.commit()
        endpoint = '/api/v1/bucketlists/1'

        response = self.client.delete(endpoint, headers={'Token': self.login_credentials()})
        delete_message = json.loads(response.get_data(as_text=True)).get('message')

        self.assertTrue(response.status_code == 200)
        self.assertTrue('BucketList has been deleted', delete_message)

    def test_get_a_bucketlist(self):
        db.session.add(self.bucketlist)
        db.session.commit()
        endpoint = '/api/v1/bucketlists/1'

        response = self.client.get(endpoint, headers={'Token': self.login_credentials()})

        self.assertTrue(response.status_code == 200)

    def test_get_all_bucketlist(self):
        db.session.add_all([self.bucketlist, self.bucketlist1])
        db.session.commit()
        endpoint = '/api/v1/bucketlists/'

        response = self.client.get(endpoint, headers={'Token': self.login_credentials()})

        self.assertTrue(response.status_code == 200)

    def test_for_invalid_url(self):
        endpoint = '/api/bucketlists/'

        response = self.client.get(endpoint, headers={'Token': self.login_credentials()})

        self.assertTrue(response.status_code == 404)

    def test_get_all_bucketlist_items(self):
        db.session.add_all([self.bucketlist, self.bucketlistitem])
        db.session.commit()
        endpoint = '/api/v1/bucketlists/1/items/'

        response = self.client.get(endpoint, headers={'Token': self.login_credentials()})

        self.assertTrue(response.status_code == 200)

    def test_post_bucketlist_item_succesfully(self):
        db.session.add_all([self.bucketlist, self.bucketlist1, self.bucketlistitem])
        db.session.commit()
        endpoint = '/api/v1/bucketlists/2/items/'
        credentials = {'name': 'By 2020'}

        response = self.client.post(endpoint, headers={'Token': self.login_credentials()}, data=credentials)

        self.assertTrue(response.status_code == 201)

    def test_post_bucketlistitem_with_existing_name(self):
        db.session.add_all([self.bucketlist, self.bucketlist1, self.bucketlistitem])
        db.session.commit()
        credentials = {'name': 'To greece'}
        endpoint = '/api/v1/bucketlists/1/items/'

        response = self.client.post(endpoint, headers={'Token': self.login_credentials()}, data=credentials)
        error_message = json.loads(response.get_data(as_text=True)).get('message')

        self.assertTrue(response.status_code == 406)
        self.assertIn('Bucketlist Item exists', error_message)

    def test_post_bucketlistitem_with_no_name(self):
        db.session.add_all([self.bucketlist, self.bucketlist1, self.bucketlistitem])
        db.session.commit()
        endpoint = '/api/v1/bucketlists/1/items/'
        credentials = {'name': ''}

        response = self.client.post(endpoint, headers={'Token': self.login_credentials()}, data=credentials)
        error_message = json.loads(response.get_data(as_text=True)).get('message')

        self.assertTrue(response.status_code == 406)
        self.assertIn('BucketList Item has no name', error_message)

    def test_delete_a_bucketlist_item(self):
        db.session.add_all([self.bucketlist, self.bucketlist1, self.bucketlistitem])
        db.session.commit()
        endpoint = '/api/v1/bucketlists/1/items/1'

        response = self.client.delete(endpoint, headers={'Token': self.login_credentials()})

        self.assertTrue(response.status_code == 200)

    def test_get_a_bucketlist_item(self):
        db.session.add_all([self.bucketlist, self.bucketlist1, self.bucketlistitem])
        db.session.commit()
        endpoint = '/api/v1/bucketlists/1/items/1'

        response = self.client.get(endpoint, headers={'Token': self.login_credentials()})

        self.assertTrue(response.status_code == 200)

    def test_put_bucketlist_item_successfully(self):
        db.session.add_all([self.bucketlist, self.bucketlist1, self.bucketlistitem])
        db.session.commit()
        endpoint = '/api/v1/bucketlists/1/items/1'
        credentials = {'done': True}

        response = self.client.put(endpoint, headers={'Token': self.login_credentials()}, data=credentials)

        self.assertTrue(response.status_code == 201)

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

    def test_models_can_convert_to_dict(self):
        user_obj = self.user.to_dict()

        self.assertIsInstance(user_obj, dict)
        self.assertIsNotNone(user_obj["username"])
        self.assertIsNotNone(user_obj["password_hash"])


if __name__ == '__main__':
    unittest.main()
