#!/usr/bin/env python
# -*- coding: utf-8 -*-
from math import pow
import re

class uuid2parameter(object):
    def __init__(self, uuid, width, height):
        self.uuid = uuid
        self.width = width
        self.height = height

    def uuid2ascii(self):
        num_list = list(re.findall(r"\d", self.uuid)[0])   # 对Arnold的加密深度也改进为从uuid中获取
        if num_list[0] == 0:                               # uuid中的第一个数字就是加密深度
            N = num_list[0] + 1                            # 避免为0的情况，第一个数字为0则+1
        else:
            N = num_list[0]

        list_ascii = []
        uuid = self.uuid.split('-')  # 先将字符串中的'-'去掉
        for segment in uuid:
            tmp = ''
            for c in segment:
                tmp += str(ord(c))
            list_ascii.append(int(tmp))
        # print(list_ascii)
        return list_ascii, int(N)

    def Logistic1(self, x_c, u_c):
        u = u_c / pow(10, len(str(u_c)))
        u = 0.43 * u + 3.57
        x = x_c / pow(10, len(str(x_c)))

        logistic1 = []
        for n in range(self.width * self.height + 200):  # 需要设置将一维的序列转变成二维使之与图像每个像素对应，顾循环总次数为w*h
            logistic1.append(round(x * 255))
            x = u * x * (1 - x)  # Logistic函数系统方程
        # print(logistic1)
        return logistic1[200:]

    def Logistic2(self, y_c, v_c):
        y = y_c / pow(10, len(str(y_c)))
        u = v_c / pow(10, len(str(v_c)))
        u = 0.625 * u + 1

        logistic = []
        for i in range(self.width * self.height + 200):
            logistic.append(y)
            y = 1 - u * y * y
        # print(logistic)
        return logistic[200:]

    def parameter(self, list_ascii):
        x_c = int(str(list_ascii[4])[:12])
        u_c = int(str(list_ascii[4])[12:])
        logistic1 = self.Logistic1(x_c, u_c)
        # print(logistic1)
        y_c = list_ascii[0]
        v_c = list_ascii[1]
        logistic2 = self.Logistic2(y_c, v_c)
        # print(logistic2)
        a = list_ascii[2]
        b = list_ascii[3]
        return logistic1, logistic2, a, b


if __name__ == '__main__':
    # uuid_A = "E5E0052B-E3C6-DC4F-BDCB-C2F0F0F658B8"  # 实验uuid
    # uuid_B = "FAF76B93-798C-11D2-AAD1-006008C78BC7"
    width = 250
    height = 250
    uuid = input("请输入接收方uuid值：")
    uuid2parameter = uuid2parameter(uuid, width, height)
    list_ascii, N = uuid2parameter.uuid2ascii()
    logistic1, logistic2, a, b = uuid2parameter.parameter(list_ascii)
    print(a, b)
    print(logistic2)



