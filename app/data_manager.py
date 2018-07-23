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


def save_model(form):
    model = form.toModel()
    print('Saving model - ' + str(model) + '...')
    db.session.add(model)
    db.session.commit()
    return model


def post_login(form):
    session.clear()
    session['user'] = form.getUser().id
    return "Logged in successfully"


def post_signup(form):
    session['user'] = save_model(form).id
    return "Signed up successfully"


def add_user(form):
    save_model(form)
    return "Created User successfully"


def add_request(form):
    save_model(form)
    return "Created Request successfully"


def add_client(form):
    save_model(form)
    return "Created Client successfully"


def add_production(form):
    save_model(form)
    return "Created Production Area successfully"


def add_role(form):
    save_model(form)
    return "Created Role successfully"
