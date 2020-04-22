#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from account.connect import sever_connect


def get_token():
    """请求token"""
    time_now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

    client, connect_result = sever_connect()  # 调用连接模块
    if connect_result:  # 如果client.connect_ex返回的是0意外的代码，说明连接出错
        return 'Error', 'Error'
    msg_c = 'token' + ',' + 'SIGN=get;msg=' + time_now
    client.sendall(msg_c.encode('utf-8'))

    msg_s = client.recv(1024).decode('utf-8')
    # print(msg_s)
    client.close()
    if msg_s:
        return msg_s, time_now
    else:
        return None, None


if __name__ == '__main__':
    get_token()
