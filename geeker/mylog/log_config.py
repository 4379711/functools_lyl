# -*- coding: utf-8 -*-

import logging
import logging.handlers
from logging.handlers import TimedRotatingFileHandler
import gzip
import os
import time
from geeker.functions import Singleton


class GzTimedRotatingFileHandler(TimedRotatingFileHandler):
    def __init__(self, filename, when, interval, **kwargs):
        super(GzTimedRotatingFileHandler, self).__init__(filename, when, interval, **kwargs)

    @staticmethod
    def do_gzip(old_log):
        with open(old_log, 'rb') as old:
            with gzip.open(old_log.replace('.log', '', 1) + '.gz', 'wb') as comp_log:
                comp_log.writelines(old)
        os.remove(old_log)

    # overwrite
    def doRollover(self):
        if self.stream:
            self.stream.close()
            self.stream = None
        current_time = int(time.time())
        dst_now = time.localtime(current_time)[-1]
        t = self.rolloverAt - self.interval
        if self.utc:
            time_tuple = time.gmtime(t)
        else:
            time_tuple = time.localtime(t)
            dst_then = time_tuple[-1]
            if dst_now != dst_then:
                if dst_now:
                    addend = 3600
                else:
                    addend = -3600
                time_tuple = time.localtime(t + addend)
        dfn = self.baseFilename + "." + time.strftime(self.suffix, time_tuple)
        if os.path.exists(dfn):
            os.remove(dfn)
        if os.path.exists(self.baseFilename):
            os.rename(self.baseFilename, dfn)
            self.do_gzip(dfn)
        if self.backupCount > 0:
            for s in self.getFilesToDelete():
                os.remove(s)
        if not self.delay:
            self.stream = self._open()
        new_rollover_at = self.computeRollover(current_time)
        while new_rollover_at <= current_time:
            new_rollover_at = new_rollover_at + self.interval
        if (self.when == 'MIDNIGHT' or self.when.startswith('W')) and not self.utc:
            ds_att_rollover = time.localtime(new_rollover_at)[-1]
            if dst_now != ds_att_rollover:
                if not dst_now:  # DST kicks in before next rollover, so we need to deduct an hour
                    addend = -3600
                else:  # DST bows out before next rollover, so we need to add an hour
                    addend = 3600
                new_rollover_at += addend
        self.rolloverAt = new_rollover_at


class LogBase(Singleton):

    def __init__(self, dir_path='./logs/',
                 logger_name='special_log_name',
                 info_name='info.log',
                 error_name='error.log',
                 warning_name='warning.log',
                 debug_name='debug.log',
                 interval=7,
                 detail=False,
                 debug=False,
                 info=True,
                 error=True,
                 warning=True,
                 ):
        self.info_name = info_name
        self.error_name = error_name
        self.warning_name = warning_name
        self.debug_name = debug_name
        self.path = dir_path
        self.interval = interval
        self._logger = logging.getLogger(logger_name)
        self._debug = debug
        self._warning = warning
        self._error = error
        self._info = info
        self._detail = detail

    def __handler(self, log_name):
        handler = GzTimedRotatingFileHandler(self.path + log_name,
                                             when='D',
                                             interval=self.interval,
                                             backupCount=3,
                                             encoding='utf-8')
        return handler

    def __filter_message(self, handler, log_level):
        """
        过滤不同等级日志的其他信息,只保留当前日志等级的信息
        :param handler: handler
        :param log_level: 字符串
        :return: handler
        """
        if self._detail:
            formatter = logging.Formatter("%(asctime)s - %(filename)s - %(funcName)s - %(lineno)d - %(message)s",
                                          "%Y%m%d %H:%M:%S")
        else:
            formatter = logging.Formatter("%(asctime)s - %(message)s", "%Y%m%d %H:%M:%S")
        _filter = logging.Filter()

        handler.suffix = "%Y%m%d.log"
        handler.setFormatter(formatter)
        handler.setLevel(log_level)
        _filter.filter = lambda record: record.levelno == log_level
        handler.addFilter(_filter)
        return handler

    def _get_logger(self):

        # 添加此行，防止日志重复记录
        if not self._logger.handlers:
            # 设置日志等级,默认是 DEBUG
            self._logger.setLevel(logging.DEBUG)

            levels = [self._debug, self._info, self._warning, self._error]
            log_names = [self.debug_name, self.info_name, self.warning_name, self.error_name]
            levels_ = [10, 20, 30, 40]

            for i, lev in enumerate(levels):
                if lev:
                    _handler = self.__handler(log_names[i])
                    _handler = self.__filter_message(_handler, levels_[i])
                    # handler添加给日志对象
                    self._logger.addHandler(_handler)
        return self._logger
