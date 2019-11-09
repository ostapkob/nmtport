import os
# app=Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
class Configuration(object):
    basedir = os.path.abspath(os.path.dirname(__file__))
    DEBUG = True
    CSRF_ENABLET = True
    SECRET_KEY = 'super'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_DATABASE_URI='mysql+mysqlconnector://ostap:1@localhost/test1'
    # SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/nmtp-mechanisms.db'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'nmtp-mechanisms.db')
