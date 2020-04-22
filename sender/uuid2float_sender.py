# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
uuid格式的字符串按一定规则转换为具有一定映射性的两种Logistic需要的参数
"""
import re
from math import pow

class uuid2float(object):
    def __init__(self, uuid):
        self.uuid = uuid

    def method(self):
        uuid = ''.join(self.uuid.split('-'))  # 先将字符串中的-去掉
        list = re.findall(r'.{2}', uuid)  # 利用正则表达式把字符串一对一对的隔开
        # print(n)
        list_dec = []
        for i in list:
            list_dec.append(int(i, 16))  # 依次转换为16进制

        list_dec_4 = [list_dec[i:i + 4] for i in range(0, len(list_dec), 4)]  # 4个4个分组
        # print(list_dec_4)
        # print(sorted(list_dec_4[i])[3], sorted(list_dec_4[i])[2])
        # print(sorted(list_dec_4[i])[0], sorted(list_dec_4[i])[1])
        x0 = u = ""
        for i in range(0, 4):
            if i < 2:  # 前一半给x0，后一半给u
                x0 += str((list_dec_4[i][0] ^ list_dec_4[i][1]) * (list_dec_4[i][2] ^ list_dec_4[i][3]))
                # 一组里面，前两个数与后两个数进行异或后相乘
            else:
                u += str((list_dec_4[i][0] ^ list_dec_4[i][1]) * (list_dec_4[i][2] ^ list_dec_4[i][3]))
        # print(x0, u)
        return x0, u

    # def spare_uuid(self):
    #     uuid_new = ''.join(str(uuid.uuid1()).split('-'))
    #     print("由于您给出的uuid处理后参数不符合规范，所以我们重新为您生成了新的uuid，请将此告知发送方：")
    #     print(uuid_new)
    #     return uuid_new

    def check(self):
        x0, u = self.method()
        # 如果碰巧遇到两者数值相同的情况，考虑到后续异或会为零的情况，所以会通知用户重新随机生成一个uuid
        # 如果生成出来参数有为0的情况，也需要重新生成（未修复！）
        # if x0 == u:
        #     print("x0 is same as u, regenerate a new UUID")
        #     self.uuid = self.spare_uuid()
        #     x0, u = self.method()
        while len(x0) <= 5:
            x0 += x0[-1]
        while len(u) <= 5:
            u += u[-1]
        # print(x0, u)
        return self.decimal(x0, u)

    def decimal(self, x0, u):
        # print(int(x0) / pow(10, len(x0)))  # x0方法可定为此
        # print(int(u) / pow(10, len(u)))  # 由于u的范围特殊，请自行设法转换
        x0_n = int(x0) / pow(10, len(x0))
        u_n = int(u) / pow(10, len(u))
        u_n = 0.43*u_n + 3.57
        return x0_n, u_n


if __name__ == '__main__':
    # uuid_A = "E5E0052B-E3C6-DC4F-BDCB-C2F0F0F658B8"  # 实验uuid
    # uuid_B = "FAF76B93-798C-11D2-AAD1-006008C78BC7"
    uuid = input("请输入接收方uuid值：")
    # 0 < X(0) < 1
    # 3.569946...(3.57) < u <= 4

    uuid = uuid2float(uuid)
    x, u = uuid.check()
    print(x, u)
