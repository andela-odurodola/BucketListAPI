from flask_restful import Resource, request, abort
from app.models import BucketListItem
from app.common.helpers import abucketlistitem, save_into_database

class AllBucketListItems(Resource):
    def get(self, bucketlist_id):
        bucketlist_item = BucketListItem.query.filter_by(bucketlist_id=bucketlist_id).all()
        bucket_list_item = [abucketlistitem(each_bucketlist_item)
                            for each_bucketlist_item in bucketlist_item]
        return {'BucketListItem': bucket_list_item}, 200

    def post(self, bucketlist_id):
        name = request.form.get('name')
        bucketlist_item = BucketListItem.query.filter_by(name=name,
                        bucketlist_id=bucketlist_id).first()
        if name:
            if bucketlist_item:
                return 'Bucketlist Item exists', 406
            else:
                bucketlistitem = BucketListItem(name=name, bucketlist_id=bucketlist_id)
                if save_into_database(bucketlistitem):
                    return abucketlistitem(bucketlistitem), 201
        else:
            'BucketList Item has no name', 406
