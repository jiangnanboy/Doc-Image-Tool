import cv2
import numpy as np

def sauvola_threshold(image, window_size=15, k=0.2, r=128):
    # 将图像转换为灰度图
    if len(image.shape) > 2:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image

    # 计算图像的平均值和标准差
    mean = cv2.blur(gray, (window_size, window_size))
    mean_square = cv2.blur(gray * gray, (window_size, window_size))
    std = np.sqrt(mean_square - mean * mean)

    # 计算阈值
    threshold = mean * (1 + k * (std / r - 1))

    # 阈值化图像
    binary = np.zeros_like(gray)
    binary[gray > threshold] = 255

    return binary


