from flask_restful import Resource, request, abort
from app.models import BucketList
from app.common.errors import custom_errors
from app.common.helpers import getbucketlist, save_into_database


class AllBucketLists(Resource):
    # It returns all bucketlists.
    # decorators = [auth.login_required]

    def get(self):
        bucketlist = BucketList.query.all()
        bucket_list = [getbucketlist(each_bucketlist)
                    for each_bucketlist in bucketlist]
        return {'BucketList': bucket_list}, 200

    def post(self):
        name = request.form.get('name')
        bucketlist = BucketList.query.filter_by(name=name).first()
        if name:
            if bucketlist:
                return custom_errors['BucketListNameExistsError']
            else:
                bucket_list = BucketList(name=name)
                if save_into_database(bucket_list):
                    return getbucketlist(bucket_list), 201
        else:
            return custom_errors['BucketListNameIsEmpty']
