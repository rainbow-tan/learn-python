python 中英文对齐

## 理论基础

在window平台的cmd中，默认中文显示占两个字符，英文显示占一个字符，要实现中英文对齐，只需要统一字符串的长度，不足的补充空格，然后打印即可，这样就看起来对齐了。

但Python中`len()函数`获取汉字也是一个字节长度。因此，字符串的长度不再通过`len()`函数自动获取，而是我们判断是汉字就占两个字节，是英文就占一个字节，然后自己统计出一个长度来。

## 自定义字符串长度

```python
def get_len(string: str):
    """
    获取字符串的长度, 中文是两个字符, 英文是一个字符
    :param string:
    :return:
    """
    length = 0
    for ch in string:
        if '\u4e00' <= ch <= '\u9fa5':  # 是中文字符
            length += 2
        else:
            length += 1
    return length
```

## 统一长度字符串

```python
def aligned(string: str, length=10, align_type='<') -> str:
    """
    :param string: 要对齐的字符串
    :param length: 要对齐的长度
    :param align_type: 要对齐的类型
    :return: 对齐后的字符串 用空格补充空白
    """
    len_s = get_len(string)
    if len_s < length:
        if align_type == '>':
            show = ' ' * (length - len_s) + string
        elif align_type == '<':
            show = string + ' ' * (length - len_s)
        else:
            left = int((length - len_s) / 2)
            show = ' ' * left + string + ' ' * (length - left - len_s)

    else:
        raise RuntimeError(f"给定的length应该大于string的长度, {length}<->{string}({len(string)})")
    return show
```

## 中英文对齐

```python
def get_len(string: str):
    """
    获取字符串的长度, 中文是两个字符, 英文是一个字符
    :param string:
    :return:
    """
    length = 0
    for ch in string:
        if '\u4e00' <= ch <= '\u9fa5':  # 是中文字符
            length += 2
        else:
            length += 1
    return length


def aligned(string: str, length=10, align_type='<') -> str:
    """
    :param string: 要对齐的字符串
    :param length: 要对齐的长度
    :param align_type: 要对齐的类型
    :return: 对齐后的字符串 用空格补充空白
    """
    len_s = get_len(string)
    if len_s < length:
        if align_type == '>':
            show = ' ' * (length - len_s) + string
        elif align_type == '<':
            show = string + ' ' * (length - len_s)
        else:
            left = int((length - len_s) / 2)
            show = ' ' * left + string + ' ' * (length - left - len_s)

    else:
        raise RuntimeError(f"给定的length应该大于string的长度, {length}<->{string}({len(string)})")
    return show


if __name__ == '__main__':
    aaaa = 50
    data = [['ip', 'core', 'disk', 'memory'],
            ['172.17.11.1', '128', '12349', '50G'],
            ['172.17.11.1', '2654', '1234984', '150G'],
            ['172.17.11.1', '128', '1234933433484', '10240G']]
    for i in data:
        s = aligned(i[0], aaaa) + aligned(i[1], aaaa) + aligned(i[2], aaaa) + aligned(i[3], aaaa)
        print(s)
    print('\n\n')
    data = [['这是IP', '这是核心数core', '这是磁盘disk', '这是内存memory'],
            ['172.17.11.1', '128', '12349', '50G'],
            ['172.17.11.1', '2654', '1234984', '150G'],
            ['172.17.11.1', '128', '1234933433484', '10240G']]
    for i in data:
        s = aligned(i[0], aaaa) + aligned(i[1], aaaa) + aligned(i[2], aaaa) + aligned(i[3], aaaa)
        print(s)

```

运行

![image-20230419155439635](https://img2023.cnblogs.com/blog/1768648/202304/1768648-20230419160756716-985158863.png)

## 在pycharm中对不齐的情况解决

![image-20230419155624823](https://img2023.cnblogs.com/blog/1768648/202304/1768648-20230419160757192-472213691.png)

想到个笨办法，就是看缩进，少了就加一个缩进，少了加一个缩进

上面看起来就是第2列多了一个缩进，就少缩进一个

因此添加一个参数，指定添加空格的数量

```python
def get_len(string: str):
    """
    获取字符串的长度, 中文是两个字符, 英文是一个字符
    :param string:
    :return:
    """
    length = 0
    for ch in string:
        if '\u4e00' <= ch <= '\u9fa5':  # 是中文字符
            length += 2
        else:
            length += 1
    return length


def aligned(string: str, length=10, align_type='<', indentation=0) -> str:
    """
    :param indentation: 笨办法, 添加一个缩进, 要缩进几个字符就去掉添加几个空格
    :param string: 要对齐的字符串
    :param length: 要对齐的长度
    :param align_type: 要对齐的类型
    :return: 对齐后的字符串 用空格补充空白
    """
    len_s = get_len(string)
    if len_s < length:
        if align_type == '>':
            show = ' ' * ((length - len_s) - indentation) + string
        elif align_type == '<':
            show = string + ' ' * ((length - len_s) - indentation)
        else:
            left = int((length - len_s) / 2)
            show = ' ' * left + string + ' ' * ((length - left - len_s) - indentation)
    else:
        raise RuntimeError(f"给定的length应该大于string的长度, {length}<->{string}({len(string)})")
    return show


if __name__ == '__main__':
    aaaa = 50
    data = [['ip', 'core', 'disk', 'memory'],
            ['172.17.11.1', '128', '12349', '50G'],
            ['172.17.11.1', '2654', '1234984', '150G'],
            ['172.17.11.1', '128', '1234933433484', '10240G']]
    for i in data:
        s = aligned(i[0], aaaa) + aligned(i[1], aaaa) + aligned(i[2], aaaa) + aligned(i[3], aaaa)
        print(s)
    print('\n\n')
    data = [['这是IP', '这是核心数core', '这是磁盘disk', '这是内存memory'],
            ['172.17.11.1', '128', '12349', '50G'],
            ['172.17.11.1', '2654', '1234984', '150G'],
            ['172.17.11.1', '128', '1234933433484', '10240G']]
    for index, i in enumerate(data):
        if index == 0:
            s = aligned(i[0], aaaa) + aligned(i[1], aaaa) + aligned(i[2], aaaa) + aligned(i[3], aaaa)
        else:
            s = aligned(i[0], aaaa, indentation=1) + aligned(i[1], aaaa, indentation=2) + \
                aligned(i[2], aaaa, indentation=1) + aligned(i[3], aaaa, indentation=1)
        print(s)
```

运行

![image-20230419160708880](https://img2023.cnblogs.com/blog/1768648/202304/1768648-20230419160757589-430678203.png)

## 参考链接

[参考链接一](https://blog.csdn.net/JayRoxis/article/details/72669952) 

[参考链接二](https://blog.csdn.net/qq_37608398/article/details/90637409)