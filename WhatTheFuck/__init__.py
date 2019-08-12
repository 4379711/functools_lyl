# -*- coding: utf-8 -*-
# @Time    : 2019/7/6 14:21
# @Author  : Liu Yalong
# @File    : __init__.py.py
from .mylog import My_log as MyLog
from .mytimeout import time_out
from . import schedule_lyl as schedule
from .timeslimit import CallTimesLimit
from .basetools import run_time, Singleton, MyType
from .md import Prpcrypt as PyCrypt

__all__ = ['MyLog', 'time_out', 'schedule', 'CallTimesLimit', 'Singleton', 'run_time', 'PyCrypt', 'MyType']

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
    
    7.PyCrypt 加密解密
    使用方法：
        from WhatTheFuck import PyCrypt      
        
        pp=PyCrypt('16位密钥字符串..........')
        aa=pp.encrypt('待加密的内容') 
        bb =pp.decrypt('加密过的字节内容') 
        
    8.MyType 类属性的类型检查
    使用方法：
        
        class Test:
            lll = MyType('str_type1', except_type=str)
            llll = MyType('str_type2', except_type=str)
        
            def __init__(self, value, ):
                self.lll = value
                self.llll = value
"""
