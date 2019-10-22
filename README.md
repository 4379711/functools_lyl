
# 刘亚龙的 functools

##### 一些很有用的工具

------------



### 使用说明：

------------

> pip install geeker

------------


> ~~觉得好用请点个star，分享给更多的人使用~~
------------


## schedule更改自schedule，修复原作者代码日期不准确BUG，并添加线程控制以解决任务延迟的问题

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
		


## timeslimit :控制函数执行频率

		from geeker import CallTimesLimit

		#每4秒执行5次abc
		@CallTimesLimit(5,4)
		def abc():
			pass
			

## run_time 此装饰器调控函数运行时间
        
        from geeker import runtime
        
        @run_time
        def abc():
            pass

##  Singleton 单例模式

    from geeker import Singleton
    
    class Test(Singleton):
        pass

##  time_out 超时装饰器

		from geeker import time_out

		@time_out(4)
		def test(*args):
		    print("开始执行", args)
		    time.sleep(args[0])
		    print("----执行完成", args)
		
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


##  特殊字典

        from geeker import MyDict
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
                
------------

