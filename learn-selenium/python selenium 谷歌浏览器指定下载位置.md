python selenium 谷歌浏览器指定下载位置

## 功能

python selenium点击浏览器的下载按钮，然后下载到指定的目录，而非下载到默认位置

## 代码

```python
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
```

## 注意事项

下载路径要写绝对路径，否则还是会下载到默认路径

## 参考链接

[(40条消息) Python selenium —— 文件下载，不弹出窗口，直接下载到指定路径_selenium下载文件_huilan_same的博客-CSDN博客](https://blog.csdn.net/huilan_same/article/details/52789954)