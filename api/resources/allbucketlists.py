from flask_restful import Resource, request, abort
from api.models import BucketList
from api.common.helpers import getbucketlist, save_into_database


class AllBucketLists(Resource):
    # It returns all bucketlists.
    def get(self):
        bucketlist = BucketList.query.all()
        for each_bucketlist in bucketlist:
            bucket_list = getbucketlist(each_bucketlist)
        return {'BucketList': bucket_list}, 200

    def post(self):
        name = request.form.get('name')
        bucket_list = BucketList(name=name)
        if name:
            if save_into_database(bucket_list):
                return getbucketlist(bucket_list), 201
        else:
            return 'BucketList has no name', 406
