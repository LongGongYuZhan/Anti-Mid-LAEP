#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
import cv2
# import time

class Arnold(object):
    def __init__(self, img, a, b, N):
        self.img = img
        self.a = a
        self.b = b
        self.N = N

    def arnold(self, img):
        c = self.a * self.b + 1
        height, weight = img.shape[: 2]
        new_img = copy.deepcopy(img)
        # 置换N次
        for i in range(self.N):
            for x in range(height):
                for y in range(weight):
                    x_n = int((x + self.b * y) % height)
                    y_n = int((self.a * x + c * y) % weight)
                    new_img[x_n, y_n, :] = img[x, y, :]
            # img = copy.deepcopy(new_img)

        return new_img

    def arnold_Re(self):
        # 还原解密
        c = self.a * self.b + 1
        height, weight = self.img.shape[: 2]
        new_img = copy.deepcopy(self.img)

        for i in range(self.N):
            for x in range(height):
                for y in range(weight):
                    nx = int((c * x + (-self.b) * y) % height)
                    ny = int(((-self.a) * x + y) % weight)
                    new_img[nx, ny] = self.img[x, y]
            # img = copy.deepcopy(new_img)

        return new_img

    def check(self):
        # 检测图片是否为正方形，如果不是则进行填充
        height, weight = self.img.shape[: 2]
        if height != weight:
            if height > weight:
                pad = height - weight
                img_new = cv2.copyMakeBorder(self.img, 0, 0, 0, pad, cv2.BORDER_CONSTANT)  # 上下左右，在右边填充
            else:
                pad = weight - height
                img_new = cv2.copyMakeBorder(self.img, pad, 0, 0, 0, cv2.BORDER_CONSTANT)  # 上下左右, 在上面填充
            # cv2.imshow('test1', img_new)
            # cv2.waitKey()
            return self.arnold(img_new)
        else:
            return self.arnold(self.img)


if __name__ == '__main__':
    username = 'Administrator'
    suffix = '.jpg'
    a = int(input("参数a："))
    b = int(input("参数b："))
    N = int(input("迭代次数："))
    img = cv2.imread(r"C:\Users\Administrator\Desktop\arnold.jpg")

    choose = input("s or r：")
    if choose == 's':
        print("加密中...")
        # start = time.time()
        img = Arnold(img, a, b, N)
        img_new = img.check()
        # end = time.time()
        cv2.namedWindow('test2', cv2.WINDOW_NORMAL)
        cv2.imshow('test2', img_new)
        cv2.waitKey()
        cv2.imwrite(r'C:\Users\%s\Desktop\arnold%s' % (username, suffix), img_new)
        # print("共耗时：%s" % str(end - start))
    else:
        print("解密中...")
        img = Arnold(img, a, b, N)
        img_new = img.arnold_Re()
        cv2.namedWindow('test2', cv2.WINDOW_NORMAL)
        cv2.imshow('test2', img_new)
        cv2.waitKey()
        cv2.imwrite(r'C:\Users\%s\Desktop\arnold_re%s' % (username, suffix), img_new)
