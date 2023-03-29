import random
import threading
import time
from concurrent.futures import ThreadPoolExecutor


def log(msg):
    t = threading.currentThread()
    name = t.name
    ident = t.ident
    print(f"[{ident}][{name}]{msg}")  # 打印线程号和线程名称


def job(name):
    log(f"I am {name} begin")
    time.sleep(random.randint(1, 10))
    log(f"I am {name} end")


def main():
    executor = ThreadPoolExecutor(max_workers=5, thread_name_prefix="MyThread")
    executor.submit(job, "墨玉麒麟")
    executor.submit(job, "张良")
    executor.submit(job, "猴子")
    log("主线程运行中.")
    log("主线程运行中..")
    log("主线程运行中...")


if __name__ == '__main__':
    main()
