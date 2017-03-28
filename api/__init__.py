#!flask/bin/python\
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

basedir = os.path.abspath(os.path.dirname(__file__))
print(basedir)
app = Flask(__name__)

# Configure database
app.config['SECRET_KEY'] = b'\xea&#Tb\xb0\x04\x12\x06c+r$\xffjQa\x0cg0'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'bucket.db')
app.config['DEBUG'] = True
db = SQLAlchemy(app)

# Configure authentication
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.init_app(app)

import api.models
import api.resources

# create_app function is here
    # inside it you will register blueprints
