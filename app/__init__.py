from flask import Flask
from config import Configuration
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment
from flask_bootstrap import Bootstrap
from flask_cors import CORS
from flask_login import LoginManager

app=Flask(__name__)
app.config.from_object(Configuration)
db=SQLAlchemy(app)
login = LoginManager(app)
migrate = Migrate(app, db)
moment = Moment(app)
bootstrap = Bootstrap(app)
CORS(app)


from app import views, api,  model
