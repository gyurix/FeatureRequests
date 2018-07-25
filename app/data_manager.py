from flask import session, json
from wtforms import BooleanField, IntegerField

from app.models import db, User, Request, Production, Role, Client
from app.utils import get_attribute, get_fields, to_json


def form_to_model(model_type, form):
    model = model_type()
    for f in get_fields(form):
        form_atr = get_attribute(form, f)
        if isinstance(form_atr, str):
            continue
        data = form_atr.data
        if isinstance(form_atr, BooleanField):
            data = data.lower() == 'true'
        elif isinstance(form_atr, IntegerField):
            data = int(data)
        setter = get_attribute(model, 'set_' + f)
        if setter is not None:
            setter(data)
            continue
        model_atr = get_attribute(model_type, f)
        if model_atr is not None:
            setattr(model, f, data)
    return model


def load_user(id):
    return User.query.filter_by(id=id).first()


def load_request(id):
    return Request.query.filter_by(id=id).first()


def load_client(id):
    return Client.query.filter_by(id=id).first()


def load_production(id):
    return Production.query.filter_by(id=id).first()


def load_role(id):
    return Role.query.filter_by(id=id).first()


def flip_pairs(list):
    return [(entry[1], entry[0]) for entry in list]


def get_clients():
    return flip_pairs(sorted([(c.name, c.id) for c in Client.query.all()]))


def get_productions():
    return flip_pairs(sorted([(p.name, p.id) for p in Production.query.all()]))


def get_priorities(client):
    return [i for i in range(1, len({Request.query.filter_by(client=client).count()}) + 2)]


def get_roles():
    return flip_pairs(sorted([(r.name, r.id) for r in Role.query.all()]))


def save_model(modelType, form):
    model = form_to_model(modelType, form)
    db.session.add(model)
    db.session.commit()
    return model


def post_login(form):
    session.clear()
    user = form.getUser()
    if not user.has_permission('enabled'):
        return 'Your account is waiting for admin approval', 400
    session['user'] = user.id
    return "Logged in successfully"


def post_signup(form):
    user = save_model(User, form)
    if user.id == 1:
        session['user'] = user.id
        return 'Signed up successfully\n' \
               'You are the first registered member, so you got admin rights'
    if not user.has_permission('enabled'):
        return 'Signed up successfully\nYour account is waiting for admin approval now'
    session['user'] = user.id
    return "Signed up successfully"


def add_user(form):
    return json.dumps(to_json(save_model(User, form)))


def add_request(form):
    return json.dumps(to_json(save_model(Request, form)))


def add_client(form):
    return json.dumps(to_json(save_model(Client, form)))


def add_production(form):
    return json.dumps(to_json(save_model(Production, form)))


def add_role(form):
    return json.dumps(to_json(save_model(Role, form)))
