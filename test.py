# conding=utf-8

import pymysql
import time
from db_config import *
import os
from Common import Config, LogUtility, Extend
from parm import *

db = pymysql.connect("127.0.0.1","test","123456","autotest",charset = 'utf8')

class Test():

    def sleep(self):
        time.sleep(20)

x = Test()


print('1')
x.sleep()
print('2')
