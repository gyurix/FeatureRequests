import pytest
from sqlalchemy import inspect

from app.main import createApp, removeTables, createTables
from app.models import db


@pytest.fixture
def app():
    app = createApp(True)
    return app


@pytest.fixture
def client(app):
    return app.test_client()


def test_empty_database(app):
    removeTables(app)
    inspector = inspect(db.get_engine(app))
    assert len(inspector.get_table_names()) == 0


def test_creating_tables(app):
    createTables(app)
    inspector = inspect(db.get_engine(app))
    assert sorted(inspector.get_table_names()) == ['clients', 'productions', 'requests', 'roles', 'users']


def test_server_is_running(client):
    assert client.get('/').status == '200 OK'


def login_field(client, field, value):
    return client.post('/api/login/' + field, data=dict(value=value)).data


def login_submit(client, data):
    return client.post('/api/login/submit', data=data).data


def signup_field(client, field, value, result):
    assert client.post('/api/signup/' + field, data=dict(value=value)).data == result


def signup_field_values(client, field, values, result):
    for v in values:
        signup_field(client, field, v, result)


def signup_submit(client, data):
    return client.post('/api/signup/submit', data=data).data


def test_signup_empty_data(client):
    signup_field(client, "username", "", b'Please enter your username')
    signup_field(client, "email", "", b'Please enter your email address')
    signup_field(client, "password", "", b'Please enter a password')
    signup_field(client, "repeat_password", "", b'Please repeat the password')


def test_signup_data_length(client):
    signup_field_values(client, "username", ['d', 'ed'],
                        b'Username must be at least 3 characters long')
    signup_field_values(client, "password", ['a', 'ab', 'abc', 'eref', 'kever'],
                        b'Password must be at least 6 characters long')
    signup_field_values(client, "username", ['a' * 17, 'b' * 18, 'c' * 19],
                        b'Username must be at most 16 characters long')
    signup_field_values(client, "password", ['x' * 33, 'Y' * 34, 'z' * 35],
                        b'Password must be at most 32 characters long')


def test_signup_field_format(client):
    signup_field_values(client, "username",
                        ['A!dsfsd', 'B@cliok', 'Ca?Or', 'te-st', 'iTNOWd.d', 'A/ccide', 'my name', 'user$name'],
                        b'Username can only contain characters a-z A-Z 0-9 and _')
    signup_field_values(client, "username",
                        ['0Cow', '1asdas', '2Sjklo', '3OPPd_dss', '4LSS_0d', '5__d86', '6ddsader1', '7fdsfds_6',
                         '8aORb8', '9_NOT_10', '_isfdf'],
                        b'Username must start with characters a-z or A-Z')
    signup_field_values(client, "email", ['apple@a#d.com', 'hap@.a', 'app@a.a'],
                        b'Please enter a valid email address')


def test_signup_correct_values(client):
    signup_field_values(client, "username", ['app', 'cow', "p0G", "Ga7", 'k_' * 7, 'y' * 15, 'aQ' * 8],
                        b'Username is correct')
    signup_field_values(client, "password", ['applet', '\'' * 6, '█-◘☺♥♦', 'x' * 32, '☺' * 32, '█♦' * 16, '?' * 31],
                        b'Password is correct')
    signup_field_values(client, 'email', ['a@a.aa', '!#$%&\'*+-/=?^_`{|}~@adr.ess'],
                        b'Email is correct')
