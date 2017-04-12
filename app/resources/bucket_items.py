from flask_restful import Resource, request

from app.models import BucketListItem
from app.common.decorators import invalid_id, login_required
from app.common.custom_messages import CustomMessages
from app.common.helpers import save_into_database

class BucketItems(Resource):

    method_decorators = [invalid_id, login_required]

    def get(self, bucketlist_id):
        bucketlist_item = BucketListItem.query.filter_by(bucketlist_id=bucketlist_id).all()
        return [bucket_list_item.to_dict() for bucket_list_item in bucketlist_item], 200

    def post(self, bucketlist_id):
        name = request.form.get('name')
        bucketlist_item = BucketListItem.query.filter_by(name=name, bucketlist_id=
                                                         bucketlist_id).first()
        if not name:
            return CustomMessages.not_acceptable('BucketList Item has no name'), 406

        if bucketlist_item:
            return CustomMessages.not_acceptable('Bucketlist Item exists'), 406

        bucketlistitem = BucketListItem(name=name, bucketlist_id=bucketlist_id)
        if save_into_database(bucketlistitem):
            return bucketlistitem.to_dict(), 201
