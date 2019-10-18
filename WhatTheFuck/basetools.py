# -*- coding: utf-8 -*-
# @Time    : 2019/7/15 14:14
# @Author  : Liu Yalong
# @File    : basetools.py
import time
from functools import wraps

__all__ = ['Singleton', 'MyType', 'MyDict', 'run_time']


class Singleton:
    """
    单例模式
    """

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = object.__new__(cls)
        return cls._instance


def run_time(func):
    # 此装饰器，用来调试函数运行时间及执行流程
    @wraps(func)  # 保留源信息
    def mywarps(*args, **kwargs):
        start_time = time.time()
        print(f'''【进入 {func.__name__}】 参数：【{args}】 【{kwargs}】''')
        aa = func(*args, **kwargs)
        cost_time = time.time() - start_time
        print(f'''【{func.__name__}】 耗时:【{cost_time}秒】''')
        print(f'''【离开 {func.__name__}】''')
        return aa

    return mywarps


class Descripter:
    def __init__(self, name=None):
        self.name = name

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value

    def __get__(self, instance, owner):
        print(instance, self.name)
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


class MyDict:

    def __getattr__(self, item):
        return None

    def __getitem__(self, item):
        return getattr(self, item)

    def __iter__(self):
        for k, v in self.__dict__.items():
            yield k, v

    def __len__(self):
        return len(self.__dict__)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __str__(self):
        return f'''< {__name__}.MyDict object at {hex(id(MyDict))}>'''

    def __repr__(self):
        return '''MyDict object ,just like :
                {'a': 5,
                 'b': [1, 2],
                 'c': {1, 2, 3}
                 }
                '''

    @staticmethod
    def _type_check_(key, expect_type):
        if not isinstance(key, expect_type):
            raise TypeError(f"The type of the value <{key}> was wrong, expected type: <{expect_type}>")

    def append_(self, key, value):
        if key not in self.__dict__:
            self.__dict__[key] = []

        else:
            self._type_check_(self.__dict__[key], list)

        self.__dict__[key].append(value)

    def add_(self, key, value):
        if key not in self.__dict__:
            self.__dict__[key] = set()

        else:
            self._type_check_(self.__dict__[key], set)

        self.__dict__[key].add(value)

    def keys(self):
        return self.__dict__.keys()
