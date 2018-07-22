from flask import session, request
from flask_recaptcha import ReCaptcha
from flask_wtf import Form
from wtforms import StringField, PasswordField, DateField, SelectField, IntegerField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp

from app.data_manager import getClients, getProductions, getRoles
from app.models import User, Role, Client
from app.utils import toCamelCase
from app.validators import NotExistingUsername, NotExistingEmail, ExistingUsernameOrEmail, CorrectPassword, \
    ExistingModelName

recaptcha = ReCaptcha()


def getAtr(obj, field, default):
    try:
        return obj.__getattribute__(field)
    except AttributeError:
        return default


def handleFormAction(formClass, field, submit):
    form_type = formClass.getType()
    if field == "submit":
        form = formClass()
        if not form.validate():
            print(list(form.errors.values()))
            return '\n'.join(el[0] for el in list(form.errors.values())), 400
        if form.hasCaptcha() and (not recaptcha.verify(request.form.get("captcha"))):
            return "Captcha verification failed", 400
        return submit(form)
    data = request.form.get("value")
    if data is None:
        return "The value parameter is not provided", 400
    if not formClass.isValidField(field):
        return "Field \"" + field + "\" in " + form_type + " form was not found", 400
    session[form_type + "_" + field] = data
    form = formClass()
    form_field = form.__getattribute__(field)
    form_field.data = data
    if form_field.validate(form):
        result = getAtr(form_field, "usedType", field)
        return toCamelCase(result) + " is correct"
    return '\n'.join(item for item in form_field.errors), 400


class SignupForm(Form):
    username = StringField('Username', validators=[DataRequired("Please enter your username"),
                                                   Length(min=3,
                                                          message="Username must be at least 3 characters long"),
                                                   Length(max=16,
                                                          message="Username must be at most 16 characters long"),
                                                   Regexp('^[a-zA-Z0-9_]+$',
                                                          message='Username can only contain characters a-z A-Z 0-9 '
                                                                  'and _'),
                                                   Regexp('^[a-zA-Z].*$',
                                                          message='Username must start with characters a-z or A-Z'),
                                                   NotExistingUsername('This username is already registered.')
                                                   ],
                           )
    email = StringField('Email', validators=[DataRequired("Please enter your email address"),
                                             Email("Please enter a valid email address"),
                                             NotExistingEmail('This email is already registered.')])
    password = PasswordField('Password', validators=[DataRequired("Please enter a password"),
                                                     Length(min=6,
                                                            message="Password must be at least 6 characters long"),
                                                     Length(max=32,
                                                            message="Password must be at most 32 characters long")])

    repeat_password = PasswordField('Repeat Password', validators=[DataRequired("Please repeat the password"),
                                                                   EqualTo('password', "Passwords must match")])

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
    email = StringField('Username or Email', validators=[DataRequired("Please enter your Email address"),
                                                         ExistingUsernameOrEmail("Invalid Username or Email address")])
    password = PasswordField('Password', validators=[DataRequired("Please enter your password"),
                                                     CorrectPassword("The entered password is incorrect")])

    def __init__(self):
        super(LoginForm, self).__init__()
        self.email.data = session.get('login_email', '')
        self.password.data = session.get('login_password', '')

    @staticmethod
    def isValidField(field):
        return field == 'email' or field == 'password'

    def getUser(self):
        user = User.query.filter_by(name=self.email.data).first()
        if user is None:
            user = User.query.filter_by(email=self.email.data).first()
        return user

    @staticmethod
    def getType():
        return 'login'

    @staticmethod
    def hasCaptcha():
        return False


class RequestForm(Form):
    title = StringField('Title', validators=[DataRequired("Please enter a title")])
    desc = StringField('Description', validators=[DataRequired("Please enter a description")])
    client = SelectField('Client', choices=getClients())
    priority = IntegerField('Priority', validators=[DataRequired("Please enter the priority")])
    date = DateField('Date', validators=[DataRequired("Please enter the date")])
    area = SelectField('Production Area', choices=getProductions())

    def __init__(self, title, desc, client, priority, date, area):
        self.title = title
        self.desc = desc
        self.client = client
        self.priority = priority
        self.date = date
        self.area = area


class RoleForm(Form):
    name = StringField('Name', validators=[DataRequired("Please enter the roles name"),
                                           ExistingModelName(Role, "This role exists already")])
    enabled = BooleanField('Enabled', default=True)
    view = BooleanField('View requests permission', default=True)
    add = BooleanField('Add requests permission', default=True)
    edit = BooleanField('Edit requests')
    admin = BooleanField('Admin mode')

    def __init__(self, name, enabled, view, add, edit, admin):
        self.name = name
        self.enabled = enabled
        self.view = view
        self.add = add
        self.edit = edit
        self.admin = admin


class UserForm(Form):
    name = StringField('Username', DataRequired("Please enter a username"),
                       Length(min=3,
                              message="Username must be at least 3 characters long"),
                       Length(max=16,
                              message="Username must be at most 16 characters long"),
                       Regexp('^[a-zA-Z0-9_]+$',
                              message='Username can only contain characters a-z A-Z 0-9 '
                                      'and _'),
                       Regexp('^[a-zA-Z].*$',
                              message='Username must start with characters a-z or A-Z'),
                       NotExistingUsername('This username is already registered.'))
    email = StringField('Email', validators=[DataRequired("Please enter an email address"),
                                             Email("Please enter a valid email address"),
                                             NotExistingEmail('This email is already registered.')])
    password = StringField('Password', validators=[DataRequired("Please enter a password"),
                                                   Length(min=6,
                                                          message="Password must be at least 6 characters long"),
                                                   Length(max=32,
                                                          message="Password must be at most 32 characters long")])
    role = SelectField('Role', choices=getRoles())

    def __init__(self, username, email, password, role):
        self.name = username
        self.email = email
        self.password = password
        self.role = role


class ClientForm(Form):
    name = StringField('Client\'s Name', validators=[DataRequired("Please enter the clients name"),
                                                     ExistingModelName(Client, "This client exists already")])

    def __init__(self, name):
        self.name = name


class ProductionForm(Form):
    name = StringField('Production Area\'s Name', validators=[DataRequired("Please enter the production name"),
                                                              ExistingModelName(Client, "This client exists already")])

    def __init__(self, name):
        self.name = name
