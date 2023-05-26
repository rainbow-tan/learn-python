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
