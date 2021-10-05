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
        'numbers': [47, 54, 14, 16, 82]},
    {'k1': 0.34346362704350686, 'b1': 118.20178293212636,
        'numbers': [28, 18, 1, 35, 31, 17]},
    {'k1': 1.6961658864830655, 'b1': 60.30071859473439,
        'numbers': [58, 60, 49, 38, 39, 23, 48, 72, 65, 10]
     }
]

names_terminals = [
    (9, 132.89300057014432, 132.8907329426648),
    (11, 132.8907329426648, 132.8891625791968),
    # (11, 132.8907329426648, 132.88946480059090),
    # (12, 132.8894648005909, 132.88875575004596),
    # (13, 132.88875575004596, 132.8875636299367),
    (13, 132.8891625791968, 132.8875636299367),
    (15, 132.8875636299367, 132.8860086482956),
    (71, 132.8947314242542, 132.8969701819788),
    (73, 132.8969701819788, 132.8991720623519),
    (74, 132.8991720623519, 132.9013194884534),
    (75, 132.9013194884534, 132.9032592788587),
    (76, 132.9031400600851, 132.9040180454223),
    (78, 132.9040180454223, 132.9048830195710),
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
usm_tons_in_hour = {
    1: 140,
    2: 140,
    3: 140,
    4: 140,
    5: 140,
    6: 140,
    7: 140,
    8: 140,
    9: 390,
    10: 390,
    11: 320,
    12: 278,
    13: 278
}



mechanisms_type =  'kran', 'usm', 'sennebogen'
