#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import requests
import re
import psutil
import platform
import prettytable as pt
import time
import os
import threading

from middleman import portscaner

thread_dict = {}

def Ports():
    """端口扫描"""
    port = portscaner.main()
    thread_dict['OS2'] = port
    # return port

def PID():
    """进程扫描"""
    pids = psutil.pids()
    pid_dict = {}
    for pid in pids:
        p = psutil.Process(pid)
        # print('PID:%s\tNAME:%s' % (pid, p.name()))
        pid_dict[pid] = p.name()
    thread_dict['PID'] = pid_dict
    # return pid_dict

def OS():
    """操作系统"""
    global cmd
    digits = platform.architecture()[0]
    os_n = platform.system()
    os_a = platform.platform()

    if os_n == 'Windows':
        cmd = 'Systeminfo | findstr /i "System Model"'
    elif os_n == 'Linux':
        cmd = 'dmidecode -s system-product-name'
    try:
        result = os.popen(cmd).read()
    except:
        thread_dict['OS'] = [os_a, digits, 'Error']
        return
        # return [os_a, digits, 'Error']

    if 'Virtual' in result or 'virtual' in result:
        thread_dict['OS'] = [os_a, digits, '是']
        # return [os_a, digits, True]
    else:
        thread_dict['OS'] = [os_a, digits, '否']
        # return [os_a, digits, False]


def IP_related():
    """ip和pc名"""
    PCname = socket.gethostname()
    url = requests.get("http://txt.go.sohu.com/ip/soip")
    text = url.text
    ip = re.findall(r'\d+.\d+.\d+.\d+', text)[0]

    url = 'https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?co=&resource_id=6006&t=1529895387942&ie=utf8&oe=gbk&cb=op_aladdin_callback&format=json&tn=baidu&cb=jQuery110203920624944751099_1529894588086&_=1529894588088&query=%s'%ip
    r = requests.get(url)
    html = r.text
    address = html.split('location":"')[1].split('","')[0]
    # print(address)

    thread_dict['IP_related'] = [ip, PCname, address]
    # return ip, address, PCname

def collation():
    """信息汇总，成表"""
    thread1 = threading.Thread(target=IP_related)
    thread2 = threading.Thread(target=OS)
    thread3 = threading.Thread(target=Ports)
    thread4 = threading.Thread(target=PID)

    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()
    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()
    # print(thread_dict)
    # ip, address, pcname = IP_related()
    # os_related = OS()  # list
    # ports = Ports()    # list
    # pid_dict = PID()   # dict

    tb_ip = pt.PrettyTable()  # ip相关表
    tb_os = pt.PrettyTable()  # os相关表
    tb_pid = pt.PrettyTable()  # pid相关表
    tb_ip.field_names = ['IP', '主机名', '地点']
    tb_os.field_names = ['操作系统', '位数', '虚拟化', '开放端口']
    tb_pid.field_names = ['PID', '进程名']

    # tb_ip.add_row([ip, pcname, address])
    # tb_os.add_row([os_related[0], os_related[1], os_related[2], ports])
    # for key in pid_dict:
    #     tb_pid.add_row([key, pid_dict[key]])
    os_related = thread_dict['OS']
    os_related.append(thread_dict['OS2'])
    tb_ip.add_row(thread_dict['IP_related'])
    tb_os.add_row(os_related)
    for key in thread_dict['PID']:
       tb_pid.add_row([key, thread_dict['PID'][key]])

    # print(tb_ip)
    # print(tb_os)
    # print(tb_pid)
    ip_text = '************************************<ip相关信息>************************************\n' + tb_ip.get_string() + '\n\n\n'
    os_text = '************************************<操作系统相关信息>************************************\n' + tb_os.get_string() + '\n\n\n'
    pid_text = '************************************<该主机所运行进程>************************************\n' + tb_pid.get_string() + '\n\n\n'
    # print(ip_text)
    # print(os_text)
    # print(pid_text)
    return ip_text + os_text + pid_text


if __name__ == '__main__':
    start = time.time()
    collation()
    end = time.time()
    print(end-start)


