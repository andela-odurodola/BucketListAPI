from flask_restful import Resource, request, url_for

from app.models import BucketList
from app.common.decorators import login_required

from app.common.custom_messages import CustomMessages
from app.common.helpers import save_into_database, get_current_user


class BucketLists(Resource):
    # It returns all bucketlists.
    method_decorators = [login_required]

    def get(self):
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 20, type=int)
        q = request.args.get('q', '')
        token = request.headers.get('Token')
        current_user = get_current_user(token)
        limit = 100 if int(limit) > 100 else limit
        bucketlist_result = BucketList.query.filter_by(created_by=current_user.id_no).filter(BucketList.name.ilike('%' +
                                                    q + '%')).paginate(page=page,
                                                    per_page=limit, error_out=False)
        bucketlists = bucketlist_result.items
        prev = None
        if bucketlist_result.has_prev:
            prev = url_for('api.allbucketlists', limit=limit, page=page-1, _external=True)
        next = None
        if bucketlist_result.has_next:
            next = url_for('api.allbucketlists', limit=limit, page=page+1, _external=True)
        return {
            'posts': [bucket_list.to_dict() for bucket_list in bucketlists],
            'prev': prev,
            'next': next,
            'count': bucketlist_result.total,
            'response': str(bucketlist_result.total) + ' bucket list records belonging to ' + current_user.username
        }, 200

    def post(self):
        name = request.form.get('name')
        token = request.headers.get('Token')
        current_user = get_current_user(token)
        bucketlist = BucketList.query.filter_by(name=name, created_by=current_user.id_no).first()
        if not name:
            return CustomMessages.bad_request('The BucketList name cannot be empty'), 400
        if bucketlist:
            return CustomMessages.conflict('A Bucketlist with the name already exists'), 409
        else:
            bucket_list = BucketList(name=name, created_by=current_user.id_no)
            if save_into_database(bucket_list):
                return bucket_list.to_dict(), 200
            else:
                return CustomMessages.server_error('Internal Error!. BucketList cannot be saved.'), 500
