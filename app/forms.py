from flask import session, request
from flask_recaptcha import ReCaptcha
from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp

from app.models import User
from app.utils import toCamelCase
from app.validators import NotExistingUsername, NotExistingEmail, ExistingUsernameOrEmail, CorrectPassword

recaptcha = ReCaptcha()


def handleFormAction(formClass, field, submit):
    type = formClass.getType()
    if field == "submit":
        form = formClass()
        if not form.validate():
            return "Invalid form", 400
        if form.hasCaptcha() and (not recaptcha.verify(request.form.get("captcha"))):
            return "Captcha verification failed", 400
        return submit(form)
    data = request.form.get("value")
    if data is None:
        return "The value parameter is not provided.", 400
    if not formClass.isValidField(field):
        return "Field \"" + field + "\" in " + type + " form was not found.", 400
    session[type + "_" + field] = data
    form = formClass()
    formField = form.__getattribute__(field)
    formField.data = data
    if formField.validate(form):
        return toCamelCase(field) + " is correct."
    return '\n'.join(item for item in formField.errors), 400


class SignupForm(Form):
    username = StringField('Username', validators=[DataRequired("Please enter your first name"),
                                                   Length(min=3,
                                                          message="Username must be at least 3 characters long"),
                                                   Length(max=16,
                                                          message="Username must be at most 16 characters long"),
                                                   Regexp('[a-zA-Z0-9_]+',
                                                          message='Username can only contain characters a-z A-Z 0-9 '
                                                                  'and _'),
                                                   Regexp('[a-zA-Z].*',
                                                          message='Username must start with characters a-z or A-Z'),
                                                   NotExistingUsername('This username is already registered.')
                                                   ],
                           )
    email = StringField('Email', validators=[DataRequired("Please enter your email address."),
                                             Email("Please enter a valid email address."),
                                             NotExistingEmail('This email is already registered.')])
    password = PasswordField('Password', validators=[DataRequired("Please enter a password."),
                                                     Length(min=6,
                                                            message="Passwords must be at least 6 characters long."),
                                                     Length(max=32,
                                                            message="Passwords must be at most 32 characters long.")])

    repeat_password = PasswordField('Repeat Password', validators=[DataRequired("Please repeat the password."),
                                                                   EqualTo('password', "Passwords must match.")])

    def __init__(self):
        super(SignupForm, self).__init__()
        self.username.data = session.get('signup_username', '')
        self.email.data = session.get('signup_email', '')
        self.password.data = session.get('signup_password', '')
        self.repeat_password.data = session.get('signup_repeat_password', '')

    def toUser(self):
        return User(self.username.data, self.email.data, self.password.data)

    @staticmethod
    def isValidField(field):
        return field == 'username' or field == 'email' or field == 'password' or field == 'repeat_password'

    @staticmethod
    def getType():
        return 'signup'

    @staticmethod
    def hasCaptcha():
        return True


class LoginForm(Form):
    email = StringField('Username or Email', validators=[DataRequired("Please enter your Email address."),
                                                         ExistingUsernameOrEmail("Invalid Username or Email address.")])
    password = PasswordField('Password', validators=[DataRequired("Please enter your password."),
                                                     CorrectPassword("The entered password is incorrect.")])

    def __init__(self):
        super(LoginForm, self).__init__()
        self.email.data = session.get('login_email', '')
        self.password.data = session.get('login_password', '')

    @staticmethod
    def isValidField(field):
        return field == 'email' or field == 'password'

    def getUser(self):
        user = User.query.filterBy(name=self.email.data).first()
        if user is None:
            user = User.query.filterBy(email=self.email.data).first()
        return user

    @staticmethod
    def getType():
        return 'login'

    @staticmethod
    def hasCaptcha():
        return False
