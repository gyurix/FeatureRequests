from flask import session

from app.models import db


def postLogin(form):
    session.clear()
    session['user'] = form.getUser
    return "Logged in successfully"


def postSignup(form):
    user = form.toUser()
    db.session.add(user)
    db.session.commit()
    return "Signed up successfully"
