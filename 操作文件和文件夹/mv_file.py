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
