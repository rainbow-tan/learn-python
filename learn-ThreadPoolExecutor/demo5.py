import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed


def log(msg):
    t = threading.currentThread()
    name = t.name
    ident = t.ident
    print(f"[{ident}][{name}]{msg}")  # 打印线程号和线程名称


def job(name, second):
    log(f"I am {name} begin")
    time.sleep(second)
    log(f"I am {name} end")
    return f'{name}--->{second}'


def main():
    executor = ThreadPoolExecutor(max_workers=5, thread_name_prefix="MyThread")
    t1 = executor.submit(job, "墨玉麒麟", 3)
    t2 = executor.submit(job, "张良", 5)
    t3 = executor.submit(job, "猴子", 4)
    for obj in as_completed([t1, t2, t3]):
        print(obj.result())
    log("主线程运行中.")
    log("主线程运行中..")
    log("主线程运行中...")


def main2():
    executor = ThreadPoolExecutor(max_workers=5, thread_name_prefix="MyThread")
    t1 = executor.submit(job, "墨玉麒麟", 4)
    t2 = executor.submit(job, "张良", 6)
    t3 = executor.submit(job, "猴子", 5)
    for obj in as_completed([t1, t2, t3], timeout=5):
        print(obj.result())
    log("主线程运行中.")
    log("主线程运行中..")
    log("主线程运行中...")


if __name__ == '__main__':
    main2()
