# coding-utf-8

import requests
import time
from Common.db_config import *
from Common.report import *
from Common.Config import *
from Common import Config, LogUtility
import json


class RunTests(object):

    def __init__(self, id, username):

        self.id = id
        self.username = username

        LogUtility.CreateLoggerFile(
            path_log+"/apilog_"+time.strftime("%Y_%m_%d_%H_%M_%S"))

    # 获取接口
    def getApis(self):
        try:
            starttime = Config.getCurrentTime()

            cur = selectone(
                'SELECT name, path, method, request, checks from apiset WHERE id=%s', [self.id])
            cases = [dict(name=row[0], path=row[1], method=row[2],
                          request=row[3], checks=row[4]) for row in cur][0]

            name = cases['name']
            url = cases['path']
            method = cases['method']
            data = json.loads(cases['request'])

            headers = {}

            r = eval('requests.'+method +
                     '(url=url, headers=headers, data=data, verify=False)')
            result = [name, url, method, data, r.text]

        except Exception as err:
            LogUtility.logger.debug(
                "Failed running test apis, error message: {}".format(str(err)))
            result = [name, url, method, data, str(err)]
        finally:
            endtime = Config.getCurrentTime()
            return result

    # 获取测试案例
    def getTestCases(self):
        starttime = Config.getCurrentTime()
        cur = selectone(
            'SELECT name,product,steps FROM apicases WHERE id=%s', [self.id])
        cases = [dict(name=row[0], product=row[1], steps=row[2])
                 for row in cur]

        case_name = cases[0]['name']
        product = cases[0]['product']
        apis_cur = selectone('SELECT name FROM apidates WHERE case_name=%s', [case_name])
        list_apis = [dict(name=row[0]) for row in apis_cur]
        list_apis = [list_api['name'] for list_api in list_apis]
        results = []
        finally_results = {'case_name': case_name, 'results': '',
                           'status': '', 'starttime': starttime, 'spenttime': '', 'error': ''}
        status = '成功'
        for i in range(len(list_apis)):
            cases_cur = selectone('SELECT name, path, method, request, checks, parameter from apidates WHERE case_name=%s and name=%s', [
                                  case_name, list_apis[i]])
            cases_list = [dict(name=row[0], path=row[1], method=row[2], request=row[3], checks=row[4], parameter=row[5]) for row in cases_cur][0]
            name = cases_list['name']
            url = cases_list['path']
            method = cases_list['method']
            parameter = cases_list['parameter']
            data = eval(cases_list['request'])
            if i>0 :
                replace_param=results[-1]['new_param']
                get_targe_value(data,replace_param)
            
            checks = cases_list['checks']

            headers = para_headers
            err = ''
            result = {'case_name': case_name, 'name': name, 'url': url,
                      'method': method, 'error': '', 'status': '失败','new_param':''}

            try:
                true=True
                r = eval('requests.'+method +
                         '(url, headers=headers, data=data, verify=False)')
                if parameter!='':
                    parameter = eval(parameter)
                else:
                    parameter=parameter
                content = eval(r.text)
                if parameter != '' and isinstance(parameter,list):
                    result['new_param']=traverse_take_field(content,parameter)
                
                if r.text == checks:
                    result['status'] = "成功"
                else:
                    result['status'] = "失败"
                    result['error'] = "断言失败"
                    status = '失败'
                    finally_results['error'] = result['error']
                    break
            except Exception as api_err:
                LogUtility.logger.debug(
                    "Failed running test siutes, error message: {}".format(str(err)))
                result['status'] = "失败"
                result['error'] = str(api_err)
                status = '失败'
                break
            finally:
                results.append(result)

        endtime = Config.getCurrentTime()
        spenttime = Config.timeDiff(starttime, endtime)
        finally_results['results'] = results
        finally_results['status'] = status
        finally_results['spenttime'] = spenttime
        return finally_results

    # 获取测试集
    def getTestSiutes(self):
        try:
            starttime = Config.getCurrentTime()
            cur = selectone(
                'SELECT name,steps FROM apisitues WHERE id=%s', [self.id])
            cases = [dict(name=row[0], steps=row[1]) for row in cur]
            cases_name = cases[0]['name']
            cases_step = cases[0]['steps'].split('\r\n')
            count = len(cases_step)
            all_id = []
            for step in cases_step:
                cur_step = selectone(
                    'select id,product from apicases where name =%s', [step])
                cases_step = [dict(id=row[0],product=row[1]) for row in cur_step]
                all_id.append([cases_step[0]['id'],cases_step[0]['product']])
            addUpdateDel('delete from report where type=%s and username=%s', [
                         'api', self.username])
            for ids in all_id:
                self.id = str(ids[0])
                res = self.getTestCases()
                addUpdateDel('insert into report (case_name,type,product,status,spenttime,error,username,create_date) values (%s,%s,%s,%s,%s,%s,%s,%s)', [
                             res['case_name'], 'api', str(ids[1]), res['status'], res['spenttime'], res['error'], self.username, time.strftime('%Y-%m-%d %X', time.localtime(time.time()))])
        except Exception as err:
            LogUtility.logger.debug(
                "Failed running test siutes, error message: {}".format(str(err)))
        finally:
            endtime = Config.getCurrentTime()
            spenttime = Config.timeDiff(starttime, endtime)
            testPass_count = selectone('select count(1) from report where status =%s and type=%s and username=%s', [
                                       '成功', 'api', self.username])[0][0]
            testFail_count = selectone('select count(1) from report where status =%s and type=%s and username=%s', [
                                       '失败', 'api', self.username])[0][0]
            testSkip_count = count-testPass_count-testFail_count
            cur = selectone(
                'select case_name,type,product,status,spenttime,error,username from report where type="api" and username=%s', [self.username])
            cases_report = [dict(case_name=row[0], type=row[1], product=row[2],status=row[3], spenttime=row[4], error=row[5], username=row[6]) for row in cur]
            content = {'cases_name': cases_name, 'count': count, 'testPass_count': testPass_count, 'testFail_count': testFail_count,
                       'testSkip_count': testSkip_count, 'starttime': starttime, 'spenttime': spenttime, 'cases_report': cases_report}
            report(content, Config.path_api)


if __name__ == "__main__":
    newrun = RunTests('3')
    print(newrun.getTestSiutes())
