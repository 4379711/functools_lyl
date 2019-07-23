
# 刘亚龙的 functools

##### 一些很有用的工具

------------



### 使用说明：

------------

> pip install WhatTheFuck

------------


> ~~觉得好用请点个star，分享给更多的人使用~~
------------


## schedule_lyl更改自schedule，修复原作者代码日期不准确BUG，并添加线程控制以解决任务延迟的问题

		from WhatTheFuck import schedule_lyl
		import time

		def abc():
		print('abc')
		
		# 注册任务
		schedule_lyl.every(2).seconds.do(abc)
		schedule_lyl.every().day.at("10:00").do(abc)

		# 开启任务
		while True:
		schedule_lyl.run_pending()
		time.sleep(1)

## mylog:日志记录,自动切割，压缩等

		from WhatTheFuck.mylog import My_log
		logger=My_log().getlogger()
		


## timeslimit :控制函数执行频率

		from WhatTheFuck.timeslimit import CallTimesLimit

		#每4秒执行5次abc
		@CallTimesLimit(5,4)
		def abc():
			pass
			

## run_time 此装饰器调控函数运行时间

##  Singleton 单例模式

##  mytimeout 超时装饰器

		from WhatTheFuck.mytimeout import time_out

		@time_out(4)
		def test(*args):
		print("开始执行", args)
		time.sleep(args[0])
		print("----执行完成", args)
		

------------
