# -*- coding: utf-8 -*-
import cv2


# Hash值对比
def cmpHash(hash1, hash2, shape=(10, 10)):
    n = 0
    # hash长度不同则返回-1代表传参出错
    if len(hash1) != len(hash2):
        return -1
    # 遍历判断
    for i in range(len(hash1)):
        # 相等则n计数+1，n最终为相似度
        if hash1[i] == hash2[i]:
            n = n + 1
    return n / (shape[0] * shape[1])


# 均值哈希算法
def aHash(img, shape=(10, 10)):
    # 缩放为10*10
    img = cv2.resize(img, shape)
    # 转换为灰度图
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # s为像素和初值为0，hash_str为hash值初值为''
    s = 0
    hash_str = ''
    # 遍历累加求像素和
    for i in range(shape[0]):
        for j in range(shape[1]):
            s = s + gray[i, j]
    # 求平均灰度
    avg = s / 100
    # 灰度大于平均值为1相反为0生成图片的hash值
    for i in range(shape[0]):
        for j in range(shape[1]):
            if gray[i, j] > avg:
                hash_str = hash_str + '1'
            else:
                hash_str = hash_str + '0'
    return hash_str


def main():
    n = cmpHash(aHash(cv2.imread('img/loading.png')), aHash(cv2.imread('img/stop_flag.png')))
    print('均值哈希算法相似度：', n)

    n = cmpHash(aHash(cv2.imread('img/loading_1.png')), aHash(cv2.imread('img/stop_flag_1.png')))  # 0.63
    print('均值哈希算法相似度：', n)

    n = cmpHash(aHash(cv2.imread('img/loading_no_background.png')),
                aHash(cv2.imread('img/stop_flag_no_background.png')))
    print('均值哈希算法相似度：', n)

    n = cmpHash(aHash(cv2.imread('img/loading_no_background_1.png')),
                aHash(cv2.imread('img/stop_flag_no_background_1.png')))
    print('均值哈希算法相似度：', n)


if __name__ == "__main__":
    main()
