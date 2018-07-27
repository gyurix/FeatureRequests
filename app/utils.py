from flask import json
from sqlalchemy import inspect


def dump(obj):
    for attr in dir(obj):
        print("obj.%s = %r" % (attr, obj.__getattr__(attr)))


def get_fields(obj, field_blacklist={'has_captcha'}):
    return [k for k in (obj if isinstance(obj, type) else obj.__class__).__dict__ if
            k[0] != '_'
            and str(type(getattr(obj, k))) != "<class 'method'>"
            and str(type(getattr(obj, k))) != "<class 'function'>"
            and not field_blacklist.__contains__(k)]


def get_attribute(obj, attr, default=None):
    return getattr(obj, attr, default)


def none_to_empty(obj):
    return '' if obj is None else obj


def to_camel_case(word, sep=' '):
    return sep.join(x.capitalize() for x in word.split('_'))


def entries_to_dict_json(entries):
    out = {}
    for e in entries:
        out[e[0]] = e[1]
    return json.dumps(out)


def to_json(model):
    out = {}
    for c in inspect(model).attrs.keys():
        if c == 'password':
            continue
        atr = getattr(model, c)
        out[c] = str(atr)
    return out


def to_json_all(models):
    return json.dumps([to_json(m) for m in models])
