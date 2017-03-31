#!flask/bin/python/
"""
Configuration settings for the Bucket List API
The definition of the different configuration settings:
- Development Configuration
- Testing Configuration
- Production Configuration.
"""

import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """
    The definition of the global configuration is defined here.
    """

    SECRET_KEY = b'\xea&#Tb\xb0\x04\x12\x06c+r$\xffjQa\x0cg0'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'bucket.db')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False

    @staticmethod
    def init_app(app):
        """
        This static method initializes the application using whatever
        configuration the user has chosen.
        """
        pass


class DevelopmentConfig(Config):
    """
    The configuration settings for development mode is defined here.
    Attributes such as SQLALCHEMY_DATABASE_URI, DEBUG are different for other
    modes, so they are defined in a class called DevelopmentConfig.
    """

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'bucket.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DEBUG = True


class TestingConfig(Config):
    """
    The configuration settings for testing mode is defined here.
    Attributes such as SQLALCHEMY_DATABASE_URI, TESTING are different for other
    modes, so they are defined in a class called TestingConfig.
    """

    USE_RATE_LIMITS = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test_bucket.db')

class ProductionConfig(Config):
    """
    The configuration settings for production mode is defined here.
    Attributes such as SQLALCHEMY_DATABASE_URI, DEBUG are different for other
    modes, so they are defined in a class called ProductionConfig.
    """

    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')


# Object containing different configuration classes.
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
