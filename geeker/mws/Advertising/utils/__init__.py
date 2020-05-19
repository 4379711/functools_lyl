# -*- coding: utf-8 -*-
import datetime
import pandas as pd

from functools import wraps
from types import MethodType


class MixParams:
    """
    Listen for all subclass methods.If subclass method parameters are passed <__kw_params>,
  Then cancel all other parameters, for example:
    the required parameters can be passed ,just use params <__kw_params> .
    """

    __kw_params = 'all_data_list'  # The word for listening

    def __getattribute__(self, item):
        func = super(MixParams, self).__getattribute__(item)
        if isinstance(func, MethodType) and not func.__name__.startswith('_'):
            @wraps(func)
            def warps_(*args, **kwargs):
                tmp = self.__kw_params
                arg_count = func.__code__.co_argcount
                values = kwargs.pop(tmp, {})
                if tmp in func.__code__.co_varnames and values:
                    # -2 : __kw_params and self
                    arg_none = [None] * (arg_count - 2)
                    kwargs.update({self.__kw_params: values})
                    return func(*arg_none, **kwargs)
                else:
                    return func(*args, **kwargs)

            return warps_
        else:
            return func


class ParameterError(Exception):

    def __init__(self, *args):
        self.args = args

    def __str__(self):
        return "{} Parameters Can't be set together !".format(self.args)

    __repr__ = __str__


class RequestDataTypeError(Exception):

    def __init__(self, arg):
        self.arg = arg

    def __str__(self):
        return "Request data parameters <{}> must be dict or list ,got {} !".format(self.arg, type(self.arg))

    __repr__ = __str__


class MyTypeError(Exception):

    def __init__(self, arg, types):
        self.arg = arg
        self.types = types

    def __str__(self):
        return "Parameters  must be {} ,got {} !".format(self.types, type(self.arg))

    __repr__ = __str__


class MyTypeAssert:

    @staticmethod
    def number_assert(*args):
        MyTypeAssert.other_assert(*args, types=(float, int))

    @staticmethod
    def bool_assert(*args):
        MyTypeAssert.other_assert(*args, types=bool)

    @staticmethod
    def str_assert(*args):
        MyTypeAssert.other_assert(*args, types=str)

    @staticmethod
    def other_assert(*args, types):
        all_types = []
        if isinstance(types, tuple):
            for i in types:
                all_types.append(i.__name__)
        else:
            all_types.append(types.__name__)

        for i in args:
            # assert isinstance(i, types)
            if not isinstance(i, types):
                raise MyTypeError(i, all_types)


def format_time(extra_data):
    """
    convert all Python date/time objects to isoformat .
    """
    for key, value in extra_data.items():
        if isinstance(value, (datetime.datetime, datetime.date)):
            extra_data[key] = value.isoformat()
    return extra_data


def remove_empty(data_):
    """
    Returns dict_ with all empty values removed.
    """

    def wrap_dict(dict_):
        assert isinstance(dict_, dict)
        new_dict = {}
        for k, v in dict_.items():
            if v is not None:
                if isinstance(v, dict):
                    new_dict[k] = {k_: v_ for k_, v_ in dict_[k].items() if v_ is not None}
                else:
                    new_dict[k] = v

        return new_dict

    if isinstance(data_, dict):
        extra_data = wrap_dict(data_)
        return extra_data
    elif isinstance(data_, list):
        result = []
        for d in data_:
            result.append(wrap_dict(d))
        return result
    else:
        raise RequestDataTypeError(data_)


def convert_json_to_csv(json_file, file_name):
    df = pd.read_json(json_file)
    to_file_path = '{}.csv'.format(file_name)
    df.to_csv(to_file_path)
