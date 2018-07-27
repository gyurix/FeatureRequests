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


def handle_remove(model_type, id):
    model = model_type.query.filter_by(id=id).first()
    if model is None:
        return model_type.__name__ + ' #' + id + ' was not found.', 400
    db.session.delete(model)
    db.session.commit()
    return 'Removed ' + model_type.__name__ + ' #' + id


def handle_edit(model_type, id, field, value):
    if value is None:
        return 'The value parameter is not provided', 400
    model = model_type.query.filter_by(id=id).first()
    if model is None:
        return model_type.__name__ + ' #' + id + ' was not found.', 400
    if field not in get_fields(model_type):
        return 'Field ' + field + ' in ' + model_type.__name__ + ' model was not found.'
    setattr(model, field, value)
    db.session.commit()
    return 'Changed field "' + field + '" of ' + model_type.__name__ + ' #' + id + ' to "' + value + '"'


def load_user(id):
    return User.query.filter_by(id=int(id)).first()


def load_request(id):
    return Request.query.filter_by(id=int(id)).first()


def load_client(id):
    return Client.query.filter_by(id=int(id)).first()


def load_production(id):
    return Production.query.filter_by(id=int(id)).first()


def load_role(id):
    return Role.query.filter_by(id=int(id)).first()


def flip_pairs(list):
    return [(entry[1], entry[0]) for entry in list]


def get_clients():
    return flip_pairs(sorted([(c.name, str(c.id)) for c in Client.query.all()]))


def get_productions():
    return flip_pairs(sorted([(p.name, str(p.id)) for p in Production.query.all()]))


def get_priorities(client):
    count = Request.query.filter_by(client=client).count()
    return [(str(i), str(i)) for i in range(1, count + 1)]


def get_roles():
    return flip_pairs(sorted([(r.name, str(r.id)) for r in Role.query.all()]))


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
    req = save_model(Request, form)
    fix_other_requests_priority(req)
    return json.dumps(to_json(req))


def fix_other_requests_priority(request):
    for r in Request.query.filter_by(client=request.client) \
            .filter(Request.priority >= request.priority, Request.id != request.id).all():
        r.priority += 1
    db.session.commit()


def add_client(form):
    return json.dumps(to_json(save_model(Client, form)))


def add_production(form):
    return json.dumps(to_json(save_model(Production, form)))


def add_role(form):
    return json.dumps(to_json(save_model(Role, form)))
