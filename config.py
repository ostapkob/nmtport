class Configuration(object):
    DEBUG = True
    CSRF_ENABLET = True
    SECRET_KEY = 'super'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_DATABASE_URI='mysql+mysqlconnector://ostap:1@localhost/test1'
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'
