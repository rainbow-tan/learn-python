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
