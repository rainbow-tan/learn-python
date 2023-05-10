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
