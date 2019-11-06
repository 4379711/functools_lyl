# -*- coding: utf-8 -*-
# @Time    : 2019/02/22 13:44
# @Author  : Liu Yalong
# @File    : __init__.py
from .timeout import time_out
from .timeslimit import Concurrency
from .singleton import Singleton
from .mydata import MyDict
from functools import wraps
import time

from colorama import init

init(autoreset=True)

__all__ = ['time_out', 'Concurrency', 'Singleton', 'MyDict', 'run_time', 'retry']


def retry(n: int, error_type: Exception = Exception):
    """
    捕获error_type异常进行重试执行函数n次
    :param n: int，重试次数
    :param error_type: Exception,需要捕获的错误类型
    :return:
    """

    def times(func):
        @wraps(func)
        def mywraps(*args, **kwargs):
            for _ in range(n):
                try:
                    # 执行函数
                    result = func(*args, **kwargs)
                    return result
                except error_type:
                    pass

            raise RuntimeError(f'执行<{func.__name__}{*args, kwargs}>\t重试{n}次后仍然失败！')

        return mywraps

    return times


def run_time(func):
    # 此装饰器，用来调试函数运行时间及执行流程
    @wraps(func)  # 保留源信息
    def mywarps(*args, **kwargs):
        start_time = time.time()
        print(f'''\033[32mSTART {func.__name__}{*args, kwargs}\033[0m''')
        try:
            aa = func(*args, **kwargs)
        finally:
            cost_time = time.time() - start_time
            print(f'''\033[32m{func.__name__}{*args, kwargs} takes <%.4f> seconds\033[0m''' % cost_time)
            print(f'''\033[32mSTOP {func.__name__}{*args, kwargs}\033[0m''')
        return aa

    return mywarps
