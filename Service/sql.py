#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pymysql
from Service import mail
from Service import read_ini

host, user, password, database = read_ini.read_ini_sql()


class sql_execute(object):
    """用于检测和破解追踪的数据库操作"""
    # 初试化链接数据库
    conn = pymysql.connect(host=host, user=user, password=password, database=database)
    cursor = conn.cursor()

    def __init__(self, id, uuid, text):
        self.id =id
        self.uuid = uuid
        self.text = text

    def check(self):
        """匹对服务器数据库中id所对应的uuid和传送的uuid"""
        sql = """
            SELECT uuid FROM id_uuid WHERE id = \'%d'\
            """ % self.id

        sql_execute.conn.ping(reconnect=True)  # 检查数据库的连接是否正常，若断开则重连，
                                               # 解决二次访问服务器数据库的pymysql.err.InterfaceError Interface Error: (0, '')错误
        # 注：类中调用全局变量要用类名引出
        sql_execute.cursor.execute(sql)  # 执行sql语句
        sql_execute.conn.commit()  # 提交事务
        sql_uuid = sql_execute.cursor.fetchone()[0]  # 返回一条结果行

        if self.uuid == sql_uuid:
            sql_execute.conn.close()
            return 'True'

        # 注：；类中方法调用其他函数用self引出
        self.select_mail(self.id)
        self.conn.close()
        return 'False'

    def select_mail(self, id):
        """配对失败，判断为截获者，查找邮箱以发送邮件"""
        sql = """
            SELECT mail1, mail2, mail3 FROM id_mail WHERE id = \'%d'\
            """ % id

        sql_execute.cursor.execute(sql)
        sql_execute.conn.commit()
        mailbox = sql_execute.cursor.fetchone()
        # print(mailbox)
        mail.send_mail(mailbox, self.text)


class sql_login_register(object):
    """用于登录注册的数据库操作"""
    # 初试化链接数据库
    conn = pymysql.connect(host=host, user=user, password=password, database=database)
    cursor = conn.cursor()

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def login(self):
        sql = """
            SELECT pwd, id FROM users WHERE username = \'%s'\
            """ % self.username

        sql_login_register.cursor.execute(sql)
        sql_login_register.conn.commit()
        # print(sql_login_register.cursor.fetchone())
        result = sql_login_register.cursor.fetchone()
        if not result:  # 如果查询结果为空，说明不存在该账户，返回特殊值处理
            return 0.5
        sql_pwd = result[0]
        sql_id = result[1]

        if self.password == sql_pwd:
            return sql_id  # 若密码正确，就返回用户id
        return 0  # 否则返回0（表中id从1开始）

    def register(self, uuid, mail_list):
        sql_test = """SELECT username FROM users WHERE username = '%s'""" % self.username
        sql1 = """INSERT INTO users (username, pwd) VALUES ('%s', '%s')""" % (self.username, self.password)
        sql2 = """INSERT INTO id_uuid (uuid) VALUES ('%s')""" % uuid
        sql3 = """INSERT INTO id_mail (mail1, mail2, mail3) VALUES ('%s', '%s', '%s')""" % (mail_list[0], mail_list[1], mail_list[2])

        sql_login_register.cursor.execute(sql_test)  # 先查一下有无重名
        sql_login_register.conn.commit()
        result = sql_login_register.cursor.fetchone()
        # print(result)
        if result:
            return 'exist'

        try:
            sql_login_register.cursor.execute(sql1)
            sql_login_register.cursor.execute(sql2)
            sql_login_register.cursor.execute(sql3)
        except Exception as e:
            sql_login_register.conn.rollback()  # 事务回滚
            return False
        else:
            sql_login_register.conn.commit()

        sql4 = """SELECT id FROM users WHERE username = '%s'""" % self.username
        sql_login_register.cursor.execute(sql4)
        sql_login_register.conn.commit()
        result = sql_login_register.cursor.fetchone()[0]
        return result


class sql_select_update(object):
    """查询和修改信息（uuid，邮箱）"""
    # 初试化链接数据库
    conn = pymysql.connect(host=host, user=user, password=password, database=database)
    cursor = conn.cursor()

    def __init__(self, id):
        self.id = id

    def uid_update(self, new_uid):
        """uuid更新"""
        sql = """UPDATE id_uuid SET uuid = '%s' WHERE id = %d
        """ % (new_uid, self.id)

        try:
            sql_select_update.cursor.execute(sql)
        except Exception as e:
            sql_select_update.conn.rollback()  # 事务回滚
            return False
        else:
            sql_select_update.conn.commit()
            return True

    def uid_select(self):
        """不修改就返回现有uuid"""
        sql = """SELECT uuid FROM id_uuid WHERE id = %d
        """ % self.id

        sql_select_update.cursor.execute(sql)
        sql_select_update.conn.commit()
        result = sql_select_update.cursor.fetchone()[0]
        return result

    def mail_update(self, mail_list):
        """邮件更新"""
        sql = """UPDATE id_mail SET mail1 = '%s', mail2 = '%s', mail3 = '%s' WHERE id = %d
        """ % (mail_list[0], mail_list[1], mail_list[2], self.id)

        try:
            sql_select_update.cursor.execute(sql)
        except Exception as e:
            sql_select_update.conn.rollback()  # 事务回滚
            return False
        else:
            sql_select_update.conn.commit()
            return True

    def mail_select(self):
        """不修改就返回现有邮箱"""
        sql = """SELECT  mail1, mail2, mail3 FROM id_mail WHERE id = %d
                """ % self.id

        sql_select_update.cursor.execute(sql)
        sql_select_update.conn.commit()
        mali_list = sql_select_update.cursor.fetchone()
        return mali_list


class sql_token(object):
    """查询token"""
    # 初试化链接数据库
    conn = pymysql.connect(host=host, user=user, password=password, database=database)
    cursor = conn.cursor()

    def __init__(self,time):
        self.time = time

    def token_select(self):
        """查询token"""
        sql = """SELECT token FROM token WHERE time = '%s'
        """ % self.time

        sql_token.cursor.execute(sql)
        sql_token.conn.commit()
        token = sql_token.cursor.fetchone()

        if token:
            return token[0]
        else:
            return


if __name__ == '__main__':
    uuid = input("uuid:")
    text = "message text"

    sql = sql_execute(2, uuid, text)
    print(sql.check())
