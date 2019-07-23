import ctypes
import inspect
import time
import threading


class MyThread(threading.Thread):
    def __init__(self, target, args=None, kwargs=None):
        super().__init__()
        self.func = target
        self.args = args
        self.kwargs = kwargs
        self.result = '<__what fuck!__>'

    def run(self):
        self.result = self.func(*self.args, **self.kwargs)

    @property
    def get_result(self):
        return self.result

    @staticmethod
    def _async_raise(tid, exctype):
        """raises the exception, performs cleanup if needed"""
        tid = ctypes.c_long(tid)
        if not inspect.isclass(exctype):
            exctype = type(exctype)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
        if res == 0:
            raise ValueError("invalid thread id")
        elif res != 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            raise SystemError("PyThreadState_SetAsyncExc failed !")

    @classmethod
    def stop_thread(cls, thread):
        cls._async_raise(thread.ident, SystemExit)


def time_out(limit_time):
    if not isinstance(limit_time, int):
        raise ValueError('The argument must be int !')

    def warps0(func):
        def warps1(*args, **kwargs):
            th = MyThread(target=func, args=args, kwargs=kwargs)
            th.setDaemon(True)
            th.start()
            # try to get result
            for _ in range(limit_time):
                time.sleep(1)
                is_result = th.get_result
                if is_result != '<__what fuck!__>':
                    return is_result
            # 核心代码 <让线程自杀!>
            th.stop_thread(th)
            raise TimeoutError('Oh,Fuck!TimeOut Error!')

        return warps1

    return warps0


if __name__ == '__main__':
    @time_out(4)
    def test(*args):
        print("开始执行", args)
        time.sleep(args[0])
        print("----执行完成", args)


    mlist = []
    for i in range(7):
        th = threading.Thread(target=test, args=(i,))
        mlist.append(th)

    for i in mlist:
        i.start()

    for i in mlist:
        i.join()
