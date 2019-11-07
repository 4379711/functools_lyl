
# functools

##### 一些很有用的工具

------------



### 使用说明：

------------

> pip install geeker

------------


> ~~觉得好用请点个star，分享给更多的人使用~~
------------


## geeker.schedule更改自schedule，修复原作者代码日期不准确等BUG，并添加线程控制以解决任务延迟等问题

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

## MyLog:日志记录,自动切割，压缩等

		from geeker import MyLog
		
		logger=MyLog().getlogger()
		logger.info('info...')
		


## timeslimit :控制函数执行频率

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

##  Singleton 单例模式

    from geeker import Singleton
    # 实例的属性为第一次初始化时的属性
    class Test(Singleton):
        pass

##  TimeOut 超时装饰器


        from geeker import TimeOut
        # 精度为0.1秒
   		
        @TimeOut(4)
        def test(i):
            time.sleep(i)
        
        
        class AA:
        
            @TimeOut(3.0)
            def test(self, i):
                time.sleep(i)

		
##  PyCrypt 加密-解密(已删除此项目)

        from geeker import PyCrypt      
        
        pp=PyCrypt('16位密钥字符串..........')
        aa=pp.encrypt('待加密的内容') 
        bb =pp.decrypt('加密过的字节内容') 

##  MyType 类属性的类型检查

        from geeker import MyType  
        
        class Test:
            lll = MyType('str_type1', except_type=str)
            llll = MyType('str_type2', except_type=str)
        
            def __init__(self, value, ):
                self.lll = value
                self.llll = value
                
                
##  MWS相关api
        from geeker import mws

        shipment = mws.OutboundShipments(...)
        resp = shipment.list_all_fulfillment_orders(...)
        data = resp.parsed
        


##  特殊字典

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

