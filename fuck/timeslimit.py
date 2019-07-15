# -*- coding: utf-8 -*-
# @Time    : 2019/7/15 14:14
# @Author  : Liu Yalong
# @File    : timeslimit.py
from collections import deque
from threading import Lock
import time
import math
from .basetools import Singleton


class CallTimesLimit(Singleton):
    """
    每seconds秒执行m次
    """

    def __init__(self, m, seconds):
        if int(m) < 1 or int(seconds) < 1:
            raise ValueError('你傻逼啊！')
        self.__len = m
        self.__seconds = seconds
        self.__dq = deque(maxlen=int(m) * 3)
        self.lock = Lock()

    def __call__(self, func):

        self.__func = func
        return self.__append

    def __popleft(self):
        self.__dq.popleft()

    def __append(self, *args, **kwargs):

        with self.lock:
            if len(self.__dq) < self.__len:
                # 前m个直接添加
                # print(f'前{self.__len}个直接添加')
                self.__dq.append(time.time())
            else:
                # 有数据,判断时间再添加进去
                need_time = self.__seconds - (time.time() - self.__dq[len(self.__dq) - self.__len])
                need_time = math.ceil(need_time)
                if need_time > 0:
                    # print(f'此处等待{need_time}秒')
                    time.sleep(need_time)
                    self.__dq.append(time.time())
                else:
                    # print(f'不需要等待')
                    self.__dq.append(time.time())

        result = self.__func(*args, **kwargs)
        return result
