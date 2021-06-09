# -*- coding: utf-8 -*-

from .timeout import TimeOut
from .timeslimit import Concurrency
from .singleton import Singleton, SingletonOverride
from .mydata import MyDict
from functools import wraps
import time
import threading
import os
import psutil

from colorama import init

init(autoreset=True)

__all__ = ['TimeOut', 'Concurrency', 'Singleton', 'SingletonOverride',
           'MyDict', 'run_time', 'retry',
           'show_memory_info']


def show_memory_info():
    """
   显示当前 python 程序占用的内存大小
    """
    pid = os.getpid()
    p = psutil.Process(pid)
    info = p.memory_full_info()
    memory = info.uss / 1024. / 1024
    print("所有线程:", threading.enumerate())
    print('线程总数:', threading.active_count())
    print("共占用", memory, "MB")


def retry(retry_times: int, error_type: (tuple, Exception) = Exception, sleep_time: int = 0):
    """
    捕获指定类型异常进行重试执行函数retry_times次,每次执行间隔sleep秒
    :param retry_times: 重试次数
    :param sleep_time: 重试间隔(秒)
    :param error_type: 需要捕获的错误类型
    """

    def my_wraps0(func):
        @wraps(func)
        def my_wraps1(*args, **kwargs):
            for _ in range(retry_times + 1):
                try:
                    result = func(*args, **kwargs)
                    return result
                except error_type as e:
                    if _ == retry_times:
                        raise e
                    time.sleep(sleep_time)
        return my_wraps1

    return my_wraps0


def run_time(func):
    # 此装饰器，用来调试函数运行时间及执行流程
    @wraps(func)  # 保留源信息
    def mywarps(*args, **kwargs):
        func_name = func.__name__
        start_time = time.time()
        print(f'''\033[32mSTART {func_name}{*args, kwargs}\033[0m''')
        try:
            aa = func(*args, **kwargs)
        finally:
            cost_time = time.time() - start_time
            print(f'''\033[32m{func_name}{*args, kwargs} takes <%.4f> seconds\033[0m''' % cost_time)
            print(f'''\033[32mSTOP {func_name}{*args, kwargs}\033[0m''')
        return aa

    return mywarps
