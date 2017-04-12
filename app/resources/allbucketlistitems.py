from flask_restful import Resource, request

from app.models import BucketListItem
from app.common.errors import custom_errors, invalid_id, login_required
from app.common.helpers import abucketlistitem, save_into_database

class AllBucketListItems(Resource):

    method_decorators = [invalid_id, login_required]

    def get(self, bucketlist_id):
        bucketlist_item = BucketListItem.query.filter_by(bucketlist_id=bucketlist_id).all()
        return [bucket_list_item.to_dict() for bucket_list_item in bucketlist_item], 200

    def post(self, bucketlist_id):
        name = request.form.get('name')
        bucketlist_item = BucketListItem.query.filter_by(name=name, bucketlist_id=
                                                         bucketlist_id).first()
        if name:
            if bucketlist_item:
                return custom_errors['BucketListItemExists'], 406
            else:
                bucketlistitem = BucketListItem(name=name, bucketlist_id=bucketlist_id)
                if save_into_database(bucketlistitem):
                    return bucketlistitem.to_dict(), 201
        else:
            return custom_errors['BucketListItemNameIsEmpty'], 406
