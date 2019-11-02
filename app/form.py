from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class AddMechanism(FlaskForm):
    id = StringField('id')
    company = StringField('company')
    type = StringField('type')
    model = StringField('type')
    number = StringField('number')
    name = StringField('name')
    btn = SubmitField('sent')
