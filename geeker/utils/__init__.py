# -*- coding: utf-8 -*-
# @Time    : 2019/05/22 13:56
# @Author  : Liu Yalong
# @File    : __init__.py.py


class Descripter:
    def __init__(self, name=None):
        self.name = name

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value

    def __get__(self, instance, owner):
        if not instance:
            return self
        return instance.__dict__[self.name]

    def __delete__(self, instance):
        del instance.__dict__[self.name]


class MyType(Descripter):
    except_type = type(None)

    def __init__(self, name=None, **opts):
        if not opts.get('except_type'):
            raise ValueError('Missing argument except_type')
        else:
            self.except_type = opts.get('except_type')
        super().__init__(name=name)

    def __set__(self, instance, value):
        if not isinstance(value, self.except_type):
            raise TypeError(f'Except {self.except_type} but got {type(value)}')
        super().__set__(instance, value)
