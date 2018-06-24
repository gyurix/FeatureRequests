from flask_recaptcha import ReCaptcha
from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo

recaptcha = ReCaptcha()


class SignupForm(Form):
    username = StringField('Username', validators=[DataRequired("Please enter your first name.")])
    email = StringField('Email', validators=[DataRequired("Please enter your email address."),
                                             Email("Please enter a valid email address.")])
    password = PasswordField('Password', validators=[DataRequired("Please enter a password."),
                                                     Length(min=6,
                                                            message="Passwords must be at least 6 characters long."),
                                                     Length(max=32,
                                                            message="Passwords must be at most 32 characters long.")])
    repeat_password = PasswordField('Repeat Password', validators=[DataRequired("Please repeat the password."),
                                                                   EqualTo('password', "Passwords must match.")])
    submit = SubmitField('Sign up')


class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired("Please enter your email address."),
                                             Email("Please enter a valid email address.")])
    password = PasswordField('Password', validators=[DataRequired("Please enter a password.")])
    submit = SubmitField("Sign in")
