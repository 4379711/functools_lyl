
# functools


##### 一些很有用的工具

------------



### 使用说明：

------------

> pip install geeker

------------


> ~~觉得好用请点个star，分享给更多的人使用~~
------------


## schedule：
#### 说明:geeker.schedule是schedule的二次开发,修复原作者代码日期不准确等BUG，并解决任务延迟等问题
    
        
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
            # 此处可添加参数max_worker 控制任务的总数,如果定时任务较多,则需要增加此参数
            # schedule.run_pending(max_worker=10)
            time.sleep(1)
            
------------     

## MyLog:将日志分日志等级记录,并自动压缩2019-11-11.info.log.gz

#### 参数:
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
            # 实例方法:
            get_logger()-->logger
    
#### 使用举例:
            from geeker import MyLog
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
#### 注意:
##### MyLog()的实例只会同时存在一个,默认记录首次创建实例的属性.
#### 例如:
    
                mylog = MyLog('./logs/logs/')
                mylog2 = MyLog()
                logger = mylog.get_logger()
                logger2 = mylog2.get_logger()
                logger.info('info')
    
                logger2 = MyLog('./logs/logs2/').get_logger()
                logger2.info('info2')
    
##### 以上两个logger logger2,会以logger(第一次创建实例)的属性为准,日志会存放在./logs/logs/下
    
------------   

## Concurrency :控制函数执行频率

>(用于多线程模型,协程无效)


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
			
------------

## run_time 此装饰器调控函数运行时间
        
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

------------

##  Singleton 单例模式

    from geeker import Singleton
    # 实例的属性为第一次初始化时的属性
    class Test(Singleton):
        pass

------------

##  TimeOut 超时装饰器

### 注意:
##### 此装饰器需要额外的线程数量来控制任务执行,
##### 如在多线程并发情况下使用,请评估机器性能(一般没啥大问题)

        from geeker import TimeOut
        # 精度为0.1秒
   		
        @TimeOut(4)
        def test(i):
            time.sleep(i)
        
        
        class AA:
        
            @TimeOut(3.0)
            def test(self, i):
                time.sleep(i)


------------
	
##  PyCrypt 加密-解密(已删除此项目)

        from geeker import PyCrypt      
        
        pp=PyCrypt('16位密钥字符串..........')
        aa=pp.encrypt('待加密的内容') 
        bb =pp.decrypt('加密过的字节内容') 

------------

##  MyType 类属性的类型检查

        from geeker import MyType  
        
        class Test:
            lll = MyType('str_type1', expect_type=str)
            llll = MyType('str_type2', expect_type=str)
        
            def __init__(self, value, ):
                self.lll = value
                self.llll = value
                
------------
          
##  MWS相关api
        from geeker import mws

        shipment = mws.OutboundShipments(...)
        resp = shipment.list_all_fulfillment_orders(...)
        data = resp.parsed
        

------------

##  特殊字典
### 注意:
##### 如需要转换成字典,需要使用dict()可直接转换,转换后可直接存mongo
        
        from geeker import MyDict
        a=MyDict()
        a.append_key('key','value')
        a.o=5
        a.c='fasf'
        a.add_key('key0','value0')
        print(dict(a))
        使用dict()函数可以直接转换为字典格式
        
        >>>{
            'key': ['value'],
            'o': 5, 
            'c': 'fasf', 
            'key0': {'value0'}
            }
                
------------

## Advertising API 
> 亚马逊广告API,目前仅实现SP部分


    from geeker import SponsoredProducts as sp
    ad = sp.ProductAds(client_id, client_secret, access_token, refresh_token, 'US',
                    profile_id=profile, sandbox=True)
    resp = ad.list_product_ads_ex()
    print(resp.json())
    
    #####################
    from geeker import Account
    ad = Account.Client(client_id, client_secret, access_token, refresh_token, 'US',
                    profile_id=profile, sandbox=True, redirect_uri=redirect_uri)

