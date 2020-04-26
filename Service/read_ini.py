#!/usr/bin/env python
# -*- coding: utf-8 -*-
import configparser

config = configparser.ConfigParser()
config.read('message.ini')


def read_ini_sql():
    """读取配置信息mysql数据库部分"""
    host = config.get('DATABASE', 'host')
    username = config.get('DATABASE', 'username')
    password = config.get('DATABASE', 'password')
    database = config.get('DATABASE', 'database')

    return host, username, password, database


def read_ini_mail():
    """读取配置信息邮箱部分"""
    sender = config.get('MAIL', 'sender')
    token = config.get('MAIL', 'token')

    return sender, token


# print(read_ini_sql())
# print(read_ini_mail())
