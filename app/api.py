from flask import Blueprint

api = Blueprint('api', __name__)


@api.route('login', methods=['POST'])
def login():
    return "Login"


@api.route("logout")
def logout():
    return "Logout"
