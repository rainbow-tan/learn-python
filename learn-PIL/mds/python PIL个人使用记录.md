python PIL个人使用记录

## 1、gif转png

```python
def gif_to_png(filename: str):
    """
    gif图片一帧一帧转换为很多png图片
    :param filename:
    :return:
    """
    filename = filename.strip()
    filename = os.path.abspath(filename)
    assert os.path.splitext(filename)[-1].lower() == '.gif', f'文件后缀不是.gif "{filename}"'  # 是否是.gif后缀
    assert os.path.isfile(filename), f'不存在文件"{filename}"'  # 是否存在文件
    index = 1
    basename = os.path.basename(filename)
    basename_without_suffix = basename.replace(os.path.splitext(filename)[-1], '')

    image = Image.open(filename)
    iterator: Iterator = ImageSequence.Iterator(image)  # GIF图片流的迭代器
    save_path = os.path.join('.', 'image', basename_without_suffix)
    save_path = os.path.abspath(save_path)
    if os.path.exists(save_path):
        shutil.rmtree(save_path)
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    for img in iterator:  # img 是 GifImageFile对象
        save_name = os.path.join(save_path, f'frame_{index}.png')
        img.save(save_name)
        index += 1
    print(f"save to dir '{save_path}'")
    return save_path
```

![01](https://img2023.cnblogs.com/blog/1768648/202304/1768648-20230404154206093-260422914.gif)

![image-20230404153820660](https://img2023.cnblogs.com/blog/1768648/202304/1768648-20230404154206620-1631444288.png)

## 2、png转gif

```python
def png_to_gif(path: str, filename: str):
    """
    遍历文件夹图片, 按照名称排序 然后合成gif图片
    :param path:
    :param filename:
    :return:
    """
    path = os.path.abspath(path.strip())
    assert os.path.isdir(path), f'不存在文件夹"{path}"'  # 是否存在文件

    filename = os.path.abspath(filename.strip())
    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))

    files = os.listdir(path)
    files.sort(key=lambda x: int(str(x).replace('frame_', '').replace('.png', '')))
    frames = []  # 读入缓冲区
    for img in files:
        f = os.path.join(path, img)
        assert os.path.splitext(f)[-1].lower() == '.png', f'文件后缀不是.png "{filename}"'  # 是否是.png后缀
        frames.append(imageio.imread(f))
    imageio.mimsave(filename, frames, 'gif', duration=0.02)
    print(f"save to '{filename}'")
    return filename
```

学习链接 https://www.cnblogs.com/fly-kaka/p/11694011.html

## 3、获取所有像素点的颜色

```python
def get_all_pixel(file):
    """
    获取所有的像素点的颜色
    :param file:
    :return:
    """
    img = Image.open(file)
    width = img.size[0]
    height = img.size[1]
    ret = list()
    for x in range(width):
        for y in range(height):
            pixel = img.getpixel((x, y))
            print(f"{x},{y} -----> {pixel}")
            ret.append(dict(x=x, y=y, pixel=pixel))
    return ret
```

## 4、图片相似度

参考[Python计算图片之间的相似度](https://blog.csdn.net/qq_38641985/article/details/118304624)，代码就不贴了，在[github](https://github.com/rainbow-tan/learn-python/tree/main/learn-PIL)复制粘贴就能用，找一个适合自己的算法。

![image-20230419094147574](https://img2023.cnblogs.com/blog/1768648/202304/1768648-20230419100201745-1373059806.png)

## 5、去除背景

```python
import os.path

from rembg import remove


def remove_bg(src, des):
    src = os.path.abspath(src)
    des = os.path.abspath(des)
    if os.path.isfile(os.path.dirname(des)):
        raise Exception(f'目标文件夹是一个已存在的文件:{os.path.dirname(des)}')

    if not os.path.isdir(os.path.dirname(des)):
        os.makedirs(os.path.dirname(des))

    with open(src, 'rb') as i:
        with open(des, 'wb') as o:
            o.write(remove(i.read()))
    print(f"remove bg success, save to {des}")
    return des


def main():
    remove_bg('img/loading.png', 'img/loading_no_background.png')
    remove_bg('img/stop_flag.png', 'img/stop_flag_no_background.png')


if __name__ == '__main__':
    main()
```

## 6、转换图片模式为模式1

```python
import os.path

from PIL import Image


def convert(src, des):
    # 转为1模式 像素点不是1就是255 非黑即白
    src = os.path.abspath(src)
    des = os.path.abspath(des)
    if os.path.isfile(os.path.dirname(des)):
        raise Exception(f'目标文件夹是一个已存在的文件:{os.path.dirname(des)}')

    if not os.path.isdir(os.path.dirname(des)):
        os.makedirs(os.path.dirname(des))
    empire = Image.open(src)
    empire_1 = empire.convert('1')
    empire_1.save(des)
    print(f"convert success, save to {des}")
    return des


def main():
    convert('img/loading.png', 'img/1/loading_1.png')
    convert('img/loading_no_background.png', 'img/1/loading_no_background_1.png')

    convert('img/stop_flag.png', 'img/1/stop_flag_1.png')
    convert('img/stop_flag_no_background.png', 'img/1/stop_flag_no_background_1.png')


if __name__ == '__main__':
    main()
```

没啥人看，就不贴运行截图了，反正也就自己记录，后续直接CV大法好

[github](https://github.com/rainbow-tan/learn-python/tree/main/learn-PIL)