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

lines_krans = [
    {'k1': 0.5938961076474917, 'b1': 107.46242811507157,
        'numbers': [45, 34, 53, 69, 21, 37, 4, 41, 5]},
    {'k1': 0.5932709085972241, 'b1': 107.49050635162425, 'numbers': [
        36, 40, 32, 25, 11, 33, 20, 8, 22, 12, 13, 6, 26]},
    {'k1': 0.5978992832844424, 'b1': 107.29311582463934,
        'numbers': [47, 54, 14, 16]}
]

names_terminals = [
    # {'name': 9, 'coords': (42.81408823514151, 132.89085937964836)},
    # {'name': 11, 'coords': (42.81059607704921, 132.888787583844)},
    # {'name': 13, 'coords': (42.80880407696847, 132.88772444232788)},
    # {'name': 15, 'coords': (42.8055582466312, 132.88579878561455)},
    # {'name': 9,  'line_longitude': (132.89275689241617, 132.89085937964836)},
    # {'name': 11, 'line_longitude': (132.89085937964836, 132.88878758384400)},
    # {'name': 13, 'line_longitude': (132.88878758384400, 132.88772444232788)},
    # {'name': 15, 'line_longitude': (132.88772444232788, 132.88579878561455)},
    (9,
        132.8908649130181
     ),
    (11,
        132.88896711975767
     ),
    (13,
        132.88878758384400
     ),
    (15,
        132.88772444232788
     ),
]

krans_if_3_then_2 = [
    47, 54, 14, 16, 33, 20, 8, 22, 12, 13, 
]

