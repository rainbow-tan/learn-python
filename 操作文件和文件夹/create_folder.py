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
