import pandas as pd
from pandas import DataFrame


def see_data(df):
    data = df.head()  # 查看前5行数据
    print(data)
    print("*" * 50)
    data = df.head(10)  # 查看前10行数据
    print(data)
    print("*" * 50)
    data = df.tail()  # 查看后5行数据
    print(data)
    print("*" * 50)
    data = df.tail(10)  # 查看后10行数据
    print(data)
    print("*" * 50)


def see_index_columns(df: DataFrame):
    index = df.index  # 查看索引
    print(index)
    columns = df.columns  # 查看列名
    print(columns)
    keys = df.keys()  # 查看列名
    print(keys)
    print(df.columns is df.keys())  # keys() 等同于 columns


def sort_by_index(df: DataFrame):
    # axis : {0 or 'index', 1 or 'columns'}, default 0
    print(df)
    print("*" * 50)
    ret = df.sort_index(axis='index', ascending=True)  # 按照X轴升序排序
    print(ret)
    print("*" * 50)
    ret = df.sort_index(axis='index', ascending=False)  # 按照X轴降序排序
    print(ret)


def sort_by_columns(df: DataFrame):
    # axis : {0 or 'index', 1 or 'columns'}, default 0
    print(df)
    print("*" * 50)
    ret = df.sort_index(axis='columns', ascending=True)  # 按照Y轴升序排序
    print(ret)
    print("*" * 50)
    ret = df.sort_index(axis='columns', ascending=False)  # 按照Y轴降序排序
    print(ret)


def main():
    df: DataFrame = pd.read_csv("csvs/Src-Affairs.csv")  # 返回DataFrame二维数组对象
    # see_data(df)

    # see_index_columns(df)
    df2 = df[:5]
    # sort_by_index(df2)
    sort_by_columns(df2)


if __name__ == '__main__':
    main()
