"""
将 VOC XML 转换为 COCO JSON

@Author: patrickcty
@filename: det_xml2json.py
"""

import os
import json
from xml.etree.ElementTree import parse



def convert_binary_to_coco(xml_file_dir, out_file, all_xmls=None, cls_name='zawu'):
    """
    将给定文件夹下的 xml 文件转换为一个 json 文件，类别标签视为二分类


    Parameters
    ----------
    xml_file_dir: xml 文件所在文件夹，文件夹下包含一个或多个 xml 文件
    out_file: 输出 json 文件绝对路径
    all_xmls: 可选, 从给定的列表中生成 json 文件
    cls_name: 类名

    Returns
    -------

    """
    if all_xmls is None:
        all_xmls = os.listdir(xml_file_dir)

    train_annotations = []
    train_images = []

    object_idx = 0
    for idx, xml_anno in enumerate(sorted(all_xmls)):
        if xml_anno.endswith('.xml'):
            info, anno, object_idx = parse_xml(os.path.join(xml_file_dir, xml_anno), idx, object_idx)
            train_annotations.extend(anno)
            train_images.append(info)

    coco_format_json_train = dict(
        images=train_images,
        annotations=train_annotations,
        categories=[{'id': 0, 'name': cls_name}])

    with open(out_file, 'w') as f:
        json.dump(coco_format_json_train, f, indent=4)
        print('Save coco json successfully in {}.'.format(out_file))


def convert_multi_to_coco(xml_file_dir, out_file, all_xmls=None):
    """
    将给定文件夹下的 xml 文件转换为一个 json 文件，类别按照原始的标签类别


    Parameters
    ----------
    xml_file_dir: xml 文件所在文件夹，文件夹下包含一个或多个 xml 文件
    out_file: 输出 json 文件绝对路径
    all_xmls: 可选, 从给定的列表中生成 json 文件

    Returns
    -------

    """
    if all_xmls is None:
        all_xmls = os.listdir(xml_file_dir)

    train_annotations = []
    train_images = []

    object_idx = 0
    all_categories = []
    for idx, xml_anno in enumerate(sorted(all_xmls)):
        if xml_anno.endswith('.xml'):
            info, anno, object_idx = parse_xml(os.path.join(xml_file_dir, xml_anno), idx, object_idx)
            # generate category id dynamically
            for a in anno:
                class_name = a['class_name']
                if class_name in all_categories:
                    a['category_id'] = all_categories.index(class_name)
                else:
                    a['category_id'] = len(all_categories)
                    all_categories.append(class_name)
                del a['class_name']
            train_annotations.extend(anno)
            train_images.append(info)

    coco_format_json_train = dict(
        images=train_images,
        annotations=train_annotations,
        categories=[{'id': i, 'name': n} for i, n in enumerate(sorted(all_categories))])

    with open(out_file, 'w') as f:
        json.dump(coco_format_json_train, f, indent=4)
        print('Save coco json successfully in {}.'.format(out_file))


def parse_xml(xml_file, idx, object_idx):
    """
    解析 xml 标注文件

    Parameters
    ----------
    xml_file: xml 文件所在绝对路径
    idx: index
    object_idx: bbox index

    Returns a tuple including:
        info dict
        a list that contains annotation dicts
        object index
    -------

    """
    doc = parse(xml_file)

    info = {
        'id': idx,
        'file_name': doc.findtext('filename'),
        'height': int(doc.findtext('size/height')),
        'width': int(doc.findtext('size/width'))
    }

    all_annos = []
    for item in doc.iterfind('object'):  # can deal with multiply bbox
        class_name = item.findtext('name')
        xmin = int(item.findtext('bndbox/xmin'))
        ymin = int(item.findtext('bndbox/ymin'))
        xmax = int(item.findtext('bndbox/xmax'))
        ymax = int(item.findtext('bndbox/ymax'))
        anno = {
            'image_id': idx,
            'id': object_idx,
            'category_id': 0,
            'bbox': [min(xmin, xmax), min(ymin, ymax), abs(xmax - xmin), abs(ymax - ymin)],
            'area': abs(xmax - xmin) * abs(ymax - ymin),
            'iscrowd': 0,
            'class_name': class_name
        }
        all_annos.append(anno)
        object_idx += 1

    return info, all_annos, object_idx
