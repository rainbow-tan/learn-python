import chardet


def get_coding(filename):
    raw = open(filename, 'rb').read()
    detect = chardet.detect(raw)
    print(f"detect:{detect}")
    return detect['encoding']


def read_file(filename):
    encoding = get_coding(filename)
    with open(filename, 'r', encoding=encoding) as f:
        content = f.read()
        print(content)


def main():
    read_file("utf-8.txt")
    read_file("gbk.txt")
    read_file("a.txt")
    read_file("asdfa.txt")


if __name__ == '__main__':
    main()
