import pytest
from sqlalchemy import inspect

from app.data_manager import form_to_model
from app.forms import LoginForm, SignupForm
from app.main import create_app, remove_tables, create_tables
from app.models import db, User
from app.utils import get_fields, to_camel_case, to_json, to_json_all


@pytest.fixture
def app():
    return create_app(True)


@pytest.fixture
def client(app):
    return app.test_client()


def test_empty_database(app):
    remove_tables(app)
    inspector = inspect(db.get_engine(app))
    assert len(inspector.get_table_names()) == 0


def test_creating_tables(app):
    create_tables(app)
    inspector = inspect(db.get_engine(app))
    assert sorted(inspector.get_table_names()) == ['clients', 'productions', 'requests', 'roles', 'users']


def test_server_is_running(client):
    assert client.get('/').status == '200 OK'


def test_utils_get_fields(app):
    with app.app_context():
        assert get_fields(User) == ['id', 'name', 'email', 'password', 'role']
        assert get_fields(LoginForm) == ['email', 'password']


def test_utils_to_camel_case():
    assert to_camel_case('apple') == 'Apple'
    assert to_camel_case('apple_pie') == 'Apple Pie'
    assert to_camel_case('MY_apple_pie') == 'My Apple Pie'


def test_utils_to_json():
    john = User()
    john.name = 'John'
    john.email = 'john@gmail.com'
    john.password = 'somepwd'
    assert to_json(john) == \
           {'id': 'None', 'name': 'John', 'email': 'john@gmail.com', 'role': '1'}


def test_utils_to_json_all():
    john = User()
    john.name = 'John'
    john.email = 'john@gmail.com'
    john.password = 'somepwd'
    cow = User()
    cow.name = 'Cow'
    cow.email = 'cow@gmail.com'
    cow.password = 'somepwd'
    assert to_json_all([john, cow]) == '[{"email": "john@gmail.com", "id": "None", "name": "John", "role": "1"}, ' \
                                       '{"email": "cow@gmail.com", "id": "None", "name": "Cow", "role": "1"}]'


def test_form_to_model(app):
    with app.app_context():
        form = SignupForm()
        form.username.data = "John"
        form.password.data = "john123"
        form.repeat_password.data = "john1234@gmail.com"
        form.email.data = "john@gmail.com"
        assert to_json(form_to_model(User, form)) == dict(id='None', name='John', email='john@gmail.com', role='1');


def form_field(client, form, field, value, result):
    assert client.post('/api/' + form + '/' + field, data=dict(value=value)).data == result


def form_multi_field(client, form, field, values, result):
    for v in values:
        form_field(client, form, field, v, result)


def form_submit(client, form, result, data=None):
    assert client.post('/api/' + form + '/submit', data=data).data == result


def test_signup_empty_data(client):
    form_field(client, 'signup', 'username', '', b'Please enter your username')
    form_field(client, 'signup', 'email', '', b'Please enter your email address')
    form_field(client, 'signup', 'password', '', b'Please enter a password')
    form_field(client, 'signup', 'repeat_password', '', b'Please repeat the password')
    form_submit(client, 'signup', b'Please enter your username\n'
                                  b'Please enter your email address\n'
                                  b'Please enter a password\n'
                                  b'Please repeat the password')


def test_signup_data_length(client):
    form_multi_field(client, 'signup', "username", ['d', 'ed'],
                     b'Username must be at least 3 characters long')
    form_multi_field(client, 'signup', "password", ['a', 'ab', 'abc', 'eref', 'kever'],
                     b'Password must be at least 6 characters long')
    form_multi_field(client, 'signup', "username", ['a' * 17, 'b' * 18, 'c' * 19],
                     b'Username must be at most 16 characters long')
    form_multi_field(client, 'signup', "password", ['x' * 33, 'Y' * 34, 'z' * 35],
                     b'Password must be at most 32 characters long')


def test_signup_field_format(client):
    form_multi_field(client, 'signup', "username",
                     ['A!dsfsd', 'B@cliok', 'Ca?Or', 'te-st', 'iTNOWd.d', 'A/ccide', 'my name', 'user$name'],
                     b'Username can only contain characters a-z A-Z 0-9 and _')
    form_multi_field(client, 'signup', "username",
                     ['0Cow', '1asdas', '2Sjklo', '3OPPd_dss', '4LSS_0d', '5__d86', '6ddsader1', '7fdsfds_6',
                      '8aORb8', '9_NOT_10', '_isfdf'],
                     b'Username must start with characters a-z or A-Z')
    form_multi_field(client, 'signup', "email", ['apple@a#d.com', 'hap@.a', 'app@a.a'],
                     b'Please enter a valid email address')


def test_signup_correct_values(client):
    form_multi_field(client, 'signup', "username", ['app', 'cow', "p0G", "Ga7", 'k_' * 7, 'y' * 15, 'aQ' * 8],
                     b'Username is correct')
    form_multi_field(client, 'signup', "password",
                     ['applet', '\'' * 6, '█-◘☺♥♦', 'x' * 32, '☺' * 32, '█♦' * 16, '?' * 31],
                     b'Password is correct')
    form_multi_field(client, 'signup', 'email', ['a@a.aa', '!#$%&\'*+-/=?^_`{|}~@adr.ess'],
                     b'Email is correct')


def test_signup_wrong_field(client):
    form_field(client, 'signup', '"', 'test', b'Field """ in signup form was not found')
    form_field(client, 'signup', 'pwd', 'test', b'Field "pwd" in signup form was not found')


def logout_success(client):
    logout = client.get('/api/logout')
    assert logout.status == '200 OK'
    assert logout.data == b'Logged out successfully'


def logout_error(client):
    logout = client.get('/api/logout')
    assert logout.status == '400 BAD REQUEST'
    assert logout.data == b'You are not logged in'


def test_signup_submit_logout(client):
    form_field(client, 'signup', 'submit', 'test',
               b'Please enter your username\n'
               b'Please enter your email address\n'
               b'Please enter a password\n'
               b'Please repeat the password')
    form_field(client, 'signup', 'username', 'Tom', b'Username is correct')
    form_field(client, 'signup', 'email', 'Tom@gmail.com', b'Email is correct')
    form_field(client, 'signup', 'password', 'tom123', b'Password is correct')
    form_field(client, 'signup', 'repeat_password', 'tom123', b'Repeat Password is correct')
    form_submit(client, 'signup', b'Signed up successfully\n'
                                  b'You are the first registered member, so you got admin rights',
                data=dict(username='Tom', email='Tom@gmail.com', password='tom123', repeat_password='tom123'))
    logout_success(client)
    logout_error(client)


def test_logout_not_logged_in(client):
    logout_error(client)


def test_login_empty_data(client):
    form_field(client, 'login', 'email', '', b'Please enter your Email address')
    form_field(client, 'login', 'password', '', b'Please enter your password')
    form_submit(client, 'login', b'Please enter your Email address\n'
                                 b'Please enter your password')


def test_login_fields(client):
    form_field(client, 'login', 'password', 'tom123', b'The entered password is incorrect')
    form_multi_field(client, 'login', 'email', ['tom', 'iTom', 'Tomi', 'tom@gmail.com', '*', '?', '\'', '"'],
                     b'Invalid Username or Email address')
    form_field(client, 'login', 'email', 'Tom', b'Username is correct')
    form_multi_field(client, 'login', 'password', ['tom', '*', '?', '\'', '"'], b'The entered password is incorrect')
    form_field(client, 'login', 'password', 'tom123', b'Password is correct')
    form_field(client, 'login', 'email', 'Tom@gmail.com', b'Email is correct')
    form_multi_field(client, 'login', 'password', ['tom', '*', '?', '\'', '"'], b'The entered password is incorrect')
    form_field(client, 'login', 'password', 'tom123', b'Password is correct')


def test_login_username_logout(client):
    form_submit(client, 'login', b'Logged in successfully', dict(email='Tom', password='tom123'))
    logout_success(client)
    logout_error(client)


def test_login_email_logout(client):
    form_submit(client, 'login', b'Logged in successfully', dict(email='Tom@gmail.com', password='tom123'))
    logout_success(client)
    logout_error(client)


def login(client, email, password):
    client.post('/api/login/submit', data=dict(email=email, password=password))


def test_dashboard_add_production(client):
    login(client, 'Tom@gmail.com', 'tom123')
    id = 1
    for name in ['Policies', 'Billing', 'Claims', 'Reports']:
        form_submit(client, 'productions',
                    b'{"id": "' + str.encode(str(id)) + b'", "name": "' + str.encode(name) + b'"}',
                    dict(name=name))
        id += 1


def test_dashboard_add_client(client):
    login(client, 'Tom@gmail.com', 'tom123')
    id = 1
    for name in ['Client A', 'Client B', 'Client C']:
        form_submit(client, 'clients', b'{"id": "' + str.encode(str(id)) + b'", "name": "' + str.encode(name) + b'"}',
                    dict(name=name))
        id += 1
