# -*- coding: utf-8 -*-
import cv2
import numpy as np


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


# 感知哈希算法(pHash)
def pHash(img, shape=(10, 10)):
    # 缩放32*32
    img = cv2.resize(img, (32, 32))  # , interpolation=cv2.INTER_CUBIC

    # 转换为灰度图
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 将灰度图转为浮点型，再进行dct变换
    dct = cv2.dct(np.float32(gray))
    # opencv实现的掩码操作
    dct_roi = dct[0:10, 0:10]

    hash = []
    avreage = np.mean(dct_roi)
    for i in range(dct_roi.shape[0]):
        for j in range(dct_roi.shape[1]):
            if dct_roi[i, j] > avreage:
                hash.append(1)
            else:
                hash.append(0)
    return hash


def main():
    n = cmpHash(pHash(cv2.imread('img/loading.png')), pHash(cv2.imread('img/stop_flag.png')))
    print('感知哈希算法哈希算法相似度：', n)

    n = cmpHash(pHash(cv2.imread('img/loading_1.png')), pHash(cv2.imread('img/stop_flag_1.png')))
    print('感知哈希算法哈希算法相似度：', n)

    n = cmpHash(pHash(cv2.imread('img/loading_no_background.png')),
                pHash(cv2.imread('img/stop_flag_no_background.png')))
    print('感知哈希算法哈希算法相似度：', n)  # 0.52

    n = cmpHash(pHash(cv2.imread('img/loading_no_background_1.png')),
                pHash(cv2.imread('img/stop_flag_no_background_1.png')))
    print('感知哈希算法哈希算法相似度：', n)


if __name__ == "__main__":
    main()
