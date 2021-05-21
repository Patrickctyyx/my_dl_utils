"""
按照一定比例划分数据集，为了节省空间，没有将训练图像拷贝到新文件夹

@Author: patrickcty (Tianyang Cheng)
@Filename: random_split_dataset.py
"""
import os
import random
import shutil
from .make_dir_if_not_exist import make_dir_if_not_exists


SPLIT_RATES = 0.7


def random_split(data_dir, gt_dir, target_dir, rates=SPLIT_RATES):
    """按照比例划分数据集

    :param data_dir    数据所在文件夹
    :param gt_dir      gt 所在文件夹
    :param target_dir  目标文件夹
    :param rates       训练集划分比例
    """
    all_data = [elem for elem in os.listdir(data_dir) if elem.endswith(('.jpg', '.png', '.bmp'))]
    random.shuffle(all_data)

    train_num = int(len(all_data) * rates)
    train_data = all_data[:train_num]
    val_data = all_data[train_num:]
    move_to_dir(train_data, data_dir, gt_dir, os.path.join(target_dir, 'train'))
    move_to_dir(val_data, data_dir, gt_dir, os.path.join(target_dir, 'val'))


def move_to_dir(all_data, data_dir, gt_dir, target_dir):
    # out_img_dir = os.path.join(target_dir, 'images')
    out_gt_dir = os.path.join(target_dir, 'gt')
    # make_dir_if_not_exists(out_img_dir)
    make_dir_if_not_exists(out_gt_dir)

    for elem in all_data:
        # shutil.copy(os.path.join(data_dir, elem), os.path.join(out_img_dir, elem))
        basename = elem.split('.')[0] + '.xml'
        shutil.copy(os.path.join(gt_dir, basename), os.path.join(out_gt_dir, basename))
        print("Copy {} successfully.".format(elem))
