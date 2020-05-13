#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""图像字节信息扰乱代码"""
from sender import uuid2parameter   # 测试用，封装时删除


class Re(object):
    def __init__(self, logistic2, suffix, id, username, height, width):
        self.logistic = logistic2
        self.suffix = suffix
        self.id = id
        self.username = username
        self.height = height
        self.width = width

    def open_img(self):
        """打开图像文件"""
        # username = getpass.getuser()
        with open(r"C:\Users\%s\Desktop\output\result%s" % (self.username, self.suffix), 'rb') as f:
            byte_hex = f.read().hex()  # 读取的二进制文件信息转化为16进制处理
        return byte_hex

    def Reorganization(self, byte_hex):
        """扰乱开始"""
        # print(position)
        hex_list = [byte_hex[i:i + 2] for i in range(0, len(byte_hex), 2)]
        # print(len(hex_list))
        hex_new = []

        start = 0
        for l in self.logistic:
            l = abs(round(l * 1024))              # round:四舍五入 abs:绝对值
            judge = int(str(l)[-1])               # 取logistic值的最后一位数，为奇数则该分组逆转
            if start + l > len(hex_list):         # 以每个值为分组长度
                hex_new.append(hex_list[start:])
                break

            if judge % 2 == 0:
                hex_new.append(hex_list[start:start + l])
            else:
                re = hex_list[start:start + l]
                re.reverse()
                hex_new.append(re)
            start += l

        return hex_new  # 返回的是有分好组的一个列表

    def tamper_jpg(self, byte_hex):
        """如果是jpg，删掉其文件头尾"""
        # byte_new = re.sub(r'ffd8ff', '', byte_hex)
        byte_new = byte_hex.replace(r'ffd8ff', '', 1)  # 去掉jpg的文件头
        byte_new = byte_new[:-4]  # 去掉jpg的文件尾
        # print(byte_new)
        byte_new = self.Reorganization(byte_new)

        return byte_new

    def tamper_png(self, byte_hex):
        """如果是png，删掉其文件头尾"""
        byte_new = byte_hex.replace(r'89504e470d0a1a0a0000000d49484452', '', 1)  # 去掉png文件头PNG IHDR
        # print(byte_new)
        byte_new = byte_new[:-16]  # 去掉png文件尾IEND
        # print(len(byte_new))
        byte_new = self.Reorganization(byte_new)

        return byte_new

    def write(self, byte_new, username, token, time_now):
        """重新写入"""
        tmp = ''
        xor = 1
        with open(r"C:\Users\%s\Desktop\output\trans.laep" % username, 'wb') as f_tamper:
            for i in range(len(byte_new)):  # 逐步取出各个分组
                for j in byte_new[i]:  # 再从分组中取出每一对hex信息拼接起来
                    tmp += j

            # token编码开始
            token_hex = ''
            for c in token:
                xor ^= ord(c)  # token的ascii异或后的数为位置
                token_hex += hex(ord(c)).replace('0x', '')
            # token_hex = ''.join([hex(ord(t)).replace('0x', '') for t in token])  # token16进制化并小写
            front = tmp[:xor]
            rear = tmp[xor:]
            tmp = front + token_hex + rear  # token直接插入指定位置
            f_tamper.write(bytes.fromhex(tmp))
            # print(len(tmp))

        with open(r"C:\Users\%s\Desktop\output\trans.laep" % username, 'a+') as f_tamper1:
            resolution = str(self.height) + "&" + str(self.width)  # 分辨率
            add = "&" + str(self.id) + "&" + resolution + '&' + time_now + " EPE"
            f_tamper1.write(add)

    def Judge(self, byte_hex, token, time_now):
        """判断是那种格式的图片"""
        if r'ffd8ff' in byte_hex[:6]:
            # print("It's JPG")
            byte_new = self.tamper_jpg(byte_hex)
            self.write(byte_new, self.username, token, time_now)
        elif r'89504e47' in byte_hex[:8]:
            # print("It's PNG")
            byte_new = self.tamper_png(byte_hex)
            self.write(byte_new, self.username, token, time_now)
        else:
            print("Not Picture!")


if __name__ == '__main__':
    # uuid_A = "E5E0052B-E3C6-DC4F-BDCB-C2F0F0F658B8"  # 实验uuid
    # 长宽根据实验图片修改
    height = 948
    width = 1400
    uuid = input("请输入接收方uuid值：")
    uuid2parameter = uuid2parameter.uuid2parameter(uuid, width, height)
    list_ascii = uuid2parameter.uuid2ascii()[0]
    logistic1, logistic2 = uuid2parameter.parameter(list_ascii)[:2]
    # print(logistic1, logistic2)
    suffix = '.png'
    id = 1
    username = 'Administrator'
    re = Re(logistic2, suffix, id, username, height, width)
    # byte_hex = re.open_img()
    # re.Judge(byte_hex)
