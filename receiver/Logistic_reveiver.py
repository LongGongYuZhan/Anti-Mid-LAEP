#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PIL import Image
import getpass

class Logistic_method(object):
    def __init__(self, filename, x, u, suffix):
        self.filename = filename
        self.x = x
        self.u = u
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

    def Logistic_default(self):
        img, height, width = self.start()
        x = 0.1
        u = 4
        logistic = []
        for n in range(width * height):  # 需要设置将一维的序列转变成二维使之与图像每个像素对应，顾循环总次数为w*h
            logistic.append(round(x * 255))  # 混沌序列取值是在(0,1)之间的，把序列归一化到(0,255)之间
            # logistic.append(x * 255)
            x = u * x * (1 - x)  # Logistic函数系统方程
        # print(logistic)
        return logistic

    def Logistic(self):
        """生成Logistic混沌序列"""
        height, width = self.start()[1:3]
        # x = 0.2305439  # 混沌序列初始值
        # u = 3.8237057792  # 控制常数
        logistic = []
        for n in range(width * height):  # 需要设置将一维的序列转变成二维使之与图像每个像素对应，顾循环总次数为w*h
            logistic.append(round(self.x * 255))  # 混沌序列取值是在(0,1)之间的，把序列归一化到(0,255)之间
            # logistic.append(x * 255)
            self.x = self.u * self.x * (1 - self.x)  # Logistic函数系统方程
        # print(logistic)
        return logistic

    def upset_default(self):
        img, height, width = self.start()
        img_pixel = self.Pixel(img)
        Logistic_list = self.Logistic_default()
        # print(img_pixel)
        # print(Logistic_list)
        for i in range(len(img_pixel)):
            for j in range(3):
                # 将原图每个像素值与序列的值进行异或运算，得到像素完全打乱后的密图
                img_pixel[i][2][j] = img_pixel[i][2][j] ^ Logistic_list[i]

        img_new = Image.new("RGB", (width, height))  # 创建新图片
        for num in img_pixel:
            img_new.putpixel((num[0], num[1]), (num[2][0], num[2][1], num[2][2]))
            # 在新图片中依次写入像素，putpixel函数内参数为（坐标，RGB像素值）
        # img_new.show()
        # img_new.save(r"C:\Users\Administrator\Desktop\操作备忘录\项目示例\fate_Logistic.jpg")
        # img_new.close()
        return img_new

    def upset(self):
        height, width = self.start()[1:3]
        img = self.upset_default()
        img_pixel = self.Pixel(img)
        Logistic_list = self.Logistic()
        for i in range(len(img_pixel)):
            for j in range(3):
                # 将原图每个像素值与序列的值进行异或运算，得到像素完全打乱后的密图
                img_pixel[i][2][j] = img_pixel[i][2][j] ^ Logistic_list[i]

        img_new = Image.new("RGB", (width, height))  # 创建新图片
        for num in img_pixel:
            img_new.putpixel((num[0], num[1]), (num[2][0], num[2][1], num[2][2]))
        # img_new.show()
        username = getpass.getuser()
        img_new.save(r'C:\Users\%s\Desktop\output\default%s' % (username, self.suffix))
        img_new.close()


if __name__ == '__main__':
    filename = r"C:\Users\Administrator\Desktop\result.jpg"
    x = 0.322447775
    u = 3.620775076476
    suffix = ".png"
    img_new = Logistic_method(filename, x, u, suffix)
    img_new.upset()
