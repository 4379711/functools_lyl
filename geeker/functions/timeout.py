# -*- coding: utf-8 -*-
# @Time    : 2019/02/22 13:39
# @Author  : Liu Yalong
# @File    : __init__.py

import ctypes
import inspect
import time
import threading
from functools import wraps


class MyThread(threading.Thread):
    def __init__(self, target, args=None, kwargs=None):
        super().__init__()
        self.func = target
        self.args = args
        self.kwargs = kwargs
        self.result = '<__what fuck!__>'

    def run(self):
        self.result = self.func(*self.args, **self.kwargs)

    @property
    def get_result(self):
        return self.result

    @staticmethod
    def _async_raise(tid, exctype):
        """raises the exception, performs cleanup if needed"""
        tid = ctypes.c_long(tid)
        if not inspect.isclass(exctype):
            exctype = type(exctype)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
        if res == 0:
            raise ValueError("invalid thread id")
        elif res != 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            raise SystemError("PyThreadState_SetAsyncExc failed !")

    @classmethod
    def stop_thread(cls, thread):
        cls._async_raise(thread.ident, SystemExit)


def time_out(limit_time):
    if not isinstance(limit_time, int):
        raise ValueError('The type of argument must be int !')

    def warps0(func):
        def warps1(*args, **kwargs):
            th = MyThread(target=func, args=args, kwargs=kwargs)
            th.setDaemon(True)
            th.start()

            # try to get result
            for _ in range(limit_time):
                time.sleep(1)
                is_result = th.get_result
                if is_result != '<__what fuck!__>':
                    return is_result

            # kill the thread by itself
            th.stop_thread(th)
            raise TimeoutError('Oh,Fuck!TimeOut Error!')

        return warps1

    return warps0


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
