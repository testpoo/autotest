# coding=UTF-8 

from datetime import datetime
import base64

SITEURL = "http://127.0.0.1:5000/"
#SITEURL = "http://192.168.213.110:8000/"

dblink = {"url":"127.0.0.1","username":"test","password":"123456","database":"autotest"}

nav = ['自动化测试平台','UI自动化','接口自动化','设置']

sub_nav_ui = [['测试用例','uicases'],['测试集','uisitues'],['测试报告','ui_report_list']]

sub_nav_api = [['测试用例','apicases'],['测试集','apisitues'],['测试报告','api_report_list']]

set_nav = [['注册','register'],['重置密码','reset_passwd']]

operation = [['编辑','edit'],['查看','query'],['执行','exec'],['删除','delete']]

recyclebin = [['恢复','restore'],['彻底删除','delete']]
#==============================================================================================================
# 案例管理
#==============================================================================================================

caseManage_nav = ['案例管理平台','UI自动化','接口自动化','设置']

caseManage_sub_nav_ui = [['UI封装','uiset'],['测试用例','uicases'],['测试用例回收站','uirecyclebin']]

caseManage_sub_nav_api = [['接口集','apiset'],['测试用例','apicases'], ['测试用例回收站','apirecyclebin']]

caseManage_set_nav = [['版本号','versions']]

#==============================================================================================================
# 案例审核
#==============================================================================================================

review_nav = ['案例审核平台','UI自动化','接口自动化']

review_sub_nav_ui = [['测试用例','uicases']]

review_sub_nav_api = [['测试用例','apicases']]

review_user = ['puyawei','lvhao']

review_operation = [['审核','query'],['执行','exec']]

#==============================================================================================================
product = ['SiCAP','OMA']

model_oma = '首页,系统设置,信息管理,定时任务,审核复查,统计报表,基本运维,特殊运维,双人协助'

model_sicap = '账号管理,资产管理,资产监控,自动化运维,运维中心,事件中心,流程中心,安全通报,等级保护,报表中心,系统设置'

http_methods = ['delete','get','patch','post','put']

page_Count = 15

path_log = 'TestLog'

path_api = 'static/TestReport/api'

path_ui = 'static/TestReport/ui'

Screenshot = 'static/Screenshot'

para_headers = {
	"Host": "192.168.213.113",
	"Connection": "keep-alive",
	"Content-Length": "170",
	"Accept": "application/json, text/plain, */*",
	"axios-header": "axios",
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36 Edg/86.0.622.38",
	"Content-Type": "application/json;charset=UTF-8",
	"Origin": "https://192.168.213.113",
	"Sec-Fetch-Site": "same-origin",
	"Sec-Fetch-Mode": "cors",
	"Sec-Fetch-Dest": "empty",
	"Referer": "https://192.168.213.113/",
	"Accept-Encoding": "gzip, deflate, br",
	"Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
	"Cookie": "SICAP_SESSIONID=1745f260-bf03-4720-b180-8aa48e309fca"
}
#==============================================================================================================
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

# 加密
def encrypt(password):
    byteString = password.encode(encoding="utf-8")
    encodestr = base64.b64encode(byteString)
    return encodestr.decode()

# 解密
def decrypt(password):
    encodestr = password.encode(encoding="utf-8")
    decodestr = base64.b64decode(encodestr)
    return decodestr.decode()

# 获取上一条响应中需要的值
def traverse_take_field(data, fields, values={}, currentKey=None):
    """遍历嵌套字典列表，取出某些字段的值
    
    :param data: 嵌套字典列表
    :param fields: 列表，某些字段
    :param values: 返回的值
    :param currentKey: 当前的键值
    :return: 列表
    """
    if isinstance(data, list):
        for i in data:
            traverse_take_field(i, fields, values, currentKey)
    elif isinstance(data, dict):
        for key, value in data.items():
            traverse_take_field(value, fields, values, key)
    else:
        if currentKey in fields:
            values[currentKey] = data
    return values

# 获取响应中的值替换下一个请求接口的数据
def get_targe_value(request_body,goods):
    # 循环字典，获取键、值
    for key, values in request_body.items():
        # 判断值的type类型，如果是list,调用get_list() 函数，
        if type(values) == list:
            get_list(values)
        # 如果是字典，调用自身
        elif type(values) == dict:
            get_targe_value(values)
        # 如果值不是list且是需要被替换的，就替换掉
        elif type(values) != list and values == "需要被替换的值":
            request_body[key] = goods[key]
        else:
            pass

def get_list(values):
    rustle = values[0]
    if type(rustle) == list:
        get_list(values)
    else:
        get_targe_value(rustle)

# 去掉前置后置事件中“-”
def deline(temp):
    list=[]
    for te in temp:
        te = te.split("_")[1]
        list.append(te)
    return list

# 中文标点符号转英文
def cn_to_uk(words):

    table = str.maketrans('‘’“”|（）【】{}，','\'\'\"\"|()[]{},') # 转换表，单个字符的替换
    new_file = words.translate(table)
    return new_file

# 能否转成字典
def is_dict(str):
    try:
        if type(eval(str)) == dict:
            return True
        else:
            return False
    except SyntaxError:
        return False
    return True

# 能否转成列表
def is_list(str):
    try:
        if type(eval(str)) == list:
            return True
        else:
            return False
    except SyntaxError:
        return False
    return True

# 图片转base64
def img_to_base64(imgurl):
    with open(Screenshot+'/'+imgurl,'rb') as f:
        img=base64.b64encode(f.read())
        img='data:image/png;base64,'+str(img, encoding = "utf-8")
    return img