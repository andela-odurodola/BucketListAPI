#!flask/bin/python3/
import json

from datetime import datetime
from flask import current_app
from flask_login import UserMixin
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer,
                          BadSignature, SignatureExpired)
from sqlalchemy.ext.declarative import DeclarativeMeta
from werkzeug.security import check_password_hash, generate_password_hash

from app import db


class SerializerMixin(object):
    RELATIONSHIPS_TO_DICT = False

    def to_dict(self, rel=None, backref=None):
        if rel is None:
            rel = self.RELATIONSHIPS_TO_DICT
        res = {column.key: str(getattr(self, attr))
               for attr, column in self.__mapper__.c.items()}
        if rel:
            for attr, relation in self.__mapper__.relationships.items():
                # Avoid recursive loop between to tables.
                if backref == relation.table:
                    continue
                value = getattr(self, attr)
                if value is None:
                    continue
                elif isinstance(value.__class__, DeclarativeMeta):
                    res[relation.key] = value.to_dict(backref=self.__table__)
                else:
                    res[relation.key] = [i.to_dict(backref=self.__table__)
                                         for i in value]
        return res


class BucketList(db.Model, SerializerMixin):
    RELATIONSHIPS_TO_DICT = True

    id_no = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), nullable=False)
    items = db.relationship('BucketListItem', backref='bucketlist', lazy='dynamic', cascade="all, delete, delete-orphan")
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_modified = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id_no'), nullable=False)

    def __repr__(self):
        return "<BucketList id '{}': '{}'>".format(self.id_no, self.name)


class User(db.Model, SerializerMixin, UserMixin):
    RELATIONSHIPS_TO_DICT = True

    id_no = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True)
    password_hash = db.Column(db.String)
    bucketlist = db.relationship('BucketList', backref='user', lazy='dynamic', cascade="all, delete, delete-orphan")

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expiration=36000):
        s = Serializer(current_app.config['SECRET_KEY'],
                       expires_in=expiration)
        return (s.dumps({'id': self.id_no}))

    @staticmethod
    def verify_auth_token(token):
        """
        Verify token.
        Verify that the token is valid and return the user id.
        """

        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        # valid token, but expired
        except (SignatureExpired, BadSignature):
            return None
        return User.query.get(data['id'])

    def __repr__(self):
        return "<User '{}'>".format(self.username)


class BucketListItem(db.Model, SerializerMixin):
    id_no = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_modified = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    done = db.Column(db.Boolean, default=False)
    bucketlist_id = db.Column(db.Integer, db.ForeignKey('bucket_list.id_no'), nullable=False)

    def __repr__(self):
        return "<BucketList id '{}': '{}'>".format(self.id_no, self.name)
