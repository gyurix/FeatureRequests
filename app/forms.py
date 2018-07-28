from flask import session, request
from flask_recaptcha import ReCaptcha
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SelectField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp

from app.data_manager import get_clients, get_productions, get_roles, get_priorities
from app.models import User, Role, Client, Production, Request
from app.utils import to_camel_case, get_fields, get_attribute
from app.validators import NotExistingUsername, NotExistingEmail, ExistingUsernameOrEmail, CorrectPassword, \
    ExistingModelName

recaptcha = ReCaptcha()


def handleFormAction(formClass, field, submit, id=0):
    form_type = formClass.__name__.lower()[:-4]
    form = formClass()
    print('INIT - done')
    form._id = id
    if field == 'submit':
        print('submit')
        for f in get_fields(formClass):
            atr = get_attribute(form, f)
            if isinstance(atr, str):
                continue
            elif isinstance(atr, SelectField):
                get_attribute(form, f).data = request.form.get(f, '')
        if get_attribute(form, 'post_load'):
            form.post_load()
        if not form.validate():
            return '\n'.join(el[0] for el in list(form.errors.values())), 400
        if getattr(form, 'has_captcha', False) and (not recaptcha.verify(request.form.get('captcha'))):
            return 'Captcha verification failed', 400
        return submit(form) if id == 0 else submit(form, id)
    for f in get_fields(formClass):
        if not isinstance(get_attribute(form, f), str):
            get_attribute(form, f).data = session.get(form_type + '_' + f, '')
    data = request.form.get('value')
    if data is None:
        return 'The value parameter is not provided', 400
    if not get_fields(formClass).__contains__(field):
        return 'Field "' + field + '" in ' + form_type + ' form was not found', 400
    form_field = get_attribute(form, field)
    if isinstance(form_field, str):
        return 'Field "' + field + '" in ' + form_type + ' form is not editable', 400
    session[form_type + '_' + field] = data
    print(form_type + '_' + field + ' = ' + data)
    form_field.data = data
    if get_attribute(form, 'post_load'):
        form.post_load()
    if form_field.validate(form):
        result = get_attribute(form_field, 'usedType', field)
        return to_camel_case(result) + ' is correct'
    return '\n'.join(item for item in form_field.errors), 400


class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired('Please enter your username'),
                                                   Length(min=3,
                                                          message='Username must be at least 3 characters long'),
                                                   Length(max=16,
                                                          message='Username must be at most 16 characters long'),
                                                   Regexp('^[a-zA-Z0-9_]+$',
                                                          message='Username can only contain characters a-z A-Z 0-9 '
                                                                  'and _'),
                                                   Regexp('^[a-zA-Z].*$',
                                                          message='Username must start with characters a-z or A-Z'),
                                                   NotExistingUsername('This username is already registered.')
                                                   ],
                           )
    email = StringField('Email', validators=[DataRequired('Please enter your email address'),
                                             Email('Please enter a valid email address'),
                                             NotExistingEmail('This email is already registered.')])
    password = PasswordField('Password', validators=[DataRequired('Please enter a password'),
                                                     Length(min=6,
                                                            message='Password must be at least 6 characters long'),
                                                     Length(max=32,
                                                            message='Password must be at most 32 characters long')])

    repeat_password = PasswordField('Repeat Password', validators=[DataRequired('Please repeat the password'),
                                                                   EqualTo('password', 'Passwords must match')])

    has_captcha = True


class LoginForm(FlaskForm):
    email = StringField('Username or Email', validators=[DataRequired('Please enter your Email address'),
                                                         ExistingUsernameOrEmail('Invalid Username or Email address')])
    password = PasswordField('Password', validators=[DataRequired('Please enter your password'),
                                                     CorrectPassword('The entered password is incorrect')])

    def __init__(self):
        super(LoginForm, self).__init__()

    def getUser(self):
        user = User.query.filter_by(name=self.email.data).first()
        if user is None:
            user = User.query.filter_by(email=self.email.data).first()
        return user


class RequestForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired('Please enter a title')])
    desc = StringField('Description', validators=[DataRequired('Please enter a description')])
    client = SelectField('Client')
    priority = SelectField('Priority', choices=[])
    date = DateField('Date', validators=[DataRequired('Please enter the date')])
    production = SelectField('Production Area')

    def __init__(self):
        super(RequestForm, self).__init__()
        self.client.data = ''
        self.client.choices = get_clients()
        self.production.data = ''
        self.production.choices = get_productions()
        self.priority.data = ''

    def is_original_client(self):
        req = Request.query.filter_by(id=self._id).first();
        return req.client == self.client

    def post_load(self):
        if self.client.data.isdigit():
            self.priority.choices = get_priorities(int(self.client.data),
                                                   2 if self._id == 0 or not self.is_original_client() else 1)


class RoleForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired('Please enter the roles name'),
                                           ExistingModelName(Role, 'This role exists already')])
    perm_label = 'Permissions'
    enabled = BooleanField(description='Able to login to dashboard', default=True)
    view = BooleanField(description='View requests posted by other users', default=True)
    add = BooleanField(description='Add requests', default=True)
    edit = BooleanField(description='Edit requests posted by other users')
    admin = BooleanField(description='Able to manage everything')


class UserForm(FlaskForm):
    username = StringField('Username', [DataRequired('Please enter a username'),
                                        Length(min=3,
                                               message='Username must be at least 3 characters long'),
                                        Length(max=16,
                                               message='Username must be at most 16 characters long'),
                                        Regexp('^[a-zA-Z0-9_]+$',
                                               message='Username can only contain characters a-z A-Z 0-9 '
                                                       'and _'),
                                        Regexp('^[a-zA-Z].*$',
                                               message='Username must start with characters a-z or A-Z'),
                                        NotExistingUsername('This username is already registered.')])
    email = StringField('Email', validators=[DataRequired('Please enter an email address'),
                                             Email('Please enter a valid email address'),
                                             NotExistingEmail('This email is already registered.')])
    password = StringField('Password', validators=[DataRequired('Please enter a password'),
                                                   Length(min=6,
                                                          message='Password must be at least 6 characters long'),
                                                   Length(max=32,
                                                          message='Password must be at most 32 characters long')])
    role = SelectField('Role')

    def __init__(self):
        super(UserForm, self).__init__()
        self.role.choices = get_roles()


class ClientForm(FlaskForm):
    name = StringField('Client\'s Name', validators=[DataRequired('Please enter the clients name'),
                                                     ExistingModelName(Client, 'This client exists already')])


class ProductionForm(FlaskForm):
    name = StringField('Production Area\'s Name', validators=[DataRequired('Please enter the production name'),
                                                              ExistingModelName(Production,
                                                                                'This production exists already')])
