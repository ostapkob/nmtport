class Configuration(object):
    DEBUG = True
    CSRF_ENABLET = True
    SECRET_KEY = 'super'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'
