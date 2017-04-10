from flask_restful import abort

from app.models import User, BucketList, BucketListItem
from app import db


def register_user(user):
    """
    After a successfull registration,
    it welcomes the user.
    """
    return {
        'message': 'Welcome ' + str(user.username) + ' to the Bucketlist Service.'
    }

def login_user(user):
    # It displays a message which confirms a valid logged in user.
    return {
        'message': 'logged in successfully as {}'.format(user.username),
        'token': str(user.generate_auth_token())
    }

def get_current_username(token):
    try:
        current_user = User.verify_auth_token(token)
        return current_user.username
    except:
        abort(401, message='Invalid Token')


def abucketlistitem(bucketitem):
    """
    It returns the output for a single bucketlist item
    in a json format.
    """
    return {
        'id': bucketitem.id_no,
        'name': bucketitem.name,
        'date_created': str(bucketitem.date_created),
        'date_modified': str(bucketitem.date_modified),
        'done': bucketitem.done
    }


def getallbucketlistitem(bucketlist_id):
    """
    It returns all bucketlist items for a
    particular bucketlist id.
    """
    list_items = BucketListItem.query.filter_by(bucketlist_id=bucketlist_id).all()
    return [abucketlistitem(bucketitem)
            for bucketitem in list_items]


def getbucketlist(bucketlist):
    """
    It returns a single bucketlist based on the
    bucket id specified.
    """
    return {
        'id': bucketlist.id_no,
        'name': bucketlist.name,
        'items': getallbucketlistitem(bucketlist.id_no),
        'date_created': str(bucketlist.date_created),
        'date_modified': str(bucketlist.date_modified),
        'created_by': bucketlist.created_by
    }


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
        abort(400)
