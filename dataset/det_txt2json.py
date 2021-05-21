"""
将 txt 转换为 COCO JSON
txt 格式为：文件名 x01,y01,x02,y02,c0 x11,y11,x12,y12,c1 ...

@Author: patrickcty
@filename: det_xml2json.py
"""

import os
import cv2
import json


def convert_txt_to_coco_dir(txt_dir, out_dir=None, class_name=None):
    """
    将 txt 文件夹中所有 txt 文件转换为 json
    """
    if out_dir is None:
        out_dir = txt_dir

    for txt_file in os.listdir(out_dir):
        if txt_file.endswith('.txt'):
            convert_txt_to_coco(os.path.join(txt_dir, txt_file),
                                os.path.join(out_dir, txt_file.replace('.txt', '.json')),
                                class_name)


def convert_txt_to_coco(txt_file, out_file, class_name=None):
    """
    将 det_xml2txt.py 中生成的 txt 文件转换为 COCO 格式 json 文件

    Parameters
    ----------
    txt_file: 输入 txt 文件绝对路径
    out_file: 输出 json 文件绝对路径
    class_name: 可选，类名，默认类名为 txt 文件名
    """
    if class_name is None:
        class_name = os.path.basename(txt_file).replace('.txt', '')

    all_annotations = []
    all_images = []
    object_idx = 0
    with open(txt_file, 'r') as f:
        for idx, anno in enumerate(f):
            image_path, bboxes = parse_txt_line(anno)
            img = cv2.imread(image_path)
            info = {
                'id': idx,
                'file_name': image_path,
                'height': img.shape[0],
                'width': img.shape[1]
            }

            all_annos = []
            for item in bboxes:  # can deal with multiply bbox
                anno = {
                    'image_id': idx,
                    'id': object_idx,
                    'category_id': 0,
                    'bbox': [item[0], item[1], item[2] - item[0], item[3] - item[1]],
                    'area': item[2] * item[3],
                    'iscrowd': 0,
                    'class_name': class_name
                }
                all_annos.append(anno)
                object_idx += 1

            all_annotations.extend(all_annos)
            all_images.append(info)

    coco_format_json_train = dict(
        images=all_images,
        annotations=all_annotations,
        categories=[{'id': 0, 'name': class_name}])

    with open(out_file, 'w') as f:
        json.dump(coco_format_json_train, f, indent=4)
        print('Save coco json successfully in {}.'.format(out_file))


def parse_txt_line(annotation):
    """
    解析 txt 每一行
    """
    line = annotation.split()
    image_path = line[0]

    # bbox [xmin, ymin, xmax, ymax, class_id]
    bboxes = [list(map(int, box.split(','))) for box in line[1:]]
    # COCO api 中 bbox [xmin, ymin, h, w, class_id]
    # 后续进行转换

    return image_path, bboxes
