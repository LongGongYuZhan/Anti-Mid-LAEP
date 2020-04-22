# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
混沌序列图像加密算法
"""
from PIL import Image
import getpass
# import os  # 多线程测试用

from sender import uuid2parameter  # 测试用

class Logistic_method(object):
    def __init__(self, filename, logistic, suffix):
        self.filename = filename
        self.logistic = logistic
        self.suffix = suffix

    def start(self):
        # 读取本机的实验图片，并得到图片的宽高
        img = Image.open(self.filename)
        height = img.height
        width = img.width
        return img, height, width

    def Pixel(self, img):
        """先获取所需加密图片的所有像素值"""
        height, width = self.start()[1:3]
        Pixel_list = []
        # 横向遍历图片
        for row in range(height):
            for col in range(width):
                Pixel_list.append([col, row, list(img.getpixel((col, row)))])
                # 将x坐标、y坐标、该坐标下的像素以[x，y，[像素值]]保存

        return Pixel_list

    def upset(self):
        img, height, width = self.start()
        if self.suffix == '.jpg' or self.suffix == '.jpeg':
            filename = self.filename.replace(self.suffix, '')
            img.save(filename + '.png')
            img_change = Image.open(filename + '.png')
            img_pixel = self.Pixel(img_change)
            self.suffix = '.png'
        else:
            img_pixel = self.Pixel(img)

        for i in range(len(img_pixel)):
            for j in range(3):
                # 将原图每个像素值与序列的值进行异或运算，得到像素完全打乱后的密图
                img_pixel[i][2][j] = img_pixel[i][2][j] ^ self.logistic[i]

        img_new = Image.new("RGB", (width, height))  # 创建新图片
        for num in img_pixel:
            img_new.putpixel((num[0], num[1]), (num[2][0], num[2][1], num[2][2]))
        # img_new.show()
        username = getpass.getuser()
        # 多线程测试代码：
        # path = r'C:\Users\%s\Desktop\output\default%s' % (username, self.suffix)
        # if os.path.isfile(path):  # 先检测文件夹是否存在
        #     path = r'C:\Users\%s\Desktop\output\default1%s' % (username, self.suffix)
        # img_new.save(path)
        img_new.save(r'C:\Users\%s\Desktop\output\default%s' % (username, self.suffix))
        img_new.close()

        return self.suffix


if __name__ == '__main__':
    filename = r"C:\Users\Administrator\Desktop\output\default.jpg"
    uuid = "E5E0052B-E3C6-DC4F-BDCB-C2F0F0F658B8"
    width = 1138
    height = 640
    parameter = uuid2parameter.uuid2parameter(uuid, width, height)
    list_ascii, N = parameter.uuid2ascii()
    logistic1, logistic2, a, b = parameter.parameter(list_ascii)

    x = 0.2305439
    u = 3.8237057792
    suffix = ".jpg"
    img_new = Logistic_method(filename, logistic1, suffix)
    img_new.upset()



