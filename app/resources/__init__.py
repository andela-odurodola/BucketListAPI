#!flask/bin/python/

"""
Blueprint for the resources folder
"""
from flask import Blueprint

resource = Blueprint('resource', __name__)


from . import abucketlist
from . import abucketlistitem
from . import allbucketlistitems
from . import allbucketlists
