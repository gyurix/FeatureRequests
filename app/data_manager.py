from flask import session

from app.models import db, User, Request, Production, Role, Client


def getUser(id):
    return User.query.filter_by(id=id).first()


def getRequest(id):
    return Request.query.filter_by(id=id).first()


def getClient(id):
    return Client.query.filter_by(id=id).first()


def getProduction(id):
    return Production.query.filter_by(id=id).first()


def getRole(id):
    return Role.query.filter_by(id=id).first()


def getClients():
    return [(c.id, c.name) for c in Client.query.all()]


def getProductions():
    return [(p.id, p.name) for p in Production.query.all()]


def getRoles():
    return [(r.id, r.name) for r in Role.query.all()]


def postLogin(form):
    session.clear()
    session['user'] = form.getUser().id
    return "Logged in successfully"


def postSignup(form):
    user = form.toUser()
    db.session.add(user)
    db.session.commit()
    session['user'] = user.id
    return "Signed up successfully"
