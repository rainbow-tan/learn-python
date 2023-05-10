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
