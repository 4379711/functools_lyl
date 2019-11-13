# -*- coding: utf-8 -*-
# @Time    : 2019/11/13 10:03
# @Author  : Liu Yalong
# @File    : import_module.py
from importlib import import_module


def load_object(path):
    """Load an object given its absolute object path, and return it.
    object can be a class, function, variable or an instance.
    path ie: 'geeker.commands.abc'
    """

    try:
        dot = path.rindex('.')
    except ValueError:
        raise ValueError("Error loading object '%s': not a full path" % path)

    module, name = path[:dot], path[dot + 1:]
    mod = import_module(module)

    try:
        obj = getattr(mod, name)
    except AttributeError:
        raise NameError("Module '%s' doesn't define any object named '%s'" % (module, name))

    return obj


if __name__ == '__main__':
    obj = load_object('geeker.commands.abc')
    # obj()
