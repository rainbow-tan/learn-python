import datetime
import threading
import time
from concurrent.futures import ThreadPoolExecutor


def log(msg):
    t = threading.currentThread()
    name = t.name
    ident = t.ident
    print(f"[{ident}][{name}]{msg}")  # 打印线程号和线程名称


def job(name, second):
    # log(f"I am {name} begin")
    time.sleep(second)
    # log(f"I am {name} end")
    return f'[{threading.currentThread().ident}]{name}--->{second}'


def main():
    now = datetime.datetime.now()
    log(f"开始时间:{now}")
    executor = ThreadPoolExecutor(max_workers=5, thread_name_prefix="MyThread")  # 超过线程个数的任务
    # 如果不接收map的返回值,是不会阻塞等待的
    executor.map(job, ("墨玉麒麟", "张良", "猴子", "弄玉", "墨子", "韩飞", "逆鳞"), (3, 5, 4, 8, 5, 6, 10))

    log("主线程运行中.")
    log("主线程运行中..")
    log("主线程运行中...")
    now = datetime.datetime.now()
    log(f"结束时间:{now}")


if __name__ == '__main__':
    main()
