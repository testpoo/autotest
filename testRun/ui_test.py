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
        if keyword.split('|')[0] == key[0].split('|')[0]:
            func = key[1]
            paras = keyword.split('|')[1]
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
                for pre_name in pre_names:
                    pre_step = selectone('SELECT steps FROM uicases WHERE name = %s',[pre_name])[0][0].split('\r\n')
                    pre_steps.extend(pre_step)

            if cases['next_steps'] == '':
                next_steps = []
            else:
                next_steps = []
                next_names = cases['next_steps'].split('\r\n')
                for next_name in next_names:
                    next_step = selectone('SELECT steps FROM uicases WHERE name = %s',[next_name])[0][0].split('\r\n')
                    next_steps.extend(next_step)
            
            steps = pre_steps+cases['steps'].split('\r\n')+next_steps

            TestCase = Extend.Extend()
            
            result = {'case_name':case_name,'status':'失败','starttime':starttime,'spenttime':'','error':''}
            print(steps)
            for step in steps:
                action = cover(step)
                eval('TestCase.'+action)

            result['status'] = "成功"

        except Exception as err:
            TestCase.getScreenshot(Config.Screenshot+'/'+case_name+'_'+Screenshottime+'.png')
            LogUtility.logger.debug(
                "Failed running test siutes, error message: {}".format(str(err)))
            result['status'] = '失败'
            result['error'] = str(err)
        finally:
            TestCase.quit()
            endtime = Config.getCurrentTime()
            spenttime = Config.timeDiff(starttime,endtime)
            result['spenttime'] = spenttime
            return result

    # 获取测试集
    def getTestSiutes(self):
        try:
            starttime = Config.getCurrentTime()

            cur = selectone('SELECT name, steps, description FROM uisitues where id=%s',[self.id])
            cases = [dict(name=row[0], steps=row[1], description=row[2]) for row in cur]
            cases_step = cases[0]['steps'].split('\r\n')
            cases_name = cases[0]['name']
            count = len(cases_step)
            all_id = []
            for step in cases_step:
                cur_step = selectone('select id, product from uicases where name =%s',[step])
                cases_step = [dict(id=row[0], product=row[1]) for row in cur_step]
                all_id.append([cases_step[0]['id'], cases_step[0]['product']])
            addUpdateDel('delete from report where type=%s and username=%s',['ui',self.username])
            for ids in all_id:
                self.id = str(ids[0])
                res = self.getTestCases()
                addUpdateDel('insert into report (case_name,type,product,status,spenttime,error,username,create_date) values (%s,%s,%s,%s,%s,%s,%s,%s)',[res['case_name'],'ui',str(ids[1]),res['status'],res['spenttime'],res['error'],self.username,time.strftime('%Y-%m-%d %X', time.localtime(time.time()))])

        except Exception as e:
            LogUtility.logger.debug(
                "Failed running test siutes, error message: {}".format(str(e)))
        finally:
            endtime = Config.getCurrentTime()
            spenttime = Config.timeDiff(starttime,endtime)
            testPass_count = selectone('select count(1) from report where status =%s and type=%s and username=%s',['成功','ui',self.username])[0][0]
            testFail_count = selectone('select count(1) from report where status =%s and type=%s and username=%s',['失败','ui',self.username])[0][0]
            testSkip_count = count-testPass_count-testFail_count
            cur = selectone('select case_name,type,product,status,spenttime,error,username from report where type="ui" and username=%s',[self.username])
            cases_report = [dict(case_name=row[0], type=row[1], product=row[2],status=row[3], spenttime=row[4], error=row[5], username=row[6]) for row in cur]
            content={'cases_name':cases_name,'count':count,'testPass_count':testPass_count,'testFail_count':testFail_count,'testSkip_count':testSkip_count,'starttime':starttime,'spenttime':spenttime,'cases_report':cases_report}
            report(content,Config.path_ui)

if __name__ == "__main__":
    newrun = RunUiTests('5','puyawei')
    print(newrun.getTestCases())
