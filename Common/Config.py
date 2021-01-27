# coding=UTF-8 

from datetime import datetime
import base64
import os
import json
import re

SITEURL = "http://127.0.0.1:5000"
#SITEURL = "http://192.168.213.110:8000"

#dblink = {"url":"127.0.0.1","username":"test","password":"123456","database":"autotest"}
dblink = {"url":"192.168.213.110","username":"test","password":"123456","database":"autotest"}
#==============================================================================================================
product = ['SiCAP','OMA']

model_oma = '首页,系统设置,信息管理,定时任务,审核复查,统计报表,基本运维,特殊运维,双人协助'

model_sicap = '首页,账号管理,资产管理,资产监控,自动化运维,运维中心,事件中心,流程中心,安全通报,等级保护,报表中心,系统设置'

http_methods = ['delete','get','patch','post','put']

page_Count = 15

path_log = 'TestLog'

path_api = 'static/TestReport/api'

path_ui = 'static/TestReport/ui'

Screenshot = 'static/Screenshot'

para_headers = {
	"Host": "192.168.212.211",
	"Connection": "keep-alive",
	"Content-Length": "170",
	"Accept": "application/json, text/plain, */*",
	"axios-header": "axios",
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36 Edg/86.0.622.38",
	"Content-Type": "application/json;charset=UTF-8",
	"Origin": "https://192.168.212.211",
	"Sec-Fetch-Site": "same-origin",
	"Sec-Fetch-Mode": "cors",
	"Sec-Fetch-Dest": "empty",
	"Referer": "https://192.168.212.211/",
	"Accept-Encoding": "gzip, deflate, br",
	"Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
	"Cookie": "SICAP_SESSIONID=1745f260-bf03-4720-b180-8aa48e309fca"
}

# 案例状态
# 0：待提交 1：待审核 2：已删除 3：已审核
activity_dict = {'delete':'["0","1","3"]','submit':'["0"]','restore':'["2"]','redelete':'["0","1","2","3"]','review':'["1"]','reject':'["1","3"]','makedate':'["0"]'}
#==============================================================================================================
sicap_url = 'https://192.168.212.211'

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
    if isinstance(data, list) and type(data[0]) != str:
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
    if type(request_body) == list and len(request_body) == 1 and len(goods) == 1:
        for key,values in goods.items():
            request_body[0] = values
    elif type(request_body) == dict:
        # 循环字典，获取键、值
        for key, values in request_body.items():
            # 判断值的type类型，如果是list,且子项不是str,调用get_list() 函数
            if type(values) == list:
                get_list(values,goods)
            # 如果是字典，调用自身
            elif type(values) == dict:
                get_targe_value(values,goods)
            # 如果值不是list且是需要被替换的，就替换掉
            elif type(values) != list and values == "需要被替换的值":
                request_body[key] = goods[key]
            else:
                pass
    else:
        print("真的无能为力了~！")

def get_list(values,goods):
    rustle = values[0]
    if type(rustle) == list:
        get_list(values)
    else:
        get_targe_value(rustle,goods)

# 中文标点符号转英文
def cn_to_uk(words):
    table = str.maketrans('‘’“”|（）【】{}，','\'\'\"\"|()[]{},') # 转换表，单个字符的替换
    new_file = words.translate(table)
    return new_file

# 能否转成字典
def is_dict(str):
    try:
        if type(json.loads(str)) == dict:
            return True
        else:
            return False
    except SyntaxError:
        return False
    return True

# 能否转成列表
def is_list(str):
    try:
        if type(list(str)) == list:
            return True
        else:
            return False
    except SyntaxError:
        return False
    return True

# 是字典或者列表
def is_list_or_dict(str):
    if is_list(str) or is_dict(str) or str == '':
        return True
    else:
        return False

# 图片转base64
def img_to_base64(imgurl):
    with open(Screenshot+'/'+imgurl,'rb') as f:
        img=base64.b64encode(f.read())
        img='data:image/png;base64,'+str(img, encoding = "utf-8")
    return img

# 删除案例时校验是否前置后置事务
def delete_pre_next(cases,pre_next):
    for case in cases:
        if case in pre_next:
            return True
        else:
            return False

# 按照报表创建时间排序
def get_file_list(file_path):
    dir_list = os.listdir(file_path)
    if not dir_list:
        return []
    else:
        dir_list = sorted(dir_list, key=lambda x: os.path.getctime(os.path.join(file_path, x)),reverse=True)
        return dir_list

# 数据库查出来的tuple转换成list
def tupleToList(tuple):
    list = []
    for tup in tuple:
        list.append(tup[0])
    return list

# 特殊字符转义
def changeWord(str):
    str = str.replace('/','%2F')
    return str

def wordChange(str):
    str = str.replace('%2F','/').replace('&gt;','>')
    return str

# json格式化
def jsonFormat(str,num):
    str = str.replace('\n', '').replace('\r', '').replace(num*' ','').strip()
    sb = []
    indent = 0
    blank = ' '
    for s in str:
        if s == '{' or s == '[':
            sb.append(s)
            sb.append('\n')
            indent+=1
            sb.append(indent*blank*num)
        if s == '}' or s == ']':
            sb.append('\n')
            indent-=1
            sb.append(indent*blank*num)
            sb.append(s)
        if s == ',':
            sb.append(s)
            sb.append('\n')
            sb.append(indent*blank*num)
        if s not in ('{','}','[',']',','):
            sb.append(s)
    str = ''.join(sb)
    return str

# 比较需要验证的值是否和响应中返回的值一致
def compare_two_dict(dict1, dict2):
    flag = True
    if type(dict1) == dict and type(dict2) == dict:
        keys1 = dict1.keys()
        keys2 = dict2.keys()
        if len(keys2) != 0:
            for key in keys2:
                if key in keys1 and key in keys2:
                    if dict1[key] == dict2[key]:
                        flag = flag & True
                    else:
                        flag = flag & False
                else:
                    raise Exception('检查项的key不正确')
        else:
            raise Exception('检查项为空')
    elif type(dict1) == list and type(dict2) == list and type(dict1[0]) == dict:
        for di1 in dict1:
            for di2 in dict2:
                flag = True
                if type(di1) == dict and type(di2) == dict:
                    keys1 = di1.keys()
                    keys2 = di2.keys()
                    if len(keys2) != 0:
                        for key in keys2:
                            if key in keys1 and key in keys2:
                                if di1[key] == di2[key]:
                                    flag = flag & True
                                else:
                                    flag = flag & False
                            else:
                                raise Exception('检查项的key不正确')
                    else:
                        raise Exception('检查项为空')
            if flag:
                break
    else:
        if dict1 == dict2:
            flag = flag & True
        else:
            flag = flag & False
    if flag:
        result = 'PASS'
    else:
        result = 'FAILED'
    return result

# str转json
def str_to_json(str):
    data = json.dumps(json.loads(str))
    return data

# 清除字符串格式，用来比较
def clear_str_format(str):
    str = str.replace(' ','').replace('\n','').replace('\r','')
    return str

# 获取get链接的参数
def get_value(url,dict):
    list = re.split('{(.*?)}', url)
    if len(dict) == 1:
        for di in dict:
            list[1] = dict[di]
    else:
        for li in list:
            for di in dict:
                if di == li:
                    list[list.index(li)] = dict[di]
    url = ''.join(list)
    return url