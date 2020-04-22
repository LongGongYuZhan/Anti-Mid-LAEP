#!/usr/bin/env python
# -*- coding: utf-8 -*-
import msvcrt
import win32api, win32con
import hashlib

from account.connect import sever_connect

LOG = '\033[4mAnti-Mid\033[0m > '  # 下划线Log


def password_hide(li):
    """密码输入隐藏"""
    while True:  # 实现将输入的密码不可视化（cmd端有效）
        char = msvcrt.getch()
        # 回车
        if char == b'\r':
            msvcrt.putch(b'\n')
            password = b''.join(li).decode()
            break
        # 退格
        elif char == b'\x08':
            if li:
                li.pop()
                msvcrt.putch(b'\b')
                msvcrt.putch(b' ')
                msvcrt.putch(b'\b')
        else:
            li.append(char)
            msvcrt.putch(b'*')

    # print("密码：%s" % password)
    return password


def login():
    """登录模块"""
    client, connect_result = sever_connect()  # 调用连接模块
    if connect_result:  # 如果client.connect_ex返回的是0意外的代码，说明连接出错
        return 'Error', 'Error'

    while True:
        username = input('[*] ' + "用户名：")
        print('[*] ' + '密码：', end='', flush=True)
        li = []
        password = password_hide(li)
        # password = input()

        if username.encode('utf-8').isalnum():  # 用户名只能包含字母和数字；encode是解决中文也判断为真的情况
            break
        else:
            win32api.MessageBox(0, "用户名只能包含字母和数字", "警告", win32con.MB_ICONASTERISK)
            li.clear()
    password = hashlib.new('md5', password.encode(encoding='UTF-8')).hexdigest()  # 密码md5加密
    # print(password)
    # print("发送数据...")
    msg_c = 'log' + ',' + 'NAME=%s;' % username + 'PWD=%s' % password
    client.sendall(msg_c.encode('utf-8'))
    # print("发送成功")

    # print("等待接收数据...")
    msg_s = client.recv(1024).decode('utf-8')  # 服务器返回的为‘0’或用户id
    # print(msg_s)
    if msg_s == '0':  # 0表示登录名或密码错误
        win32api.MessageBox(0, "登录名或密码错误！", "登录失败", win32con.MB_ICONERROR)
        client.close()
        return 0, 0  # bool不能分给两个变量，故返回两个0
    elif msg_s == '0.5':  # 0.5表示不存在该用户
        win32api.MessageBox(0, "用户不存在！", "登录失败", win32con.MB_ICONERROR)
        client.close()
        return 0, 0

    client.close()
    return username, msg_s  # 其余情况就返回用户名和id（msg_s）


def register():
    """注册"""
    client, connect_result = sever_connect()  # 调用连接模块
    if connect_result:  # 如果client.connect_ex返回的是0意外的代码，说明连接出错
        return 'Error', 'Error'

    while True:
        username = input('[*] ' + "请设置您的用户名（仅支持字母和数字）：")
        li1 = []
        li2 = []
        print('[*] ' + '请设置密码：', end='', flush=True)
        password1 = password_hide(li1)
        print('[*] ' + '请再次输入密码：', end='', flush=True)
        password2 = password_hide(li2)

        if username.encode('utf-8').isalnum():  # 用户名只能包含字母和数字；encode是解决中文也判断为真的情况
            if password1 == password2:
                break
            else:
                win32api.MessageBox(0, "两次密码不一致！", "错误", win32con.MB_ICONERROR)
                li1.clear()
                li2.clear()
        else:
            win32api.MessageBox(0, "用户名只能包含字母和数字", "警告", win32con.MB_ICONASTERISK)
            li1.clear()
            li2.clear()
    password = hashlib.new('md5', password1.encode(encoding='UTF-8')).hexdigest()  # 密码md5加密

    win32api.MessageBox(0, "若您的加密图片被中途非法截获，设定指定邮箱能向您即时反馈非法截获者的各项信息", "说明", win32con.MB_ICONASTERISK)
    while True:
        print(LOG + "设置指定邮箱：")
        mail1 = input(LOG + "请输入邮箱号1（请确保至少1号邮箱有邮箱号）：")
        mail2 = input(LOG + "请输入邮箱号2（若无需设定直接回车即可）：")
        mail3 = input(LOG + "请输入邮箱号3（若无需设定直接回车即可）：")
        if not mail1:
            win32api.MessageBox(0, "请确保至少1号邮箱有邮箱号！", "更改失败", win32con.MB_ICONERROR)
            continue
        if mail2 == '':
            mail2 = ' '
        if mail3 == '':
            mail3 = ' '
        if win32api.MessageBox(0, "Mail_1：%s\nMail_2：%s\nMail_3：%s" % (mail1, mail2, mail3), "信息确认",
                            win32con.MB_YESNO):
            break

    win32api.MessageBox(0, "接收方的uuid能作为加密的唯一参数，请提前向您所指定的接收方沟通", "说明", win32con.MB_ICONASTERISK)
    while True:
        print('\033[33m[*]\033[0m  ' + "设置接收方uuid（可暂时为空，但请后续登录时添加，否则无法加密）")
        print('\033[33m[*]\033[0m ' + "uuid格式参照：FAF76B93-798C-11D2-AAD1-006008C78BC7")
        uuid = input(LOG + "uuid：").upper()
        if uuid == '':
            uuid = ' '
            break
        uid_list = uuid.split('-')
        while True:
            if len(uid_list) == 5 and len(uid_list[0]) == 8 and len(uid_list[1]) == 4 and len(
                    uid_list[2]) == 4 and len(uid_list[3]) == 4 and len(uid_list[4]) == 12:
                break
            else:
                win32api.MessageBox(0, "uuid格式错误！", "警告", win32con.MB_ICONWARNING)
                print('\033[33m[*]\033[0m ' + "uuid格式参照：FAF76B93-798C-11D2-AAD1-006008C78BC7")
                uuid = input(LOG + "请重新输入接收方的uuid：").upper()
                uid_list = uuid.split('-')

        if win32api.MessageBox(0, "UUID：%s" % uuid, "信息确认", win32con.MB_YESNO):
            break

    msg_c = 'reg' + ',' + 'NAME=%s' % username + '#' + 'PASSWORD=%s' % password + '#' + 'UID=%s' % uuid + '#' + 'Mail1=%sMail2=%sMail3=%s' % (mail1, mail2, mail3)
    client.sendall(msg_c.encode('utf-8'))
    msg_s = client.recv(1024).decode('utf-8')
    if msg_s == 'False':
        client.close()
        win32api.MessageBox(0, "注册失败！", "失败", win32con.MB_ICONERROR)
        return False
    elif msg_s == 'exist':
        client.close()
        win32api.MessageBox(0, "该用户名已存在！", "失败", win32con.MB_ICONERROR)
        return False
    else:
        client.close()
        return msg_s


if __name__ == '__main__':
    register()
