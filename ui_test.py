# coding-utf-8

import requests
import time
from db_config import *
from report import *

from Common import Config, LogUtility, Extend
from parm import *

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
            path_log+"_"+time.strftime("%Y_%m_%d_%H_%M_%S"))
            
    # 获取测试案例
    def getTestCases(self):

        try:
            starttime = Config.getCurrentTime()

            cur = selectone('SELECT name, steps from uicases WHERE id=%s', [self.id])
            cases = [dict(name=row[0], steps=row[1]) for row in cur][0]
            case_name = cases['name']
            steps = cases['steps'].split(';')

            TestCase = Extend.Extend()

            for step in steps:
                action = cover(step)
                eval('TestCase.'+action)

            TestCase.quit()
            err=''
            status = '成功'
        except Exception as err:
            LogUtility.logger.debug(
                "Failed running test siutes, error message: {}".format(str(err)))
            status = '失败'
            err = str(err)
            print('失败了吗')
        finally:
            endtime = Config.getCurrentTime()
            spenttime = Config.timeDiff(starttime,endtime)
            print(case_name,status,starttime,spenttime,str(err))
            return (case_name,status,starttime,spenttime,str(err))

    # 获取测试集
    def getTestSiutes(self):
        try:
            starttime = Config.getCurrentTime()

            cur = selectone('SELECT name, steps, description FROM uisitues where id=%s',[self.id])
            cases = [dict(name=row[0], steps=row[1], description=row[2]) for row in cur]
            cases_step = cases[0]['steps'].split(';')
            cases_name = cases[0]['name']

            count = len(cases_step)
            all_id = []
            for step in cases_step:
                cur_step = selectone('select id from uicases where name =%s',[step])
                cases_step = [dict(id=row[0]) for row in cur_step]
                all_id.append(cases_step[0]['id'])
            addUpdateDel('delete from report where type=%s and username=%s',['ui',self.username])
            for ids in all_id:
                self.id = str(ids)
                res = self.getTestCases()
                addUpdateDel('insert into report (case_name,type,status,spenttime,error,username,create_date) values (%s,%s,%s,%s,%s,%s,%s)',[res[0],'ui',res[1],res[3],res[4],self.username,time.strftime('%Y-%m-%d %X', time.localtime(time.time()))])

        except Exception as e:
            LogUtility.logger.debug(
                "Failed running test siutes, error message: {}".format(str(e)))
            print(str(e))
        finally:
            endtime = Config.getCurrentTime()
            spenttime = Config.timeDiff(starttime,endtime)
            testPass_count = selectone('select count(1) from report where status =%s and type=%s and username=%s',['成功','ui',self.username])[0][0]
            testFail_count = selectone('select count(1) from report where status =%s and type=%s and username=%s',['失败','ui',self.username])[0][0]
            testSkip_count = count-testPass_count-testFail_count
            cur = selectone('select case_name,type,status,spenttime,error,username from report where type="ui" and username=%s',[self.username])
            cases_report = [dict(case_name=row[0], type=row[1], status=row[2], spenttime=row[3], error=row[4], username=row[5]) for row in cur]
            content={'cases_name':cases_name,'count':count,'testPass_count':testPass_count,'testFail_count':testFail_count,'testSkip_count':testSkip_count,'starttime':starttime,'spenttime':spenttime,'cases_report':cases_report}
            report(content,path_ui)

if __name__ == "__main__":
    newrun = RunUiTests('5','puyawei')
    print(newrun.getTestCases())
