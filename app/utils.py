def dump(obj):
    for attr in dir(obj):
        print("obj.%s = %r" % (attr, getattr(obj, attr)))


def toCamelCase(word, sep=' '):
    return sep.join(x.capitalize() or '_' for x in word.split('_'))
