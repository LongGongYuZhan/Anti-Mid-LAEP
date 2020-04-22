#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os


def is_ep(filename):
    """判断是否为该软件加密的文件"""
    suffix = os.path.splitext(filename)[1]  # 后缀名
    with open(filename, 'rb') as file:
        ed = str(file.read())[-4:-1]        # 文件尾
        # print(ed)
    if suffix == '.laep' and ed == 'EPE':
        return True

    return False


if __name__ == '__main__':
    filename = r'C:\Users\Administrator\Desktop\output\trans.laep'
    print(is_ep(filename))
