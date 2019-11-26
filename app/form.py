from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, RadioField
from wtforms.validators import DataRequired, Required


class AddMechanism(FlaskForm):
    id = StringField('id')
    company = StringField('company', validators=[Required()])
    type = StringField('type', validators=[Required()])
    model = StringField('model', validators=[Required()])
    number = StringField('number', validators=[Required()])
    name = StringField('name', validators=[Required()])
    btn = SubmitField('sent')


class SelectDataShift(FlaskForm):
    # company = StringField('company', validators=[Required()])
    type = StringField('type', validators=[Required()])
    date_shift = StringField('Date', validators=[Required()])
    # date_shift = DateField('Start Date', format='%Y-%m-%d')#, validators=(validators.Optional(),))
    # shift = StringField('Shift', validators=[DataRequired()])
    shift = RadioField('shift',choices= [('1', 'День'), ('2', 'Ночь')] )

    submit = SubmitField('Submit')
