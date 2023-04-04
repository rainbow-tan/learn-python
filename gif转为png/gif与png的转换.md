python gif与png的转换

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

![01](E:\MD文档\learn-python\gif转为png\01.gif)

![image-20230404153820660](C:\Users\dell\AppData\Roaming\Typora\typora-user-images\image-20230404153820660.png)

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

github