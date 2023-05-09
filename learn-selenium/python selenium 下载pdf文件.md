python selenium 下载pdf文件

## 功能

python selenium下载链接后面是xxx.pdf的pdf文件，当默认打开链接是，直接默认显示的是pdf文件，例如

![image-20230509141558477](https://img2023.cnblogs.com/blog/1768648/202305/1768648-20230509141731855-791801845.png)

## 代码

```python
import os
import time

from selenium import webdriver

"""
指定默认下载路径, 下载链接是xxx.pdf的链接 如果浏览器直接打开则会显示pdf
https://www.cnblogs.com/lingwang3/p/14440087.html
https://www.codenong.com/81d215683e7fbf0ebd81/
"""
down_load_dir = os.path.abspath("./AAA/BBB/CCC")  # 浏览器会自动创建文件夹 写绝对路径
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ['enable-automation'])
prefs = {
    "download.default_directory": down_load_dir,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True
}
options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(options=options)
url = 'https://www.soumu.go.jp/johotsusintokei/whitepaper/ja/h30/pdf/30daijin.pdf'
driver.get(url)
time.sleep(3)
driver.quit()
```

## 注意事项

下载路径要写绝对路径，否则还是会下载到默认路径

下载路径可以自己创建，也可以不创建，浏览器会自动创建

## 参考链接

https://www.cnblogs.com/lingwang3/p/14440087.html
https://www.codenong.com/81d215683e7fbf0ebd81/