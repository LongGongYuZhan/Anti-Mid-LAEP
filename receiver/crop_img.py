#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PIL import Image

def crop(username, filename, width, height, suffix):
    img = Image.open(filename)
    img_size = img.size
    l = img_size[0]                   # 图片宽度,解密图片肯定为正方形，故只需记录一边
    height_crop = l - height          # 根据加密时的填充方法，只需切割上方或者右方区域

    img_new = img.crop((0, height_crop, width, l))  # Image.crop(left, up, right, below)：
                                                    # left：与左边界的距离 up：与上边界的距离
                                                    # right：还是与左边界的距离below：还是与上边界的距离
    img_new.save(r"C:\Users\%s\Desktop\result%s" % (username, suffix))


if __name__ == '__main__':
    crop(r"C:\Users\Administrator\Desktop\result.jpg", 1400, 948)
