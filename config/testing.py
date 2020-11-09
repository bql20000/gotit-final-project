from config.default import DefaultConfig


class TestingConfig(DefaultConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@localhost/catalog_test'
    SECRET_KEY = 'F8EFEC90F2B54C313DCEDC386A764F86C88CF45C8EB192D663A53B7B8F646CA8'


config = TestingConfig
