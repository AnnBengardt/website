from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from blog.models import User


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log in')


class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm_password', message='enter matching passwords')])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def check_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('This email has been used already')

    def check_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('This username has been used already')


class UpdateUserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    picture = FileField('Update your profile picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def check_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('This email has been used already')

    def check_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('This username has been used already')