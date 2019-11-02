# -*- coding: utf-8 -*-
# @Time    : 2019/7/6 14:21
# @Author  : Liu Yalong
# @File    : __init__.py.py
from __future__ import absolute_import

from .mylog import MyLog
from . import schedule
from . import mws
from .functions import *
from .utils import *

__all__ = ['MyType', 'MyLog', 'time_out',
           'schedule', 'mws', 'Concurrency',
           'Singleton', 'MyDict', 'run_time'
           ]

"""
说明：
    1.schedule更改自schedule，修复原作者代码日期不准确BUG，并添加线程控制以解决任务延迟的问题
    使用方法：
        from geeker import schedule
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
    使用方法: from geeker import MyLog
              logger=MyLog().getlogger()


    3.timeslimit :控制函数执行频率
    使用方法：
        from geeker import Concurrency

        每4秒执行5次abc

        @Concurrency(5,4)
        def abc():
            pass
        
        并发量为5
        @Concurrency(5)
        def abc():
            pass
            
        同样可以装饰类方法
        
        class Test:
            def __init__(self):
                pass
    
            @Concurrency(3)
            def test(self, a):
                print(a, self)
                time.sleep(a)
                
        
    4.run_time 此装饰器调控函数运行时间
    使用方法：
        from geeker import runtime
            
            @run_time
            def abc():
                pass

    5.Singleton 单例模式
    使用方法：
        from geeker import Singleton
        
        class Test(Singleton):
            pass

    6.mytimeout 超时装饰器
    使用方法：
        from geeker import time_out

        @time_out(4)
        def test(*args):
            print("开始执行", args)
            time.sleep(args[0])
            print("----执行完成", args)
         
    7.MyType 类属性的类型检查
    使用方法：
        from geeker import MyType
        
        class Test:
            lll = MyType('str_type1', except_type=str)
            llll = MyType('str_type2', except_type=str)
        
            def __init__(self, value, ):
                self.lll = value
                self.llll = value
                
    8.MWS相关api
    使用方法：
        from geeker import mws
        
    9.MyDict
    a=MyDict()
    a.append_key('key','value')
    a.o=5
    a.c='fasf'
    a.add_key('key0','value0')
    print(dict(a))
    >>>{
        'key': ['value'],
        'o': 5, 
        'c': 'fasf', 
        'key0': {'value0'}
        }
"""
