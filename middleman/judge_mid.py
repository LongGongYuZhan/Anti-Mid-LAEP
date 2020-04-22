#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
# import sys  # 测试用
from account.connect import sever_connect
from middleman import anti_msg


def check_msg(id):
    """核对本机信息"""
    uuid = str(os.popen("wmic csproduct get uuid").readlines()[2]).strip()
    text = anti_msg.collation()
    return send_msg(id, uuid, text)


def send_msg(id, uuid, text):
    """与服务器通信"""
    client, connect_result = sever_connect()  # 调用连接模块

    # print("发送数据中...")
    msg_c = 'cs' + ',' + str(id) + '#' + uuid + '#' + text   # cs即check_sendmail，作标识位用，逗号隔开，以让服务器用相应功能处理该数据
    # l = sys.getsizeof(msg_c)
    client.sendall(msg_c.encode('utf-8'))
    # print("数据发送成功！")

    # print("等待接收数据...")
    msg_s = client.recv(1024)
    # print(msg_s.decode('utf-8'))
    if msg_s.decode('utf-8') == 'True':
        client.close()
        return True

    client.close()
    return False


if __name__ == '__main__':
    print(check_msg(2))
