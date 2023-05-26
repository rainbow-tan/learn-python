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
