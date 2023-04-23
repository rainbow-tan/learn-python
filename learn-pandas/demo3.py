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

    data = df[df['gender'] == 'male']  # 选择gender列等于male的行
    print(data)
    print('*' * 50)

    data = df[df['education'].isin([12, 14, 18])]  # 选择education的值在[12,14,18]的行
    print(data)

    data = df[filter_fun2(df['education'])]  # 自定义函数,选择education是偶数的行
    print(data)

    data = df[filter_fun(df['gender'])]  # 自定义函数,选择gender是male的行
    print(data)


def add_one_column(df: DataFrame):
    df = df.copy()
    # 因为df是截取出来的, 因此需要copy一份 认为是一个新的df 不然就无法添加新列 会报警告
    # A value is trying to be set on a copy of a slice from a DataFrame.
    new = list(range(10))
    df['new'] = new  # 添加新的一列
    print(df)


def assign_values_by_index(df: DataFrame):
    df = df.copy()
    df.at[2, 'affairs'] = 100  # 按位置赋值
    df.iat[5, 1] = 455  # 按位置赋值
    print(df)


def fun(a):
    return a % 2 == 0


def assign_velues_by_where(df: DataFrame):
    df = df.loc[:, ["Unnamed: 0", "affairs"]]
    print(df)
    print('*' * 50)
    df = df.copy()
    df[df == 0] = 10086  # 等于0的值变成10086
    print(df)

    print('*' * 50)
    df[fun] = 1414  # 传入函数, 偶数的值变成1414
    print(df)


def main():
    df: DataFrame = pd.read_csv("csvs/Src-Affairs.csv")  # 返回DataFrame二维数组对象
    df2 = df[:10]
    print(df2)
    print('*' * 50)
    # choose_by_bool(df2)
    # add_one_column(df2)
    # assign_values_by_index(df2)

    assign_velues_by_where(df2)


if __name__ == '__main__':
    main()
