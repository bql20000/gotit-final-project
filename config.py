class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@localhost/catalog'
    SECRET_KEY = 'key'      # todo: how to generate key?


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@localhost/catalog_test'
    SECRET_KEY = 'testing bla bla bla'


