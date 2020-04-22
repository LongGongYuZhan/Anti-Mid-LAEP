#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import datetime
# import hashlib
# import os
import string
import random
import pymysql

# import winsound
# import win32com.client  # 测试好玩用

conn = pymysql.connect(host='127.0.0.1', user='root', password='', database='')
cursor = conn.cursor()


def creat_token(ymd, hms):
    """生成1440个token并存入数据库"""
    year = int(ymd.split('-')[0])
    month = int(ymd.split('-')[1])
    day = int(ymd.split('-')[2])
    hour = int(hms.split(':')[0])
    minute = int(hms.split(':')[1])
    second = int(hms.split(':')[2])

    sql_truncate = """TRUNCATE table token"""  # 每天新生成时先清空数据（也就是说token时限只有一天）
    cursor.execute(sql_truncate)
    conn.commit()

    for i in range(1440):
        # token = hashlib.sha1(os.urandom(24)).hexdigest()
        count = 16  # token位数
        str_from = string.ascii_letters + string.digits  # 从大小字母和数字中选
        token = "".join([random.choice(str_from) for _ in range(count)])

        time_begin = datetime.datetime(year, month, day, hour, minute, second)

        sql = """INSERT INTO token (time, token) VALUES ('%s', '%s')""" % (time_begin, token)
        cursor.execute(sql)

        if minute+1 == 60:
            hour += 1
            minute = 0
        else:
            minute += 1

    conn.commit()  # 对于数量很大的数据库操作，没必要执行一个sql就commit一下（好比打篇文章，打一个字保存一个字能不慢么）
                   # 可以所有sql语句执行完了，再commit


def checkTime():
    """确认每日0时整生成新一天的token"""
    print("等待0时更新token")
    while True:
        time_now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        time_now_split = time_now.split()  # 以空格分割
        if time_now_split[1] == '00:00:00':  # 若时分秒正好0时，开始生成一天的token
            creat_token(time_now_split[0], time_now_split[1])
            # winsound.Beep(2015, 3000)
            # speak = win32com.client.Dispatch('SAPI.SPVOICE')
            # speak.Speak('token更新完毕！')
            # print("token更新完毕！")
        else:
            continue

        time.sleep(2)  # 因为以秒定时，所以暂停2秒，使之不会在1秒内执行多次
        # print("等待0时更新token")


if __name__ == '__main__':
    # time_now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    # time_now = '2020-4-21 00:00:00'
    # time_now_split = time_now.split()  # 以空格分割

    # begin = time.time()
    # creat_token(time_now_split[0], time_now_split[1])
    # end = time.time()
    # print(end-begin)  # 生成token的时间大概要0.6秒左右（代码改进后）
    checkTime()
