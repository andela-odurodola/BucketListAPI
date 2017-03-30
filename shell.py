#!flask/bin/python/

"""
Create an context to access the application
from an interactive shell.
"""
import os

from app.models import User, BucketList, BucketListItem
from app import db, create_app

app = create_app(os.getenv('FLASK_CONFIG') or 'default')


def make_shell_context():
    """
    Create a context for interacting in a shell for the application.
    Import the model objects to enable easy interaction.
    """
    return dict(app=app, db=db, User=User, BucketList=BucketList, BucketListItem=BucketListItem)
