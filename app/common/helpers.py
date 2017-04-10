from flask_restful import abort

from app.models import User, BucketList, BucketListItem
from app import db


def register_user(user):
    # After successfull registration, it welcomes the user

    return dict(
        message='Welcome {} to the Bucketlist Service.'.format(user.username)
    )

def login_user(user):
    # It displays a message which confirms a valid logged in user.

    return dict(
        message='logged in successfully as {}'.format(user.username),
        token=str(user.generate_auth_token())
    )

def user_detail(user):
    """
    After a successfull registration,
    it welcomes the user.
    """
    return {
        'message': 'Welcome ' + str(user.username) + ' to the Bucketlist Service.'
    }


def get_current_username(token):
    try:
        current_user = User.verify_auth_token(token)
        return current_user.username
    except:
        abort(401, message='Invalid Token')


def delete_bucketlist(bucketlist):
    # It deletes a single bucketlist

    try:
        db.session.delete(bucketlist)
        db.session.commit()
        return True
    except:
        db.session.rollback()
        raise


def update_database():
    # It updates the content of the database.

    try:
        db.session.commit()
        return True
    except:
        return False


def save_into_database(bucketlist):
    try:
        db.session.add(bucketlist)
        db.session.commit()
        return True
    except:
        return False
