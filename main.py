#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""主函数"""
import win32ui
import win32api, win32con
import os
import getpass
import cv2
import console
from pathlib import Path
from halo import Halo
import numpy as np

import Logo
from account import login_register
from account import uuid_mail_operate

from sender import uuid2parameter
from sender import Logistic_sender
from sender import Arnold
from sender import Re_ex
from sender import token_sender
from receiver import Re_receiver_ex
from receiver import crop_img
from receiver import judge_ep

LOG = '\033[4mAnti-Mid\033[0m > '  # 下划线Log
sign = ['[*] ', '\033[32m[*]\033[0m ', '\033[33m[!]\033[0m ',  '\033[32m[!]\033[0m ', '\033[31m[-]\033[0m ']  # 默认[*]、绿[*]、黄[!]、绿[!]、红[-]
bots = {
    'interval': 100,
    'frames': ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
}
resolution = {
    '标清': 921600,
    '高清': 2073600,
    '超清': 3542400
}


def input_uuid(height, width):
    # 输入接收方uuid方法
    win32api.MessageBox(0, "检测到您未登录，故请手动输入接收方uuid", "提醒", win32con.MB_ICONASTERISK)
    print('\033[33m[*]\033[0m ' + "uuid格式参照：FAF76B93-798C-11D2-AAD1-006008C78BC7")
    uuid = input(sign[0] + "请输入接收方的uuid：").upper()  # 将字母大写
    uid_list = uuid.split('-')
    while True:
        if uuid.strip() == "":
            win32api.MessageBox(0, "输入不能为空！", "警告", win32con.MB_ICONWARNING)
            print('\033[33m[*]\033[0m ' + "uuid格式参照：FAF76B93-798C-11D2-AAD1-006008C78BC7")
            uuid = input(sign[0] + "请重新输入接收方的uuid：")
        if len(uid_list) == 5 and len(uid_list[0]) == 8 and len(uid_list[1]) == 4 and len(uid_list[2]) == 4 and len(uid_list[3]) == 4 and len(uid_list[4]) == 12:
            break
        else:
            win32api.MessageBox(0, "uuid格式错误！", "警告", win32con.MB_ICONWARNING)
            print('\033[33m[*]\033[0m ' + "uuid格式参照：FAF76B93-798C-11D2-AAD1-006008C78BC7")
            uuid = input(sign[0] + "请重新输入接收方的uuid：").upper()
            uid_list = uuid.split('-')

    print(sign[0] + '生成加密参数')
    parameter = uuid2parameter.uuid2parameter(uuid, width, height)
    list_ascii, N = parameter.uuid2ascii()
    logistic1, logistic2, a, b = parameter.parameter(list_ascii)
    print(sign[1] + '加密参数生成完毕')

    return logistic1, logistic2, a, b, N


def choose():
    # 打开文件选择对话框，返回所选文件绝对路径
    dlg = win32ui.CreateFileDialog(1)  # 1表示打开文件对话框
    username = getpass.getuser()
    print(sign[0] + "请选择需要加密的图片")
    dlg.SetOFNTitle("请选择需要加密的图片")
    dlg.SetOFNInitialDir(r'C:\Users\%s\Pictures' % username)  # 设置打开文件对话框中的初始显示目录
    dlg.DoModal()
    filename = dlg.GetPathName()  # 获取选择的文件名称（绝对路径）
    return filename, username


def Intro(id):
    """登录后的加密操作前序步骤"""
    def print_menu():
        print(sign[0] + "请选择您所要进行的操作：\n"
                        '--------------------------\n'
                        "|1、加密                 |\n"
                        "|2、修改接收方uuid       |\n"
                        "|3、修改邮箱             |\n"
                        "|4、退出                 |\n"
                        '--------------------------')

    print_menu()
    while True:
        c = input(LOG)
        if c == '1':  # 显示基本信息后加密
            if not id:  # 如果id为0，说明没有登录，直接返回空值
                return
            uuid = uuid_mail_operate.msg_select(id)  # 查找所有信息，主要任务是返回uuid
            return uuid
        elif c == '2':
            if not id:
                win32api.MessageBox(0, "您没有登录，无法修改信息！", "错误", win32con.MB_ICONERROR)
                print_menu()
                continue

            uuid_mail_operate.uuid_inquire(id)  # 更改uuid
            print_menu()  # 循环重新选择操作
        elif c == '3':
            if not id:
                win32api.MessageBox(0, "您没有登录，无法修改信息！", "错误", win32con.MB_ICONERROR)
                print_menu()
                continue

            uuid_mail_operate.mail_inquire(id)  # 更改邮箱
            print_menu()  # 循环重新选择操作
        elif c == '4':
            exit(0)
        else:
            print(sign[2] + "输入格式错误！请重新输入！")
            win32api.MessageBox(0, "输入格式错误！请重新输入！", "错误", win32con.MB_ICONERROR)
            print_menu()


def encryption(filename, username, height, width, ID, uuid, token, time_now):
    if not uuid:  # 若uuid为空，说明加密方没有登录，只能手动输入uuid
        logistic1, logistic2, a, b, N = input_uuid(height, width)
    else:
        print(sign[0] + '生成加密参数')
        parameter = uuid2parameter.uuid2parameter(uuid, width, height)
        list_ascii, N = parameter.uuid2ascii()
        logistic1, logistic2, a, b = parameter.parameter(list_ascii)
        print(sign[1] + '加密参数生成完毕')
    # 将所选图片进行图像加密
    # N = int(input("请选择加密深度（1/3/5/10）："))

    # print("加密中......(像素值越大，加密时间越长)")
    path = Path(r'C:\Users\%s\Desktop\output' % username)
    if path.is_dir():  # 先检测文件夹是否存在
        pass
    else:
        os.mkdir(r'C:\Users\%s\Desktop\output' % username)

    try:
        if height*width <= resolution['标清']:
            print(sign[2] + '检测到为标清图像(<=1280x720)')
        elif height*width <= resolution['高清']:
            print(sign[2] + '检测到为高清图像(>=1280x720, <=1920x1080),加密可能需要一段时间,请稍等片刻')
        else:
            print(sign[2] + '检测到为\超清图像(>1920x1080),加密可能需要较长时间,请耐心等待')

        spinner = Halo(text='Logistic第一次加密', color='blue', spinner=bots)
        spinner.start()
        suffix = os.path.splitext(filename)[1]
        img_L = Logistic_sender.Logistic_method(filename, logistic1, suffix)
        suffix = img_L.upset()  # 考虑到jpg格式更改问题，后缀名重新复制
        spinner.stop()
        print(sign[1] + 'Logistic第一次加密完成')

        spinner = Halo(text='Arnold第二次加密', color='blue', spinner=bots)
        spinner.start()
        img = cv2.imread(r"C:\Users\%s\Desktop\output\default%s" % (username, suffix))
        img_A = Arnold.Arnold(img, a, b, N)
        img_new = img_A.check()
        cv2.imwrite(r'C:\Users\%s\Desktop\output\result%s' % (username, suffix), img_new)
        spinner.stop()
        print(sign[1] + 'Arnold第二次加密完成')

        spinner = Halo(text='Logistic第三次加密', color='blue', spinner=bots)
        spinner.start()
        Reorganization = Re_ex.Re(logistic2, suffix, ID, username, height, width)
        byte_hex = Reorganization.open_img()
        Reorganization.Judge(byte_hex, token, time_now)
        spinner.stop()
        print(sign[1] + 'Logistic第三次加密完成')

        os.remove(r'C:\Users\%s\Desktop\output\default%s' % (username, suffix))
        os.remove(r'C:\Users\%s\Desktop\output\result%s' % (username, suffix))
        print(sign[1] + '删除中间图片')

        win32api.MessageBox(0, "加密成功！", "提醒", win32con.MB_ICONASTERISK)
        print(sign[3] + "加密成功！")
        # os.system('pause')
    except:
        win32api.MessageBox(0, "图像加密失败", "错误", win32con.MB_ICONWARNING)
        print(sign[4] + "加密失败！")
        # win32api.MessageBox(0, "加密成功！", "提醒", win32con.MB_ICONASTERISK)
        exit(0)


def decryption(username, uid):
    # path = r'C:\Users\%s\Desktop\output' % username
    while True:
        dlg = win32ui.CreateFileDialog(1)  # 1表示打开文件对话框
        print(LOG + "请选择需要解密的文件")
        dlg.SetOFNTitle("请选择需要解密的文件")
        dlg.SetOFNInitialDir(r'C:\Users\%s\Desktop' % username)  # 设置打开文件对话框中的初始显示目录
        dlg.DoModal()
        file = dlg.GetPathName()  # 获取选择的文件名称（绝对路径）
        if file == '':
            exit(0)

        if judge_ep.is_ep(file):  # 判断是否时该由软件加密
            # 解密开始：（顺序为加密时的逆序）
            print(sign[0] + "解密程序初始化中......")
            Reorganization = Re_receiver_ex.Re_receiver(file)  # 先进行二次logistic的字节流扰乱还原
            result = Reorganization.reduction(file, uid)
            if result and result != 'Expired':
                suffix, logistic1, a, b, N, height, width = result

                if height * width <= resolution['标清']:
                    print(sign[2] + '检测到为标清图像(<=1280x720)')
                elif height * width <= resolution['高清']:
                    print(sign[2] + '检测到为高清图像(>=1280x720, <=1920x1080),解密可能需要一段时间,请稍等片刻')
                else:
                    print(sign[2] + '检测到为超清图像(>1920x1080),解密可能需要较长时间,请耐心等待')

                print(sign[0] + '像素解密开始')
                spinner = Halo(text='Arnold反转中', color='green', spinner=bots)
                spinner.start()

                filename = r'C:\Users\%s\Desktop' % username + r'\result%s' % suffix

                img = cv2.imread(filename)  # 再进行Arnold置换还原
                img_A = Arnold.Arnold(img, a, b, N)
                img_new = img_A.arnold_Re()
                cv2.imwrite(filename, img_new)
                spinner.stop()
                print(sign[3] + 'Arnold反转成功')

                print(sign[0] + '切割填充部分')
                crop_img.crop(username, filename, width, height, suffix)  # 对加密时填充的部分进行删除

                spinner = Halo(text='Logistic反转中', color='green', spinner=bots)
                spinner.start()
                img_L = Logistic_sender.Logistic_method(filename, logistic1, suffix)
                img_L.upset()
                spinner.stop()
                print(sign[3] + 'Logistic反转成功')

                print(sign[0] + '删除中间图片')
                os.remove(r'C:\Users\%s\Desktop\result%s' % (username, suffix))

                win32api.MessageBox(0, "解密成功！", "提醒", win32con.MB_ICONASTERISK)
                print(sign[3] + "解密成功！")
                break
                # os.system('pause')
            elif result == 'Expired':
                win32api.MessageBox(0, "解密时效已过期！", "错误", win32con.MB_ICONERROR)
                print(sign[4] + "解密失败！")
                break
            else:
                win32api.MessageBox(0, "解密发生未知错误！", "错误", win32con.MB_ICONERROR)
                print(sign[4] + "解密失败！")
                break

        print(sign[2] + "该文件非经由本软件加密！")
        win32api.MessageBox(0, "该文件非经由本软件加密！请重新选择！", "无法解密", win32con.MB_ICONERROR)
        continue


def sender_main():
    login = input(LOG + "是否登录？(Y/n)")
    while True:
        if login in ('n', 'no'):
            win32api.MessageBox(0, "不登陆将无法使用反追踪功能", "通知", win32con.MB_ICONASTERISK)
            ID = 0  # ID必须设个初值(0)，以备不登录时使用
            break
        elif login in ('y', 'Y', 'yes', ''):
            lor = input(LOG + "登录/注册：（L/r）")
            if lor in ('l', 'L', ''):
                # 登录
                name, ID = login_register.login()
                if name == 'Error':
                    win32api.MessageBox(0, "当前网络不通，请检查您是否连网。\n或离线模式不登录加密。", "网络故障", win32con.MB_ICONERROR)
                    print(sign[4] + '登录失败！')
                    login = input(LOG + "是否登录？(Y/n)")  # 循环回去重新登录
                    continue
                if ID:
                    win32api.MessageBox(0, "登录成功！\n欢迎！%s\nID:%s" % (name, ID), "登录成功", win32con.MB_ICONASTERISK)
                    print(sign[1] + "登录成功！\n" + sign[2] + "欢迎！%s     ID:%s" % (name, ID))
                    break
                else:
                    login = input(LOG + "是否登录？(Y/n)")  # 循环回去重新登录
            elif lor == 'r':
                # 注册
                ID = login_register.register()
                if ID:
                    print(sign[1] + "注册成功!")
                    win32api.MessageBox(0, "注册成功！\n您所分配到的ID号：%s" % ID, "注册成功", win32con.MB_ICONASTERISK)
                    login = input(LOG + "是否登录？(Y/n)")  # 循环回去重新登录
                else:
                    login = input(LOG + "是否登录？(Y/n)")  # 循环回去重新登录
            else:
                print(sign[2] + "输入格式错误！请重新输入！")
                win32api.MessageBox(0, "输入格式错误！请重新输入！", "错误", win32con.MB_ICONERROR)
                login = input(LOG + "是否登录？(Y/n)")
        else:
            print(sign[2] + "输入格式错误！请重新输入！")
            login = input(LOG + "是否登录？(Y/n)")

    uuid = Intro(ID)  # 加密前序步骤

    filename, username = choose()
    if filename == '':
        exit(0)
    img = cv2.imdecode(np.fromfile(filename, dtype=np.uint8), -1)
    # img = cv2.imread(filename)
    # print(img)
    height, weight = img.shape[: 2]
    while True:
        suffix = os.path.splitext(filename)[1]
        if suffix not in ['.jpg', '.png', '.jpeg']:
            # print("该文件不是所支持的图片格式，请选择正确格式的图片！")
            win32api.MessageBox(0, "该文件不是所支持的图片格式，请选择正确格式的图片！", "图片格式错误", win32con.MB_ICONWARNING)
            filename, username = choose()
        else:
            break

    token, time_now = token_sender.get_token()  # 向服务器请求token
    if token == 'Error':
        win32api.MessageBox(0, "未连接服务器！", "通信故障", win32con.MB_ICONWARNING)
        print(sign[2] + "加密失败！")
        exit(0)
    if token and time_now:
        encryption(filename, username, height, weight, ID, uuid, token, time_now)
    else:
        win32api.MessageBox(0, "服务器信息未更新！请稍后再试", "通信故障", win32con.MB_ICONWARNING)
        print(sign[2] + "加密失败！")
        exit(0)


def receiver_main():
    username = getpass.getuser()
    uuid = str(os.popen("wmic csproduct get uuid").readlines()[2]).strip()
    wait = input(LOG + "是否已将您的uuid信息告知发送方？(Y/n)")
    while True:
        if wait in ('n', 'no'):
            win32api.MessageBox(0, "请将您的uuid信息通过安全可靠的方式提前告知发送方：\nYour UUID:\n%s" % uuid, "通知", win32con.MB_ICONASTERISK)
            print(sign[3] + "Your UUID：%s" % uuid)
            # os.system('pause')
            break
        elif wait in ('y', 'Y', 'yes', ''):
            # 在此补充接收方传输代码，并保证返回个布尔常量以控制只有接受文件后才能解密
            decryption(username, uuid)
            break
        else:
            print(sign[2] + "输入格式错误！请重新输入！")
            wait = input(LOG + "是否已将您的uuid信息告知发送方？(Y/n)")


if __name__ == '__main__':
    # 示例UUID：E5E0052B-E3C6-DC4F-BDCB-C2F0F0F658B9
    i = os.system("cls")  # 清屏
    Logo.print_Logo()  # 打印logo

    c = input(LOG + "请问您是图片发送方(sender)，还是图片接收方(receiver) (s/r)：")
    while True:
        if c in ('s', 'sender'):
            sender_main()
            break
        elif c in ('r', 'receiver'):
            receiver_main()
            break
        else:
            print(sign[2] + "输入格式错误！请重新输入！")
            c = input(LOG + "请问您是图片发送方sender，还是图片接收方receiver (s/r)：")
