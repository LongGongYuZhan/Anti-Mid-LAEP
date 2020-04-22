#!/usr/bin/env python
# -*- coding: utf-8 -*-
# import time, sys
import socket
import queue
import threading

ports = []

class PortScaner(object):

    class PortScan(threading.Thread):
        def __init__(self, port_queue, ip, timeout=3):
            threading.Thread.__init__(self)
            self.__port_queue = port_queue
            self.__ip = ip
            self.__timeout = timeout

        def run(self):
            '''多线程实际调用的方法，如果端口队列不为空，循环执行'''
            while True:
                if self.__port_queue.empty():
                    break
                OPEN_MSG = "% 6d [OPEN]\n"
                port = self.__port_queue.get(timeout=0.5)
                ip = self.__ip
                timeout = self.__timeout

                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(timeout)
                    result_code = s.connect_ex((ip, port))  # 开放放回0
                    if result_code == 0:
                        # sys.stdout.write(OPEN_MSG % port)
                        ports.append(port)
                except Exception as e:
                    print(e)


def main():
    # start_time = time.time()  # 脚本开始执行的时间
    port_scner = PortScaner()
    port_queue = queue.Queue()  # py3的写法，使用queue模块, 线程专用
    thread_num = 100  # 线程数量
    threads = []  # 保存新线程
    ip = "127.0.0.1"  # 扫描的ip
    port_list = [7,9,13,21,22,25,37,53,79,80,88,106,110,113,119,135,139,143,179,199,389,427,443,444,465,513,514,543,548,554,587,631,646,873,990,993,995,1025,1026,1027,1028,1110,1433,1720,1723,1755,1900,2000,2049,2121,2717,3000,3128,3306,3389,3986,4899,5000,5009,5051,5060,5101,5190,5357,5432,5631,5666,5800,5900,6000,6646,7070,8000,8008,8080,8443,8888,9100,9999,32768,49152,49153,49154,49155,49156]

    for port in port_list:
        port_queue.put(port)
    for t in range(thread_num):
        threads.append(port_scner.PortScan(port_queue, ip, timeout=3))
    # 启动线程
    for thread in threads:
        thread.start()
    # 阻塞线程
    for thread in threads:
        thread.join()
    # end_time = time.time()  # 脚本结束执行的时间
    # print("[end time] %3ss" % (end_time-start_time,))
    # print(ports)
    return ports


if __name__ == '__main__':
    main()
