
# 刘亚龙的 functools

##### 一些很有用的工具

------------



### 使用说明：

------------

> pip install WhatTheFuck

------------


> ~~觉得好用请点个star，分享给更多的人使用~~
------------


## schedule更改自schedule，修复原作者代码日期不准确BUG，并添加线程控制以解决任务延迟的问题

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

## MyLog:日志记录,自动切割，压缩等

		from WhatTheFuck import MyLog
		logger=MyLog().getlogger()
		


## timeslimit :控制函数执行频率

		from WhatTheFuck import CallTimesLimit

		#每4秒执行5次abc
		@CallTimesLimit(5,4)
		def abc():
			pass
			

## run_time 此装饰器调控函数运行时间
        
        from WhatTheFuck import runtime
        
        @run_time
        def abc():
            pass

##  Singleton 单例模式

    from WhatTheFuck import Singleton
    
    class Test(Singleton):
        pass

##  time_out 超时装饰器

		from WhatTheFuck import time_out

		@time_out(4)
		def test(*args):
		print("开始执行", args)
		time.sleep(args[0])
		print("----执行完成", args)
		
##  PyCrypt 加密-解密

        from WhatTheFuck import PyCrypt      
        
        pp=PyCrypt('16位密钥字符串..........')
        aa=pp.encrypt('待加密的内容') 
        bb =pp.decrypt('加密过的字节内容') 

##  MyType 类属性的类型检查

        from WhatTheFuck import MyType  
        
        class Test:
            lll = MyType('str_type1', except_type=str)
            llll = MyType('str_type2', except_type=str)
        
            def __init__(self, value, ):
                self.lll = value
                self.llll = value
                
------------

