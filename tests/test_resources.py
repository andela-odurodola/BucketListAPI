#!flask/bin/python3/

import unittest
import json

from app import db
from app.models import User, BucketList
from tests.test_utils import BaseTest


class TestResources(BaseTest):
    """
    Unit tests for each resource method such as GET, POST,
    PUT and DELETE.
    """

    def test_get_bucketlist_without_login(self):
        response = self.client.get('/api/v1/bucketlists/')
        output = response.data
        self.assertEqual(response.status_code, 401)
        self.assertIn(b'Login is required', output)

    def test_post_bucketlist(self):
        endpoint = '/api/v1/bucketlists/'
        data = {'name': 'Win a Soul'}

        response = self.client.post(endpoint, headers={'Token': self.token}, data=data)

        self.assertEqual(response.status_code, 200)

    def test_post_bucketlist_with_existing_name(self):
        db.session.add(self.bucketlist)
        db.session.commit()
        endpoint = '/api/v1/bucketlists/'
        data = {'name': 'Leggo'}

        response = self.client.post(endpoint, headers={'Token':
                                    self.token}, data=data)
        error_message = json.loads(response.get_data(as_text=True)).get('message')

        self.assertEqual(response.status_code, 409)
        self.assertIn('A Bucketlist with the name already exists', error_message)

    def test_post_bucketlist_with_no_name(self):
        endpoint = '/api/v1/bucketlists/'
        data = {'name': ''}

        response = self.client.post(endpoint, headers={'Token': self.token}, data=data)
        error_message = json.loads(response.get_data(as_text=True)).get('message')

        self.assertEqual(response.status_code, 400)
        self.assertIn('The BucketList name cannot be empty', error_message)

    def test_for_invalid_bucketlist_id(self):
        db.session.add_all([self.bucketlist, self.bucketlist1])
        db.session.commit()
        endpoint = '/api/v1/bucketlists/6'

        response = self.client.get(endpoint, headers={'Token': self.token})

        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Bucketlist does not exist', response.data)

    def test_put_bucketlist_successfully(self):
        db.session.add(self.bucketlist)
        db.session.commit()
        endpoint = '/api/v1/bucketlists/1'
        data = {'name': 'Leggo to ibadan'}

        response = self.client.put(endpoint, headers={'Token': self.token}, data=data)

        self.assertEqual(response.status_code, 200)

    def test_persistence_of_method_put(self):
        db.session.add(self.bucketlist)
        db.session.commit()
        endpoint = '/api/v1/bucketlists/1'
        data = {'name': 'Leggo to ibadan'}

        self.client.put(endpoint, headers={'Token': self.token}, data=data)
        bucketlist1 = BucketList.query.filter_by(name='Leggo').first()
        bucketlist2 = BucketList.query.filter_by(name='Leggo to ibadan').first()

        self.assertFalse(bucketlist1 == bucketlist2)

    def test_put_bucketlist_fail(self):
        endpoint = '/api/v1/bucketlists/1'
        data = {'name': ''}
        response = self.client.put(endpoint, headers={'Token': self.token}, data=data)
        error_message = json.loads(response.get_data(as_text=True)).get('message')

        self.assertEqual(response.status_code, 400)
        self.assertEqual('BucketList Item is not updated', error_message)

    def test_delete_a_bucketlist(self):
        db.session.add(self.bucketlist)
        db.session.commit()
        endpoint = '/api/v1/bucketlists/1'

        response = self.client.delete(endpoint, headers={'Token': self.token})
        delete_message = json.loads(response.get_data(as_text=True)).get('message')

        self.assertEqual(response.status_code, 200)
        self.assertEqual('BucketList has been deleted', delete_message)

    def test_get_a_bucketlist(self):
        db.session.add(self.bucketlist)
        db.session.commit()
        endpoint = '/api/v1/bucketlists/1'

        response = self.client.get(endpoint, headers={'Token': self.token})

        self.assertEqual(response.status_code, 200)

    def test_get_all_bucketlist(self):
        db.session.add_all([self.bucketlist, self.bucketlist1])
        db.session.commit()
        endpoint = '/api/v1/bucketlists/'

        response = self.client.get(endpoint, headers={'Token': self.token})

        self.assertEqual(response.status_code, 200)

    def test_for_invalid_url(self):
        endpoint = '/api/bucketlists/'

        response = self.client.get(endpoint, headers={'Token': self.token})

        self.assertEqual(response.status_code, 404)

    def test_get_all_bucketlist_items(self):
        db.session.add_all([self.bucketlist, self.bucketlistitem])
        db.session.commit()
        endpoint = '/api/v1/bucketlists/1/items/'

        response = self.client.get(endpoint, headers={'Token': self.token})

        self.assertEqual(response.status_code, 200)

    def test_post_bucketlist_item_succesfully(self):
        db.session.add_all([self.bucketlist, self.bucketlist1, self.bucketlistitem])
        db.session.commit()
        endpoint = '/api/v1/bucketlists/2/items/'
        data = {'name': 'By 2020'}

        response = self.client.post(endpoint, headers={'Token': self.token}, data=data)

        self.assertEqual(response.status_code, 200)

    def test_post_bucketlistitem_with_existing_name(self):
        db.session.add_all([self.bucketlist, self.bucketlist1, self.bucketlistitem])
        db.session.commit()
        data = {'name': 'To greece'}
        endpoint = '/api/v1/bucketlists/1/items/'

        response = self.client.post(endpoint, headers={'Token': self.token}, data=data)
        error_message = json.loads(response.get_data(as_text=True)).get('message')

        self.assertEqual(response.status_code, 409)
        self.assertIn('Bucketlist Item exists', error_message)

    def test_post_bucketlistitem_with_no_name(self):
        db.session.add_all([self.bucketlist, self.bucketlist1, self.bucketlistitem])
        db.session.commit()
        endpoint = '/api/v1/bucketlists/1/items/'
        data = {'name': ''}

        response = self.client.post(endpoint, headers={'Token': self.token}, data=data)
        error_message = json.loads(response.get_data(as_text=True)).get('message')

        self.assertEqual(response.status_code, 400)
        self.assertIn('BucketList Item has no name', error_message)

    def test_delete_a_bucketlist_item(self):
        db.session.add_all([self.bucketlist, self.bucketlist1, self.bucketlistitem])
        db.session.commit()
        endpoint = '/api/v1/bucketlists/1/items/1'

        response = self.client.delete(endpoint, headers={'Token': self.token})

        self.assertEqual(response.status_code, 200)

    def test_get_a_bucketlist_item(self):
        db.session.add_all([self.bucketlist, self.bucketlist1, self.bucketlistitem])
        db.session.commit()
        endpoint = '/api/v1/bucketlists/1/items/1'

        response = self.client.get(endpoint, headers={'Token': self.token})

        self.assertEqual(response.status_code, 200)

    def test_put_bucketlist_item_successfully(self):
        db.session.add_all([self.bucketlist, self.bucketlist1, self.bucketlistitem])
        db.session.commit()
        endpoint = '/api/v1/bucketlists/1/items/1'
        data = {'done': True}

        response = self.client.put(endpoint, headers={'Token': self.token}, data=data)

        self.assertEqual(response.status_code, 200)

    def test_search_bucketlist_name(self):
        db.session.add_all([self.bucketlist, self.bucketlist1, self.bucketlistitem])
        db.session.commit()

        response = self.client.get('/api/v1/bucketlists/?q=leggo', headers={'Token': self.token})

        self.assertEqual(response.status_code, 200)

    def test_paginate_bucketlist(self):
        db.session.add_all([self.bucketlist, self.bucketlist1, self.bucketlistitem])
        db.session.commit()

        response = self.client.get('/api/v1/bucketlists/?limit=50', headers={'Token': self.token})

        self.assertEqual(response.status_code, 200)

    def test_models_can_convert_to_dict(self):
        user_obj = self.user.to_dict()

        self.assertIsInstance(user_obj, dict)
        self.assertIsNotNone(user_obj["username"])
        self.assertIsNotNone(user_obj["password_hash"])
