﻿# coding=UTF-8 

from datetime import datetime
import base64

SITEURL = "http://127.0.0.1:5000/"
#SITEURL = "http://192.168.213.110:8000/"

dblink = {"url":"127.0.0.1","username":"test","password":"123456","database":"autotest"}

nav = [['自动化测试平台',''],['UI自动化',''],['接口自动化',''],['设置','']]

sub_nav_ui = [['UI封装','uiset'],['测试用例','uicases'],['测试集','uisitues'],['测试报告','ui_report_list']]

sub_nav_api = [['接口集','apiset'],['测试用例','apicases'],['测试集','apisitues'],['测试报告','api_report_list']]

set_nav = [['注册','register'],['重置密码','reset_passwd']]

operation = [['删除','delete'],['编辑','edit'],['查看','query'],['执行','exec']]

product = ['SiCAP','OMA']

model_oma = ['系统设置','信息管理','定时任务','审核复查','统计报表','基本运维','特殊运维','双人协助']

model_sicap = ['账号管理','资产管理','资产监控','自动化运维','运维中心','事件中心','流程中心','安全通报','等级保护','报表中心','系统设置']

http_methods = ['delete','get','patch','post','put']

page_Count = 15

path_log = 'TestLog'

path_api = 'static/TestReport/api'

path_ui = 'static/TestReport/ui'

Screenshot = 'static/Screenshot'

para_headers = {}

#change time to str
def getCurrentTime():
    #format = "%a %b %d %H:%M:%S %Y"
    format = "%Y-%m-%d %H:%M:%S"
    return datetime.now().strftime(format)

# Get time diff
def timeDiff(starttime,endtime):
    #format = "%a %b %d %H:%M:%S %Y"
    format = "%Y-%m-%d %H:%M:%S"
    return datetime.strptime(endtime,format) - datetime.strptime(starttime,format)

def encrypt(password):
    byteString = password.encode(encoding="utf-8")
    encodestr = base64.b64encode(byteString)
    return encodestr.decode()

def decrypt(password):
    encodestr = password.encode(encoding="utf-8")
    decodestr = base64.b64decode(encodestr)
    return decodestr.decode()