from config.default import DefaultConfig


class DevelopmentConfig(DefaultConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@localhost/catalog'
    SECRET_KEY = '495DE9B3D0D6BB7480F90D0B373EA4438F76798DCE81337449434D78460C046A'


config = DevelopmentConfig
