from flask import session, request
from flask_recaptcha import ReCaptcha
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SelectField, IntegerField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp

from app.data_manager import getClients, getProductions, getRoles
from app.models import User, Role, Client
from app.utils import to_camel_case, get_fields, get_attribute
from app.validators import NotExistingUsername, NotExistingEmail, ExistingUsernameOrEmail, CorrectPassword, \
    ExistingModelName

recaptcha = ReCaptcha()


def handleFormAction(formClass, field, submit):
    form_type = formClass.__name__.lower()[:-4]
    if field == "submit":
        form = formClass()
        if not form.validate():
            return '\n'.join(el[0] for el in list(form.errors.values())), 400
        if getattr(form, 'has_captcha', False) and (not recaptcha.verify(request.form.get("captcha"))):
            return "Captcha verification failed", 400
        return submit(form)
    data = request.form.get("value")
    if data is None:
        return "The value parameter is not provided", 400
    if not get_fields(formClass).__contains__(field):
        return "Field \"" + field + "\" in " + form_type + " form was not found", 400
    session[form_type + "_" + field] = data
    form = formClass()
    form_field = get_attribute(form, field)
    form_field.data = data
    if form_field.validate(form):
        result = get_attribute(form_field, "usedType", field)
        return to_camel_case(result) + " is correct"
    return '\n'.join(item for item in form_field.errors), 400


class SignupForm(FlaskForm):
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

    has_captcha = True

    def __init__(self):
        super(SignupForm, self).__init__()
        self.username.data = session.get('signup_username', '')
        self.email.data = session.get('signup_email', '')
        self.password.data = session.get('signup_password', '')
        self.repeat_password.data = session.get('signup_repeat_password', '')

    def toModel(self):
        return User(self.username.data, self.email.data, self.password.data)


class LoginForm(FlaskForm):
    email = StringField('Username or Email', validators=[DataRequired("Please enter your Email address"),
                                                         ExistingUsernameOrEmail("Invalid Username or Email address")])
    password = PasswordField('Password', validators=[DataRequired("Please enter your password"),
                                                     CorrectPassword("The entered password is incorrect")])

    def __init__(self):
        super(LoginForm, self).__init__()
        self.email.data = session.get('login_email', '')
        self.password.data = session.get('login_password', '')

    def getUser(self):
        user = User.query.filter_by(name=self.email.data).first()
        if user is None:
            user = User.query.filter_by(email=self.email.data).first()
        return user


class RequestForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired("Please enter a title")])
    desc = StringField('Description', validators=[DataRequired("Please enter a description")])
    client = SelectField('Client')
    priority = IntegerField('Priority', validators=[DataRequired("Please enter the priority")])
    date = DateField('Date', validators=[DataRequired("Please enter the date")])
    area = SelectField('Production Area')

    def __init__(self):
        super(RequestForm, self).__init__()
        self.client.choices = getClients()
        self.area.choices = getProductions()


class RoleForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired("Please enter the roles name"),
                                           ExistingModelName(Role, "This role exists already")])
    enabled = BooleanField('Enabled', default=True)
    view = BooleanField('View requests permission', default=True)
    add = BooleanField('Add requests permission', default=True)
    edit = BooleanField('Edit requests')
    admin = BooleanField('Admin mode')


class UserForm(FlaskForm):
    username = StringField('Username', [DataRequired("Please enter a username"),
                                        Length(min=3,
                                               message="Username must be at least 3 characters long"),
                                        Length(max=16,
                                               message="Username must be at most 16 characters long"),
                                        Regexp('^[a-zA-Z0-9_]+$',
                                               message='Username can only contain characters a-z A-Z 0-9 '
                                                       'and _'),
                                        Regexp('^[a-zA-Z].*$',
                                               message='Username must start with characters a-z or A-Z'),
                                        NotExistingUsername('This username is already registered.')])
    email = StringField('Email', validators=[DataRequired("Please enter an email address"),
                                             Email("Please enter a valid email address"),
                                             NotExistingEmail('This email is already registered.')])
    password = StringField('Password', validators=[DataRequired("Please enter a password"),
                                                   Length(min=6,
                                                          message="Password must be at least 6 characters long"),
                                                   Length(max=32,
                                                          message="Password must be at most 32 characters long")])
    role = SelectField('Role')

    def __init__(self):
        super(UserForm, self).__init__()
        self.role.choices = getRoles()


class ClientForm(FlaskForm):
    name = StringField('Client\'s Name', validators=[DataRequired("Please enter the clients name"),
                                                     ExistingModelName(Client, "This client exists already")])

    def __init__(self):
        super(ClientForm, self).__init__()


class ProductionForm(FlaskForm):
    name = StringField('Production Area\'s Name', validators=[DataRequired("Please enter the production name"),
                                                              ExistingModelName(Client, "This client exists already")])

    def __init__(self):
        super(ProductionForm, self).__init__()
