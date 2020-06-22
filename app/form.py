from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, RadioField, SelectField
from wtforms import PasswordField, BooleanField
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
    # type = StringField('', validators=[Required()], default="usm",  render_kw={ 'class': 'form-control', 'style': 'font-size:100%'})
    type = SelectField('', coerce=str, choices=[
        ('kran', 'Кран'),
        ('usm', 'УСМ'),
    ])
    date_shift = StringField('', validators=[Required()], render_kw={})
    # date_shift = DateField('Start Date', format='%Y-%m-%d')#,
    # validators=(validators.Optional(),))-control
    shift = RadioField('shift', choices=[('1', 'День'), ('2', 'Ночь')],  render_kw={
                       'class': 'form-control', 'style': 'font-size:100%'})
    submit = SubmitField('Показать', validators=[Required()])

class LoginForm(FlaskForm):
    username = StringField('Имя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомни меня')
    submit = SubmitField('Войти')
