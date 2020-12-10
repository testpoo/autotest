# coding=utf-8

import pymysql
from Common import Config, LogUtility
import time

LogUtility.CreateLoggerFile(Config.path_log+"/dblog_"+time.strftime("%Y_%m_%d_%H_%M_%S"))

def selectall(sql):
    try:
        #连接MySQL数据库
        db = pymysql.connect(Config.dblink['url'],Config.dblink['username'],Config.dblink['password'],Config.dblink['database'],charset = 'utf8')
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
        db = pymysql.connect(Config.dblink['url'],Config.dblink['username'],Config.dblink['password'],Config.dblink['database'],charset = 'utf8')
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
        db = pymysql.connect(Config.dblink['url'],Config.dblink['username'],Config.dblink['password'],Config.dblink['database'],charset = 'utf8')
        #使用cursor()方法获取操作游标
        cursor = db.cursor()
        #使用execute()方法执行sql语句
        cursor.execute(sql,info)
    except Exception as err:
        db.rollback()
        LogUtility.logger.debug("事务处理失败: {}".format(str(err)))
    else:
        db.commit()
        LogUtility.logger.debug("事务处理成功")
    #关闭数据库
    db.close()

def sDelte(sql):
    try:
        #连接MySQL数据库
        db = pymysql.connect(Config.dblink['url'],Config.dblink['username'],Config.dblink['password'],Config.dblink['database'],charset = 'utf8')
        #使用cursor()方法获取操作游标
        cursor = db.cursor()
        #使用execute()方法执行sql语句
        cursor.execute(sql)
    except Exception as err:
        db.rollback()
        LogUtility.logger.debug("事务处理失败: {}".format(str(err)))
    else:
        db.commit()
        LogUtility.logger.debug("事务处理成功")
    #关闭数据库
    db.close()

def uDelete(sql):
    try:
        #连接MySQL数据库
        db = pymysql.connect(host = '192.168.213.105',port = 13507,user = 'oma_admin',password = 'ca@OmaLK*&67',database = 'oma_dbmodel',charset = 'utf8')
        #使用cursor()方法获取操作游标
        cursor = db.cursor()
        #使用execute()方法执行sql语句
        cursor.execute(sql)
    except Exception as err:
        db.rollback()
        LogUtility.logger.debug("事务处理失败: {}".format(str(err)))
    else:
        db.commit()
        LogUtility.logger.debug("事务处理成功")
    #关闭数据库
    db.close()