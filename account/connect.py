#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket


def sever_connect():
    """专门为连接服务器写一个方法以重复使用"""
    client = socket.socket()  # 创建socket对象
    ip_port = ("127.0.0.1", 10010)  # 确定IP
    # print("连接服务器中...")
    connect_result = client.connect_ex(ip_port)  # 建立客户端链接

    return client, connect_result
