#!flask/bin/python/

import os

from app import create_app, db
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, prompt_bool, Shell, Server

from shell import make_shell_context

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)
manager.add_command('runserver', Server())


@manager.command
def initdb():
    """
    It creates database tables
    using the SQLAlchemy models.
    """
    app = create_app('default')
    with app.app_context():
        db.create_all()
        print("Initialized the database")


@manager.command
def dropdb():
    """
    It deletes all database tables
    after confimation from the user.
    """
    if prompt_bool(
            "Are you sure you want to lose all your data"):
        app = create_app('default')
        with app.app_context():
            db.drop_all()
            print("Dropped the database")


@manager.command
def test():
    """
    It runs nosetest automatically.
    """
    from subprocess import call
    call(['nosetests',
          '--with-coverage', '--cover-package=app', '--cover-branches'])


if __name__ == '__main__':
    manager.run()
