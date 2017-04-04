#!flask/bin/python3/

from flask import Flask, Blueprint
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

from config import config


db = SQLAlchemy()


def create_app(config_name):
    """
    Initialization of the application after runtime.
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)
    api_blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
    api = Api(api_blueprint)

    # Blueprint for the routes
    from app.resources.abucketlist import ABucketList
    from app.resources.abucketlistitem import ABucketListItem
    from app.resources.allbucketlistitems import AllBucketListItems
    from app.resources.allbucketlists import AllBucketLists

    api.add_resource(AllBucketLists, '/bucketlists/')
    api.add_resource(ABucketList, '/bucketlists/<bucketlist_id>')
    api.add_resource(AllBucketListItems, '/bucketlists/<bucketlist_id>/items/')
    api.add_resource(ABucketListItem, '/bucketlists/<bucketlist_id>/items/<bucketitem_id>')
    app.register_blueprint(api_blueprint)

    # Blueprint for the helpers
    from app.common import common as common_blueprint
    app.register_blueprint(common_blueprint, common_folder='common')

    return app
