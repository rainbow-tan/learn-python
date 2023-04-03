import pandas as pd
from pandas import DataFrame


def filter_fun2(value):
    return value % 2 == 0


def filter_fun(value):
    return value == 'male'


def choose_by_bool(df: DataFrame):
    data = df[df['education'] > 15]  # 选择education列大于15的行
    print(data)
    print('*' * 50)

    data = df[df['gender'] == 'male']  # 现在gender列等于male的行
    print(data)
    print('*' * 50)

    data = df[df['education'].isin([12, 14, 18])]  # 现在education的值在[12,14,18]的行
    print(data)

    data = df[filter_fun2(df['education'])]  # 自定义函数,选择education是偶数的行
    print(data)

    data = df[filter_fun(df['gender'])]  # 自定义函数,选择gender是male的行
    print(data)


def main():
    df: DataFrame = pd.read_csv("csvs/Src-Affairs.csv")  # 返回DataFrame二维数组对象
    df2 = df[:10]
    print(df2)
    print('*' * 50)
    choose_by_bool(df2)


if __name__ == '__main__':
    main()
