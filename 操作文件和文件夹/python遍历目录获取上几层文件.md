## 功能

python遍历目录，获取上N层的文件，例如获取第一层，第二层，第三层的文件。

## 代码

path表示要遍历的文件夹路径

n表示要获取的层数 必须是大于0的整数 默认99 默认获取所有层数（应该层数不会大于99吧）

```python
import os


def traverse_folder(path: str, n: int = 99):
    path = os.path.abspath(path)
    assert os.path.isdir(path)
    assert n > 0
    all_files = []
    all_dirs = []
    for root, dirs, files in os.walk(path):
        for one_file in files:
            all_files.append(os.path.join(root, one_file))  # 所有文件
        for one_dir in dirs:
            all_dirs.append(os.path.join(root, one_dir))  # 所有文件夹

    path_split = path.split(os.sep)
    len_path_split = len(path_split)

    need_dir = []
    for d_name in all_dirs:
        dir_split = d_name.split(os.sep)
        dir_split_ = dir_split[len_path_split:]
        if len(dir_split_) <= n:
            need_dir.append(d_name)

    need_files = []
    for f_name in all_files:
        f_name_split = f_name.split(os.sep)
        f_name_split_ = f_name_split[len_path_split:]
        if len(f_name_split_) <= n:
            need_files.append(f_name)

    return need_dir, need_files


if __name__ == '__main__':
    d, f = traverse_folder(".", 3)
    for i in d:
        print(i)
    print("-" * 50)
    for i in f:
        print(i)

```

## 运行

目录结构

![image-20230512152113192](https://img2023.cnblogs.com/blog/1768648/202305/1768648-20230512152553287-1476152085.png)

运行结果

![image-20230512152147124](https://img2023.cnblogs.com/blog/1768648/202305/1768648-20230512152553846-99685693.png)
