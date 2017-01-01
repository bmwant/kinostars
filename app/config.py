class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE_URI = 'sqlite://:memory:'
    SECRET_KEY = 'some-radnom-conbimation'
    ADMIN_USER = 'admin'
    ADMIN_PASS = 'nevermind'


class ProductionConfig(Config):
    HOST = '0.0.0.0'
    PORT = 5050
    DB_URI = 'mongodb://127.0.0.1:27017'


class DevelopmentConfig(Config):
    DEBUG = True
    HOST = '0.0.0.0'
    PORT = 3234
    DB_URI = 'mongodb://127.0.0.1:27017'
