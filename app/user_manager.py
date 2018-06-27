from flask import session

from app.models import User


def postLogin(form):
    session.clear()
    u = User.query.filterBy(name=form.email.data).first()
    if u is None:
        u = User.query.filterBy(email=form.email.data).first()
    session['user'] = u.id
    return "Logged in successfully"


def postSignup(form):
    return "Signed up successfully"
