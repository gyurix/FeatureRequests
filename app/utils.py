from flask import json
from sqlalchemy import inspect


def dump(obj):
    for attr in dir(obj):
        print("obj.%s = %r" % (attr, getattr(obj, attr)))


def toCamelCase(word, sep=' '):
    return sep.join(x.capitalize() or '_' for x in word.split('_'))


def toJson(model):
    out = {}
    for c in inspect(model).attrs.keys():
        if c != 'password':
            out[c] = getattr(model, c)
    return out


def toJsonAll(models):
    return json.dumps([toJson(m) for m in models])
