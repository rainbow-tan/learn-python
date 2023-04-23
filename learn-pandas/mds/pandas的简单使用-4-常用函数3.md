pandas的简单使用-4-常用函数3

记录一下潘大师的常用的函数和实现的功能

## 常用函数

### 平均数

```
print(df.mean())  # 所有列的平均数
print('*' * 50)
df2 = df.loc[:, ['affairs', 'education', 'rating']]
mead = df2.mean()  # 指定列的平均数
print(mead)
print(df2.mean(1))  # 按行获取平均值
print(df2.mean(0))  # 按列获取平均数
```

### 求和

```
mead = df2.sum()  # 指定列的总和
print(mead)
print(df2.sum(1))  # 按行获取总和
print(df2.sum(0))  # 按列获取总和
```

### 调用自定义函数处理某一列

```
df2.apply(func=func)
```

