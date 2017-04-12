#!flask/bin/python3/
from flask import Flask, Blueprint
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from config import config

db = SQLAlchemy()


def create_app(config_name):
    # Initialization of the application after runtime.

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    db.init_app(app)
    api_blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
    api = Api(api_blueprint)

    # resources
    from app.resources.bucket_list import ABucketList
    from app.resources.bucket_item import BucketItem
    from app.resources.bucket_items import BucketItems
    from app.resources.bucket_lists import BucketLists
    from app.auth.register_user import Register_User
    from app.auth.login_user import Login_User

    # Routes for each resource
    api.add_resource(Register_User, '/auth/register')
    api.add_resource(Login_User, '/auth/login')
    api.add_resource(BucketLists, '/bucketlists/')
    api.add_resource(ABucketList, '/bucketlists/<bucketlist_id>')
    api.add_resource(BucketItems, '/bucketlists/<bucketlist_id>/items/')
    api.add_resource(BucketItem, '/bucketlists/<bucketlist_id>/items/<bucketitem_id>')
    app.register_blueprint(api_blueprint)

    # Blueprint for the helpers
    from app.common import common as common_blueprint
    app.register_blueprint(common_blueprint, common_folder='common')

    return app
