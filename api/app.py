from flask import Flask
from flask_restful import Resource, Api
from resources import ABucketList, ABucketListItem, AllBucketLists, AllBucketListItems
# import app, db, login_manager
from flask_login import login_required, login_user, logout_user, current_user


app = Flask(__name__)
api = Api(app=app, prefix='/api/v1/')


api.add_resource(AllBucketLists, 'bucketlists/')
api.add_resource(ABucketList, 'bucketlists/<bucketlist_id>')
api.add_resource(AllBucketListItems, 'bucketlists/<bucketlist_id>/items/')
api.add_resource(ABucketListItem, 'bucketlists/<bucketlist_id>/items/<bucketitem_id>')


if __name__ == '__main__':
    app.run(debug=True)
