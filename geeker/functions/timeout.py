# -*- coding: utf-8 -*-


import ctypes
import inspect
import time
import threading
from functools import wraps


# import traceback
# import sys


class MyThread(threading.Thread):
    def __init__(self, target, args=None, kwargs=None):
        super().__init__()
        self.func = target
        self.args = args
        self.kwargs = kwargs
        self.result = '<_^&^_@**@__what fuck!__@**@_^&^_>'
        self.exitcode = False
        self.exception = None
        # self.exc_traceback = None

    def _run(self):
        self.result = self.func(*self.args, **self.kwargs)

    def run(self):  # Overwrite run() method
        try:
            self._run()
        except Exception as e:
            self.exitcode = True
            self.exception = e
            # self.exc_traceback = sys.exc_info()

    @property
    def get_result(self):
        return self.result

    @staticmethod
    def _async_raise(tid, exctype):
        """raises the exception, performs cleanup if needed"""
        # tid = ctypes.c_long(tid)
        if not inspect.isclass(exctype):
            exctype = type(exctype)
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
        # res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
        # if res == 0:
        #     raise ValueError("invalid thread id")
        # elif res != 1:
        #     ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        #     raise SystemError("PyThreadState_SetAsyncExc failed !")

    def stop_thread(self, ident=None):
        if ident:
            self._async_raise(ident, SystemExit)
        else:
            # self._async_raise(threading.get_ident(), SystemExit)
            for fuck in threading.enumerate():
                if fuck is self:
                    self._async_raise(fuck.ident, SystemExit)
                    break


class TimeOut:
    def __init__(self, limit_time=1):
        if not (isinstance(limit_time, (int, float)) and limit_time > 0):
            raise ValueError('The type of parameter <limit_time> must be int and greater than 0!')
        self.limit = int(limit_time * 10)

    def __raise_error(self, th):
        # exec_type = th.exc_traceback[0]
        # tmp_str = traceback.format_exception(th.exc_traceback[0], th.exc_traceback[1], th.exc_traceback[2])
        # str_ = ''.join(tmp_str[1:])
        #
        # th.stop_thread()
        #
        # # raise exec_type('\n'+str_)
        raise th.exception

    def __call__(self, func):
        @wraps(func)
        def warp_(*args, **kwargs):
            warp_.__name__ = func.__name__
            th = MyThread(target=func, args=args, kwargs=kwargs)
            th.daemon = True
            th.start()
            # Add 0.1 second here
            for _ in range(self.limit + 2):
                if th.exitcode:
                    self.__raise_error(th)

                is_result = th.get_result

                if is_result != '<_^&^_@**@__what fuck!__@**@_^&^_>':
                    return is_result

                if _ == self.limit:
                    # kill the thread by itself
                    th.stop_thread()
                    raise TimeoutError('Unfinished tasks within the specified time !')
                time.sleep(0.1)

        return warp_
