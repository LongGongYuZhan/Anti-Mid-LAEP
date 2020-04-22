#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import re
import threading
from Service import sql

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建服务端套接字
ip_port = ("127.0.0.1", 10010)
server.bind(ip_port)  # 把地址绑定到套接字
server.listen(5)  # 对连接进行监听，最大监听5
pool = []  # 多线程缓冲池（此处用做连接池）


def accept_client():
    """接收新连接"""
    while True:
        print("开始监听客户端链接...")
        client, addr = server.accept()  # 阻塞，等待客户端连接
        pool.append(client)  # 加入连接池
        print('客户端链接地址：%s' % str(addr))

        thread = threading.Thread(target=handel, args=(client,))  # 给每个客户端创建一个独立的线程进行管理（target对应函数，args对应函数参数）
        thread.setDaemon(True)  # 设置成守护线程
        thread.start()


def check(client,data):
    """检测和破解追踪功能"""
    msg = re.findall(r'(\d+)#(.+)#([\s\S]+)', data)[0]
    id = int(msg[0])
    uuid = msg[1]
    text = msg[2]
    # print(id)
    # print(uuid)
    # print(text)
    sql_main = sql.sql_execute(id, uuid, text)
    result = sql_main.check()  # 执行uuid验证
    # print(result)

    client.sendall(result.encode('utf-8'))


def login(client, msg):
    """登录功能"""
    # msg格式：NAME=XXXXX;PWD=XXXXX
    username = re.findall(r'NAME=(.+)', msg.split(';')[0])[0]
    password = re.findall(r'PWD=(.+)', msg.split(';')[1])[0]
    # print(username, password)
    sql_main = sql.sql_login_register(username, password)
    result = sql_main.login()

    client.sendall(str(result).encode('utf-8'))


def register(client, msg):
    """注册功能"""
    msg_split = re.findall(r'NAME=(.+)#PASSWORD=(.+)#UID=(.+)#', msg)[0]
    username = msg_split[0]
    password = msg_split[1]
    uuid = msg_split[2]
    mail_list = re.findall(r'Mail1=(.+)Mail2=(.+)Mail3=(.+)', msg)[0]

    sql_main = sql.sql_login_register(username, password)
    id = sql_main.register(uuid, mail_list)

    client.sendall(str(id).encode('utf-8'))


def uuid(client, msg):
    """处理uuid相关事宜"""
    id = int(re.findall(r'(\d+)#(.+)', msg)[0][0])
    new_uid = re.findall(r'(\d+)#(.+)', msg)[0][1]
    if not new_uid == ' ':  # 若有新的uuid，就执行更新功能
        sql_main = sql.sql_select_update(id)
        result = sql_main.uid_update(new_uid)  # 返回字符串型True/False
    else:  # 若没有，就返回现有uuid
        sql_main = sql.sql_select_update(id)
        result = sql_main.uid_select()  # 返回uuid

    client.sendall(str(result).encode('utf-8'))


def mail(client, msg):
    """处理邮箱相关事宜"""
    msg_list = re.findall(r'(\d+)#(.+)', msg)[0]
    id = int(msg_list[0])
    if msg_list[1] == ' ':  # 若没有新的邮箱，就返回现有邮箱
        sql_main = sql.sql_select_update(id)
        mail_list = sql_main.mail_select()
        result = 'MAIL1=%s ' % mail_list[0] + 'MAIL2=%s ' % mail_list[1] + 'MAIL3=%s ' % mail_list[2]
    else:  # 若有，就更新
        mail_list = re.findall(r'MAIL1=(.+)MAIL2=(.+)MAIL3=(.+)', msg_list[1])[0]
        sql_main = sql.sql_select_update(id)
        result = sql_main.mail_update(mail_list)

    client.sendall(str(result).encode('utf-8'))


def token(client, msg):
    """处理token相关"""
    msg_list = re.findall(r'SIGN=(.+);msg=(.+)', msg)[0]
    # id = msg_list[0]
    sign = msg_list[0]
    time = msg_list[1][:-2] + '00'  # 把秒换成整点

    sql_main = sql.sql_token(time)
    if sign == 'get':
        token = sql_main.token_select()
        if token:
            client.sendall(token.encode('utf-8'))
        else:
            client.sendall(''.encode('utf-8'))
    elif sign == 'check':
        token = sql_main.token_select()
        if token:
            client.sendall(token.encode('utf-8'))
        else:
            client.sendall('Expired'.encode('utf-8'))


def handel(client):
    """处理功能（数据接收、sql）"""
    # 主要服务器端监听链接的双重死循环写法
    # client.sendall("连接服务器成功!".encode(encoding='utf8'))  # 多线程测试用
    while True:
        data = client.recv(10000)  # 缓冲区大小设置成1kb，确保接收所有数据
        list = data.decode('utf-8').split(',', 1)  # 分割且只分1次，分离标识位和数据位
        signal = list[0]

        if signal == 'cs':  # 若标识位为cs，就调用check功能模块
            check(client, list[1])
        elif signal == 'log':  # 若标识位为log，就调用登录功能模块
            login(client, list[1])
        elif signal == 'reg':  # 若标识位为reg，就调用注册功能模块
            register(client, list[1])
        elif signal == 'uid':  # 若标识位为uid，就调用uuid功能模块
            uuid(client, list[1])
        elif signal == 'mail':  # 若标识位为mail，就调用邮件功能模块
            mail(client, list[1])
        elif signal == 'token':
            token(client, list[1])
        break  # 这里直接跳出循环结束连接，因为服务器把判断结果返回客户端，客户端不再需要服务器

        # 多线程测试用代码:
        # print("等待客户端数据发送")
        # bytes = client.recv(1024)
        # print("客户端消息:", bytes.decode(encoding='utf8'))
        # if len(bytes) == 0:
        #     client.close()
        #     # 删除连接
        #     pool.remove(client)
        #     print("有一个客户端下线了。")
        #     break
    client.close()  # 跳出循环后handle结束，也意味着结束了一个子进程


if __name__ == '__main__':
    accept_client()
    # thread = threading.Thread(target=accept_client)  # 新开一个线程，用于接收新连接，否则后面的循环执行不了
    # thread.setDaemon(True)
    # thread.start()

    # while True:
    #     cmd = input("""--------------------------\n输入1:查看当前在线人数\n输入2:给指定客户端发送消息\n输入3:关闭服务端""")
    #     if cmd == '1':
    #         print("--------------------------\n")
    #         print("当前在线人数：", len(pool))
    #     elif cmd == '2':
    #         print("--------------------------\n")
    #         index, msg = input("请输入“索引,消息”的形式：").split(",")
    #         pool[int(index)].sendall(msg.encode(encoding='utf8'))
    #     elif cmd == '3':
    #         exit()
    #         server.close()

