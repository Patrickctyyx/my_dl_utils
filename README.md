# 深度学习常用代码片段

很多时候为了方便会写一些脚本来批处理，但是经常没有保存或者不知道放到哪里去了，后面再用的时候又得再写一次。干脆开个仓库把这些保存下来，以后需要的时候方便查阅。

## 目录

- dataset
    - [det_xml2json.py](dataset/det_xml2json.py)：将 VOC XML 转换为 COCO JSON
    - [det_txt2json.py](dataset/det_txt2json.py)：将 TXT 转换为 COCO JSON
    - [det_xml2txt.py](dataset/det_txt2json.py)：将 VOC XML 转换为 TXT
    - [sod_mask2labelid.py](dataset/sod_mask2labelid.py)：将 mask (0 表示 background，255 表示 saliency)转换为类别 id（0 表示 background，1 表示 saliency）
    - [make_dir_if_not_exist.py](dataset/make_dir_if_not_exist.py)：文件夹不存在时创建
    - [random_split_dataset.py](dataset/random_split_dataset.py)：随机划分数据集
- postprocessing
    - [det_bbox_iou.py](postprocessing/det_bbox_iou.py)：计算一组 bbox 的 iou
    - [det_nms.py](postprocessing/det_nms.py)：NMS
    - [det_draw_bbox.py](postprocessing/det_draw_bbox.py)：生成带框图
    - [det_visualize_from_txt.py](postprocessing/det_visualize_from_txt.py)：从 txt 标注可视化数据集
