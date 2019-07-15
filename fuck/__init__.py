# -*- coding: utf-8 -*-
# @Time    : 2019/7/6 14:21
# @Author  : Liu Yalong
# @File    : __init__.py.py
"""
说明：
    1.schedule_lyl更改自schedule，修复日期不准确BUG，并添加线程控制以解决任务延迟的问题
    使用方法：
        from functools_lyl import schedule_lyl

    2.mylog:日志记录,自动切割，压缩等
    使用方法: from functools_lyl.mylog import My_log
              logger=My_log('dirpath').getlogger()

    3.timeslimit :控制函数执行频率
    使用方法：
        from functools_lyl.timeslimit import CallTimesLimit

        每4秒执行5次abc

        @CallTimesLimit(5,4)
        def abc():
            pass

"""