class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@localhost/catalog'
    SECRET_KEY = '\xc8\xaaj\xbf\x0c\xe5\xbb\xb1\xcc\x10?\x83i\x1b\x93]\x07$\xd8\xaf\xfb\xed\xa9\x0c'      # todo: how to generate key?


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@localhost/catalog_test'
    SECRET_KEY = '\xc8\xaaj\xbf\x0c\xe5\xbb\xb1\xcc\x10?\x83i\x1b\x93]\x07$\xd8\xaf\xfb\xed\xa9\x0c'


