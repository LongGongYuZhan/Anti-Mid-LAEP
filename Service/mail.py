#!/usr/bin/env python
# -*- coding: utf-8 -*-
import smtplib
import re
from email.mime.text import MIMEText
from email.utils import formataddr
from Service import read_ini

sender, token = read_ini.read_ini_mail()

def send_mail(mail_Recipient, text):
    """发送邮件"""
    sender_mail = sender  # 这里我用的qq邮箱作为服务器发件箱
    sender_pass = token  # qq邮箱验证码

    # text_all = re.findall(r'<table>([\s\S]*)</table>', text)
    # ip_text = text_all[0]
    # os_text = text_all[1]
    # pid_text = text_all[2]

    msg = MIMEText(text, 'plain', 'utf-8')  # 邮件内容（plain指定文本格式，纯文本）
    msg['From'] = formataddr(["文件发送者", sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
    msg['To'] = formataddr(["接收者", ''])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
    msg['Subject'] = "中间人数据截获警告！"  # 邮件的主题，也可以说是标题

    server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是465
    server.login(sender, sender_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
    server.sendmail(sender, list(mail_Recipient), msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
    server.quit()  # 关闭连接


