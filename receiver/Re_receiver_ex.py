#!/usr/bin/env python
# -*- coding: utf-8 -*-
import getpass
import re
import os
from sender import uuid2parameter
from middleman import judge_mid
from receiver import token_receiver


class Re_receiver(object):
    def __init__(self,filename):
        self.filename = filename

    def Reorganization(self, byte_hex, logistic2):
        """扰乱解密"""
        hex_list = [byte_hex[i:i + 2] for i in range(0, len(byte_hex), 2)]
        # print(len(hex_list))
        hex_new = []

        start = 0
        for l in logistic2:
            l = abs(round(l * 1024))
            judge = int(str(l)[-1])
            if start + l > len(hex_list):
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

    def reduction(self, filename, uid):
        global byte_hex, pos  # 定义一下全局，不然编译器看着黄着一坨难受
        with open(filename, 'rb') as f_fin:
            context = f_fin.read()
            id_resolutionList = re.findall(r"""&(\d+)&(\d+)&(\d+)&(.+) EPE""", str(context))[0]
            id = id_resolutionList[0]
            timestamp = id_resolutionList[3]
            context_del_N = context.hex()
            # print(len(context_del_N))

        token = token_receiver.check_token(timestamp)  # 根据时间戳返回token
        if not id == '0':  # 若i不为0，则触发破解追踪
            result = judge_mid.check_msg(id)  # 开始触发反追踪检测机制
        else:  # 若id为0，说明发送方没有选择破解追踪功能，可以直接解密（反正截获者解不出来）
            result = True

        if result:  # 如果返回的结果为真，则继续解密
            if not token:
                return 'Expired'
            print('[*] ' + "开始解码")
            # token编码开始
            token_hex = ''
            for c in token:
                token_hex += hex(ord(c)).replace('0x', '')
            context_del_N = context_del_N.replace(token_hex, '', 1)  # 删除隐藏在其中的token
            # for i in re.finditer(r"""26(\d+)26(\d+)26(\d+)""", str(context_del_N)):  # 耗时巨多的天坑修改代码，用finditer找到匹配的位置然后用切片法删
            #     # print(i.group(), i.span())
            #     pos = i.span()[0]  # finditer返回的式迭代器，需和for配套使用；i.group()：匹配的字符，i.span()：起始和结束位置
            # context_del_Y = context_del_N[:pos]
            context_del_Y = re.sub(r"""26(\d+)26(\d+)26(\d+)26(.+)20455045""", "", context_del_N)  # 天坑，用re的sub匹配在一些情况下会多删，导致后续解密全错，算是一个隐藏bug了
            byte_hex = context_del_Y
            print('\033[32m[*]\033[0m ' + '解码完成')
            # print(len(byte_hex))
        else:
            os.remove(filename)
            return False

        height = int(id_resolutionList[1])
        width = int(id_resolutionList[2])
        print('[*] ' + '生成加密参数')
        parameter = uuid2parameter.uuid2parameter(uid, width, height)
        list_ascii, N = parameter.uuid2ascii()
        logistic1, logistic2, a, b = parameter.parameter(list_ascii)
        print('\033[32m[*]\033[0m ' + '加密参数生成完毕')

        print('[*] ' + '开始字节重组')
        hex_list = self.Reorganization(byte_hex, logistic2)
        hex_new = ''
        for i in range(len(hex_list)):  # 逐步取出各个分组
            for j in hex_list[i]:  # 再从分组中取出每一对hex信息拼接起来
                hex_new += j
        print('\033[32m[*]\033[0m ' + '字节重组完毕')

        JoP = re.findall('4a464946', hex_new)
        username = getpass.getuser()
        if JoP:
            print('\033[33m[*]\033[0m ' + '原图格式: JPG')
            byte_hex = 'ffd8ff' + hex_new + 'ffd9'
            with open(r'C:\Users\%s\Desktop\result.jpg' % username, 'wb') as f:
                f.write(bytes.fromhex(byte_hex))
                suffix = os.path.splitext(r'C:\Users\%s\Desktop\result.jpg')[1]
            print('\033[32m[*]\033[0m ' + '图像生成成功')
            return suffix, logistic1, a, b, N, height, width
        else:
            print('\033[33m[*]\033[0m ' + '原图格式: PNG')
            byte_hex = '89504e470d0a1a0a0000000d49484452' + hex_new + '49454e44ae426082'
            with open(r'C:\Users\%s\Desktop\result.png' % username, 'wb') as f:
                f.write(bytes.fromhex(byte_hex))
                suffix = os.path.splitext(r'C:\Users\%s\Desktop\result.png')[1]
            print('\033[32m[*]\033[0m ' + '图像生成成功')
            return suffix, logistic1, a, b, N, height, width


if __name__ == '__main__':
    height = 948
    width = 1400
    filename = r'C:\Users\Administrator\Desktop\output\tamper'
    uuid = input("请输入接收方uuid值：")
    # uuid2parameter = uuid2parameter.uuid2parameter(uuid, width, height)
    # list_ascii = uuid2parameter.uuid2ascii()
    # logistic1, logistic2 = uuid2parameter.parameter(list_ascii)[:2]
    Re = Re_receiver(filename)
    Re.reduction(filename, uuid)
