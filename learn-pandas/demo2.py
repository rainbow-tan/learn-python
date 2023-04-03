import pandas as pd
from pandas import DataFrame, RangeIndex


def choose_one_row(df: DataFrame):
    data = df.loc[RangeIndex(1)]  # 默认是RangeIndex类型的索引,所以可以这么选择第1行 但不会降维 不会从二维数组降到一维数组
    print(data)
    print("*" * 50)
    data = df.loc[0]  # 默认是RangeIndex类型的索引,所以可以这么选择第1行 会降维 直接从二维数组降到一维数组
    print(data)
    print("*" * 50)

    data = df.loc[RangeIndex(start=5, stop=6)]  # 默认是RangeIndex类型的索引,所以可以这么选择第5行 但不会降维 不会从二维数组降到一维数组
    print(data)
    print("*" * 50)
    data = df.loc[5]  # 默认是RangeIndex类型的索引,所以可以这么选择第5行 会降维 直接从二维数组降到一维数组
    print(data)
    print("*" * 50)


def choose_rows(df: DataFrame):
    print(df)
    print("*" * 50)
    data = df[1:3]  # 从第1行截取到第3行,不包括第3行, 和python的切片一致
    print(data)
    print("*" * 50)
    data = df[1:]  # 从第1行截取到尾, 和python的切片一致
    print(data)
    print("*" * 50)
    data = df[:5]  # 从头截取到第5行,不包括第5行, 和python的切片一致
    print(data)
    print("*" * 50)
    data = df[:]  # 截取所有数据, 和python的切片一致
    print(data)


def choose_one_column(df: DataFrame):
    gender = df['gender']  # 类似字典形式选择某列
    print(gender)
    print("*" * 50)
    other = df.gender  # 类似属性形式选择某列
    print(other)
    print("*" * 50)
    print(gender is other)  # df['gender']等效于df.gender


def choose_columns(df: DataFrame):
    print(df)
    print("*" * 50)
    data = df.loc[:, ['affairs', 'gender', 'education']]  # loc[:,] 形式 冒号表示所有行
    print(data)


def choose_rows_columns(df: DataFrame):
    print(df)
    print("*" * 50)
    data = df.loc[[1, 2, 4], ['affairs', 'gender']]
    print(data)
    print("*" * 50)
    data = df.loc[1:5, ['affairs', 'education']]
    print(data)
    print("*" * 50)
    data = df.loc[:, ['affairs', 'gender', 'education']]
    print(data)
    print("*" * 50)
    data = df.loc[6:, ['affairs', 'gender', 'education']]
    print(data)
    print("*" * 50)
    data = df.loc[:5, ['affairs', 'gender', 'education']]
    print(data)
    print("*" * 50)


def choose_rows_columns2(df: DataFrame):
    print(df)
    print("*" * 50)
    data = df.iloc[[1, 2, 4], [1, 2, 3]]
    print(data)
    print("*" * 50)
    data = df.iloc[1:5, 2:]
    print(data)
    print("*" * 50)
    data = df.iloc[:, :5]
    print(data)
    print("*" * 50)
    data = df.iloc[6:, 2:5]
    print(data)
    print("*" * 50)
    data = df.iloc[:5, :]
    print(data)
    print("*" * 50)


def choose_value(df: DataFrame):
    print(df)
    print("*" * 50)
    data = df.at[1, 'gender']  # 获取第1行, 第gender列的值
    print(data)
    print("*" * 50)
    data = df.at[5, 'education']  # 获取第5行, 第education列的值
    print(data)
    print("*" * 50)

    data = df.iat[5, 3]  # 获取第5行第3列的值
    print(data)
    print("*" * 50)
    data = df.iat[3, 8]  # 获取第3行第8列的值
    print(data)
    print("*" * 50)


def main():
    df: DataFrame = pd.read_csv("csvs/Src-Affairs.csv")  # 返回DataFrame二维数组对象
    # choose_one_column(df)
    df2 = df[:10]
    # choose_rows(df2)
    # choose_one_row(df2)
    # choose_columns(df2)
    # choose_rows_columns(df2)
    choose_value(df2)


if __name__ == '__main__':
    main()
