from flask_restful import Resource, request
from api.models import BucketListItem
from api.common.helpers import abucketlistitem, delete_bucketlist, update_database


class ABucketListItem(Resource):
    """
    It retrieves a single bucket list item based
    on the bucket list id specified.
    """
    def get(self, bucketlist_id, bucketitem_id):
        """
        The query searches first by looking into the database
        for the bucketlist id and then the bucketlistitem id.
        """
        bucketlist_item = BucketListItem.query.filter_by(bucketlist_id=bucketlist_id, id_no=bucketitem_id).first()
        bucket_list_item = abucketlistitem(bucketlist_item)
        return {'BucketListItem': bucket_list_item}, 200

    def delete(self, bucketlist_id, bucketitem_id):
        bucketlist_item = BucketListItem.query.filter_by(bucketlist_id=bucketlist_id, id_no=bucketitem_id).first()
        delete_bucketlist(bucketlist_item)
        return 'BucketListItem {} has been deleted'.format(bucketitem_id), 204

    def put(self, bucketlist_id, bucketitem_id):
        name = request.form.get('name')
        bucketlist_item = BucketListItem.query.filter_by(bucketlist_id=bucketlist_id, id_no=bucketitem_id).first()
        bucketlist_item.name = name
        if update_database():
            bucket_list_item = abucketlistitem(bucketlist_item)
            return {'BucketList Item': bucket_list_item}, 201
        else:
            return 'BucketList Item {} is not updated'.format(bucketitem_id), 400
