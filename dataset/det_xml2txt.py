"""将 xml 文件按照类别生成多个标注文件，每个文件都是 txt 文件，包含该类别的框信息

@Author: patrickcty (Tianyang Cheng)
@Filename: separate_classes_from_xml.py
"""

import os
import xml.etree.ElementTree as ET
from collections import defaultdict
from .make_dir_if_not_exist import make_dir_if_not_exists


def generate_txt(xml_dir, target_dir, image_path):
    """
    将 xml 文件按照类别生成多个标注文件，每个文件都是 txt 文件

    :param xml_dir      xml 标注所在文件夹
    :param target_dir   生成 txt 文件所在文件夹
    :param image_path   xml 对应图像所在文件夹
    """
    xml_dict = xml_to_txt_sep(xml_dir, image_path)
    make_dir_if_not_exists(target_dir)
    for k, v in xml_dict.items():
        with open(os.path.join(target_dir, '{}.txt'.format(k)), 'w') as f:
            for r in v:
                f.writelines(r + '\n')
        print('Generate {}.txt successfully.'.format(k))


def xml_to_txt_sep(path, image_path):
    """
    处理给定目录下所有 xml 文件，
    其中单个 xml 中的各个类别标注分别保存到一个 list 中
    每个 list 由若干个字符串组成，每个字符串表示单个图像的标注信息
    标注信息格式为 xmin,ymin,xmax,ymax,class_id
    """
    xml_dict = defaultdict(list)
    for file in os.scandir(path):
        if file.is_file() and file.name.endswith('.xml'):
            xml_file = os.path.join(path, file.name)
            tree = ET.parse(xml_file)
            root = tree.getroot()
            filename = root.find('filename').text
            row_dict = defaultdict(str)
            for member in root.findall('object'):
                classname = member[0].text
                if row_dict[classname] == '':
                    row_dict[classname] = os.path.join(image_path, filename)
                value = (member[4][0].text,
                         member[4][1].text,
                         member[4][2].text,
                         member[4][3].text,
                         '0')
                row_dict[classname] = row_dict[classname] + ' ' + ','.join(value)

            for k, v in row_dict.items():
                xml_dict[k].append(v)

    return xml_dict


def xml_to_txt(path, target_dir, image_path):
    """
    将路径下的 xml 文件生成一个 txt 文件，各个框类别无关
    """
    xml_list = []
    for file in os.scandir(path):
        if file.is_file() and file.name.endswith('.xml'):
            xml_file = os.path.join(path, file.name)
            tree = ET.parse(xml_file)
            root = tree.getroot()
            row = os.path.join(image_path, root.find('filename').text)
            for member in root.findall('object'):
                value = (member[4][0].text,
                         member[4][1].text,
                         member[4][2].text,
                         member[4][3].text,
                         '0')
                row = row + ' ' + ','.join(value)

            xml_list.append(row)

    make_dir_if_not_exists(target_dir)

    with open(os.path.join(target_dir, 'label.txt'), 'w') as f:
        for r in xml_list:
            f.writelines(r + '\n')
    print('Generate label.txt successfully.')

    return xml_list