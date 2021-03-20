from flask import Flask
from config import Configuration
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment
from flask_bootstrap import Bootstrap
from flask_cors import CORS
from flask_login import LoginManager
from loguru import logger
import threading
import datetime
import time


app = Flask(__name__)
app.config.from_object(Configuration)
db = SQLAlchemy(app)
login = LoginManager(app)
migrate = Migrate(app, db)
moment = Moment(app)
bootstrap = Bootstrap(app)
CORS(app)
logger.add("debug.json", format="{time} {level} {message}", level="DEBUG", rotation="1 day", compression="zip", serialize=True)

from app import views, api,  model, functions
hash_last_data = functions.hash_all_last_data_state
hash_now = functions.hash_now

db.create_all()

def loop():
    while True:
        logger.info('------------------------------------------------------------------')
        hash_last_data()
        hash_now('kran')
        hash_now('usm')
        dt = str(datetime.datetime.now())
        print('>>>>>', dt)
        with open('hash.log', 'w') as f:
            f.write(dt)
        time.sleep(60)

thread = threading.Thread(target=loop, daemon=True)
thread.start()


