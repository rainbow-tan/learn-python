# -*- coding: utf-8 -*-
import cv2


# 计算单通道的直方图的相似值
def calculate(image1, image2):
    hist1 = cv2.calcHist([image1], [0], None, [256], [0.0, 255.0])
    hist2 = cv2.calcHist([image2], [0], None, [256], [0.0, 255.0])
    # 计算直方图的重合度
    degree = 0
    for i in range(len(hist1)):
        if hist1[i] != hist2[i]:
            degree = degree + (1 - abs(hist1[i] - hist2[i]) / max(hist1[i], hist2[i]))
        else:
            degree = degree + 1
    degree = degree / len(hist1)
    return degree


def main():
    n = calculate(cv2.imread('img/loading.png'), cv2.imread('img/stop_flag.png'))
    print('单通道的直方图算法相似度：', n)

    n = calculate(cv2.imread('img/loading_1.png'), cv2.imread('img/stop_flag_1.png'))
    print('单通道的直方图算法相似度：', n)

    n = calculate(cv2.imread('img/loading_no_background.png'),
                  cv2.imread('img/stop_flag_no_background.png'))
    print('单通道的直方图算法相似度：', n)  # 0.47

    n = calculate(cv2.imread('img/loading_no_background_1.png'),
                  cv2.imread('img/stop_flag_no_background_1.png'))
    print('单通道的直方图算法相似度：', n)


if __name__ == "__main__":
    main()
