"""
将 txt 转换为 COCO JSON
txt 格式为：文件名 x01,y01,x02,y02,c0 x11,y11,x12,y12,c1 ...

@Author: patrickcty
@filename: det_visualize_from_txt.py
"""

import os
import cv2
import numpy as np
from dataset.make_dir_if_not_exist import make_dir_if_not_exists

def visualize_from_txt(txt_file, target_dir):
    """
    可视化 txt 标注文件中的图像
    """
    make_dir_if_not_exists(target_dir)
    with open(txt_file, 'r') as f:
        for line in f:
            total = line.split()
            filepath = total[0]
            anns = total[1:]
            anns = list(map(str_ann_to_list, anns))

            img = cv2.imread(filepath)
            img = draw_bbox(img, anns)

            basename = os.path.basename(filepath)
            cv2.imwrite(os.path.join(target_dir, basename), img)
            print('Save {} successfully.'.format(basename))


def str_ann_to_list(strann):
    """
    将 "x1,y1,x2,y2,c" 形式转换成 [x1,y1,x2,y2,c]
    """
    return list(map(int, strann.split(',')))


def draw_bbox(image, bboxes):
    """
    bboxes: 一个 list，其中每个元素都是 [x_min, y_min, x_max, y_max, cls_id]
    """

    image_h, image_w, _ = image.shape

    for i, bbox in enumerate(bboxes):
        coor = np.array(bbox[:4], dtype=np.int32)
        bbox_color = [0, 0, 255]
        bbox_thick = int(0.6 * (image_h + image_w) / 600)
        c1, c2 = (coor[0], coor[1]), (coor[2], coor[3])
        cv2.rectangle(image, c1, c2, bbox_color, bbox_thick)

    return image