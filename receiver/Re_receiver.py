#!/usr/bin/env python
# -*- coding: utf-8 -*-
import zipfile
import os
import re
import getpass

class Re(object):
    def __init__(self, path):
        self.path = path

    def Decompression(self):
        path = self.path
        os.mkdir(path)
        f = zipfile.ZipFile(path + '.zip', 'r')
        f.extractall(path)
        # os.remove(path + r'\Decrypt.exe')

    def read(self):
        list = os.listdir(self.path)
        # print(list)
        # n = len(list)
        # if (n % 2) == 0:
        #     num = int(n / 2)
        # else:
        #     num = int(n / 2) + 1
        # print(list[list.index("tamper%s" % num)])
        target = list[list.index("tamper")]
        with open(self.path + r'\%s' % (target), 'rb') as fp:
            date = fp.read()
        # regex = re.compile(r'strs(.*)stre')
        # msg_all = regex.findall(str(date))[0]
        # print(msg_all)
        # length = len(msg_all) + 8
        # date = date[:-length]

        with open(self.path + r'\%s' % (target), 'wb') as fw:
            fw.write(date)

    def reduction(self):
        filenames = os.listdir(self.path)
        byte_hex = ''
        # filenames.sort(key=lambda x: int(x[6:]), reverse=True)
        # print(filenames)
        for filename in filenames[1:]:               # 旧方法：对文件进行拆解分组的解密算法
            # print(filename)
            filepath = self.path + r'\%s' % filename
            with open(filepath, 'rb') as ff:
                byte_hex += ff.read().hex()
                # print(byte_hex)
        with open(self.path + r'\%s' % filenames[0], 'rb') as f_fin:
            byte_hex += f_fin.read().hex()

        JoP = re.findall('4a464946', byte_hex)
        username = getpass.getuser()
        if JoP:
            byte_hex = 'ffd8ff' + byte_hex + 'ffd9'
            with open(r'C:\Users\%s\Desktop\result.jpg' % username, 'wb') as f:
                f.write(bytes.fromhex(byte_hex))
                suffix = os.path.splitext(r'C:\Users\%s\Desktop\result.jpg')[1]
            return suffix
        else:
            byte_hex = '89504e470d0a1a0a0000000d49484452' + byte_hex + '49454e44ae426082'
            with open(r'C:\Users\%s\Desktop\result.png' % username, 'wb') as f:
                f.write(bytes.fromhex(byte_hex))
                suffix = os.path.splitext(r'C:\Users\%s\Desktop\result.png')[1]
            return suffix


if __name__ == '__main__':
    path = r'C:\Users\Administrator\Desktop\output'
    Reorganization = Re(path)
    Reorganization.Decompression()
    Reorganization.read()
    Reorganization.reduction()


