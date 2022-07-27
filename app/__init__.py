from flask import Flask
from config import Configuration, mechanisms_type
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment
from flask_bootstrap import Bootstrap
from flask_cors import CORS
from flask_login import LoginManager
from loguru import logger
import threading
# import datetime
from datetime import datetime
import time
from flask_redis import FlaskRedis
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config.from_object(Configuration)
db = SQLAlchemy(app)
login = LoginManager(app)
migrate = Migrate(app, db)
moment = Moment(app)
bootstrap = Bootstrap(app)
redis_client = FlaskRedis(app)
mongodb_client = PyMongo(app, uri="mongodb://localhost:27017/HashShift")
mongodb = mongodb_client.db
CORS(app)

logger.add(
        "logs/debug.json", 
        format="{time} {level} {message}", 
        level="DEBUG", 
        rotation="1 day", 
        compression="zip", 
        serialize=True
        )

from app import  api,  model, functions
hash_last_data = functions.hash_all_last_data_state
hash_now = functions.hash_now

db.create_all()


def _loop():
    while True:
        hash_last_data()
        for mech_type in mechanisms_type:
            hash_now(mech_type)
        time.sleep(15)


logger.debug("RESTART: " + str(datetime.now()))
thread = threading.Thread(target=_loop, daemon=True)
thread.start()


