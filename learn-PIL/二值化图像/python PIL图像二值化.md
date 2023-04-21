python PIL图像二值化

## 1、写在前面

对于图像的知识，我是一点不了解。这里主要是以个人使用的方式来记录一下二值化的用法以及个人感觉知识点，不保证是正确内容。

算是给自己留个笔记，下次遇到同样的场景，能直接拿来用。

## 2、图像的模式

先简单了解一下图像的模式，只列出其中几个模式，其他模式可自行百度

- 模式“1”

  模式“1”为二值图像，非黑即白。每个像素用8个bit表示，0表示黑，255表示白。

  像素的值只有0和255

- 模式“L”

  模式“L”为灰色图像，它的每个像素用8个bit表示，0表示黑，255表示白，其他数字表示不同的灰度。

  在PIL中，从模式“RGB”转换为“L”模式是按照下面的公式转换的：L = R * 299/1000 + G * 587/1000+ B * 114/1000

  像素的值从0到255

- 模式“RGB”

  对于彩色图像，不管其图像格式是PNG，还是BMP，或者JPG，在PIL中，使用Image模块的open()函数打开后，返回的图像对象的模式都是“RGB”。

  像素的值是三元组，每个元素值都是0到255

- 模式“RGBA”

  模式“RGBA”为32位彩色图像，它的每个像素用32个bit表示，其中24bit表示红色、绿色和蓝色三个通道，另外8bit表示alpha通道，即透明通道。

  相对于模式“RGB”，多了一个透明通道

通过图像的模式可以知道，图像可以分为以下几类

- 彩色图像

  彩色图像有blue，green，red三个通道，取值范围均为0-255（模式RGB）

- 灰度图

  灰度图：只有一个通道，取值范围在0-255，所以一共有256种颜色（模式L）

- 二值图像

  二值图像，只有两种颜色,既黑色和白色（模式1）

## 3、转换RGB模式为1模式、L模式

RGB模式获取像素点，值是三元组，三元组中每个元素值是0到255

1模式获取像素点，值是0或者255

L模式获取像素点，值是0到255中的一个数

```python
import json

from PIL import Image


def get_all_pixel(img):
    width = img.size[0]
    height = img.size[1]
    ret = []
    for x in range(width):
        for y in range(height):
            pixel = img.getpixel((x, y))
            # print(f"{x},{y} -----> {pixel}")
            ret.append(pixel)
    return ret


def main():
    img = Image.open('img/img.png')
    mode = img.mode
    print(f"img_ mode:{mode}")  # RGB
    ret = get_all_pixel(img)  # RGB模式, 像素点是三元组 (136, 161, 193)
    with open('mode/mode_rgb.txt', 'w') as f:
        json.dump(ret, f)

    img_1 = img.convert("1")
    mode = img_1.mode
    print(f"img_1 mode:{mode}")  # 1
    ret_1 = get_all_pixel(img_1)  # 1模式, 像素点0或者255
    with open('mode/model_1.txt', 'w') as f:
        json.dump(ret_1, f)
    img_1.save('img/img_1.png')

    img_2 = img.convert("L")
    mode = img_2.mode
    print(f"img_2 mode:{mode}")  # L
    ret_2 = get_all_pixel(img_2)  # L模式, 像素点0到255
    with open('mode/model_l.txt', 'w') as f:
        json.dump(ret_2, f)
    img_2.save('img/img_L.png')


if __name__ == '__main__':
    main()

```

运行

![image-20230421153443271](C:\Users\dell\AppData\Roaming\Typora\typora-user-images\image-20230421153443271.png)

## 4、二值化图像

我们可以自定义二值化规则来生成二值化图像，先把图像转换为模式L（像素点在0至255），然后自定义规则（像素点大于某值就认为是黑，否则就是白），然后把模式L转换为模式1，就得到了自定义规则的模式1二值化图像

- 使用场景

  我认为应该是用于图片背景和主题人物形成比较鲜明对比的图片，然后想要抛弃图片背景的影响。相当于把人物从背景中抠出来，不让背景影响后续的操作

  比如我想比较PUBG中的配件信息，就把配件抠出来，而忽略背景，让后续的比较图像相似度的效果更好一些

```python
import json

from PIL import Image


def get_all_pixel(img):
    width = img.size[0]
    height = img.size[1]
    ret = []
    for x in range(width):
        for y in range(height):
            pixel = img.getpixel((x, y))
            # print(f"{x},{y} -----> {pixel}")
            ret.append(pixel)
    return ret


def main():
    img = Image.open('img/img.png')
    img_2 = img.convert("L")

    # 自定义灰度界限，大于这个值为黑色，小于这个值为白色
    threshold = 150

    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)

    img_3 = img_2.point(table, "1")  # 图片二值化 使用table来设置二值化的规则
    img_3.save(f"img/img_L_1_{threshold}.png")
    ret = get_all_pixel(img_3)
    with open(f'mode/img_L_1_{threshold}.txt', 'w') as f:
        json.dump(ret, f)


if __name__ == '__main__':
    main()
```

运行

![image-20230421155705899](C:\Users\dell\AppData\Roaming\Typora\typora-user-images\image-20230421155705899.png)



阈值设置为150，看得出效果很好，非常棒

## 参考链接

https://www.cnblogs.com/zhanghaiyan/p/icamera0.html

[ Python图像的二值化_python二值化图像处理_ljx1400052550的博客-CSDN博客](https://blog.csdn.net/ljx1400052550/article/details/114735364)

## 代码地址

