from flask import request
from flask_restful import Resource, Api, abort
from api.models import BucketList
from api.common.helpers import getbucketlist, delete_bucketlist, update_database
# check if bucketlistid exists and return an error if not


class ABucketList(Resource):
    """
    It returns a single bucketlist response based
    on a particular request.
    """

    def get(self, bucketlist_id):
        bucketlist = BucketList.query.filter_by(id_no=bucketlist_id).first()
        bucket_list = getbucketlist(bucketlist)
        return {'BucketList': bucket_list}, 200

    def delete(self, bucketlist_id):
        bucketlist = BucketList.query.filter_by(id_no=bucketlist_id).first()
        delete_bucketlist(bucketlist)
        return 'BucketList {} has been deleted'.format(bucketlist_id), 204

    def put(self, bucketlist_id):
        """
        It updates the bucketlist with a particular id.
        """
        name = request.form.get('name')
        bucketlist = BucketList.query.filter_by(id_no=bucketlist_id).first()
        bucketlist.name = name
        if update_database():
            bucket_list = getbucketlist(bucketlist)
            return {'BucketList': bucket_list}, 201
        else:
            return 'BucketList {} is not updated'.format(bucketlist_id), 400
