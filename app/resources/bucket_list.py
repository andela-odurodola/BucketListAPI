from flask_restful import Resource, request

from app.models import BucketList
from app.common.decorators import invalid_id, login_required
from app.common.custom_messages import CustomMessages
from app.common.helpers import delete_bucketlist, update_database, get_current_user


class ABucketList(Resource):
    """
    It returns a single bucketlist response based
    on a particular request.
    """

    method_decorators = [invalid_id, login_required]

    def get(self, bucketlist_id):
        token = request.headers.get('Token')
        current_user = get_current_user(token)
        bucketlist = BucketList.query.filter_by(id_no=bucketlist_id, created_by=current_user.id_no).first()
        return bucketlist.to_dict(), 200

    def delete(self, bucketlist_id):
        token = request.headers.get('Token')
        current_user = get_current_user(token)
        bucketlist = BucketList.query.filter_by(id_no=bucketlist_id, created_by=current_user.id_no).first()
        delete_message = delete_bucketlist(bucketlist)
        if delete_message['delete_successful']:
            return CustomMessages.sucess_message('BucketList has been deleted'), 200
        return delete_message['error_message']

    def put(self, bucketlist_id):
        # It updates the bucketlist with a particular id.

        name = request.form.get('name')
        token = request.headers.get('Token')
        current_user = get_current_user(token)
        bucketlist_check = BucketList.query.filter_by(name=name, created_by=current_user.id_no).first()
        if bucketlist_check:
            return CustomMessages.conflict('This bucketlist has been created by you!'), 409
        else:
            bucketlist = BucketList.query.filter_by(id_no=bucketlist_id).first()
            bucketlist.name = name
            if name:
                update_message = update_database()
                if update_message['update_successful']:
                    return bucketlist.to_dict(), 200
                return update_message['error_message'], 500

            return CustomMessages.bad_request('BucketList Item is not updated'), 400
