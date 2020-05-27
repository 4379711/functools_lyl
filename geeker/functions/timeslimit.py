# -*- coding: utf-8 -*-

from collections import deque
import time
import math
from queue import Queue
from threading import Lock


class BaseNeedTime:
    """
    使用deque控制执行频率
    """
    __slots__ = ()
    _func = None
    _seconds = None
    _maxlen = None
    _dq = None
    lock = Lock()

    def append_time(self, *args, **kwargs):
        # 这里需要加锁,否则并发情况下无法控制
        with self.lock:
            if len(self._dq) < self._maxlen:
                self._dq.append(time.time())
            else:
                need_time = self._seconds - (time.time() - self._dq[0])
                need_time = math.ceil(need_time)
                if need_time > 0:
                    time.sleep(need_time)
                self._dq.append(time.time())
        result = self._func(*args, **kwargs)
        return result


class BaseConcurrency:
    """
    使用queue控制并发量
    """
    __slots__ = ()
    _func = None
    _dq = None

    def control_(self, *args, **kwargs):
        self._dq.put(None)
        try:
            result = self._func(*args, **kwargs)
            return result
        finally:
            self._dq.get()


class Concurrency(BaseNeedTime, BaseConcurrency):

    def __init__(self, times: int, seconds: int = None):
        """
        seconds秒执行m次,当只传入times参数,则并发量为times
        :param times: 次数
        :param seconds: 秒数
        """

        ERR_STR = 'Parameter <%s> must be <TYPE:int> and bigger than 0 !'
        if not (isinstance(times, int) and times > 0):
            raise ValueError(ERR_STR.format(times))

        if seconds is None:
            self._dq = Queue(maxsize=times)

        else:
            if not (isinstance(seconds, int) and seconds > 0):
                raise ValueError(ERR_STR.format(seconds))
            self._dq = deque(maxlen=times)
        self._seconds = seconds
        self._maxlen = times

    def __call__(self, func):

        self._func = func

        # 这里需要把函数的参数封装进args,并传递(如果是类方法,args的第0个参数是调用者的self)
        def warp_(*args, **kwargs):
            warp_.__name__ = func.__name__
            if self._seconds is None:
                return self.control_(*args, **kwargs)
            return self.append_time(*args, **kwargs)

        return warp_
