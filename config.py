import os
from sys import platform
from psw import form_pass


class Configuration(object):
    basedir = os.path.abspath(os.path.dirname(__file__))
    DEBUG = True
    CSRF_ENABLET = True
    SECRET_KEY = form_pass  # don't forget to change
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_DATABASE_URI='mysql+mysqlconnector://ostap:1@localhost/test1'
    # SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/nmtp-mechanisms.db'
    if platform == 'win32':
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
            os.path.join(basedir, 'nmtp-mechanisms.db')
    else:
        SQLALCHEMY_DATABASE_URI = 'sqlite:////' + \
            os.path.join(basedir, 'nmtp-mechanisms.db')
