python 创建、拷贝、移动、删除、遍历文件和文件夹

## 1、创建文件夹

```python
import os


def create_folder(folder: str):
    folder = os.path.abspath(folder)
    if not os.path.exists(folder):
        try:
            os.makedirs(folder)
            print(f"创建了文件夹:{folder}")
        except FileExistsError:
            print(f"文件夹已存在, 无需创建:{folder}")
        except Exception as e:
            msg = f"创建文件夹失败, folder:{folder}, e:{e}"
            print(msg)


def main():
    create_folder('A')


if __name__ == '__main__':
    main()
```

## 2、拷贝文件夹

```python
import os.path
import shutil


def copy_folder(src: str, target: str):
    # 如果target是已存在的目录 则抛出FileExistsError异常
    # 如果target是已存在的文件 则抛出FileExistsError异常
    # 如果target不存在, 则拷贝
    src = os.path.abspath(src)
    target = os.path.abspath(target)
    try:
        shutil.copytree(src, target)
        print(f"拷贝文件夹成功, src:{src}, target:{target}")
    except FileExistsError as e:
        print(f"由于target已存在, 导致拷贝文件夹失败, src:{src}, target:{target}, e:{e}")
    except Exception as e:
        print(f"拷贝文件夹失败, src:{src}, target:{target}, e:{e}")


def main():
    copy_folder("A", 'C')


if __name__ == '__main__':
    main()
```

## 3、移动文件夹

```python
import os.path
import shutil


def mv_folder(src: str, target: str):
    # 如果target是已存在的目录, 则移动src到该target目录下 target中出现同名的src文件夹
    # 如果target是已存在的文件 则抛出FileExistsError异常
    # 如果target不存在, 则重命名src为target 相当于移动
    src = os.path.abspath(src)
    target = os.path.abspath(target)
    try:
        shutil.move(src, target)
        print(f"移动文件夹成功, src:{src}, target:{target}")
    except FileExistsError as e:
        print(f"由于target已存在, 导致移动文件夹失败, src:{src}, target:{target}, e:{e}")
    except Exception as e:
        print(f"移动文件夹失败, src:{src}, target:{target}, e:{e}")


def main():
    mv_folder("A", 'B')


if __name__ == '__main__':
    main()
```

## 4、删除文件夹

```python
import os.path
import shutil


def rm_folder(folder: str):
    folder = os.path.abspath(folder)
    if os.path.isdir(folder):
        try:
            shutil.rmtree(folder)
            print(f"删除文件夹成功, folder:{folder}")
        except FileNotFoundError as e:
            print(f"文件夹不存在, 无需删除, folder:{folder}, e:{e}")
        except Exception as e:
            print(f"删除文件夹失败, folder:{folder}, e:{e}")


def main():
    rm_folder("A")


if __name__ == '__main__':
    main()
```

## 5、拷贝文件

```python
import os
import shutil


def copy_file(src: str, target: str):
    # 如果target是一个已存在的文件, 则覆盖文件内容
    # 如果target是一个已存在的文件夹, 则拷贝src到文件夹中, target文件夹中多一个src文件 如果target中存在同名src文件 则覆盖
    src = os.path.abspath(src)
    target = os.path.abspath(target)
    if os.path.isfile(src):
        try:
            shutil.copy2(src, target)
            print(f"拷贝文件成功, src:{src}, target:{target}")
        except Exception as e:
            print(f"拷贝文件失败, src:{src}, target:{target}, e:{e}")


def main():
    copy_file('a.txt', 'a.txt')


if __name__ == '__main__':
    main()
```

## 6、移动文件

```python
import os.path
import shutil


def mv_file(src: str, target: str):
    # 如果target是一个已存在的文件, 则覆盖文件内容
    # 如果target是一个已存在的文件夹, 则移动src到文件夹中, target文件中多一个src文件 如果target中存在同名src文件 则覆盖
    src = os.path.abspath(src)
    target = os.path.abspath(target)
    if os.path.isfile(src):
        try:
            shutil.move(src, target)
            print(f"移动文件成功, src:{src}, target:{target}")
        except FileExistsError as e:
            print(f"由于target已存在, 导致移动文件失败, src:{src}, target:{target}, e:{e}")
        except Exception as e:
            print(f"移动文件失败, src:{src}, target:{target}, e:{e}")


def main():
    mv_file('a.txt', 'b.txt')


if __name__ == '__main__':
    main()
```

## 7、删除文件

```python
import os.path


def rm_file(filename: str):
    filename = os.path.abspath(filename)
    if os.path.isfile(filename):
        try:
            os.remove(filename)
            print(f"删除文件成功, filename:{filename}")
        except FileNotFoundError:
            print(f"无需删除不存在的文件, filename:{filename}")
        except Exception as e:
            print(f"删除文件失败, filename:{filename}, e:{e}")


def main():
    rm_file("a.txt")


if __name__ == '__main__':
    main()
```

## 8、遍历文件夹

### 功能

python遍历目录，获取上N层的文件，例如获取第一层，第二层，第三层的文件。

### 代码

path表示要遍历的文件夹路径

n表示要获取的层数 必须是大于0的整数 默认9999 默认获取所有层数（应该层数不会大于9999吧）

```python
import os


def traverse_folder(path: str, n: int = 9999):
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
    d, f = traverse_folder("..", 3)
    for i in d:
        print(i)
    print("-" * 50)
    for i in f:
        print(i)

```

### 运行

目录结构

![image-20230512152113192](https://img2023.cnblogs.com/blog/1768648/202305/1768648-20230512152553287-1476152085.png)

运行结果

![image-20230512152147124](https://img2023.cnblogs.com/blog/1768648/202305/1768648-20230512152553846-99685693.png)
