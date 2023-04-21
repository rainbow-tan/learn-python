# -*- coding: utf-8 -*-
import cv2


# 通过得到RGB每个通道的直方图来计算相似度
def classify_hist_with_split(image1, image2, size=(256, 256)):
    # 将图像resize后，分离为RGB三个通道，再计算每个通道的相似值
    image1 = cv2.resize(image1, size)
    image2 = cv2.resize(image2, size)
    sub_image1 = cv2.split(image1)
    sub_image2 = cv2.split(image2)
    sub_data = 0
    for im1, im2 in zip(sub_image1, sub_image2):
        sub_data += calculate(im1, im2)
    sub_data = sub_data / 3
    return sub_data


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
    n = classify_hist_with_split(cv2.imread('img/loading.png'), cv2.imread('img/stop_flag.png'))
    print('三直方图算法相似度：', n)

    n = classify_hist_with_split(cv2.imread('img/loading_1.png'), cv2.imread('img/stop_flag_1.png'))
    print('三直方图算法相似度：', n)

    n = classify_hist_with_split(cv2.imread('img/loading_no_background.png'),
                                 cv2.imread('img/stop_flag_no_background.png'))
    print('三直方图算法相似度：', n)  # 0.55

    n = classify_hist_with_split(cv2.imread('img/loading_no_background_1.png'),
                                 cv2.imread('img/stop_flag_no_background_1.png'))
    print('三直方图算法相似度：', n)


if __name__ == "__main__":
    main()
