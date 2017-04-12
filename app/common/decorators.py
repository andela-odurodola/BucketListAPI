from flask_restful import abort, request

from app.models import BucketList, BucketListItem, User
from functools import wraps


def login_required(f):
    # A decorator function that checks for a valid user.

    @wraps(f)
    def decorator(*args, **kwargs):
        try:
            token = request.headers.get('Token')
            user = User.verify_auth_token(token)
        except:
            abort(401, message='Login is required')
        return f(*args, **kwargs)
    return decorator


def invalid_id(f):
    # A decorator function that checks for a valid bucketlist id

    @wraps(f)
    def decorator(*args, **kwargs):
        bucketlist_id = kwargs.get('bucketlist_id')
        bucketlist = BucketList.query.filter_by(id_no=bucketlist_id).first()
        if not bucketlist:
            abort(400, message='Bucketlist does not exist')
        return f(*args, **kwargs)
    return decorator


def invalid_item_id(f):
    # A decorator function that checks for a valid bucketlist item id
    
    @wraps(f)
    def decorator(*args, **kwargs):
        bucketlistitem_id = kwargs.get('bucketitem_id')
        bucketlist_item = BucketListItem.query.filter_by(id_no=bucketlistitem_id).first()
        if not bucketlist_item:
            abort(400, message='Bucketlist Item does not exist')
        return f(*args, **kwargs)
    return decorator
