from flask import Blueprint

from app.forms import SignupForm, recaptcha, LoginForm
from app.models import db

api = Blueprint('api', __name__)


@api.route('/api/login', methods=['POST'])
def login():
    form = LoginForm()
    db.use
    return form.email.data.title() + ":" + form.password.data.title()
    # redirect("/")


@api.route('/api/signup', methods=['POST'])
def signup():
    if not recaptcha.verify():
        return "Captcha verification failed"
    form = SignupForm()
    if not form.validate():
        return "Invalid form"
    return "Success"


@api.route("/api/logout")
def logout():
    return "Logout"
