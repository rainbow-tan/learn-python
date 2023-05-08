import os.path
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By

"""
指定默认下载路径,通过点击按钮时,下载到指定位置
https://blog.csdn.net/huilan_same/article/details/52789954
"""
download_dir = os.path.abspath('./AAA/BBB')  # 浏览器会自动创建文件夹 写绝对路径
options = webdriver.ChromeOptions()
prefs = {'profile.default_content_settings.popups': 0,
         'download.default_directory': download_dir}
options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(options=options)
driver.get('http://sahitest.com/demo/saveAs.htm')
driver.find_element(By.XPATH, '//a[text()="testsaveas.zip"]').click()
sleep(30)
driver.quit()
