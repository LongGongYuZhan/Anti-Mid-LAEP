#!/usr/bin/env python
# -*- coding: utf-8 -*-
import zipfile
import os

class zip(object):
    def __init__(self, startdir, file_news):
        self.startdir = startdir
        self.file_news = file_news

    def zip_file(self):
        z = zipfile.ZipFile(self.file_news, 'w', zipfile.ZIP_DEFLATED)  # 参数一：文件夹名
        for dirpath, dirnames, filenames in os.walk(self.startdir):
            fpath = dirpath.replace(self.startdir, '')  # 这一句很重要，不replace的话，就从根目录开始复制
            for filename in filenames:
                z.write(os.path.join(dirpath, filename), fpath + filename)
                # print('压缩成功')
        z.close()


if __name__ == '__main__':
    startdir = r"C:\Users\Administrator\Desktop\output"  # 要压缩的文件夹路径
    file_news = startdir + '.zip'  # 压缩后文件夹的名字
    compression = zip(startdir, file_news)
    compression.zip_file()