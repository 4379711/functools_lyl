# -*- coding: utf-8 -*-
# @Time    : 2019/7/15 14:14
# @Author  : Liu Yalong
# @File    : basetools.py


class Singleton:
    """
    单例模式
    """

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = object.__new__(cls)
        return cls._instance
