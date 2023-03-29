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


def main():
    executor = ThreadPoolExecutor(max_workers=5, thread_name_prefix="MyThread")
    t1 = executor.submit(job, "墨玉麒麟", 3)
    t2 = executor.submit(job, "张良", 7)
    t3 = executor.submit(job, "猴子", 5)
    log("主线程运行中.")
    time.sleep(4)
    log("主线程运行中..")
    log(f"{t1.done()}")
    log(f"{t2.done()}")
    log(f"{t3.done()}")
    log("主线程运行中...")


if __name__ == '__main__':
    main()
