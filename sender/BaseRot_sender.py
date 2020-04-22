#!/usr/bin/env python
# -*- coding: utf-8 -*-
import base64

def base(my_sender, my_user, my_pass):
    global list_new
    my_sender = str(base64.b64encode(my_sender.encode('utf-8')), 'utf-8')[::-1]
    my_user = str(base64.b64encode(my_user.encode('utf-8')), 'utf-8')[::-1]
    my_pass = str(base64.b64encode(my_pass.encode('utf-8')), 'utf-8')[::-1]
    list = [my_sender, my_user, my_pass]
    list_new = rot13_pluse(list)
    # print(list_new)
    return list_new

def rot13_pluse(list):
    list_new = []
    for n in list:
        translate = ''
        for i in n:
            if i.isupper():  # rot13加密解密可区分大小写分开加解密
                if i <= 'M':
                    translate += chr(ord(i) + 13)  # ord()函数是chr()或unichr()（对于Unicode对象）的配对函数,返回对应的ASCII数值
                else:
                    translate += chr(ord(i) - 13)
            elif i.islower():
                if i <= 'm':
                    translate += chr(ord(i) + 13)
                else:
                    translate += chr(ord(i) - 13)
            elif i.isdigit():
                digit = (int(i) + 5) % 10  # 加5与10取余，就可直接得出往后位移5位后的数字
                encode_digit = '%d' % digit  # %d格式化为整数
                translate += encode_digit
            else:
                translate += i
        list_new.append(translate)
    return list_new

def sign(my_sender, my_user, my_pass):
    list_new = base(my_sender, my_user, my_pass)
    # print(list_new)
    msg = "strs" + list_new[0] + '@' + list_new[1] + '@' + list_new[2] + "stre"
    # my_sender = ".?!&" + list_new[0] + "`@#"
    # my_user = ".?!&" + list_new[1] + "`@#"
    # my_pass = ".?!&" + list_new[2] + "`@#"
    return msg


if __name__ == '__main__':
    my_sender = '1471864319@qq.com'
    my_pass = 'lkxttgimvhatjigd'
    my_user = '1471864319maki@gmail.com'
    msg = sign(my_sender, my_user, my_pass)
    print(msg)
