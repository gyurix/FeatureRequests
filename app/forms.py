from flask import session, request
from flask_recaptcha import ReCaptcha
from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp

from app.validators import NotExistingUsername, NotExistingEmail, ExistingUsernameOrEmail, CorrectPassword

recaptcha = ReCaptcha()


def handleFormAction(form, field, submit):
    data = request.form["value"]
    type = form.getType()
    if field == "submit":
        if not form.validate():
            return "Invalid form", 400
        if form.hasCaptcha() and (not recaptcha.verify()):
            return "Captcha verification failed", 400
        return submit(form)
    if not form.isValidField(field):
        return "Field \"" + field + "\" in " + type + " form was not found.", 404
    session[type + "_" + field] = data
    formField = form.__getattribute__(field)
    formField.data = data
    if formField.validate(form):
        return field[0].upper() + field[1:] + " is correct."
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
        self.username.value = session.get('signup_username')
        self.email.value = session.get('signup_email')
        self.password.value = session.get('signup_password')
        print("Password = " + session.get('signup_password'))
        print("Password repeat = " + session.get('signup_repeat_password'))
        self.repeat_password.value = session.get('signup_repeat_password')

    def isValidField(self, field):
        return field == 'username' or field == 'email' or field == 'password' or field == 'repeat_password'

    def getType(self):
        return 'signup'

    def hasCaptch(self):
        return True


class LoginForm(Form):
    email = StringField('Username or Email', validators=[DataRequired("Please enter your Email address."),
                                                         ExistingUsernameOrEmail("Invalid Username or Email address.")])
    password = PasswordField('Password', validators=[DataRequired("Please enter your password."),
                                                     CorrectPassword("The entered password is incorrect.")])

    def __init__(self):
        super(LoginForm, self).__init__()
        self.email.value = session.get('login_email')
        self.password.value = session.get('login_password')

    def isValidField(self, field):
        return field == 'name' or field == 'password'

    def getType(self):
        return 'login'

    def hasCaptcha(self):
        return False
