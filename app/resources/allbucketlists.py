from flask_restful import Resource, request, url_for

from app.models import BucketList
from app.common.errors import custom_errors, login_required
from app.common.helpers import getbucketlist, save_into_database, get_current_username


class AllBucketLists(Resource):
    # It returns all bucketlists.
    method_decorators = [login_required]

    def get(self):
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 20, type=int)
        q = request.args.get('q', '')
        token = request.headers.get('Token')
        current_user = get_current_username(token)
        limit = 100 if int(limit) > 100 else limit
        bucketlist_result = BucketList.query.filter_by(created_by=current_user).filter(BucketList.name.ilike('%' +
                                                    q + '%')).paginate(page=page,
                                                    per_page=limit, error_out=False)
        bucketlists = bucketlist_result.items
        prev = None
        if bucketlist_result.has_prev:
            prev = url_for('api.allbucketlists', limit=limit, page=page-1, _external=True)
        next = None
        if bucketlist_result.has_next:
            next = url_for('api.allbucketlists', limit=limit, page=page+1, _external=True)
        bucket_list = [getbucketlist(each_bucketlist)
                       for each_bucketlist in bucketlists]
        return {
            'posts': bucket_list,
            'prev': prev,
            'next': next,
            'count': bucketlist_result.total,
            'response': str(limit) + ' bucket list records belonging to ' + current_user
        }, 200

    def post(self):
        name = request.form.get('name')
        token = request.headers.get('Token')
        current_user = get_current_username(token)
        bucketlist = BucketList.query.filter_by(name=name, created_by=current_user).first()
        if name:
            if bucketlist:
                return custom_errors['BucketListNameExistsError'], 406
            else:
                bucket_list = BucketList(name=name, created_by=current_user)
                if save_into_database(bucket_list):
                    return getbucketlist(bucket_list), 201
        else:
            return custom_errors['BucketListNameIsEmpty'], 406
