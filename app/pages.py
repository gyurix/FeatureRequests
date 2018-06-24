from flask import render_template, Blueprint, session

from app.forms import SignupForm, LoginForm

pages = Blueprint('pages', __name__)


@pages.route('/')
def main_page():
    if 'username' in session:
        return render_template("dashboard.html")
    signup_form = SignupForm()
    login_form = LoginForm()
    return render_template("index.html", signup=signup_form, login=login_form)
