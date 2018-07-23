from flask import Blueprint, session
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf import CSRFProtect

from app.data_manager import post_login, post_signup, add_user, add_client, add_production, add_request, add_role
from app.forms import SignupForm, LoginForm, handleFormAction, UserForm, ClientForm, ProductionForm, RequestForm, \
    RoleForm
from app.models import User, Request, Production, Client, Role
from app.utils import to_json_all

api = Blueprint('api', __name__)

limiter = Limiter(key_func=get_remote_address,
                  default_limits=["200/minute"])

csrf = CSRFProtect()


@api.route('/api/login/<field>', methods=['POST'])
@limiter.limit("20/minute")
def login(field):
    return handleFormAction(LoginForm, field, post_login)


@api.route('/api/signup/<field>', methods=['POST'])
@limiter.limit("20/minute")
def signup(field):
    return handleFormAction(SignupForm, field, post_signup)


@api.route("/api/logout")
def logout():
    if session.get('user') is None:
        return "You are not logged in", 400
    session.clear()
    return "Logged out successfully"


@api.route('/api/clients', methods=['GET'])
def clients():
    return to_json_all(Client.query.all())


@api.route('/api/production', methods=['GET'])
def production():
    return to_json_all(Production.query.all())


@api.route('/api/requests', methods=['GET'])
def requests():
    return to_json_all(Request.query.all())


@api.route('/api/users', methods=['GET'])
def users():
    return to_json_all(User.query.all())


@api.route('/api/roles', methods=['GET'])
def roles():
    return to_json_all(Role.query.all())


@api.route('/api/requests/<field>', methods=['POST'])
def new_requests(field):
    return handleFormAction(RequestForm, field, add_request)


@api.route('/api/clients/<field>', methods=['POST'])
def new_clients(field):
    return handleFormAction(ClientForm, field, add_client)


@api.route('/api/production/<field>', methods=['POST'])
def new_production(field):
    return handleFormAction(ProductionForm, field, add_production)


@api.route('/api/users/<field>', methods=['POST'])
def new_users(field):
    return handleFormAction(UserForm, field, add_user)


@api.route('/api/roles/<field>', methods=['POST'])
def new_roles(field):
    return handleFormAction(RoleForm, field, add_role)
