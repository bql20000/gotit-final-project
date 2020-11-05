class Config(object):           # divide
    SQLALCHEMY_TRACK_MODIFICATIONS = False  #
    HASHING_SALT = '[|1\xfa\xb7\x13\xbb^c\x9a-i7\xbb\xba`\x19\xa4\x83A\xe0U\x94]'
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@localhost/catalog'
    SECRET_KEY = '\xc8\xaaj\xbf\x0c\xe5\xbb\xb1\xcc\x10?\x83i\x1b\x93]\x07$\xd8\xaf\xfb\xed\xa9\x0c'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@localhost/catalog_test'
    SECRET_KEY = '\xc8\xaaj\xbf\x0c\xe5\xbb\xb1\xcc\x10?\x83i\x1b\x93]\x07$\xd8\xaf\xfb\xed\xa9\x0c'
