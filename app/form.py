from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Required

class AddMechanism(FlaskForm):
    id = StringField('id')
    company = StringField('company', validators=[Required()])
    type = StringField('type', validators=[Required()])
    model = StringField('type', validators=[Required()])
    number = StringField('number', validators=[Required()])
    name = StringField('name', validators=[Required()])
    btn = SubmitField('sent')
