import pandas as pd
from pandas import DataFrame, Series


def mean(df: DataFrame):
    print(df.mean())  # 所有列的平均数
    print('*' * 50)
    df2: DataFrame = df.loc[:, ['affairs', 'education', 'rating']]
    mead = df2.mean()  # 指定列的平均数
    print(mead)

    print(df2)
    print(df2.mean(1))  # 按行获取平均值
    print(df2.mean(0))  # 按列获取平均数


def sum_(df: DataFrame):
    df2: DataFrame = df.loc[:, ['affairs', 'education', 'rating']]
    print(df2)
    mead = df2.sum()  # 指定列的总和
    print(mead)
    print(df2.sum(1))  # 按行获取总和
    print(df2.sum(0))  # 按列获取总和


def func(x: Series):
    print(f"x:{x}")
    print(f"type x:{type(x)}")
    m = x.max()  # 最大值
    n = x.min()  # 最小值
    print(f"最大值-最小值为:{m}-{n}={m - n}")


def call_fun(df: DataFrame):
    # 调用自定义函数
    df2: DataFrame = df.loc[:, ['affairs', 'education', 'rating']]
    print(df2)
    df2.apply(func=func)




def main():
    df: DataFrame = pd.read_csv("csvs/Src-Affairs.csv")  # 返回DataFrame二维数组对象
    df2 = df[:10]
    print(df2)
    print('*' * 50)

    # mean(df2)
    # sum_(df2)
    call_fun(df2)




if __name__ == '__main__':
    main()
