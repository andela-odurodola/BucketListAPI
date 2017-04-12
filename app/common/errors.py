#!flask/bin/python3/
from flask_restful import abort, request

from app.models import BucketList, BucketListItem, User
from functools import wraps


# Custom errors for the Restful API is defined here.
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


custom_errors = {
    'BucketListNameExistsError': {
        'message': 'A Bucketlist with the name already exists',
        'status': 406
    },
    'BucketListNameIsEmpty': {
        'message': 'The BucketList name cannot be empty',
        'status': 406
    },
    'BucketListNotUpdated': {
        'message': 'The Bucketlist is not updated',
        'status': 400
    },
    'BucketListDeleted': {
        'message': 'BucketList has been deleted',
        'status': 204
    },
    'BucketListItemExists': {
        'message': 'Bucketlist Item exists',
        'status': 406
    },
    'BucketListItemNameIsEmpty': {
        'message': 'BucketList Item has no name',
        'status': 406
    },
    'BucketListItemNotUpdated': {
        'message': 'BucketList Item is not updated',
        'status': 400
    },
    'UserNameExists': {
        'message': 'The username already exist.Choose another',
        'status': 406
    },
    'UserDetailsEmpty': {
        'message': "User's details cannot be empty. Please specify a username and password",
        'status': 406
    },
    'IncorrectLoginDetails': {
        'message': "Please enter a valid username or password",
        'status': 400
    },
    'BucketListAlreadyCreated': {
        'message': "This bucketlist has been created by you!",
        'status': 406
    },
    'Account Creation not successfull': {
        'message': "Oops!.Something went wrong.",
        'status': 500
    }
}
