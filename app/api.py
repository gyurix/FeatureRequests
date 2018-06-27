from flask import Blueprint, session
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf import CSRFProtect

from app.forms import SignupForm, LoginForm, handleFormAction
from app.user_manager import postLogin, postSignup

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
