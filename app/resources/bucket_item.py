from flask_restful import Resource, request

from app.models import BucketListItem
from app.common.decorators import invalid_id, invalid_item_id, login_required
from app.common.custom_messages import CustomMessages
from app.common.helpers import delete_bucketlist, update_database


class BucketItem(Resource):
    """
    It retrieves a single bucket list item based
    on the bucket list id specified.
    """

    method_decorators = [invalid_id, invalid_item_id, login_required]

    def get(self, bucketlist_id, bucketitem_id):
        """
        The query searches first by looking into the database
        for the bucketlist id and then the bucketlistitem id.
        """

        bucketlist_item = BucketListItem.query.filter_by(bucketlist_id=bucketlist_id,
                        id_no=bucketitem_id).first()
        return bucketlist_item.to_dict(), 200

    def delete(self, bucketlist_id, bucketitem_id):
        bucketlist_item = BucketListItem.query.filter_by(bucketlist_id=bucketlist_id,
                        id_no=bucketitem_id).first()
        delete_bucketlist(bucketlist_item)
        return CustomMessages.sucess_message('BucketListItem has been deleted'), 200

    def put(self, bucketlist_id, bucketitem_id):
        bucketlist_item = BucketListItem.query.filter_by(bucketlist_id=bucketlist_id,
                        id_no=bucketitem_id).first()
        name = request.form.get('name')
        bucketlist_item.name = name or bucketlist_item.name
        done = request.form.get('done')
        if done:
            done = (done.lower() == 'true')
            bucketlist_item.done = done
        if update_database():
            return bucketlist_item.to_dict(), 200
        else:
            return CustomMessages.bad_request('The Bucketlist is not updated'), 400
