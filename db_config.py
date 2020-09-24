# coding=utf-8

import pymysql
from Common import Config, LogUtility

def selectall(sql):
    try:
        #连接MySQL数据库
        db = pymysql.connect("127.0.0.1","test","123456","autotest",charset = 'utf8')
        #使用cursor()方法获取操作游标
        cursor = db.cursor()
        #使用execute()方法执行sql语句
        cursor.execute(sql)
        #使用fetchone()方法获取所有数据
        results = cursor.fetchall()
        return results
    except Exception as err:
        LogUtility.logger.debug("事务处理失败: {}".format(str(err)))
    else:
        LogUtility.logger.debug("事务处理成功")
    #关闭数据库
    db.close()

def selectone(sql,info):
    try:
        #连接MySQL数据库
        db = pymysql.connect("127.0.0.1","test","123456","autotest",charset = 'utf8')
        #使用cursor()方法获取操作游标
        cursor = db.cursor()
        #使用execute()方法执行sql语句
        cursor.execute(sql,info)
        #使用fetchone()方法获取所有数据
        results = cursor.fetchall()
        return results
    except Exception as err:
        LogUtility.logger.debug("事务处理失败: {}".format(str(err)))
    else:
        LogUtility.logger.debug("事务处理成功")
    #关闭数据库
    db.close()

def addUpdateDel(sql,info):
    try:
        #连接MySQL数据库
        db = pymysql.connect("127.0.0.1","test","123456","autotest",charset = 'utf8')
        #使用cursor()方法获取操作游标
        cursor = db.cursor()
        #使用execute()方法执行sql语句
        cursor.execute(sql,info)
    except Exception as err:
        db.rollback()
        LogUtility.logger.debug("事务处理失败: {}".format(str(err)))
        print(err)
    else:
        db.commit()
        LogUtility.logger.debug("事务处理成功")
    #关闭数据库
    db.close()

def sDelte(sql):
    try:
        #连接MySQL数据库
        db = pymysql.connect("127.0.0.1","test","123456","autotest",charset = 'utf8')
        #使用cursor()方法获取操作游标
        cursor = db.cursor()
        #使用execute()方法执行sql语句
        cursor.execute(sql)
    except Exception as err:
        db.rollback()
        LogUtility.logger.debug("事务处理失败: {}".format(str(err)))
        print(err)
    else:
        db.commit()
        LogUtility.logger.debug("事务处理成功")
    #关闭数据库
    db.close()