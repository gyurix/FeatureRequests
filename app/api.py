from flask import Blueprint, session, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf import CSRFProtect

from app.data_manager import post_login, post_signup, add_user, add_client, add_production, add_request, add_role, \
    load_user, handle_remove, load_request, handle_edit
from app.forms import SignupForm, LoginForm, handleFormAction, UserForm, ClientForm, ProductionForm, RequestForm, \
    RoleForm
from app.models import User, Request, Production, Client, Role
from app.utils import to_json_all

api = Blueprint('api', __name__)

limiter = Limiter(key_func=get_remote_address,
                  default_limits=["200/minute"])

csrf = CSRFProtect()


@api.route('/api/login/<field>', methods=['POST'])
@limiter.limit("30/minute")
def login(field):
    return handleFormAction(LoginForm, field, post_login)


@api.route('/api/signup/<field>', methods=['POST'])
@limiter.limit("30/minute")
def signup(field):
    return handleFormAction(SignupForm, field, post_signup)


def get_user():
    if 'user' not in session:
        return None
    return load_user(session['user'])


@api.route("/api/logout")
def logout():
    if 'user' not in session:
        return "You are not logged in", 400
    session.clear()
    return "Logged out successfully"


def verify_perm(perm):
    user = get_user()
    if user is None:
        return "You are not logged in", 400
    if not user.has_permission(perm):
        return "You don't have permission for this action", 400


def is_own_request(id):
    user = get_user()
    if user is None:
        return "You are not logged in", 400
    req = load_request(id)
    return req is not None and req.poster == user.id


@api.route('/api/clients', methods=['GET'])
def clients():
    return verify_perm('view') or to_json_all(Client.query.all())


@api.route('/api/production', methods=['GET'])
def production():
    return verify_perm('view') or to_json_all(Production.query.all())


@api.route('/api/requests', methods=['GET'])
def requests():
    user = get_user()
    if user is None:
        return "You are not logged in", 400
    return to_json_all(Request.query.filter(poster=user.id).all() if verify_perm('view') else Request.query.all())


@api.route('/api/users', methods=['GET'])
def users():
    user = get_user()
    if user is None:
        return "You are not logged in", 400
    return to_json_all([User.query.filter(id=user.id).first()] if verify_perm('view') else User.query.all())


@api.route('/api/roles', methods=['GET'])
def roles():
    user = get_user()
    if user is None:
        return "You are not logged in", 400
    return to_json_all([Role.query.filter(id=user.role).first()] if verify_perm('view') else Role.query.all())


@api.route('/api/requests/<field>', methods=['POST'])
def new_requests(field):
    return verify_perm('add') or handleFormAction(RequestForm, field, add_request)


@api.route('/api/clients/<field>', methods=['POST'])
def new_clients(field):
    return verify_perm('admin') or handleFormAction(ClientForm, field, add_client)


@api.route('/api/production/<field>', methods=['POST'])
def new_production(field):
    return verify_perm('admin') or handleFormAction(ProductionForm, field, add_production)


@api.route('/api/users/<field>', methods=['POST'])
def new_users(field):
    return verify_perm('admin') or handleFormAction(UserForm, field, add_user)


@api.route('/api/roles/<field>', methods=['POST'])
def new_roles(field):
    return verify_perm('admin') or handleFormAction(RoleForm, field, add_role)


@api.route('/api/requests/edit/<id>/<field>', methods=['POST'])
def edit_requests(id, field):
    return verify_perm('add' if is_own_request(id) else 'edit') or handle_edit(Request, id, field,
                                                                               request.form.get('value'))


@api.route('/api/clients/edit/<id>/<field>', methods=['POST'])
def edit_clients(id, field):
    return verify_perm('admin') or handle_edit(Client, id, field, request.form.get('value'))


@api.route('/api/production/edit/<id>/<field>', methods=['POST'])
def edit_production(id, field):
    return verify_perm('admin') or handle_edit(Production, id, field, request.form.get('value'))


@api.route('/api/users/edit/<id>/<field>', methods=['POST'])
def edit_users(id, field):
    return verify_perm('admin') or handle_edit(User, id, field, request.form.get('value'))


@api.route('/api/roles/edit/<id>/<field>', methods=['POST'])
def edit_roles(id, field):
    return verify_perm('admin') or handle_edit(Role, id, field, request.form.get('value'))


@api.route('/api/requests/remove/<id>')
def remove_requests(id):
    return verify_perm('add' if is_own_request(id) else 'edit') or handle_remove(Request, id)


@api.route('/api/clients/remove/<id>')
def remove_clients(id):
    return verify_perm('admin') or handle_remove(Client, id)


@api.route('/api/production/remove/<id>')
def remove_production(id):
    return verify_perm('admin') or handle_remove(Production, id)


@api.route('/api/users/remove/<id>')
def remove_users(id):
    return verify_perm('admin') or handle_remove(User, id)


@api.route('/api/roles/remove/<id>')
def remove_roles(id):
    return verify_perm('admin') or handle_remove(Role, id)
