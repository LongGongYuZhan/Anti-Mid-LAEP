#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import win32api, win32con

from account.connect import sever_connect


def uuid_inquire(id):
    """查询或修改在服务器中保存的接收方uuid"""
    client, connect_result = sever_connect()  # 调用连接模块

    choose = input('\033[4mAnti-Mid\033[0m > ' + "是否修改您所指定的接收方uuid信息？（Y/n）")
    while True:
        if choose in ('y', 'Y', 'yes', ''):
            print('\033[33m[*]\033[0m ' + "uuid格式参照：FAF76B93-798C-11D2-AAD1-006008C78BC7")
            new_uuid = input('\033[4mAnti-Mid\033[0m > ' + "请输入您所指定的接收方新uuid：").upper()
            uid_list = new_uuid.split('-')
            while True:
                if new_uuid.strip() == "":
                    win32api.MessageBox(0, "输入不能为空！", "警告", win32con.MB_ICONWARNING)
                    print('\033[33m[*]\033[0m ' + "uuid格式参照：FAF76B93-798C-11D2-AAD1-006008C78BC7")
                    new_uuid = input('\033[4mAnti-Mid\033[0m > ' + "请重新输入接收方的uuid：")
                if len(uid_list) == 5 and len(uid_list[0]) == 8 and len(uid_list[1]) == 4 and len(
                        uid_list[2]) == 4 and len(uid_list[3]) == 4 and len(uid_list[4]) == 12:
                    break
                else:
                    win32api.MessageBox(0, "uuid格式错误！", "警告", win32con.MB_ICONWARNING)
                    print('\033[33m[*]\033[0m ' + "uuid格式参照：FAF76B93-798C-11D2-AAD1-006008C78BC7")
                    new_uuid = input('\033[4mAnti-Mid\033[0m > ' + "请重新输入接收方的uuid：").upper()
                    uid_list = new_uuid.split('-')

            msg = 'uid' + ',' + id + '#' + new_uuid
            client.sendall(msg.encode('utf-8'))
            result = client.recv(1024).decode('utf-8')
            if result == 'True':
                win32api.MessageBox(0, "更改成功！\n现在所记录的接收方uuid为：%s" % new_uuid, "成功", win32con.MB_ICONASTERISK)
                print('\033[32m[!]\033[0m ' + '现在所记录的接收方uuid为：%s' % new_uuid)
                client.close()

                return new_uuid

            client.close()
            win32api.MessageBox(0, "更改失败！", "失败", win32con.MB_ICONERROR)
            print('\033[31m[-]\033[0m ' + '更改失败')
            choose = input('\033[4mAnti-Mid\033[0m > ' + "是否修改您所指定的接收方uuid信息？（Y/n）")

        elif choose in ('n', 'no'):
            msg = 'uid' + ',' + id + '#' + ' '  # 不更改，则更改位为空格
            client.sendall(msg.encode('utf-8'))
            result = client.recv(1024).decode('utf-8')
            win32api.MessageBox(0, "目前所记录的接收方uuid为：%s" % result, "提示", win32con.MB_ICONASTERISK)
            print('\033[32m[*]\033[0m ' + '现在所记录的接收方uuid为：%s' % result)
            client.close()

            return result

        else:
            print('\033[33m[!]\033[0m ' + "输入格式错误！请重新输入！")
            win32api.MessageBox(0, "输入格式错误！请重新输入！", "错误", win32con.MB_ICONERROR)


def mail_inquire(id):
    """查询或修改在服务器中保存的指定邮箱"""
    client, connect_result = sever_connect()  # 调用连接模块

    choose = input('\033[4mAnti-Mid\033[0m > ' + "是否修改您所指定的邮箱信息？（Y/n）")
    while True:
        if choose in ('y', 'Y', 'yes', ''):
            mail1 = input('\033[4mAnti-Mid\033[0m > ' + "请输入邮箱号1（请确保至少1号邮箱有邮箱号）：")
            mail2 = input('\033[4mAnti-Mid\033[0m > ' + "请输入邮箱号2（若无需设定直接回车即可，但会清除原先设定的邮箱）：")
            mail3 = input('\033[4mAnti-Mid\033[0m > ' + "请输入邮箱号3（若无需设定直接回车即可，但会清除原先设定的邮箱）：")
            if not mail1:
                win32api.MessageBox(0, "请确保至少1号邮箱有邮箱号！", "更改失败", win32con.MB_ICONERROR)
                choose = input('\033[4mAnti-Mid\033[0m > ' + "是否修改您所指定的邮箱信息？（Y/n）")
                continue

            mail_list = 'MAIL1=%s ' % mail1 + 'MAIL2=%s ' % mail2 + 'MAIL3=%s ' % mail3
            msg = 'mail' + ',' + id + '#' + mail_list
            client.sendall(msg.encode('utf-8'))
            result = client.recv(1024).decode('utf-8')
            if result == 'True':
                win32api.MessageBox(0, "更改成功！\nMail_1：%s\nMail_2：%s\nMail_3：%s" % (mail1, mail2, mail3), "成功", win32con.MB_ICONASTERISK)
                print('\033[32m[!]\033[0m ' + '更改成功！')
                client.close()
                return

            client.close()
            win32api.MessageBox(0, "更改失败！", "失败", win32con.MB_ICONERROR)
            choose = input('\033[4mAnti-Mid\033[0m > ' + "是否修改您所指定的邮箱信息？（Y/n）")

        elif choose in ('n', 'no'):
            msg = 'mail' + ',' + id + '#' + ' '  # 不更改，则更改位为空格
            client.sendall(msg.encode('utf-8'))
            result = client.recv(1024).decode('utf-8')
            mail_list = re.findall(r'MAIL1=(.+)MAIL2=(.+)MAIL3=(.+)', result)[0]
            win32api.MessageBox(0, "目前所记录的邮箱号为：\nMail_1：%s\nMail_2：%s\nMail_3：%s" % (mail_list[0], mail_list[1], mail_list[2]), "提示", win32con.MB_ICONASTERISK)
            client.close()

            return
        else:
            print('\033[33m[!]\033[0m ' + "输入格式错误！请重新输入！")
            win32api.MessageBox(0, "输入格式错误！请重新输入！", "错误", win32con.MB_ICONERROR)


def msg_select(id):
    """查询所有信息"""
    client, connect_result = sever_connect()  # 调用连接模块

    msg = 'uid' + ',' + id + '#' + ' '
    client.sendall(msg.encode('utf-8'))
    uuid = client.recv(1024).decode('utf-8')  # uuid更改位置空格时返回的是现存uuid
    client.close()

    client, connect_result = sever_connect()  # 调用连接模块
    msg = 'mail' + ',' + id + '#' + ' '
    client.sendall(msg.encode('utf-8'))
    mail_list = re.findall(r'MAIL1=(.+)MAIL2=(.+)MAIL3=(.+)', client.recv(1024).decode('utf-8'))[0]  # 邮箱更改位置空格时返回的时现存邮箱

    win32api.MessageBox(0, "当前信息如下：\n"
                           "ID：%s\n接收方uuid：%s\n"
                           "指定邮箱：\nMail_1：%s\nMail_2：%s\nMail_3：%s" % (id, uuid, mail_list[0], mail_list[1], mail_list[2]), "信息显示",
                        win32con.MB_ICONASTERISK)
    client.close()
    return uuid


