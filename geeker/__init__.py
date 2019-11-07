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

__all__ = ['MyType', 'MyLog', 'TimeOut',
           'schedule', 'mws', 'Concurrency',
           'Singleton', 'MyDict', 'run_time'
           ]
__UpdateTime__ = '2019/11/7 17:30'

"""
说明：
    1.geeker.schedule更改自schedule，修复原作者代码日期不准确等BUG，并添加线程控制以解决任务延迟等问题
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
              logger.info('info...')


    3.timeslimit :控制函数执行频率
    使用方法：
        from geeker import Concurrency

        # 每4秒执行5次abc()

        @Concurrency(5,4)
        def abc():
            pass
        
        # 并发量为5
        @Concurrency(5)
        def abc():
            pass
            
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
        def test(i):
            # int('asfa')
            time.sleep(i)
            print('运行结果:', i)
            
        >>>
            START test(1, {})
            运行结果: 1
            test(1, {}) takes <1.0006> seconds
            STOP test(1, {})

    5.Singleton 单例模式
    使用方法：
        from geeker import Singleton
        
        class Test(Singleton):
            pass

    6.TimeOut 超时装饰器
    使用方法：
        from geeker import TimeOut
        
        # 最小精度为0.1秒
        @TimeOut(4)
        def test(i):
            time.sleep(i)
        
        
        class AA:
        
            @TimeOut(3.0)
            def test(self, i):
                time.sleep(i)

         
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

        shipment = mws.OutboundShipments(...)
        resp = shipment.list_all_fulfillment_orders(...)
        data = resp.parsed
        
    9.MyDict,一个特殊数据类型的字典
    使用方法：
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
