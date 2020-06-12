# -*- coding: utf-8 -*-
import time
from threading import Lock
from geeker.functions.singleton import Singleton


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
    expect_type = type(None)

    def __init__(self, name=None, **opts):
        if not opts.get('expect_type'):
            raise ValueError('Missing argument except_type')
        else:
            self.expect_type = opts.get('expect_type')
        super().__init__(name=name)

    def __set__(self, instance, value):
        if not isinstance(value, self.expect_type):
            raise TypeError(f'Except {self.expect_type} but got {type(value)}')
        super().__set__(instance, value)


class InvalidSystemClock(Exception):
    """
    时钟回拨异常
    """
    pass


"""
snow 算法

符号位            41bit时间戳,精确到毫秒          共10bit(数据中心ID+机器ID)    12bit序列号,每毫秒生成4096个ID
  1     00000000000000000000000000000000000000000         0000000000                   000000000000


"""

# 64位ID的划分
WORKER_ID_BITS = 5
DATA_CENTER_ID_BITS = 5
SEQUENCE_BITS = 12

# 最大取值计算
MAX_WORKER_ID = -1 ^ (-1 << WORKER_ID_BITS)  # 2**5-1 0b11111
MAX_DATA_CENTER_ID = -1 ^ (-1 << DATA_CENTER_ID_BITS)

# 移位偏移计算
WORKER_ID_SHIFT = SEQUENCE_BITS
DATA_CENTER_ID_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS
TIMESTAMP_LEFT_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS + DATA_CENTER_ID_BITS

# 序号循环掩码
SEQUENCE_MASK = -1 ^ (-1 << SEQUENCE_BITS)

# 开始时间截 (2020-01-01)
START_TIME_STAMP = 1577808000000


class IdGenerator(Singleton):
    """
    分布式唯一ID生成器

    """
    _lock = Lock()

    def __init__(self, data_center_id=5, worker_id=5, sequence=0):
        """
        :param data_center_id: 数据中心ID
        :param worker_id: 机器ID
        :param sequence: 序列号
        """

        if worker_id > MAX_WORKER_ID or worker_id < 0:
            raise ValueError('参数worker_id必须在0-31之间')

        if data_center_id > MAX_DATA_CENTER_ID or data_center_id < 0:
            raise ValueError('参数data_center_id值必须在0-31之间')

        self.worker_id = worker_id
        self.data_center_id = data_center_id
        self.sequence = sequence
        # 上次计算的时间戳
        self.last_timestamp = -1

    @staticmethod
    def _gen_timestamp():
        """
        生成整数时间戳
        :return:int timestamp
        """
        return int(time.time() * 1000)

    def get_id(self):
        with self._lock:
            return self._get_id()

    def _get_id(self):
        """
        获取新ID
        """

        timestamp = self._gen_timestamp()

        # 时钟回拨
        if timestamp < self.last_timestamp:
            raise InvalidSystemClock("clock is moving backwards.")

        if timestamp == self.last_timestamp:
            self.sequence = (self.sequence + 1) & SEQUENCE_MASK
            if self.sequence == 0:
                timestamp = self._til_next_millis(self.last_timestamp)
        else:
            self.sequence = 0

        self.last_timestamp = timestamp

        new_id = ((timestamp - START_TIME_STAMP) << TIMESTAMP_LEFT_SHIFT) | \
                 (self.data_center_id << DATA_CENTER_ID_SHIFT) | (self.worker_id << WORKER_ID_SHIFT) | self.sequence
        return new_id

    def _til_next_millis(self, last_timestamp):
        """
        需要等到下一毫秒
        """
        timestamp = self._gen_timestamp()
        while timestamp <= last_timestamp:
            timestamp = self._gen_timestamp()
        return timestamp
