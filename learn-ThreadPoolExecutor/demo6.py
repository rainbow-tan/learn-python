import threading
import time
from concurrent.futures import ThreadPoolExecutor


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
    for result in executor.map(job, ("墨玉麒麟", "张良", "猴子"), (3, 5, 4)):
        print(result)
    log("主线程运行中.")
    log("主线程运行中..")
    log("主线程运行中...")


def main2():
    executor = ThreadPoolExecutor(max_workers=5, thread_name_prefix="MyThread")
    for result in executor.map(job, ("墨玉麒麟", "张良", "猴子"), (4, 7, 5), timeout=3):
        print(result)
    log("主线程运行中.")
    log("主线程运行中..")
    log("主线程运行中...")


if __name__ == '__main__':
    main2()
