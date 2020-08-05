# -*- coding: utf-8 -*-

from __future__ import absolute_import
from .mylog import *
from . import schedule
from . import mws
from .functions import *
from .utils import *
from .mws.Advertising import SponsoredProducts
from .mws.Advertising import Account

__all__ = ['MyType', 'MyLog', 'TimeOut',
           'schedule', 'mws', 'Concurrency',
           'Singleton', 'MyDict', 'run_time',
           "retry", 'SponsoredProducts', 'Account',
           "IdGenerator", 'show_memory_info'
           ]
__UpdateTime__ = '2020/08/05 15:15'

"""
说明：
    1.geeker.schedule是schedule的二次开发
        修复原作者代码日期不准确等BUG，并解决任务延迟等问题
    
    使用方法：
        from geeker import schedule
        import time
        
        # 待执行任务
        def abc():
            print('abc')

        # 注册任务
        schedule.every(2).seconds.do(abc)
        schedule.every().day.at("10:00").do(abc)

        # 开启任务
        while True:
            schedule.run_pending()
             
            # 参数max_worker 控制任务的总数,默认是任务数的2倍.
            # 注意,如果设置一个较大值,请考虑内存是否允许
           
            # schedule.run_pending(max_worker=2)
            time.sleep(1)

    2.MyLog:

        功能:
            将日志分日志等级记录,并自动压缩2019-11-11.info.log.gz
    
        参数:
            :param dir_path: 日志记录的路径,默认是当前路径下的log文件夹
            :param logger_name: logger对象的名字
            :param info_name: 保存info等级的文件名字
            :param error_name:
            :param warning_name:
            :param debug_name:
            :param interval: 压缩日志的频率,默认是7天
            :param detail: bool值,记录日志是否为详细记录
            :param debug: 是否记录debug,默认不记录
            :param info: 是否记录info,默认记录
            :param error:
            :param warning:
        实例方法:
            get_logger()-->logger
    
        使用举例:
            # 记录四种类型的日志
            logger = MyLog(debug=True).get_logger()
            logger.info('info')
            logger.debug('debug')
            logger.error('error')
            logger.warning('warning')
    
            # # # # # # # # # # # # # # # # # # # # # # # # #
    
            # 只记录错误日志
            logger = MyLog(info=False,warning=False).get_logger()
            logger.info('info')
            logger.debug('debug')
            logger.error('error')
            logger.warning('warning')
        注意:
            MyLog()的实例只会同时存在一个,默认记录首次创建实例的属性.
            例如:
    
                mylog = MyLog('./logs/logs/')
                mylog2 = MyLog()
                logger = mylog.get_logger()
                logger2 = mylog2.get_logger()
                logger.info('info')
    
                logger2 = MyLog('./logs/logs2/').get_logger()
                logger2.info('info2')
    
                以上两个logger logger2,会以logger(第一次创建实例)的属性为准,日志会存放在./logs/logs/下
    
        
        
        使用方法: from geeker import MyLog
                  logger=MyLog().getlogger()
                  logger.info('info...')


    3.Concurrency :控制函数执行频率(多线程模型,协程无效)
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
    注意:
        此装饰器需要额外的线程数量来控制任务执行,
        如在多线程并发情况下使用,请评估机器性能(一般没啥大问题)
        
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
    注意:
        如需要转换成字典,需要使用dict()可直接转换,转换后可直接存mongo
        
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
    10.Advertising API 亚马逊广告API,目前仅实现SP部分
    from geeker import SponsoredProducts as sp
    ad = sp.ProductAds(client_id, client_secret, access_token, refresh_token, 'US',
                    profile_id=profile, sandbox=True)
    resp = ad.list_product_ads_ex()
    print(resp.json())
    
    from geeker import Account
    #####################
    ad = Account.Client(client_id, client_secret, access_token, refresh_token, 'US',
                    profile_id=profile, sandbox=True, redirect_uri=redirect_uri)
    
    11 .分布式唯一ID生成器
    
    from geeker import IdGenerator
    
    id_generator =IdGenerator()
    _id =id_generator.get_id()
    
    12 .查看当前python进程占用的内存
    from geeker import show_memory_info
    
    show_memory_info()
    
"""
