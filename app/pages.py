from flask import render_template, Blueprint, session, redirect

from app.data_manager import getUser
from app.forms import SignupForm, LoginForm, UserForm, RequestForm, ClientForm, ProductionForm, RoleForm

pages = Blueprint('pages', __name__)


@pages.route('/')
def main_page():
    if 'user' not in session:
        return render_template("index.html", signup=SignupForm(), login=LoginForm())
    return redirect("/dashboard"), 302


@pages.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect("/"), 302
    user = getUser(session['user'])
    return render_template("dashboard.html",
                           user=user,
                           forms=dict(users=UserForm(),
                                      requests=RequestForm(),
                                      clients=ClientForm(),
                                      production=ProductionForm(),
                                      roles=RoleForm()))
