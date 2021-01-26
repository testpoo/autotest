# coding-utf-8

import requests
import time
from Common.db_config import *
from Common.report import *

from Common import Config, LogUtility, Extend

# word cover program
def cover(keyword):
    cur = selectall('SELECT keyword, template from uiset')
    cases = [dict(keyword=row[0], template=row[1]) for row in cur]
    keywords = [[case['keyword'],case['template']] for case in cases]
    for key in keywords:
        if keyword.split('|',1)[0] == key[0].split('|',1)[0]:
            func = key[1]
            paras = keyword.split('|',1)[1]
            comend = func + paras
            return comend

class RunUiTests(object):

    def __init__(self, id,username):

        self.id = id
        self.username = username

        LogUtility.CreateLoggerFile(
            Config.path_log+"/uilog_"+time.strftime("%Y_%m_%d_%H_%M_%S"))
            
    # 获取测试案例
    def getTestCases(self):

        try:
            starttime = Config.getCurrentTime()
            Screenshottime = time.strftime("%Y_%m_%d_%H_%M_%S")
            cur = selectone('SELECT name,pre_steps, steps, next_steps from uicases WHERE id=%s', [self.id])
            cases = [dict(name=row[0], pre_steps=row[1], steps=row[2], next_steps=row[3]) for row in cur][0]
            case_name = cases['name']
            
            if cases['pre_steps'] == '':
                pre_steps = []
            else:
                pre_steps = []
                pre_names = cases['pre_steps'].split('\r\n')
                while '' in pre_names:
                    pre_names.remove('')
                for pre_name in pre_names:
                    pre_step = selectone('SELECT steps FROM uicases WHERE name = %s',[pre_name])[0][0].split('\r\n')
                    pre_steps.extend(pre_step)

            if cases['next_steps'] == '':
                next_steps = []
            else:
                next_steps = []
                next_names = cases['next_steps'].split('\r\n')

                while '' in next_names:
                    next_names.remove('')
                for next_name in next_names:
                    next_step = selectone('SELECT steps FROM uicases WHERE name = %s',[next_name])[0][0].split('\r\n')
                    next_steps.extend(next_step)
                    
            steps = pre_steps+cases['steps'].split('\r\n')
            while '' in steps:
                steps.remove('')

            TestCase = Extend.Extend()
            
            result = {'case_name':case_name,'status':'失败','starttime':starttime,'Screenshot':[],'spenttime':'','error':[]}

            for step in steps:
                action = cover(step)
                time.sleep(0.3)
                LogUtility.logger.debug("执行步骤: {}".format(action))
                eval('TestCase.'+action)

            result['status'] = "成功"

        except Exception as err:
            LogUtility.logger.debug(
                "测试用例运行失败, 错误信息是: {}".format(str(err)))
            result['status'] = '失败'
            result['error'].append("用例错误："+str(err))
            TestCase.getScreenshot(Config.Screenshot+'/'+case_name+'_'+Screenshottime+'.png')
            result['Screenshot'].append(Config.img_to_base64(case_name+'_'+Screenshottime+'.png'))
        finally:
            try:
                if next_steps != []:
                    for next_step in next_steps:
                        action = cover(next_step)
                        time.sleep(0.5)
                        LogUtility.logger.debug("执行步骤: {}".format(action))
                        eval('TestCase.'+action)
            except Exception as next_err:
                LogUtility.logger.debug("后置事务执行出错: {}".format(str(next_err)))
                try:
                    result['status'] = '失败'
                    result['error'].append("后置错误："+str(next_err))
                    TestCase.getScreenshot(Config.Screenshot+'/'+case_name+'_next_'+Screenshottime+'.png')
                    result['Screenshot'].append(Config.img_to_base64(case_name+'_next_'+Screenshottime+'.png'))
                except Exception as next_err:
                    LogUtility.logger.debug("后置事务执行出错: {}".format(str(next_err)))
            TestCase.quit()
            endtime = Config.getCurrentTime()
            spenttime = Config.timeDiff(starttime,endtime)
            result['spenttime'] = spenttime
            addUpdateDel('update uicases set exec_result=%s where id=%s',[result['status'],self.id])
            return result

    # 获取测试集
    def getTestSiutes(self):
        try:
            starttime = Config.getCurrentTime()

            cur = selectone('SELECT name, exec_mode, steps, description FROM uisitues where id=%s',[self.id])
            cases = [dict(name=row[0], exec_mode=row[1], steps=row[2], description=row[3]) for row in cur]
            if cases == []:
                exec_mode = '按失败'
                cases_name = '失败'
            else:
                cases_step = cases[0]['steps'].split('\r\n')
                exec_mode = cases[0]['exec_mode']
                cases_name = cases[0]['name']
            
            if exec_mode == '按用例':
                steps_case = cases_step
            elif exec_mode == '按用户':
                steps_case = []
                for case_step in cases_step:
                    cur_name= selectone("SELECT name FROM uicases WHERE username = %s and activity='3'",[cases_step])
                    cases_dict = [dict(name=row[0]) for row in cur_name]
                    case_step_list = [case['name'] for case in cases_dict]
                    steps_case.extend(case_step_list)
            elif exec_mode == '按模块':
                steps_case = []
                for case_step in cases_step:
                    cur_model= selectone("SELECT name FROM uicases WHERE model = %s and activity='3'",[cases_step])
                    cases_dict = [dict(name=row[0]) for row in cur_model]
                    case_step_list = [case['name'] for case in cases_dict]
                    steps_case.extend(case_step_list)
            elif exec_mode == '按版本':
                steps_case = []
                for case_step in cases_step:
                    cur_version= selectone("SELECT name FROM uicases WHERE version = %s and activity='3'",[cases_step])
                    cases_dict = [dict(name=row[0]) for row in cur_version]
                    case_step_list = [case['name'] for case in cases_dict]
                    steps_case.extend(case_step_list)
            elif exec_mode == '按失败':
                cur = selectall('SELECT case_name FROM report a WHERE a.`status` = \'失败\' and type = \'ui\'')
                steps_case = []
                for case in cur:
                    steps_case.append(case[0])

            count = len(steps_case)
            all_id = []
            for step in steps_case:
                if step.startswith('#'):
                    continue
                cur_step = selectone('select id, product from uicases where name =%s',[step])
                cases_step = [dict(id=row[0], product=row[1]) for row in cur_step]
                if cases_step == []:
                    continue
                all_id.append([cases_step[0]['id'], cases_step[0]['product']])
            addUpdateDel('delete from report where type=%s and username=%s',['ui',self.username])
            for ids in all_id:
                self.id = str(ids[0])
                res = self.getTestCases()
                addUpdateDel('insert into report (case_name,type,product,status,Screenshot,spenttime,error,username,create_date) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)',[res['case_name'],'ui',str(ids[1]),res['status'],str(res['Screenshot']),res['spenttime'],str(res['error']),self.username,time.strftime('%Y-%m-%d %X', time.localtime(time.time()))])

        except Exception as e:
            LogUtility.logger.debug(
                "测试集运行失败, 错误信息是: {}".format(str(e)))
        finally:
            endtime = Config.getCurrentTime()
            spenttime = Config.timeDiff(starttime,endtime)
            testPass_count = selectone('select count(1) from report where status =%s and type=%s and username=%s',['成功','ui',self.username])[0][0]
            testFail_count = selectone('select count(1) from report where status =%s and type=%s and username=%s',['失败','ui',self.username])[0][0]
            testSkip_count = count-testPass_count-testFail_count
            cur = selectone('select case_name,type,product,status,Screenshot,spenttime,error,username from report where type="ui" and username=%s',[self.username])
            cases_report = [dict(case_name=row[0], type=row[1], product=row[2],status=row[3], Screenshot=eval(row[4]),  spenttime=row[5], error=eval(row[6]), username=row[7]) for row in cur]
            content={'cases_name':cases_name,'count':count,'testPass_count':testPass_count,'testFail_count':testFail_count,'testSkip_count':testSkip_count,'starttime':starttime,'spenttime':spenttime,'cases_report':cases_report}
            report(cases_name,content,Config.path_ui)

if __name__ == "__main__":
    newrun = RunUiTests('5','puyawei')
