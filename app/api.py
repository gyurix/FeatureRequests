from flask import Blueprint, session
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf import CSRFProtect

from app.data_manager import postLogin, postSignup
from app.forms import SignupForm, LoginForm, handleFormAction
from app.models import User, Request, Production, Client, Role
from app.utils import toJsonAll

api = Blueprint('api', __name__)

limiter = Limiter(key_func=get_remote_address,
                  default_limits=["200/minute"])

csrf = CSRFProtect()


@api.route('/api/login/<field>', methods=['POST'])
@limiter.limit("20/minute")
def login(field):
    return handleFormAction(LoginForm, field, postLogin)


@api.route('/api/signup/<field>', methods=['POST'])
@limiter.limit("20/minute")
def signup(field):
    return handleFormAction(SignupForm, field, postSignup)


@api.route("/api/logout")
def logout():
    if session.get('user') is None:
        return "You are not logged in", 400
    session.clear()
    return "Logged out successfully"


@api.route('/api/clients', methods=['GET'])
def clients():
    return toJsonAll(Client.query.all())


@api.route('/api/production', methods=['GET'])
def production():
    return toJsonAll(Production.query.all())


@api.route('/api/requests', methods=['GET'])
def requests():
    return toJsonAll(Request.query.all())


@api.route('/api/roles', methods=['GET'])
def roles():
    return toJsonAll(Role.query.all())


@api.route('/api/users', methods=['GET'])
def users():
    return toJsonAll(User.query.all())
