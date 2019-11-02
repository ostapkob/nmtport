from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db=SQLAlchemy(app)
app.config['CSRF_ENABLET'] = True
app.config['SECRET_KEY'] = 'super'
app.config['DEBUG']=True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
from app import views, model
