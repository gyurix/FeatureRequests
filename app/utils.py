from flask import json
from sqlalchemy import inspect


def dump(obj):
    for attr in dir(obj):
        print("obj.%s = %r" % (attr, getattr(obj, attr)))


def get_fields(obj, field_blacklist={'data', 'errors', 'metadata', 'query', 'meta', 'Meta', 'csrf_token'}):
    print(str({attr for attr in dir(obj) if
               attr[0] != '_' and not field_blacklist.__contains__(attr) and
               str(type(get_attribute(obj, attr))) != "<class 'method'>"}))

    return {attr for attr in dir(obj) if
            attr[0] != '_' and not field_blacklist.__contains__(attr) and
            str(type(get_attribute(obj, attr))) != "<class 'method'>"}


def get_attribute(obj, atr):
    return getattr(obj, atr)


def to_camel_case(word, sep=' '):
    return sep.join(x.capitalize() for x in word.split('_'))


def to_json(model):
    out = {}
    for c in inspect(model).attrs.keys():
        if c != 'password':
            out[c] = getattr(model, c)
    return out


def to_json_all(models):
    return json.dumps([to_json(m) for m in models])
