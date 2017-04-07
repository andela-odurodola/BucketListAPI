from flask_restful import Resource, request

from app.models import BucketList
from app.common.errors import custom_errors, invalid_id, login_required
from app.common.helpers import getbucketlist, delete_bucketlist, update_database, get_current_username


class ABucketList(Resource):
    """
    It returns a single bucketlist response based
    on a particular request.
    """
    method_decorators = [invalid_id, login_required]

    def get(self, bucketlist_id):
        bucketlist = BucketList.query.filter_by(id_no=bucketlist_id).first()
        bucket_list = getbucketlist(bucketlist)
        return {'BucketList': bucket_list}, 200

    def delete(self, bucketlist_id):
        bucketlist = BucketList.query.filter_by(id_no=bucketlist_id).first()
        delete_bucketlist(bucketlist)
        return custom_errors['BucketListDeleted'], 200

    def put(self, bucketlist_id):
        """
        It updates the bucketlist with a particular id.
        """
        name = request.form.get('name')
        token = request.headers.get('Token')
        current_user = get_current_username(token)
        bucketlist_check = BucketList.query.filter_by(name=name, created_by=current_user).first()
        if bucketlist_check:
            return custom_errors['BucketListAlreadyCreated'], 406
        else:
            bucketlist = BucketList.query.filter_by(id_no=bucketlist_id).first()
            bucketlist.name = name
            if name:
                if update_database():
                    bucket_list = getbucketlist(bucketlist)
                    return {'BucketList': bucket_list}, 201
            else:
                return custom_errors['BucketListNotUpdated'], 400
