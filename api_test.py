# coding-utf-8

import requests
import time
from db_config import *
from report import *

from Common import Config, LogUtility
from parm import *


class RunTests(object):

    def __init__(self, id,username):

        self.id = id
        self.username = username

        LogUtility.CreateLoggerFile(
            path_log+"/apilog_"+time.strftime("%Y_%m_%d_%H_%M_%S"))

    # 获取接口
    def getApis(self):
        try:
            starttime = Config.getCurrentTime()

            cur = selectone('SELECT name, path, method, request, checks from apiset WHERE id=%s', [self.id])
            cases = [dict(name=row[0], path=row[1], method=row[2],request=row[3],checks=row[4]) for row in cur][0]

            name = cases['name']
            url = cases['path']
            method = cases['method']
            data = cases['request']

            headers = {}

            r = eval('requests.'+method + '(url, headers=headers, data=data)')
            result = [name, url, method, data, r.text]
        except Exception as err:
            LogUtility.logger.debug(
                "Failed running test apis, error message: {}".format(str(err)))
            result = '执行失败'+str(err)
        finally:
            endtime = Config.getCurrentTime()
            return result
            
    # 获取测试案例
    def getTestCases(self):
        try:
            starttime = Config.getCurrentTime()
            cur = selectone('SELECT name,product,steps FROM apicases WHERE id=%s', [self.id])
            cases = [dict(name=row[0],product=row[1], steps=row[2]) for row in cur]

            case_name = cases[0]['name']
            product = cases[0]['product']
            list_apis = cases[0]['steps'] = cases[0]['steps'].split(';')
            results = []
            status = '成功'
            err = ''
            for i in range(len(list_apis)):
                cases_cur = selectone('SELECT name, path, method, request, checks from apidates WHERE case_name=%s and name=%s', [case_name, list_apis[i]+'_'+str(i)])
                cases_list = [dict(name=row[0], path=row[1], method=row[2], request=row[3],checks=row[4]) for row in cases_cur][0]
                name = cases_list['name']
                url = cases_list['path']
                method = cases_list['method']
                data = cases_list['request']
                headers = para_headers

                result = {'case_name':case_name,'name':name,'url':url,'method':method,'error':'','status':'成功'}
                
                try:
                    r = eval('requests.'+method + '(url, headers=headers, data=data, verify=False)')
                
                    if r.status_code == 200:
                        result['status'] = "成功"
                    else:
                        result['status'] = "失败"
                except Exception as api_err:
                    result['status'] = "失败"
                    result['error'] = api_err
                    status = '失败'
                finally:
                    results.append(result)
        except Exception as err:
            LogUtility.logger.debug(
                "Failed running test siutes, error message: {}".format(str(err)))
            status = "失败"
        finally:
            endtime = Config.getCurrentTime()
            spenttime = Config.timeDiff(starttime,endtime)
            return {'case_name':case_name,'results':results,'status':status,'starttime':starttime,'spenttime':spenttime,'error':str(err)}

    # 获取测试集
    def getTestSiutes(self):
        try:
            starttime = Config.getCurrentTime()
            cur = selectone('SELECT name,steps FROM apisitues WHERE id=%s', [self.id])
            cases = [dict(name=row[0], steps=row[1]) for row in cur]
            cases_name = cases[0]['name']
            cases_step = cases[0]['steps'].split(';')
            count = len(cases_step)
            all_id = []
            for step in cases_step:
                cur_step = selectone('select id from apicases where name =%s',[step])
                cases_step = [dict(id=row[0]) for row in cur_step]
                all_id.append(cases_step[0]['id'])
            addUpdateDel('delete from report where type=%s and username=%s',['api',self.username])
            for ids in all_id:
                self.id = str(ids)
                res = self.getTestCases()
                addUpdateDel('insert into report (case_name,type,status,spenttime,error,username,create_date) values (%s,%s,%s,%s,%s,%s,%s)',[res['case_name'],'api',res['status'],res['spenttime'],res['error'],self.username,time.strftime('%Y-%m-%d %X', time.localtime(time.time()))])
        except Exception as e:
            LogUtility.logger.debug(
                "Failed running test siutes, error message: {}".format(str(e)))
        finally:
            endtime = Config.getCurrentTime()
            spenttime = Config.timeDiff(starttime,endtime)
            testPass_count = selectone('select count(1) from report where status =%s and type=%s and username=%s',['成功','api',self.username])[0][0]
            testFail_count = selectone('select count(1) from report where status =%s and type=%s and username=%s',['失败','api',self.username])[0][0]
            testSkip_count = count-testPass_count-testFail_count
            cur = selectone('select case_name,type,status,spenttime,error,username from report where type="api" and username=%s',[self.username])
            cases_report = [dict(case_name=row[0], type=row[1], status=row[2], spenttime=row[3], error=row[4], username=row[5]) for row in cur]
            content={'cases_name':cases_name,'count':count,'testPass_count':testPass_count,'testFail_count':testFail_count,'testSkip_count':testSkip_count,'starttime':starttime,'spenttime':spenttime,'cases_report':cases_report}
            report(content,path_api)

if __name__ == "__main__":
    newrun = RunTests('3')
    print(newrun.getTestSiutes())
