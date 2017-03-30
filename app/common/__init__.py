#!flask/bin/python/

"""
Blueprint for the common folder
"""
from flask import Blueprint

common = Blueprint('common', __name__)


from . import helpers
