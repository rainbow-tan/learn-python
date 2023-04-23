pandas的简单使用-1-简单了解一下潘大师

学习链接[Pandas中文网](https://pypandas.cn/docs/getting_started/overview.html)，非常好的文档！

## 前言

**Pandas** 是 Python的核心数据分析支持库，提供了快速、灵活、明确的数据结构，旨在简单、直观地处理关系型、标记型数据。

Pandas 的目标是成为 Python 数据分析实践与实战的必备高级工具，其长远目标是成为最强大、最灵活、可以支持任何语言的开源数据分析工具。经过多年不懈的努力，Pandas 离这个目标已经越来越近了。

## 数据结构

| 维数 | 名称      | 描述                               |
| ---- | --------- | ---------------------------------- |
| 1    | Series    | 带标签的一维同构数组               |
| 2    | DataFrame | 带标签的，大小可变的，二维异构表格 |

了解了pandas的数据结构，就比较好理解pandas的使用方法和API了，我们可以简单理解为：

①Series是一维数组，里面的元素类型一致

②DataFrame是二维数组，里面的元素类型可以不一致

## 获取学习数据

想要学习pandas的常用函数，必须构造一些假数据进行测试，但是自己写假数据费力费时的。

我的做法是直接通过读取csv文件，获取里面的数据作为测试数据

可以通过[船长博客](https://www.cnblogs.com/v5captain/p/14156329.html)的链接获取学习数据，使用csv文件中的数据作为学习数据，相当便利，不用自己伪造数据。

这里下载的是https://vincentarelbundock.github.io/Rdatasets/datasets.html中的 Affairs来进行测试

![image-20230403150917892](https://img2023.cnblogs.com/blog/1768648/202304/1768648-20230413162326984-2046442760.png)

[github](https://github.com/rainbow-tan/learn-python/tree/main/learn-pandas)

