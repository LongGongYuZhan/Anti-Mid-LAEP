#!/usr/bin/env python
# -*- coding: utf-8 -*-
from account.connect import sever_connect


def check_token(timestamp):
    """接收方解密前先看时间段是否有token匹对"""
    client, connect_result = sever_connect()  # 调用连接模块
    if connect_result:  # 如果client.connect_ex返回的是0意外的代码，说明连接出错
        return 'Error'

    msg_c = 'token' + ',' + 'SIGN=check;msg=' + timestamp
    client.sendall(msg_c.encode('utf-8'))

    msg_s = client.recv(1024).decode('utf-8')
    client.close()
    if msg_s == 'Expired':
        return False
    else:
        return msg_s
