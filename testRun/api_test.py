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
            url = sicap_url + cases['path']
            method = cases['method']
            if cases['request'] == '':
                cases['request'] = '{}'
            else:
                cases['request'] = cases['request']
            data = str_to_json(cases['request'])

            headers = para_headers
            r = eval('requests.'+method +
                     '(url=url, headers=headers, data=data, verify=False)')
            result = [name, url, method, jsonFormat(data,4), jsonFormat(r.text,4)]

        except Exception as err:
            LogUtility.logger.debug(
                "接口运行失败, 错误信息是: {}".format(str(err)))
            result = [name, url, method, data, str(err)]
        finally:
            endtime = Config.getCurrentTime()
            return result

    # 获取测试案例
    def getTestCases(self):
        starttime = Config.getCurrentTime()

        # 获取测试用例步骤
        cur = selectone('SELECT name,product,pre_steps,next_steps FROM apicases WHERE id=%s', [self.id])
        cases = [dict(name=row[0], product=row[1], pre_steps=row[2],next_steps=row[3]) for row in cur]
        pre_steps = cases[0]['pre_steps'].split('\r\n')
        next_steps = cases[0]['next_steps'].split('\r\n')
        case_name = cases[0]['name']
        pre_steps.append(case_name)
        all_steps = pre_steps + next_steps

        # 获取测试用例接口明细
        list_apis = ()
        for all_step in all_steps:
            if all_step == '':
                continue
            apis_cur = selectone('SELECT case_name,name FROM apidates WHERE case_name = %s', [all_step])
            list_apis += apis_cur

        # 创建结果存储
        results = []
        finally_results = {'case_name': case_name, 'results': '','status': '', 'starttime': starttime, 'spenttime': '', 'error': []}
        status = '成功'
        headers = para_headers
        # 执行接口
        for i in range(len(list_apis)):
            LogUtility.logger.debug("测试用例运行提示信息: {}".format('执行第'+str(i+1)+'次'))
            cases_cur = selectone('SELECT name, path, method, request, checks, parameter from apidates WHERE case_name=%s and name=%s', [list_apis[i][0], list_apis[i][1]])
            cases_list = [dict(name=row[0], path=row[1], method=row[2], request=row[3], checks=row[4], parameter=row[5]) for row in cases_cur][0]
            name = cases_list['name']
            url = sicap_url + cases_list['path']
            method = cases_list['method']
            parameter = cases_list['parameter']
            if cases_list['request'] == '':
                cases_list['request'] = '{}'
            else:
                cases_list['request'] = cases_list['request']
            # strict=False用于处理\"无法正常转换的问题
            LogUtility.logger.debug("测试用例运行提示信息: {}".format('请求数据是'+cases_list["request"]))
            data = json.loads(cases_list['request'],strict=False)
            
            # 获取随机名称
            make_random_name(data)

            LogUtility.logger.debug("测试用例运行提示信息: {}".format('临时存储的数据'+str(results)))
            # 获取上一个接口的参数覆盖到新接口的请求中
            if  method == 'post':
                if i>0:
                    replace_param=results[-1]['new_param']
                    if replace_param != '':
                        get_targe_value(data,replace_param)
            elif method == 'get':
                if i>0:
                    replace_param=results[-1]['new_param']
                    url = get_value(url,replace_param)
            LogUtility.logger.debug("测试用例运行提示信息: {}".format('替换后的请求数据是'+str(data)))
            LogUtility.logger.debug("测试用例运行提示信息: {}".format('替换后的URL是'+url))
            data = json.dumps(data)
            checks = cases_list['checks']
            err = ''
            result = {'case_name': case_name, 'name': name, 'url': url,'method': method, 'error': [], 'status': '失败','new_param':''}
            try:
                LogUtility.logger.debug("测试用例运行提示信息: {}".format('发起新的请求'+url))
                r = eval('requests.'+method + '(url, headers=headers, data=data, verify=False)')
                if 'Set-Cookie' in r.headers.keys():
                    headers['Cookie'] = r.headers['Set-Cookie'].split(';')[0]
                if parameter!='':
                    parameter = eval(parameter)
                else:
                    parameter=parameter
                if r.text == '':
                    content = {}
                else:
                    content = json.loads(r.text)
                LogUtility.logger.debug("测试用例运行提示信息: {}".format('响应报文'+str(content)))
                LogUtility.logger.debug("测试用例运行提示信息: {}".format('参数'+str(parameter)))
                
                if parameter != '' and isinstance(parameter,list):
                    if results[-1]['new_param'] == '':
                        result['new_param']=traverse_take_field(content,parameter,{},None)
                    else:
                        result['new_param']=Merge(results[-1]['new_param'],traverse_take_field(content,parameter,{},None))
                    LogUtility.logger.debug("测试用例运行提示信息: {}".format('获取的需要转换的参数是'+str(result['new_param'])))
                else:
                    result['new_param']=''
                    LogUtility.logger.debug("测试用例运行提示信息: {}".format('参数不是列表或为空'))
                if checks == '':
                    if r.status_code == 200:
                        result['status'] = "成功"
                    else:
                        result['status'] = "失败"
                        result['error'].append("断言失败：状态码不正确")
                        status = '失败'
                        break
                else:
                    LogUtility.logger.debug("测试用例运行提示信息: {}".format('处理过用于对比的content '+str(content)))
                    LogUtility.logger.debug("测试用例运行提示信息: {}".format('原始checks '+checks))
                    LogUtility.logger.debug("测试用例运行提示信息: {}".format('处理过用于对比的checks '+str(json.loads(checks))))
                    if compare_two_dict(content,json.loads(checks)) == 'PASS':
                        result['status'] = "成功"
                    else:
                        result['status'] = "失败"
                        result['error'].append("断言失败：检查项不正确")
                        status = '失败'
                        break
            except Exception as api_err:
                LogUtility.logger.debug("测试用例运行失败,错误信息: {}".format(str(api_err)))
                result['status'] = "失败"
                result['error'].append(str(api_err))
                status = '失败'
                break
            finally:
                addUpdateDel('update apicases set exec_result=%s where id=%s',[status,self.id])
                results.append(result)

        endtime = Config.getCurrentTime()
        spenttime = Config.timeDiff(starttime, endtime)
        finally_results['error'] = result['error']
        finally_results['results'] = results
        finally_results['status'] = status
        finally_results['spenttime'] = spenttime
        return finally_results

    # 获取测试集
    def getTestSiutes(self):
        try:
            starttime = Config.getCurrentTime()
            cur = selectone('SELECT name,exec_mode,steps FROM apisitues WHERE id=%s', [self.id])
            cases = [dict(name=row[0], exec_mode=row[1], steps=row[2]) for row in cur]
            if cases == []:
                exec_mode = '按失败'
                cases_name = '失败'
            else:
                cases_name = cases[0]['name']
                exec_mode = cases[0]['exec_mode']
                cases_step = cases[0]['steps'].split('\r\n')

            if exec_mode == '按用例':
                steps_case = cases_step
            elif exec_mode == '按模块':
                steps_case = []
                for case_step in cases_step:
                    cur_model= selectone("SELECT name FROM apicases WHERE model = %s and activity='1'",[cases_step])
                    cases_dict = [dict(name=row[0]) for row in cur_model]
                    case_step_list = [case['name'] for case in cases_dict]
                    steps_case.extend(case_step_list)
            elif exec_mode == '按版本':
                steps_case = []
                for case_step in cases_step:
                    cur_version= selectone("SELECT name FROM apicases WHERE version = %s and activity='1'",[cases_step])
                    cases_dict = [dict(name=row[0]) for row in cur_version]
                    case_step_list = [case['name'] for case in cases_dict]
                    steps_case.extend(case_step_list)
            elif exec_mode == '按失败':
                cur = selectall('SELECT case_name FROM report a WHERE a.`status` = \'失败\' and type = \'api\'')
                steps_case = []
                for case in cur:
                    steps_case.append(case[0])

            count = len(steps_case)

            all_id = []
            for step in cases_step:
                if step.startswith('#'):
                    continue
                cur_step = selectone('select id,product from apicases where name =%s', [step])
                cases_step = [dict(id=row[0],product=row[1]) for row in cur_step]
                if cases_step == []:
                    continue
                all_id.append([cases_step[0]['id'],cases_step[0]['product']])
            addUpdateDel('delete from report where type=%s and username=%s', ['api', self.username])
            for ids in all_id:
                self.id = str(ids[0])
                res = self.getTestCases()
                addUpdateDel('insert into report (case_name,type,product,status,spenttime,error,username,create_date) values (%s,%s,%s,%s,%s,%s,%s,%s)', [
                             res['case_name'], 'api', str(ids[1]), res['status'], res['spenttime'], str(res['error']), self.username, time.strftime('%Y-%m-%d %X', time.localtime(time.time()))])
        except Exception as err:
            LogUtility.logger.debug(
                "测试用例运行失败，错误信息是: {}".format(str(err)))
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
            cases_report = [dict(case_name=row[0], type=row[1], product=row[2],status=row[3], spenttime=row[4], error=eval(row[5]), username=row[6]) for row in cur]
            content = {'cases_name': cases_name, 'count': count, 'testPass_count': testPass_count, 'testFail_count': testFail_count,
                       'testSkip_count': testSkip_count, 'starttime': starttime, 'spenttime': spenttime, 'cases_report': cases_report}
            report(cases_name, content, Config.path_api)


if __name__ == "__main__":
    newrun = RunTests('3')
    print(newrun.getTestSiutes())
