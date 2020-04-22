#!/usr/bin/env python
# -*- coding: utf-8 -*-
import getpass
from sender import BaseRot_sender

class Re(object):
    def __init__(self, x, u, my_sender, my_pass, my_user, suffix):
        self.x = x
        self.u = u
        self.my_sender = my_sender
        self.my_pass = my_pass
        self.my_user = my_user
        self.suffix = suffix

    def open_img(self):
        username = getpass.getuser()
        with open(r"C:\Users\%s\Desktop\test%s" % (username, self.suffix), 'rb') as f:
            byte_hex = f.read().hex()  # 读取的二进制文件信息转化为16进制处理
        return byte_hex, username

    def xu2tamper(self, x, u):
        x = str(x).split('.')[1]  # 各取小数点后的数字（字符串形式）
        u = str(u).split('.')[1]
        while len(x) <= 5:  # 如果位数小于6位，则以最后一位补全
            x += x[-1]
        while len(u) <= 5:
            u += u[-1]
        # print(x, u)
        x_n = int(x[::3])  # 以步数为3取数组成新的数
        u_n = int(u[::3])
        xor = x_n ^ u_n  # 最后对加工后的参数进行异或的到一个新参数
        # print(x_n, u_n)
        # print(xor)  # 得到的xor是按这么此位数分片
        return xor

    def Reorganization_default(self, hex_list):
        # 如果生成的position小于文件本身长度，就默认全体翻转
        hex_list.reverse()
        hex_list_re = [hex_list[i:i + 20] for i in range(0, len(hex_list), 20)]  # 默认分为20组
        return hex_list_re

    def Reorganization_position(self, hex_list, position):
        # 指定位置分组的翻转
        hex_list_re = [hex_list[i:i + position] for i in range(0, len(hex_list), position)]  # 将文件16进制列表按position分组
        hex_list_new = hex_list_re[:-1]  # 除去最后一组（因为最后一组长度不定），其余所有分组翻转
        hex_list_new.reverse()
        hex_list_new.append(hex_list_re[-1])
        # print(hex_list_new)
        return hex_list_new

    def Reorganization(self, byte_hex):
        position = self.xu2tamper(self.x, self.u)
        # print(position)
        hex_list = [byte_hex[i:i + 2] for i in range(0, len(byte_hex), 2)]
        # print(hex_list)

        if len(hex_list) < position:
            # print(hex_list)
            hex_new = self.Reorganization_default(hex_list)
            # print(hex_new[0])
            # for i in hex_new:
            #     hex_tamper += i
            return hex_new
        else:
            hex_new = self.Reorganization_position(hex_list, position)
            # print(hex_new[-1])
            # for i in hex_new:  # 由于分组了，列表中还有列表，所以用2层循环
            #     for j in i:
            #         hex_tamper += j
            return hex_new  # 返回的是有分好组的一个列表

    def tamper_jpg(self, byte_hex):
        # byte_new = re.sub(r'ffd8ff', '', byte_hex)
        byte_new = byte_hex.replace(r'ffd8ff', '', 1)  # 去掉jpg的文件头
        byte_new = byte_new[:-8]  # 去掉jpg的文件尾
        # print(byte_new)
        byte_new = self.Reorganization(byte_new)

        return byte_new

    def tamper_png(self, byte_hex):
        byte_new = byte_hex.replace(r'89504e470d0a1a0a0000000d49484452', '', 1)  # 去掉png文件头PNG IHDR
        # print(byte_new)
        byte_new = byte_new[:-16]  # 去掉png文件尾IEND
        # print(byte_new)
        byte_new = self.Reorganization(byte_new)

        return byte_new

    def write(self, byte_new, username):
        for i in range(len(byte_new)):  # 逐步取出各个分组
            with open(r"C:\Users\%s\Desktop\output\tamper%s" % (username, i + 1), 'wb') as f_tamper:
                tmp = ''
                for j in byte_new[i]:  # 再从分组中取出每一对hex信息拼接起来
                    tmp += j
                f_tamper.write(bytes.fromhex(tmp))  # 这样就成了一个分组一个文件

        msg = BaseRot_sender.sign(self.my_sender, self.my_user, self.my_pass)
        if len(byte_new) % 2 == 0:  # 判断有多少个分组及多少个文件，如果是偶数个就取中间的两个
            mid1 = int(len(byte_new) / 2)
            # mid2 = mid1 + 1
            # with open(r"C:\Users\%s\Desktop\output\tamper%s" % (username, mid1), 'a+') as f_add1:
            #     f_add1.write(my_sender + '|' + my_user)
            with open(r"C:\Users\%s\Desktop\output\tamper%s" % (username, mid1), 'a+') as f_add1:
                f_add1.write(msg)
        else:  # 如果是奇数个就取中间的一个
            mid = int(len(byte_new) / 2) + 1
            with open(r"C:\Users\%s\Desktop\output\tamper%s" % (username, mid), 'a+') as f_add:
                f_add.write(msg)

    def Judge(self):
        byte_hex, username = self.open_img()
        if r'ffd8ff' in byte_hex[:6]:
            # print("It's JPG")
            byte_new = self.tamper_jpg(byte_hex)
            self.write(byte_new, username)
        elif r'89504e47' in byte_hex[:8]:
            # print("It's PNG")
            byte_new = self.tamper_png(byte_hex)
            self.write(byte_new, username)
        else:
            print("Not Picture!")


if __name__ == '__main__':
    x = 0.322447775
    u = 3.620775076476
    my_sender = '1471864319@qq.com'
    my_pass = 'lkxttgimvhatjigd'
    my_user = '1471864319maki@gmail.com'
    suffix = '.jpg'
    Reorganization = Re(x, u, my_sender, my_pass, my_user, suffix)
    Reorganization.Judge()