from flask import render_template, Blueprint, session

pages = Blueprint('pages', __name__)


@pages.route('/')
def main_page():
    if 'username' in session:
        return render_template("dashboard.html")
    return render_template("login.html")
