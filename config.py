import os
from sys import platform
from psw import form_pass, debug
# import pyodbc
import urllib.parse


class Configuration(object):
    basedir = os.path.abspath(os.path.dirname(__file__))
    DEBUG = debug
    CSRF_ENABLET = True
    SECRET_KEY = form_pass  # don't forget to change
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    params = urllib.parse.quote_plus("DRIVER={ODBC Driver 17 for SQL Server};"
                                     "SERVER=192.168.99.106;"
                                     "PORT=1433;"
                                     "DATABASE=nmtport;"
                                     "UID=ubuntu;"
                                     "PWD=Port2020")
    params_win = urllib.parse.quote_plus("DRIVER={SQL Server};"
                                         "SERVER=192.168.99.106;"
                                         "PORT=1433;"
                                         "DATABASE=nmtport;"
                                         "UID=ubuntu;"
                                         "PWD=Port2020")
    # cnx = mysql.connector.connect(
    #     host="192.168.99.106",
    #     port=1433,
    #     user="ubuntu",
    #     password="Port2020")
    # SQLALCHEMY_DATABASE_URI='mysql+mysqlconnector://ostap:1@localhost/test1'
    if DEBUG:
        if platform == 'win32':
            SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
                os.path.join(basedir, 'nmtp-mechanisms.db')
        else:
            SQLALCHEMY_DATABASE_URI = 'sqlite:////' + \
                os.path.join(basedir, 'nmtp-mechanisms.db')
    else:
        if platform == 'win32':
            SQLALCHEMY_DATABASE_URI = "mssql+pyodbc:///?odbc_connect=%s" % params_win
        else:
            SQLALCHEMY_DATABASE_URI = "mssql+pyodbc:///?odbc_connect=%s" % params


TIME_PERIODS = [1, 2], [4, 5], [7.5, 8], [12, 13], [
    16, 17], [19.5, 20]  # then alarm not True
