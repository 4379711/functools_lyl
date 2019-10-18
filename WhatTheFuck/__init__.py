# -*- coding: utf-8 -*-
# @Time    : 2019/7/6 14:21
# @Author  : Liu Yalong
# @File    : __init__.py.py
from .mylog import MyLog
from .mytimeout import time_out
from . import schedule
from .timeslimit import CallTimesLimit
from .basetools import *
from . import mws

__all__ = ['MyLog', 'time_out', 'schedule', 'CallTimesLimit',
           'Singleton', 'run_time', 'MyType', 'mws',
           'MyDict'
           ]

"""
说明：
    1.schedule更改自schedule，修复原作者代码日期不准确BUG，并添加线程控制以解决任务延迟的问题
    使用方法：
        from WhatTheFuck import schedule
        import time

        def abc():
            print('abc')

        # 注册任务
        schedule.every(2).seconds.do(abc)
        schedule.every().day.at("10:00").do(abc)

        # 开启任务
        while True:
            schedule.run_pending()
            time.sleep(1)

    2.mylog:日志记录,自动切割，压缩等
    使用方法: from WhatTheFuck import MyLog
              logger=MyLog().getlogger()


    3.timeslimit :控制函数执行频率
    使用方法：
        from WhatTheFuck import CallTimesLimit

        每4秒执行5次abc

        @CallTimesLimit(5,4)
        def abc():
            pass

    4.run_time 此装饰器调控函数运行时间
    使用方法：
        from WhatTheFuck import runtime
            
            @run_time
            def abc():
                pass

    5.Singleton 单例模式
    使用方法：
        from WhatTheFuck import Singleton
        
        class Test(Singleton):
            pass

    6.mytimeout 超时装饰器
    使用方法：
        from WhatTheFuck import time_out

        @time_out(4)
        def test(*args):
            print("开始执行", args)
            time.sleep(args[0])
            print("----执行完成", args)
         
    7.MyType 类属性的类型检查
    使用方法：
        from WhatTheFuck import MyType
        
        class Test:
            lll = MyType('str_type1', except_type=str)
            llll = MyType('str_type2', except_type=str)
        
            def __init__(self, value, ):
                self.lll = value
                self.llll = value
                
    8.MWS相关api
    使用方法：
        from WhatTheFuck import mws
        
    9.MyDict
    a=MyDict()
    a.append_('key','value')
    a.o=5
    a.c='fasf'
    a.add_('key0','value0')
    print(dict(a))
    >>>{
        'key': ['value'],
        'o': 5, 
        'c': 'fasf', 
        'key0': {'value0'}
        }
"""
