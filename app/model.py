from app import db
from datetime import datetime

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key = True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     email = db.Column(db.String(40),    unique=True, nullable=False)
#     def __init__(self, username, email):
#         self.username = username
#         self.email = email
#     def __repr__(self):
#         return f'={self.username}  {self.email}='

class Mechanism(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(64), nullable=False, index=True)
    type = db.Column(db.String(64), nullable=False, index=True)
    model = db.Column(db.String(64), nullable=False, index=True)
    number = db.Column(db.SmallInteger, nullable=False, index=True)
    name = db.Column(db.String(64), nullable=False, index=True, unique=True)
    posts = db.relationship('Post', backref='mech', lazy='dynamic')

    def __init__(self, id, company, type, model, number, name):
        self.id = id
        self.company = company
        self.type = type
        self.model = model
        self.number = number
        self.name = name
    def __repr__(self):
        return f'<{self.name}>'

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    mechanism_id = db.Column(db.Integer, db.ForeignKey('mechanism.id'))

    def __init__(self, value, latitude, longitude, mechanism_id):
        self.value = value
        self.latitude = latitude
        self.longitude = longitude
        self.mechanism_id = mechanism_id

    def __repr__(self):
        return f'<{self.timestamp}>'




# class Post(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String, nullable=False)
#     body=db.Column(db.Text, nullable=False)
    # pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    # category = db.relationship('Category', backref=db.backref('posts', lazy=True))

#     def __repr__(self):
#         return f'post:{self.title}'


# class Category(db.Model):
#     id = db.Column(db.Integer, primary_key = True)
#     name = db.Column(db.String(50), nullable=False)

#     def __repr__(self) :
#         return f'#Category {self.name}#'


