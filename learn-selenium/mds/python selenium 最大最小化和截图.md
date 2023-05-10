python selenium 最大最小化和截图

## 代码

```python
import os.path
import time
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)

time.sleep(3)
driver.minimize_window()  # 最小化窗口

time.sleep(3)
driver.maximize_window()  # 最大化窗口

time.sleep(3)
driver.minimize_window()  # 最小化窗口

time.sleep(3)
driver.fullscreen_window()  # 窗口全屏化

time.sleep(3)
driver.set_window_size(500, 500)  # 设置为指定大小

time.sleep(3)
driver.set_window_position(400, 400)  # 指定窗口的坐标

driver.get('http://sahitest.com/demo/saveAs.htm')

time.sleep(3)
driver.save_screenshot(os.path.abspath('./image.png'))  # 窗口截图

ele = driver.find_element(By.XPATH, '//a[text()="testsaveas.zip"]')
time.sleep(3)
ele.screenshot(os.path.abspath('./image-ele.png'))  # 特定元素截图

ele.click()
sleep(6)
driver.quit()

"""
https://blog.csdn.net/lan_yangbi/article/details/127968172
"""
```

上面的代码，默认打开都是大窗口，然后才会改变大小，我们可以指定options，当打开时，就改变窗口大小

```
options.add_argument("--start-maximized")  # 启动时最大化
```

```
options.add_argument('window-size=100,300')  # 启动时指定宽高
```

```
options.add_argument('window-position=800,100')  # 启动时指定位置
```

以上完整测试代码

```python
import time

from selenium import webdriver
from selenium.webdriver.common.by import By


def max_when_start():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")  # 启动时最大化
    driver = webdriver.Chrome(options=options)

    driver.get('http://sahitest.com/demo/saveAs.htm')
    ele = driver.find_element(By.XPATH, '//a[text()="testsaveas.zip"]')
    ele.click()
    time.sleep(2)
    driver.quit()


def resize_when_start():
    options = webdriver.ChromeOptions()

    options.add_argument('window-size=100,300')  # 启动时指定宽高

    driver = webdriver.Chrome(options=options)
    driver.get('http://sahitest.com/demo/saveAs.htm')
    ele = driver.find_element(By.XPATH, '//a[text()="testsaveas.zip"]')
    ele.click()
    time.sleep(2)
    driver.quit()


def point_when_start():
    options = webdriver.ChromeOptions()

    options.add_argument('window-position=800,100')  # 启动时指定位置

    driver = webdriver.Chrome(options=options)
    driver.get('http://sahitest.com/demo/saveAs.htm')
    ele = driver.find_element(By.XPATH, '//a[text()="testsaveas.zip"]')
    ele.click()
    time.sleep(2)
    driver.quit()


if __name__ == '__main__':
    # max_when_start()
    # resize_when_start()
    point_when_start()
   
```

## 参考链接

https://blog.csdn.net/lan_yangbi/article/details/127968172

https://www.cnblogs.com/superhin/p/12607074.html

## 代码github

https://github.com/rainbow-tan/learn-python/tree/main/learn-selenium