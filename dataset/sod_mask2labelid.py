"""
将 mask (0 表示 background，255 表示 saliency)转换为类别 id（0 表示 background，1 表示 saliency）

@Author: patrickcty
@filename: sod_mask_2_labelid.py
"""

import os
import cv2


def convert(image, thres=0):
    # 数据集可能有非 255 的值，因此引入 thres 来增加容错率
    image[image > thres] = 1  

    return image


def convert_dir(input_dir, output_dir, thres=0):
    for img in os.listdir(input_dir):
        image = cv2.imread(os.path.join(input_dir, img), 0)
        image01 = convert(image, thres)
        cv2.imwrite(os.path.join(output_dir, img), image01)
