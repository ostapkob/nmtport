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

HOURS = 10  # your timezone

TIME_PERIODS = [1, 2], [4, 5], [7.33, 8], [12, 13], [
    16, 17], [19.33, 20]  # then alarm not True

lines_krans = [
    {'k1': 0.5938961076474917, 'b1': 107.46242811507157,
        'numbers': [45, 34, 53, 69, 21, 37, 4, 41, 5]},
    {'k1': 0.5932709085972241, 'b1': 107.49050635162425, 'numbers': [
        36, 40, 32, 25, 11, 33, 20, 8, 22, 12, 13, 6, 26]},
    {'k1': 0.5978992832844424, 'b1': 107.29311582463934,
        'numbers': [47, 54, 14, 16, 82]}
]

names_terminals = [
    (9,
     132.89300057014432, 132.8907329426648
     ),
    (11,
     132.8907329426648, 132.8891625791968
     ),
    (13,
     132.8891625791968, 132.88756362993672
     ),
    (15,
     132.88756362993672, 132.88600864829567
     ),
]

krans_if_1_then_0 = [
    47, 54, 14, 16, 82
]
krans_if_3_then_2 = [
    47, 54, 14, 16, 33, 20, 8, 22, 12, 13
]
usm_no_move = [
  9, 10,  11, 12, 13   
]
mechanisms_type =  'kran', 'usm', 'sennebogen'
