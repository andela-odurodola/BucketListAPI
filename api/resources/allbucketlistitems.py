from flask_restful import Resource, request, abort
from api.models import BucketListItem
from api.common.helpers import abucketlistitem, save_into_database

class AllBucketListItems(Resource):
    def get(self, bucketlist_id):
        bucketlist_item = BucketListItem.query.filter_by(bucketlist_id=bucketlist_id).all()
        for each_bucketlist_item in bucketlist_item:
            bucket_list_item = abucketlistitem(each_bucketlist_item)
        return {'BucketListItem': bucket_list_item}, 200

    def post(self, bucketlist_id):
        name = request.form.get('name')
        bucketlist_item = BucketListItem.query.filter_by(name=name,
                        bucketlist_id=bucketlist_id).first()
        if name:
            if bucketlist_item:
                return 'Bucketlist Item exists', 406
            else:
                bucketlistitem = BucketListItem(name=name)
                if save_into_database(bucketlistitem):
                    return abucketlistitem(bucketlistitem), 201
        else:
            'BucketList Item has no name', 406
