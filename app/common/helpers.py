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

def get_current_user(token):
    try:
        current_user = User.verify_auth_token(token)
        return current_user
    except:
        abort(401, message='Invalid Token')


def delete_bucketlist(bucketlist):
    # It deletes a single bucketlist

    try:
        db.session.delete(bucketlist)
        db.session.commit()
        return {
            'delete_successful': True
        }
    except Exception as e:
        db.session.rollback()
        return {
            'delete_successful': False,
            'error_message': 'Could not delete Item. Please try again later'
        }


def update_database():
    # It updates the content of the database.

    try:
        db.session.commit()
        return {
            'update_successful': True
        }
    except Exception as e:
        return {
            'update_successful': False,
            'error_message': 'Could not update Item. Please try again later'
        }


def save_into_database(bucketlist):
    try:
        db.session.add(bucketlist)
        db.session.commit()
        return {
            'save_successful': True
        }
    except Exception as e:
        print(e)
        return {
            'save_successful': False,
            'error_message': 'Could not create Item. Please try again later'
        }
