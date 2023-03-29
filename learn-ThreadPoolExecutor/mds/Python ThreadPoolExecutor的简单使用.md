python ThreadPoolExecutor的简单使用

# 一、前言

Python3.2以后，官方新增了concurrent.futures模块，该模块提供线程池ThreadPoolExecutor和进程池ProcessPoolExecutor 。使用起来非常方便。以下是个人对于线程池ThreadPoolExecutor的使用笔记。[官网](https://docs.python.org/zh-cn/3.7/library/concurrent.futures.html)

# 二、基本使用

### 1、简单使用线程池

只需要两步，即可简单使用线程池

- 通过ThreadPoolExecutor()创建线程池

- 通过submit提交任务到线程池

```python
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
    executor.submit(job, "墨玉麒麟", 3)
    executor.submit(job, "张良", 7)
    executor.submit(job, "猴子", 5)
    log("主线程运行中.")
    log("主线程运行中..")
    log("主线程运行中...")


if __name__ == '__main__':
    main()
```

运行

![image-20230329160400142](C:\Users\dell\AppData\Roaming\Typora\typora-user-images\image-20230329160400142.png)

### 2、查看子线程是否运行结束

- 通过done函数判断子线程是否运行结束

```python
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
```

运行

![image-20230329160253390](C:\Users\dell\AppData\Roaming\Typora\typora-user-images\image-20230329160253390.png)

### 3、获取子线程的返回

- 通过result函数获取子线程的返回值

- result函数可以接收一个timeout参数，表示最大等待时间。
  - 不设置，则默认一直等到子线程结束，获取返回值。这是阻塞的！
  - 设置一个值，则表示最多等timeout秒，
    - 如果还没到timeout秒，子线程就结束了，则获取到子线程返回值
    - 如果超过了timeout秒，子线程还没结束，则主线程抛出TimeoutError异常，但子线程依旧会执行，直到返回

```python
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
    t1 = executor.submit(job, "墨玉麒麟", 3)
    t2 = executor.submit(job, "张良", 4)
    t3 = executor.submit(job, "猴子", 5)
    log("主线程运行中.")
    time.sleep(7)
    log("主线程运行中..")
    log(f"{t1.result()}")
    log(f"{t2.result()}")
    log(f"{t3.result()}")
    log("主线程运行中...")


def main2():
    executor = ThreadPoolExecutor(max_workers=5, thread_name_prefix="MyThread")
    t1 = executor.submit(job, "墨玉麒麟", 3)
    t2 = executor.submit(job, "张良", 4)
    t3 = executor.submit(job, "猴子", 10)
    log("主线程运行中.")
    log("主线程运行中..")
    log(f"{t1.result()}")
    log(f"{t2.result()}")
    log(f"{t3.result(timeout=3)}")
    log("主线程运行中...")


if __name__ == '__main__':
    # main()
    main2()
```

### 4、等待部分或所有子线程结束

有三种方式可以等待部分或所有子线程结束

#### 4.1、通过wait函数等待

- 通过wait函数等待所有子线程结束
- wait函数可以接收一个timeout参数，表示最大等待时间。
  - 不设置，则默认一直等到所有子线程结束。这是阻塞的！
  - 设置一个值，则表示最多等timeout秒，
    - 如果还没到timeout秒，子线程就结束了，则继续执行主线程
    - 如果超过了timeout秒，子线程还没结束，也继续执行主线程

```python
import threading
import time
from concurrent.futures import ThreadPoolExecutor, wait


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
    t2 = executor.submit(job, "张良", 4)
    t3 = executor.submit(job, "猴子", 5)

    wait([t1, t2, t3])
    log(f"{t1.result()}")
    log(f"{t2.result()}")
    log(f"{t3.result()}")
    log("主线程运行中.")
    log("主线程运行中..")
    log("主线程运行中...")


def main2():
    executor = ThreadPoolExecutor(max_workers=5, thread_name_prefix="MyThread")
    t1 = executor.submit(job, "墨玉麒麟", 3)
    t2 = executor.submit(job, "张良", 5)
    t3 = executor.submit(job, "猴子", 6)

    wait([t1, t2, t3], timeout=4)
    log(f"{t1.done()}")
    log(f"{t2.done()}")
    log(f"{t3.done()}")
    log("主线程运行中.")
    log("主线程运行中..")
    log("主线程运行中...")


if __name__ == '__main__':
    # main()
    main2()
```

#### 4.2、通过as_completed函数等待

- 通过as_completed函数等待所有子线程结束

- as_completed函数可以接收一个timeout参数，表示最大等待时间。

  - 不设置，则默认一直等到所有子线程结束，获取返回值。这是阻塞的！

  - 设置一个值，则表示最多等timeout秒，
    - 如果还没到timeout秒，子线程就结束了，则获取到子线程返回值
    - 如果超过了timeout秒，子线程还没结束，则主线程抛出TimeoutError异常，但子线程依旧会执行，直到返回

- 不同于wait函数，as_completed函数直接返回的是子线程的返回值

```python
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
```

#### 4.3、通过map函数等待

- 通过map函数等待所有子线程结束
- map函数可以接收一个timeout参数，表示最大等待时间。
  - 不设置，则默认一直等到所有子线程结束，获取返回值。这是阻塞的！
  - 设置一个值，则表示最多等timeout秒，
    - 如果还没到timeout秒，子线程就结束了，则获取到子线程返回值
    - 如果超过了timeout秒，子线程还没结束，则主线程抛出TimeoutError异常，但子线程依旧会执行，直到返回
- 不同于as_completed函数，map函数获取的返回值是顺序的

```python
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
```

#### 4.4、等待子线程结束函数对比

- 不论设置不设置timeout参数，wait函数都不会抛出异常。要获取返回值，需要调用result方法
- as_completed函数，如果设置了timeout参数，根据运行情况，会抛出异常。直接返回的是子线程的返回值，无需调用result方法，但返回值的顺序是不固定的，哪个线程先执行完，则先返回哪个线程的返回值
- map函数，如果设置了timeout参数，根据运行情况，会抛出异常。直接返回的是子线程的返回值，无需调用result方法，且返回值的顺序是固定的，不论哪个线程执行完毕，都根据顺序返回结果
