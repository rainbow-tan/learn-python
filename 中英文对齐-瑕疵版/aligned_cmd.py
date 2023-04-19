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
