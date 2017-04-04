#!flask/bin/python3/

from datetime import datetime

from sqlalchemy import desc
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app import db


class BucketList(db.Model):
    id_no = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), nullable=False)
    items = db.relationship('BucketListItem', backref='bucketlist', lazy='dynamic', cascade="all, delete, delete-orphan")
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_modified = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id_no'))

    def __repr__(self):
        return "<BucketList id '{}': '{}'>".format(self.id_no, self.name)


class User(db.Model, UserMixin):
    id_no = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True)
    password = db.Column(db.String(25), nullable=False)
    bucketlist = db.relationship('BucketList', backref='user', lazy='dynamic', cascade="all, delete, delete-orphan")

    def __repr__(self):
        return "<User '{}'>".format(self.username)


class BucketListItem(db.Model):
    id_no = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_modified = db.Column(db.DateTime, default=datetime.utcnow) # onupdate=datetime.utcnow
    done = db.Column(db.Boolean, default=False)
    bucketlist_id = db.Column(db.Integer, db.ForeignKey('bucket_list.id_no'), nullable=False)

    def __repr__(self):
        return "<BucketList id '{}': '{}'>".format(self.id_no, self.name)
