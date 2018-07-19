from flask import render_template, Blueprint
from jinja2 import TemplateNotFound

from app.forms import SignupForm, LoginForm

pages = Blueprint('pages', __name__)


@pages.route('/')
def main_page():
    signup_form = SignupForm()
    login_form = LoginForm()
    return render_template("index.html", signup=signup_form, login=login_form)


@pages.route('/page/<page>')
def page(page):
    try:
        return render_template("page/" + page + ".html")
    except TemplateNotFound:
        return "Invalid page", 404


@pages.route('/dashboard')
def dashboard():
    # if 'user' not in session:
    #     return main_page()
    return render_template("dashboard.html")
