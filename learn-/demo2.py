import datetime
import threading
import time
from concurrent.futures import ThreadPoolExecutor, wait


def log(msg):
    t = threading.currentThread()
    name = t.name
    ident = t.ident
    print(f"[{ident}][{name}]{msg}")  # 打印线程号和线程名称


def job(name):
    log(f"I am {name} begin")
    time.sleep(10)
    log(f"I am {name} end")


def main():
    log(str(datetime.datetime.now()))
    executor = ThreadPoolExecutor(max_workers=5, thread_name_prefix="MyThread")
    t1 = executor.submit(job, "墨玉麒麟")
    t2 = executor.submit(job, "张良")
    t3 = executor.submit(job, "猴子")
    ts = [t1, t2, t3]
    wait(ts)  # 等待所有线程结束

    log(str(datetime.datetime.now()))
    log("主线程运行中.")
    log("主线程运行中..")
    log("主线程运行中...")


def main2():
    log(str(datetime.datetime.now()))
    executor = ThreadPoolExecutor(max_workers=5, thread_name_prefix="MyThread")
    t1 = executor.submit(job, "墨玉麒麟")
    t2 = executor.submit(job, "张良")
    t3 = executor.submit(job, "猴子")
    ts = [t1, t2, t3]
    wait(ts, timeout=5)  # 等待所有线程结束  如果5秒还没结束 也继续往下执行

    log(str(datetime.datetime.now()))
    log("主线程运行中.")
    log("主线程运行中..")
    log("主线程运行中...")


def main3():
    log(str(datetime.datetime.now()))
    executor = ThreadPoolExecutor(max_workers=5, thread_name_prefix="MyThread")
    t1 = executor.submit(job, "墨玉麒麟")
    t2 = executor.submit(job, "张良")
    t3 = executor.submit(job, "猴子")
    ts = [t1, t2]
    wait(ts)  # 只等待t1和t2线程结束

    log(str(datetime.datetime.now()))
    log("主线程运行中.")
    log("主线程运行中..")
    log("主线程运行中...")


if __name__ == '__main__':
    # main()
    # main2()
    main3()
