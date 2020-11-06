from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import EqualTo, DataRequired, Email

class UserForm(FlaskForm):
    name = StringField('Name')
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = StringField('Password', validators = [DataRequired()])
    confirm_pass = PasswordField('Confirm Password', validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField()

class LoginForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    submit = SubmitField()