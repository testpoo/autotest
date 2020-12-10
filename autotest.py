# coding=utf-8

import os
import math
import pymysql
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
import time
from contextlib import closing
import json

from Common.db_config import *
from Common.Config import *
import requests
from testRun.api_test import RunTests
from testRun.ui_test import RunUiTests

# configuration
DATABASE = 'flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
#DEBUG = False
#SECRET_KEY = '\xcfZs\xf8\x0cQ\x02l|\xb1\xe0\xaal\x07\x0c\xaf\x9b\x8f3<\x9a]\xfb\xf7'

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

#app.config.from_envvar('FLASKR_SETTINGS', silent=True)

# 导入time
@app.context_processor
def get_current_time():
    def get_time(timeFormat="%b %d, %Y - %H:%M:%S"):
        return time.strftime(timeFormat)
    return dict(current_time=get_time)

@app.context_processor
def get_zh_name():
    def get_name(username):
        zname = selectone('select zh_name from user where username = %s',(username,))
        return zname[0][0]
    return dict(get_name=get_name)

# 首页
@app.route('/')
def initial():
    return redirect(url_for('login'))

# 登陆页面
@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('logged_in'):
        return redirect(url_for('index',current_user = session['username']))
    error = None
    result = selectall('select username,password from user')
    date = []
    for i in list(range(len(result))):
        date.append(result[i][0])
    if request.method == 'POST':
        session['username']=request.form['username']
        if request.form['username'] in date:
            cur = selectone('select username,password from user where username = %s',(request.form['username'],))
            uname,pw = cur[0]
            if request.form['username'] != uname:
                error = '无效的用户名'
            elif request.form['password'] != decrypt(pw):
                error = '无效的密码'
            elif request.form['username'] == 'admin':
                session['logged_in'] = True
                addUpdateDel('update user set last_login = %s where username = %s',[time.strftime('%Y-%m-%d %X', time.localtime(time.time())), session['username']])
                flash('你已经登陆管理员...')
                return redirect(url_for('index',current_user = session['username']))
            else:
                session['logged_in'] = True
                addUpdateDel('update user set last_login = %s where username = %s',[time.strftime('%Y-%m-%d %X', time.localtime(time.time())), session['username']])
                flash('你已经登陆...')
                return redirect(url_for('index',current_user = session['username']))
        else:
            error = '用户名不存在'
    return render_template('login.html', error=error)

@app.route('/<current_user>/')
def index(current_user):
    if session.get('logged_in'):
        return render_template('index.html', username=session['username'],nav=nav, sub_nav_ui = sub_nav_ui, sub_nav_api = sub_nav_api, set_nav=set_nav,pagename = '主页')
    else:
        return redirect(url_for('login'))

###############################
#             UI
###############################

# UI CASES
@app.route('/uicases/<category>/<value>/<int:num>', methods=['GET', 'POST'])
def uicases(category,value,num):
    if not session.get('logged_in'):
        abort(401)
    else:
        error = None
        if category == 'a.name':
            all_Count = selectall('SELECT count(1) FROM uicases a inner join user b on a.username=b.username where activity="1" and '+category+' like "%'+value+'%"')[0][0]
        else:
            all_Count = selectall('SELECT count(1) FROM uicases a inner join user b on a.username=b.username where activity="1" and '+category+'="'+value+'"')[0][0]
        all_Page = math.ceil(all_Count/page_Count)
        cur_usernames=selectall('SELECT b.zh_name FROM uicases a inner join user b ON a.username=b.username WHERE a.activity="1" GROUP BY a.username')
        usernames=[dict(zh_name=row[0]) for row in cur_usernames]
        cur_versions=selectall('SELECT version FROM uicases WHERE activity="1" group by version')
        versions=[dict(version=row[0]) for row in cur_versions]
        cur_models=selectall('SELECT model FROM uicases WHERE activity="1" group by model')
        models=[dict(model=row[0]) for row in cur_models]
        if request.method == 'POST':
            if request.form['select-model'].strip() == '':
                category = '1'
                value ='1'
            elif request.form['select-model'].strip() == '按名称' and request.form['query-name'].strip() != '':
                category = 'a.name'
                value = request.form['query-name']
            elif request.form['select-model'].strip() == '按版本' and request.form['query-version'].strip() != '':
                category = 'a.version'
                value = request.form['query-version']
            elif request.form['select-model'].strip() == '按模块' and request.form['query-model'].strip() != '':
                category = 'a.model'
                value = request.form['query-model']
            elif request.form['select-model'].strip() == '按用户' and request.form['query-username'].strip() != '':
                category = 'b.zh_name'
                value = request.form['query-username']
            return redirect(url_for('uicases',category=category,value=value,num='1'))
        if category == 'a.name':
            cur = selectall('SELECT a.id,a.type,a.version, a.model, a.product, a.name,a.pre_steps, a.steps, a.next_steps,a.description,a.exec_result, b.zh_name, a.create_date FROM uicases a inner join user b on a.username=b.username where activity="1" and '+category+' like "%'+value+'%" order by a.id desc LIMIT '+str((num-1)*page_Count)+','+str(page_Count))
        else:
            cur = selectall('SELECT a.id,a.type,a.version, a.model, a.product, a.name,a.pre_steps, a.steps, a.next_steps,a.description,a.exec_result, b.zh_name, a.create_date FROM uicases a inner join user b on a.username=b.username where activity="1" and '+category+'="'+value+'" order by a.id desc LIMIT '+str((num-1)*page_Count)+','+str(page_Count))
        cases = [dict(id=row[0], type=row[1], version=row[2], model=row[3], product=row[4], name=row[5], pre_steps=row[6], steps=row[7], next_steps=row[8], description=row[9], exec_result=row[10], zh_name=row[11], create_date=row[12]) for row in cur]
        return render_template('ui/uicases.html', SITEURL=SITEURL, username=session['username'], cases=cases, nav=nav, sub_nav_ui = sub_nav_ui, sub_nav_api = sub_nav_api, set_nav=set_nav, operation_exec=operation_exec, all_Page=all_Page,category=category,value=value, num=num,usernames=usernames,versions=versions,models=models,current='uicases',error=error,pagename = 'UI测试用例')

# UI CASE QUERY
@app.route('/uicase_query/<int:id>', methods=['GET', 'POST'])
def uicase_query(id):
    if not session.get('logged_in'):
        abort(401)
    else:
        cur = selectone('SELECT type,version, model, product, name,pre_steps, steps, description,next_steps, username, create_date FROM uicases where id=%s',[id])
        cases = [dict(type=row[0], version=row[1], model=row[2], product=row[3], name=row[4], pre_steps=row[5], steps=row[6], description=row[7], next_steps=row[8], username=row[9], create_date=row[10]) for row in cur]
        return render_template('ui/uicase_query.html', SITEURL=SITEURL, username=session['username'], case=cases[0], nav=nav, sub_nav_ui = sub_nav_ui, sub_nav_api = sub_nav_api, set_nav=set_nav, operation=operation,current='uicases', pagename = '测试用例查看')

# UI CASE DELETE
@app.route('/uicase_delete/<int:id>', methods=['GET', 'POST'])
def uicase_delete(id):
    if not session.get('logged_in'):
        abort(401)
    else:
        uisitue = selectall('select steps from uisitues')
        uisitues = [dict(steps=row[0]) for row in uisitue]
        uisitues = [uisitue['steps'] for uisitue in uisitues]
        uisitues_all=[]
        for uisitue in uisitues:
            uisitues_all.extend(uisitue.split('\r\n'))

        uicase = selectone('select name from uicases where id=%s',[id])
        uicases = [dict(name=row[0]) for row in uicase]
        uicase_name = uicases[0]['name']
        
        uicase_pre_step = selectall('select pre_steps from uicases')
        uicase_pre_steps = [dict(pre_steps=row[0]) for row in uicase_pre_step]
        uicase_pre_steps = [uicase_pre_step['pre_steps'] for uicase_pre_step in uicase_pre_steps]
        uicase_pre_steps_all=[]
        for uicase_pre in uicase_pre_steps:
            if uicase_pre != '':
                uicase_pre_steps_all.extend(uicase_pre.split('\r\n'))

        uicase_next_step = selectall('select next_steps from uicases')
        uicase_next_steps = [dict(next_steps=row[0]) for row in uicase_next_step]
        uicase_next_steps = [uicase_next_step['next_steps'] for uicase_next_step in uicase_next_steps]
        uicase_next_steps_all=[]
        for uicase_next in uicase_next_steps:
            if uicase_next != '':
                uicase_next_steps_all.extend(uicase_next.split('\r\n'))

        if uicase_name in uisitues_all:
            flash("该用例被测试集引用，不能删除~！")
        elif uicase_name in uicase_pre_steps_all or uicase_name in uicase_next_steps_all:
            flash("该案例被其他用例前置/后置事务引用，不能删除~！")
        else:
            cur = addUpdateDel('update uicases set activity = "2" where id=%s',[id])

            cur_uicases_del= selectone("SELECT * FROM uicases where id=%s and activity !=2",[id])
            if cur_uicases_del == ():
                flash('删除成功...')
            else:
                flash('删除失败...')

        return redirect(url_for('uicases',num=1))

# UI CASE EXEC
@app.route('/uicase_exec/<int:id>', methods=['GET', 'POST'])
def uicase_exec(id):
    if not session.get('logged_in'):
        abort(401)
    else:
        error = None
        newrun = RunUiTests(id,session['username'])
        res = newrun.getTestCases()
        return render_template('ui/uicase_exec.html',res=res,SITEURL=SITEURL, username=session['username'], nav=nav, sub_nav_ui = sub_nav_ui, sub_nav_api = sub_nav_api, set_nav=set_nav, operation=operation, pagename = '用例执行结果')

# UI CASE reject
@app.route('/uicase_reject/<int:id>', methods=['GET', 'POST'])
def uicase_reject(id):
    if not session.get('logged_in'):
        abort(401)
    else:
        cur = addUpdateDel('update uicases set activity=0 where id=%s and activity=1',[id])

        cur_uicases_reject= selectone("SELECT * FROM uicases where id=%s and activity=0",[id])
        if cur_uicases_reject == ():
            flash('驳回失败...')
        else:
            flash('驳回成功...')

        return redirect(url_for('uicases',num=1))

# UI SITUES
@app.route('/uisitues/<int:num>', methods=['GET', 'POST'])
def uisitues(num):
    if not session.get('logged_in'):
        abort(401)
    else:
        all_Count = selectall('SELECT count(1) FROM uisitues')[0][0]
        all_Page = math.ceil(all_Count/page_Count)
        cur = selectone('SELECT a.id,a.name,a.exec_mode,a.steps,a.description,b.zh_name,a.create_date FROM uisitues a inner join user b on a.username=b.username order by a.id desc LIMIT %s,%s',[(num-1)*page_Count,page_Count])
        uisitues = [dict(id=row[0], name=row[1], exec_mode=row[2], steps=row[3], description=row[4], username=row[5], create_date=row[6]) for row in cur]
        return render_template('ui/uisitues.html', SITEURL=SITEURL, username=session['username'], uisitues=uisitues, nav=nav, sub_nav_ui = sub_nav_ui, sub_nav_api = sub_nav_api, set_nav=set_nav, operation=operation, all_Page=all_Page,current="uisitues", pagename = '测试集')

# UI SITUES EDIT
@app.route('/uisitue_edit/<int:id>', methods=['GET', 'POST'])
def uisitue_edit(id):
    if not session.get('logged_in'):
        abort(401)
    else:
        cur_issue = selectall('SELECT name FROM uicases where activity="1"')
        uisitues_issue = [dict(name=row[0]) for row in cur_issue]

        cur_model = selectall('SELECT model FROM uicases where activity="1" group by model')
        uisitues_model = [dict(model=row[0]) for row in cur_model]

        cur_version = selectall('SELECT version FROM uicases where activity="1" group by version')
        uisitues_version = [dict(version=row[0]) for row in cur_version]

        cur = selectone('SELECT name, steps, description FROM uisitues where id=%s',[id])
        cases = [dict(name=row[0], steps=row[1], description=row[2]) for row in cur]
        if request.method == 'POST':
            if request.form['steps'].strip == '':
                error = '必输项不能为空'
            else:
                addUpdateDel('update uisitues set steps=%s, description=%s where id=%s',[request.form['steps'], request.form['description'],id])

                cur_edit= selectone("SELECT steps,description FROM uisitues WHERE id = %s",[id])
                uisitues_edit = [dict(steps=row[0],description=row[1]) for row in cur_edit]
                uisitues_steps = uisitues_edit[0]['steps']
                uisitues_description = uisitues_edit[0]['description']
                if request.form['steps'] == uisitues_steps and request.form['description'] == uisitues_description:
                    flash('编辑成功...')
                else:
                    flash('编辑失败...')
                return redirect(url_for('uisitues',num=1))
        return render_template('ui/uisitue_edit.html',SITEURL=SITEURL, username=session['username'], uisitues_issue=uisitues_issue, uisitues_model=uisitues_model, uisitues_version=uisitues_version, case=cases[0], nav=nav, sub_nav_ui = sub_nav_ui, sub_nav_api = sub_nav_api, set_nav=set_nav, operation=operation,current="uisitues", pagename = '测试集编辑',id=id)

# UI SITUES QUERY
@app.route('/uisitue_query/<int:id>', methods=['GET', 'POST'])
def uisitue_query(id):
    if not session.get('logged_in'):
        abort(401)
    else:
        cur = selectone('SELECT name,exec_mode, steps, description FROM uisitues where id=%s',[id])
        cases = [dict(name=row[0], exec_mode=row[1], steps=row[2], description=row[3]) for row in cur]
        return render_template('ui/uisitue_query.html',SITEURL=SITEURL, username=session['username'],  case=cases[0], nav=nav, sub_nav_ui = sub_nav_ui, sub_nav_api = sub_nav_api, set_nav=set_nav, operation=operation,current="uisitues", pagename = '测试集查看')

# UI SITUES DELETE
@app.route('/uisitue_delete/<int:id>', methods=['GET', 'POST'])
def uisitue_delete(id):
    if not session.get('logged_in'):
        abort(401)
    else:
        cur = addUpdateDel('delete from uisitues where id=%s',[id])

        cur_uisitues_del= selectone("SELECT * FROM uisitues where id=%s",[id])
        if cur_uisitues_del == ():
            flash('删除成功...')
        else:
            flash('删除失败...')

        return redirect(url_for('uisitues',num=1))

# UI SITUES EXEC
@app.route('/uisitue_exec/<int:id>', methods=['GET', 'POST'])
def uisitue_exec(id):
    if not session.get('logged_in'):
        abort(401)
    else:
        error = None
        username = session['username']
        newrun = RunUiTests(id,username)
        newrun.getTestSiutes()
        flash('执行成功...')
        return redirect(url_for('uisitues',num=1))

# NEW UI SITUE
@app.route('/new_uisitue', methods=['GET', 'POST'])
def new_uisitue():
    if not session.get('logged_in'):
        abort(401)
    error = None
    cur_issue = selectall('SELECT name FROM uicases where activity="1"')
    uisitues_issue = [dict(name=row[0]) for row in cur_issue]

    cur_model = selectall('SELECT model FROM uicases where activity="1" group by model')
    uisitues_model = [dict(model=row[0]) for row in cur_model]

    cur_version = selectall('SELECT version FROM uicases where activity="1" group by version')
    uisitues_version = [dict(version=row[0]) for row in cur_version]

    cur_name = selectall('SELECT zh_name FROM user WHERE username != "admin"')
    uisitues_name = [dict(username=row[0]) for row in cur_name]

    if request.method == 'POST':
        uiname = selectall('select name from uisitues')
        uinames = [dict(name=row[0]) for row in uiname]
        uinames = [uiname['name'] for uiname in uinames]

        if request.form['name'].strip() == '' or request.form['exec-mode'].strip() == '' or request.form['steps'].strip() == '':
            error = '必输项不能为空'
        elif request.form['name'].strip() in uinames:
            error = "该用例集已经存在"
        else:
            addUpdateDel('insert into uisitues (name, exec_mode, steps, description, username, create_date) values (%s, %s, %s, %s, %s, %s)',
                         [request.form['name'], request.form['exec-mode'], request.form['steps'], request.form['description'], session['username'], time.strftime('%Y-%m-%d %X', time.localtime(time.time()))])
            
            cur_new= selectone("SELECT * FROM uisitues WHERE name = %s",[request.form['name']])
            if cur_new != ():
                flash('创建成功...')
            else:
                flash('创建失败...')
            return redirect(url_for('uisitues',num=1))
    return render_template('ui/new_uisitue.html',SITEURL=SITEURL, username=session['username'], uisitues_issue=uisitues_issue, uisitues_name=uisitues_name, uisitues_model=uisitues_model, uisitues_version=uisitues_version, nav=nav, sub_nav_ui = sub_nav_ui, sub_nav_api = sub_nav_api, set_nav=set_nav,current="uisitues", pagename = '新增测试集',error=error)

# UI SIUTE REPORT
@app.route('/ui_report_list/1', methods=['GET', 'POST'])
def ui_report_list():
    if not session.get('logged_in'):
        abort(401)
    else:
        report_lists = get_file_list(path_ui)[0:18]
        return render_template('report_list.html',SITEURL=SITEURL, username=session['username'], nav=nav, sub_nav_ui = sub_nav_ui, sub_nav_api = sub_nav_api, set_nav=set_nav, pagename = '测试报告列表',report_lists=report_lists,path = path_ui,current='ui_report_list')


###############################
#             API
###############################
# API SITUES
@app.route('/apisitues/<int:num>', methods=['GET', 'POST'])
def apisitues(num):
    if not session.get('logged_in'):
        abort(401)
    else:
        all_Count = selectall('SELECT count(1) FROM apisitues')[0][0]
        all_Page = math.ceil(all_Count/page_Count)
        cur = selectone('SELECT a.id,a.name,a.exec_mode, a.steps,a.description,b.zh_name,a.create_date FROM apisitues a inner join user b on a.username=b.username order by a.id desc LIMIT %s,%s',[(num-1)*page_Count,page_Count])
        apisitues = [dict(id=row[0], name=row[1], exec_mode=row[2], steps=row[3], description=row[4], username=row[5], create_date=row[6]) for row in cur]
        return render_template('api/apisitues.html', SITEURL=SITEURL, username=session['username'], apisitues=apisitues, nav=nav, sub_nav_ui = sub_nav_ui, sub_nav_api = sub_nav_api, set_nav=set_nav, operation=operation, all_Page=all_Page, num=num,pagename = '测试集',current='apisitues')

# API SITUES EDIT
@app.route('/apisitue_edit/<int:id>', methods=['GET', 'POST'])
def apisitue_edit(id):
    if not session.get('logged_in'):
        abort(401)
    else:
        error=None
        cur_issue = selectall('SELECT name FROM apicases where activity="1"')
        apisitues_issue = [dict(name=row[0]) for row in cur_issue]

        cur_model = selectall('SELECT model FROM apicases where activity="1" group by model')
        apisitues_model = [dict(model=row[0]) for row in cur_model]

        cur_version = selectall('SELECT version FROM apicases where activity="1" group by version')
        apisitues_version = [dict(version=row[0]) for row in cur_version]

        cur = selectone('SELECT name, exec_mode, steps, description FROM apisitues where id=%s',[id])
        cases = [dict(name=row[0], exec_mode=row[1], steps=row[2], description=row[3]) for row in cur]
        if request.method == 'POST':
            if request.form['steps'].strip == '' or request.form['exec-mode'] == '':
                error = '必输项不能为空'
            else:
                addUpdateDel('update apisitues set exec_mode=%s, steps=%s, description=%s where id=%s',[request.form['exec-mode'], request.form['steps'], request.form['description'],id])

                cur_edit= selectone("SELECT exec_mode,steps,description FROM apisitues WHERE id = %s",[id])
                apisitues_edit = [dict(exec_mode=row[0],steps=row[1],description=row[2]) for row in cur_edit]
                apisitues_exec_mode = apisitues_edit[0]['exec_mode']
                apisitues_steps = apisitues_edit[0]['steps']
                apisitues_description = apisitues_edit[0]['description']
                if request.form['exec-mode'] == apisitues_exec_mode and request.form['steps'] == apisitues_steps and request.form['description'] == apisitues_description:
                    flash('编辑成功...')
                else:
                    flash('编辑失败...')
                return redirect(url_for('apisitues',num=1))
        return render_template('api/apisitue_edit.html',SITEURL=SITEURL, username=session['username'], case=cases[0], nav=nav, sub_nav_ui = sub_nav_ui, sub_nav_api = sub_nav_api, set_nav=set_nav, operation=operation, pagename = '测试集编辑',id=id,apisitues_issue=apisitues_issue,apisitues_model=apisitues_model,apisitues_version=apisitues_version,error=error,current='apisitues')

# API SITUES QUERY
@app.route('/apisitue_query/<int:id>', methods=['GET', 'POST'])
def apisitue_query(id):
    if not session.get('logged_in'):
        abort(401)
    else:
        cur = selectone('SELECT name, exec_mode, steps, description FROM apisitues where id=%s',[id])
        cases = [dict(name=row[0], exec_mode=row[1], steps=row[2], description=row[3]) for row in cur]
        return render_template('api/apisitue_query.html',SITEURL=SITEURL, username=session['username'], case=cases[0], nav=nav, sub_nav_ui = sub_nav_ui, sub_nav_api = sub_nav_api, set_nav=set_nav, operation=operation,current='apisitues', pagename = '测试集查看')

# API SITUES DELETE
@app.route('/apisitue_delete/<int:id>', methods=['GET', 'POST'])
def apisitue_delete(id):
    if not session.get('logged_in'):
        abort(401)
    else:
        cur = addUpdateDel('delete from apisitues where id=%s',[id])

        cur_apisitues_del= selectone("SELECT * FROM apisitues where id=%s",[id])
        if cur_apisitues_del == ():
            flash('删除成功...')
        else:
            flash('删除失败...')

        return redirect(url_for('apisitues',num=1))

# API SITUES EXEC
@app.route('/apisitue_exec/<int:id>', methods=['GET', 'POST'])
def apisitue_exec(id):
    if not session.get('logged_in'):
        abort(401)
    else:
        error = None
        username = session['username']
        newrun = RunTests(id,username)
        res=newrun.getTestSiutes()
        flash('执行成功...')
        return redirect(url_for('apisitues',num=1))

# NEW API SITUE
@app.route('/new_apisitue', methods=['GET', 'POST'])
def new_apisitue():
    if not session.get('logged_in'):
        abort(401)
    error = None
    cur_issue = selectall('SELECT name FROM apicases where activity="1"')
    apisitues_issue = [dict(name=row[0]) for row in cur_issue]

    cur_model = selectall('SELECT model FROM apicases where activity="1" group by model')
    apisitues_model = [dict(model=row[0]) for row in cur_model]

    cur_version = selectall('SELECT version FROM apicases where activity="1" group by version')
    apisitues_version = [dict(version=row[0]) for row in cur_version]

    if request.method == 'POST':
        apiname = selectall('select name from apisitues')
        apinames = [dict(name=row[0]) for row in apiname]
        apinames = [apiname['name'] for apiname in apinames]

        if request.form['name'].strip() == '' or request.form['exec-mode'].strip() == '' or request.form['steps'].strip() == '':
            error = '必输项不能为空'
        elif request.form['name'].strip() in apinames:
            error = "该用例集已经存在"
        else:
            addUpdateDel('insert into apisitues (name, exec_mode, steps, description, username, create_date) values (%s, %s, %s, %s, %s, %s)',
                         [request.form['name'], request.form['exec-mode'], request.form['steps'], request.form['description'], session['username'], time.strftime('%Y-%m-%d %X', time.localtime(time.time()))])

            cur_new= selectone("SELECT * FROM apisitues WHERE name = %s",[request.form['name']])
            if cur_new != ():
                flash('创建成功...')
            else:
                flash('创建失败...')

            return redirect(url_for('apisitues',num=1))
    return render_template('api/new_apisitue.html',SITEURL=SITEURL, username=session['username'], nav=nav, sub_nav_ui = sub_nav_ui, sub_nav_api = sub_nav_api, set_nav=set_nav, pagename = '新增测试集',error=error,apisitues_issue=apisitues_issue,apisitues_model=apisitues_model,apisitues_version=apisitues_version,current='apisitues')

# API SIUTE REPORT
@app.route('/api_report_list/1', methods=['GET', 'POST'])
def api_report_list():
    if not session.get('logged_in'):
        abort(401)
    else:
        report_lists = get_file_list(path_api)[0:18]
        return render_template('report_list.html',SITEURL=SITEURL, username=session['username'], nav=nav, sub_nav_ui = sub_nav_ui, sub_nav_api = sub_nav_api, set_nav=set_nav, pagename = '测试报告列表',report_lists=report_lists,path = path_api,current='api_report_list')

# API CASE
@app.route('/apicases/<category>/<value>/<int:num>', methods=['GET', 'POST'])
def apicases(category,value,num):
    if not session.get('logged_in'):
        abort(401)
    else:
        error = None
        if category == 'a.name':
            all_Count = selectall('SELECT count(1) FROM apicases a inner join user b on a.username=b.username where activity="1" and '+category+' like "%'+value+'%"')[0][0]
        else:
            all_Count = selectall('SELECT count(1) FROM apicases a inner join user b on a.username=b.username where activity="1" and '+category+'="'+value+'"')[0][0]
        all_Page = math.ceil(all_Count/page_Count)
        cur_usernames=selectall('SELECT b.zh_name FROM apicases a inner join user b ON a.username=b.username WHERE a.activity="1" GROUP BY a.username')
        usernames=[dict(zh_name=row[0]) for row in cur_usernames]
        cur_versions=selectall('SELECT version FROM apicases WHERE activity="1" group by version')
        versions=[dict(version=row[0]) for row in cur_versions]
        cur_models=selectall('SELECT model FROM apicases WHERE activity="1" group by model')
        models=[dict(model=row[0]) for row in cur_models]
        if request.method == 'POST':
            if request.form['select-model'].strip() == '':
                category = '1'
                value ='1'
            elif request.form['select-model'].strip() == '按名称' and request.form['query-name'].strip() != '':
                category = 'a.name'
                value = request.form['query-name']
            elif request.form['select-model'].strip() == '按版本' and request.form['query-version'].strip() != '':
                category = 'a.version'
                value = request.form['query-version']
            elif request.form['select-model'].strip() == '按模块' and request.form['query-model'].strip() != '':
                category = 'a.model'
                value = request.form['query-model']
            elif request.form['select-model'].strip() == '按用户' and request.form['query-username'].strip() != '':
                category = 'b.zh_name'
                value = request.form['query-username']
            return redirect(url_for('apicases',category=category,value=value,num='1'))
        if category == 'a.name':
            cur = selectall('SELECT a.id,a.type,a.version, a.model, a.product, a.name,a.pre_steps, a.steps, a.next_steps,a.description,a.exec_result, b.zh_name, a.create_date FROM apicases a inner join user b on a.username=b.username where activity="1" and '+category+' like "%'+value+'%" order by a.id desc LIMIT '+str((num-1)*page_Count)+','+str(page_Count))
        else:
            cur = selectall('SELECT a.id,a.type,a.version, a.model, a.product, a.name,a.pre_steps, a.steps, a.next_steps,a.description,a.exec_result, b.zh_name, a.create_date FROM apicases a inner join user b on a.username=b.username where activity="1" and '+category+'="'+value+'" order by a.id desc LIMIT '+str((num-1)*page_Count)+','+str(page_Count))
        cases = [dict(id=row[0], type=row[1], version=row[2], model=row[3], product=row[4], name=row[5], pre_steps=row[6], steps=row[7], next_steps=row[8], description=row[9], exec_result=row[10], zh_name=row[11], create_date=row[12]) for row in cur]
        return render_template('api/apicases.html', SITEURL=SITEURL, username=session['username'], cases=cases, nav=nav, sub_nav_api = sub_nav_api, sub_nav_ui = sub_nav_ui, set_nav=set_nav, operation_exec=operation_exec, all_Page=all_Page,category=category,value=value, num=num,usernames=usernames,versions=versions,models=models,current='apicases',error=error,pagename = '接口测试用例')

# API CASE QUERY
@app.route('/apicase_query/<int:id>', methods=['GET', 'POST'])
def apicase_query(id):
    if not session.get('logged_in'):
        abort(401)
    else:
        cur = selectone('SELECT version, name, product, model, steps, description FROM apicases where id=%s',[id])
        cases = [dict(version=row[0], name=row[1], product=row[2], model=row[3], steps=row[4], description=row[5]) for row in cur]
        steps = cases[0]['steps'].split('\r\n')
        case_name = cases[0]['name']
        case_details = []
        for i in range(len(steps)):
            cur = selectone('select name,path,method,request,checks,parameter from apidates where case_name=%s and name=%s',[case_name,str(i)+'_'+steps[i]])
            case_detail = [dict(name=row[0], path=row[1], method=row[2], request=row[3], checks=row[4], parameter=row[5]) for row in cur]
            case_details.append(case_detail[0])
        return render_template('api/apicase_query.html',SITEURL=SITEURL, username=session['username'], case_details=case_details, case=cases[0], nav=nav, sub_nav_ui = sub_nav_ui, sub_nav_api = sub_nav_api, set_nav=set_nav, operation=operation, pagename = '接口查看',current='apicases')

# API CASE DELETE
@app.route('/apicase_delete/<int:id>', methods=['GET', 'POST'])
def apicase_delete(id):
    if not session.get('logged_in'):
        abort(401)
    else:
        apisitue = selectall('select steps from apisitues')
        apisitues = [dict(steps=row[0]) for row in apisitue]
        apisitues = [apisitue['steps'] for apisitue in apisitues]
        apisitues_all=[]
        for apisitue in apisitues:
            apisitues_all.extend(apisitue.split('\r\n'))

        apicase = selectone('select name from apicases where id=%s',[id])
        apicases = [dict(name=row[0]) for row in apicase]
        apicase_name = apicases[0]['name']
        
        apicase_pre_step = selectall('select pre_steps from apicases')
        apicase_pre_steps = [dict(pre_steps=row[0]) for row in apicase_pre_step]
        apicase_pre_steps = [apicase_pre_step['pre_steps'] for apicase_pre_step in apicase_pre_steps]
        apicase_pre_steps_all=[]
        for apicase_pre in apicase_pre_steps:
            if apicase_pre != '':
                apicase_pre_steps_all.extend(apicase_pre.split('\r\n'))

        apicase_next_step = selectall('select next_steps from apicases')
        apicase_next_steps = [dict(next_steps=row[0]) for row in apicase_next_step]
        apicase_next_steps = [apicase_next_step['next_steps'] for apicase_next_step in apicase_next_steps]
        apicase_next_steps_all=[]
        for apicase_next in apicase_next_steps:
            if apicase_next != '':
                apicase_next_steps_all.extend(apicase_next.split('\r\n'))

        if apicase_name in apisitues_all:
            flash("该用例被测试集引用，不能删除~！")
        elif apicase_name in apicase_pre_steps_all or apicase_name in apicase_next_steps_all:
            flash("该案例被其他用例前置/后置事务引用，不能删除~！")
        else:
            cur = addUpdateDel('update apicases set activity = "2" where id=%s',[id])

            cur_apicases_del= selectone("SELECT * FROM apicases where id=%s and activity !=2",[id])
            if cur_apicases_del == ():
                flash('删除成功...')
            else:
                flash('删除失败...')

        return redirect(url_for('apicases',num=1))

# API CASE EXEC
@app.route('/apicase_exec/<int:id>', methods=['GET', 'POST'])
def apicase_exec(id):
    if not session.get('logged_in'):
        abort(401)
    else:
        error = None
        newrun = RunTests(id,session['username'])
        res=newrun.getTestCases()

        return render_template('api/apicase_exec.html',SITEURL=SITEURL, username=session['username'], res=res,nav=nav, sub_nav_ui = sub_nav_ui, sub_nav_api = sub_nav_api, set_nav=set_nav, operation=operation, pagename = '接口执行结果',current='apicases')

# API CASE reject
@app.route('/apicase_reject/<int:id>', methods=['GET', 'POST'])
def apicase_reject(id):
    if not session.get('logged_in'):
        abort(401)
    else:
        cur = addUpdateDel('update apicases set activity=0 where id=%s and activity=1',[id])

        cur_apicases_reject= selectone("SELECT * FROM apicases where id=%s and activity=0",[id])
        if cur_apicases_reject == ():
            flash('驳回失败...')
        else:
            flash('驳回成功...')

        return redirect(url_for('apicases',num=1))

###############################
#             SET
###############################
# UI SET
@app.route('/caseManage/uiset/<int:num>', methods=['GET', 'POST'])
def uiset(num):
    if not session.get('logged_in'):
        abort(401)
    else:
        all_Count = selectall('SELECT count(1) FROM uiset')[0][0]
        all_Page = math.ceil(all_Count/page_Count)
        cur = selectone('SELECT a.id,a.keyword,a.description,a.template,a.example,b.zh_name,a.create_date FROM uiset a inner join user b on a.username=b.username order by a.id desc LIMIT %s,%s',[(num-1)*page_Count,page_Count])
        uisets = [dict(id=row[0], keyword=row[1], description=row[2], template=row[3], example=row[4], username=row[5], create_date=row[6]) for row in cur]
        return render_template('set/uiset.html',SITEURL=SITEURL, username=session['username'],  uisets=uisets, caseManage_nav=caseManage_nav, caseManage_sub_nav_ui = caseManage_sub_nav_ui, caseManage_sub_nav_api = caseManage_sub_nav_api, caseManage_set_nav=caseManage_set_nav, operation=operation, all_Page=all_Page,num=num, current='uiset',pagename = 'UI封装')

# UI SET EDIT
@app.route('/caseManage/uiset_edit/<int:id>', methods=['GET', 'POST'])
def uiset_edit(id):
    if not session.get('logged_in'):
        abort(401)
    else:
        cur = selectone('SELECT id,keyword,description,template,example FROM uiset where id=%s',[id])
        cases = [dict(id=row[0], keyword=row[1], description=row[2], template=row[3], example=row[4]) for row in cur]
        if request.method == 'POST':
            if request.form['template'].strip() == '' or request.form['example'].strip == '':
                error = '必输项不能为空'
            else:
                addUpdateDel('update uiset set template=%s, example=%s, description=%s where id=%s',[request.form['template'], request.form['example'], request.form['description'],id])

                cur_edit= selectone("SELECT template,example,description FROM uiset WHERE id = %s",[id])
                uiset_edit = [dict(template=row[0],example=row[1],description=row[2]) for row in cur_edit]
                uiset_template = uiset_edit[0]['template']
                uiset_steps = uiset_edit[0]['example']
                uiset_description = uiset_edit[0]['description']
                if request.form['template'] == uiset_template and request.form['example'] == uiset_steps and request.form['description'] == uiset_description:
                    flash('编辑成功...')
                else:
                    flash('编辑失败...')

                return redirect(url_for('uiset',num=1))
        return render_template('set/uiset_edit.html', SITEURL=SITEURL, username=session['username'], case=cases[0], caseManage_nav=caseManage_nav, caseManage_sub_nav_ui = caseManage_sub_nav_ui, caseManage_sub_nav_api = caseManage_sub_nav_api, caseManage_set_nav=caseManage_set_nav, operation=operation,current='uiset', pagename = 'UI封装编辑',id=id)

# UI SET QUERY
@app.route('/caseManage/uiset_query/<int:id>', methods=['GET', 'POST'])
def uiset_query(id):
    if not session.get('logged_in'):
        abort(401)
    else:
        cur = selectone('SELECT id,keyword,description,template,example FROM uiset where id=%s',[id])
        cases = [dict(id=row[0], keyword=row[1], description=row[2], template=row[3], example=row[4]) for row in cur]
        return render_template('set/uiset_query.html', SITEURL=SITEURL, username=session['username'], case=cases[0], caseManage_nav=caseManage_nav, caseManage_sub_nav_ui = caseManage_sub_nav_ui, caseManage_sub_nav_api = caseManage_sub_nav_api, caseManage_set_nav=caseManage_set_nav, operation=operation,current='uiset', pagename = 'UI封装查看')

# UI SET DELETE
@app.route('/caseManage/uiset_delete/<int:id>', methods=['GET', 'POST'])
def uiset_delete(id):
    if not session.get('logged_in'):
        abort(401)
    else:
        addUpdateDel('delete from uiset where id=%s',[id])

        cur_uiset_del= selectone("SELECT * FROM uiset where id=%s",[id])
        if cur_uiset_del == ():
            flash('删除成功...')
        else:
            flash('删除失败...')

        return redirect(url_for('uiset',num=1))

# NEW UI SET
@app.route('/caseManage/new_uiset', methods=['GET', 'POST'])
def new_uiset():
    if not session.get('logged_in'):
        abort(401)
    error = None
    if request.method == 'POST':
        uiset = selectall('select keyword from uiset')
        uisets = [dict(keyword=row[0]) for row in uiset]
        uisets = [uiname['keyword'] for uiname in uisets]

        if request.form['keyword'].strip() == '' or request.form['template'].strip() == '' or request.form['example'].strip == '':
            error = '必输项不能为空'
        elif request.form['keyword'].strip() in uisets:
            error = "该关键字已经存在"
        else:
            addUpdateDel('insert into uiset (keyword,description,template,example, username, create_date) values (%s, %s, %s, %s, %s, %s)',
                         [cn_to_uk(request.form['keyword']), cn_to_uk(request.form['description']), request.form['template'], cn_to_uk(request.form['example']), session['username'], time.strftime('%Y-%m-%d %X', time.localtime(time.time()))])

            cur_new= selectone("SELECT * FROM uiset WHERE keyword = %s",[request.form['keyword']])
            if cur_new != ():
                flash('创建成功...')
            else:
                flash('创建失败...')

            return redirect(url_for('uiset',num=1))
    return render_template('set/new_uiset.html', SITEURL=SITEURL, username=session['username'], caseManage_nav=caseManage_nav, caseManage_sub_nav_ui = caseManage_sub_nav_ui, caseManage_sub_nav_api = caseManage_sub_nav_api, caseManage_set_nav=caseManage_set_nav,current='uiset', pagename = '新建UI封装',error=error)

# API SET
@app.route('/caseManage/apiset/<int:num>', methods=['GET', 'POST'])
def apiset(num):
    if not session.get('logged_in'):
        abort(401)
    else:
        all_Count = selectall('SELECT count(1) FROM apiset')[0][0]
        all_Page = math.ceil(all_Count/page_Count)
        cur = selectone('SELECT a.id,a.name,a.path,a.method,a.request,a.checks,a.description,b.zh_name,a.create_date FROM apiset a inner join user b on a.username=b.username order by a.id desc LIMIT %s,%s',[(num-1)*page_Count,page_Count])
        apisets = [dict(id=row[0], name=row[1], path=row[2], method=row[3], request=row[4], checks=row[5], description=row[6], username=row[7], create_date=row[8]) for row in cur]
        return render_template('set/apiset.html',SITEURL=SITEURL, username=session['username'], apisets=apisets, caseManage_nav=caseManage_nav, caseManage_sub_nav_ui = caseManage_sub_nav_ui, caseManage_sub_nav_api = caseManage_sub_nav_api, caseManage_set_nav=caseManage_set_nav, operation=operation, all_Page=all_Page, num=num, current='apiset',pagename = '全部接口')

# API SET EDIT
@app.route('/caseManage/apiset_edit/<int:id>', methods=['GET', 'POST'])
def apiset_edit(id):
    if not session.get('logged_in'):
        abort(401)
    else:
        error=None
        cur = selectone('SELECT id,name,path,method,request,checks,description FROM apiset where id=%s',[id])
        cases = [dict(id=row[0], name=row[1], path=row[2], method=row[3], request=row[4], checks=row[5], description=row[6]) for row in cur]

        if request.method == 'POST':
            if request.form['path'].strip() == '' or request.form['request'].strip() == '':
                error = '必输项不能为空'
            elif request.form['path'][0:7] != 'http://':
                error = '路径格式不对'
            elif request.form['path'][0:8] !='https://':
                error = '路径格式不对'
            elif is_dict(request.form['request'].strip()) == False:
                error = '请求项格式不对'
            elif request.form['checks'].strip() != '':
                if is_dict(request.form['checks'].strip()) == False:
                    error = '检查项格式不对'
            else:
                addUpdateDel('update apiset set path=%s, request=%s, checks=%s, description=%s where id=%s',[request.form['path'], request.form['request'], request.form['checks'], request.form['description'],id])
                cur_edit= selectone("SELECT path,request,checks,description FROM apiset WHERE id = %s",[id])
                apiset_edit = [dict(path=row[0],request=row[1],checks=row[2],description=row[3]) for row in cur_edit]
                apiset_path = apiset_edit[0]['path']
                apiset_request = apiset_edit[0]['request']
                apiset_checks = apiset_edit[0]['checks']
                apiset_description = apiset_edit[0]['description']
                if request.form['path'] == apiset_path and request.form['request'] == apiset_request and request.form['checks'] == apiset_checks and request.form['description'] == apiset_description:
                    flash('编辑成功...')
                else:
                    flash('编辑失败...')

                return redirect(url_for('apiset',num=1))
        return render_template('set/apiset_edit.html',SITEURL=SITEURL, username=session['username'], case=cases[0], caseManage_nav=caseManage_nav, caseManage_sub_nav_ui = caseManage_sub_nav_ui, caseManage_sub_nav_api = caseManage_sub_nav_api, caseManage_set_nav=caseManage_set_nav, operation=operation,error=error,current='apiset', pagename = '接口编辑', id=id)

# API SET QUERY
@app.route('/caseManage/apiset_query/<int:id>', methods=['GET', 'POST'])
def apiset_query(id):
    if not session.get('logged_in'):
        abort(401)
    else:
        cur = selectone('SELECT id,name,path,method,request,checks,description FROM apiset where id=%s',[id])
        cases = [dict(id=row[0], name=row[1], path=row[2], method=row[3], request=row[4], checks=row[5], description=row[6]) for row in cur]
        return render_template('set/apiset_query.html',SITEURL=SITEURL, username=session['username'],  case=cases[0], caseManage_nav=caseManage_nav, caseManage_sub_nav_ui = caseManage_sub_nav_ui, caseManage_sub_nav_api = caseManage_sub_nav_api, caseManage_set_nav=caseManage_set_nav, operation=operation,current='apiset', pagename = '接口查看')

# API SET DELETE
@app.route('/caseManage/apiset_delete/<int:id>', methods=['GET', 'POST'])
def apiset_delete(id):
    if not session.get('logged_in'):
        abort(401)
    else:
        addUpdateDel('delete from apiset where id=%s',[id])

        cur_apiset_del= selectone("SELECT * FROM apiset where id=%s",[id])
        if cur_apiset_del == ():
            flash('删除成功...')
        else:
            flash('删除失败...')

        return redirect(url_for('apiset',num=1))

# API SET EXEC
@app.route('/caseManage/apiset_exec/<int:id>', methods=['GET', 'POST'])
def apiset_exec(id):
    if not session.get('logged_in'):
        abort(401)
    else:
        error = None
        newrun = RunTests(id,session['username'])
        res=newrun.getApis()
        flash('执行成功...')
        return render_template('set/apiset_exec.html',SITEURL=SITEURL, username=session['username'], res=res,caseManage_nav=caseManage_nav, caseManage_sub_nav_ui = caseManage_sub_nav_ui, caseManage_sub_nav_api = caseManage_sub_nav_api, caseManage_set_nav=caseManage_set_nav, operation=operation,current="apiset", pagename = '接口执行结果')

# NEW API
@app.route('/caseManage/new_apiset', methods=['GET', 'POST'])
def new_apiset():
    if not session.get('logged_in'):
        abort(401)
    error = None
    if request.method == 'POST':
        apiset = selectall('select name from apiset')
        apisets = [dict(name=row[0]) for row in apiset]
        apisets = [apiset['name'] for apiset in apisets]

        if request.form['name'].strip() == '' or request.form['path'].strip == '' or request.form['method'].strip == '' or request.form['request'].strip == '':
            error = '必输项不能为空'
        elif request.form['name'].strip() in apisets:
            error = "该API已经存在"
        elif request.form['path'][0:7] != 'http://':
            error = '路径格式不对'
        elif request.form['path'][0:8] !='https://':
            error = '路径格式不对'
        elif is_dict(request.form['request'].strip()) == False:
            error = '请求项格式不对'
        elif request.form['checks'].strip() != '':
            if is_dict(request.form['checks'].strip()) == False:
                error = '检查项格式不对'
        else:
            addUpdateDel('insert into apiset (name, description, path, method, request, checks, username, create_date) values (%s, %s, %s, %s, %s, %s, %s, %s)',
                         [request.form['name'], request.form['description'], cn_to_uk(request.form['path']), request.form['method'], cn_to_uk(request.form['request']), cn_to_uk(request.form['checks']), session['username'], time.strftime('%Y-%m-%d %X', time.localtime(time.time()))])

            cur_new= selectone("SELECT * FROM apiset WHERE name = %s",[request.form['name']])
            if cur_new != ():
                flash('创建成功...')
            else:
                flash('创建失败...')

            return redirect(url_for('apiset',num=1))
    return render_template('set/new_apiset.html',SITEURL=SITEURL, username=session['username'], caseManage_nav=caseManage_nav, caseManage_sub_nav_ui = caseManage_sub_nav_ui, caseManage_sub_nav_api = caseManage_sub_nav_api, caseManage_set_nav=caseManage_set_nav, pagename = '新增接口', product=product, model_sicap=model_sicap, error=error,current='apiset', methods=http_methods)

##############################
#         version
##############################
# VERSION DELETE
@app.route('/caseManage/version_delete/<int:id>', methods=['GET', 'POST'])
def version_delete(id):
    if not session.get('logged_in'):
        abort(401)
    else:
        cur = addUpdateDel('delete from versions where id=%s',[id])

        cur_versions_del= selectone("SELECT * FROM versions where id=%s",[id])
        if cur_versions_del == ():
            flash('删除成功...')
        else:
            flash('删除失败...')

        return redirect(url_for('versions',num=1))

# NEW VERSION
@app.route('/caseManage/new_version', methods=['GET', 'POST'])
def new_version():
    if not session.get('logged_in'):
        abort(401)
    error = None
    if request.method == 'POST':
        version = selectall('select version from versions')
        versions = [dict(version=row[0]) for row in version]
        versions = [version['version'] for version in versions]

        if request.form['version'].strip() == '':
            error = '必输项不能为空'
        elif request.form['version'].strip() in versions:
            error = "该版本号已经存在"
        else:
            addUpdateDel('insert into versions (version, username, create_date) values (%s, %s, %s)',
                         [request.form['version'], session['username'], time.strftime('%Y-%m-%d %X', time.localtime(time.time()))])

            cur_new= selectone("SELECT * FROM versions WHERE version = %s",[request.form['version']])
            if cur_new != ():
                flash('创建成功...')
            else:
                flash('创建失败...')

            return redirect(url_for('versions',num=1))
    return render_template('version/new_version.html',  SITEURL=SITEURL, username=session['username'], caseManage_nav=caseManage_nav, caseManage_sub_nav_ui = caseManage_sub_nav_ui, caseManage_sub_nav_api = caseManage_sub_nav_api, caseManage_set_nav=caseManage_set_nav, pagename = '新增版本号', product=product, current='versions', model_oma=model_oma, error=error)

# VERSION
@app.route('/caseManage/versions/<int:num>', methods=['GET', 'POST'])
def versions(num):
    if not session.get('logged_in'):
        abort(401)
    else:
        all_Count = selectall('SELECT count(1) FROM versions')[0][0]
        all_Page = math.ceil(all_Count/page_Count)
        cur = selectone('SELECT a.id,a.version,b.zh_name,a.create_date FROM versions a inner join user b on a.username=b.username order by a.id desc LIMIT %s,%s',[(num-1)*page_Count,page_Count])
        versions = [dict(id=row[0], version=row[1], username=row[2], create_date=row[3]) for row in cur]
        return render_template('version/versions.html', SITEURL=SITEURL, username=session['username'], versions=versions, caseManage_nav=caseManage_nav, caseManage_sub_nav_ui = caseManage_sub_nav_ui, caseManage_sub_nav_api = caseManage_sub_nav_api, caseManage_set_nav=caseManage_set_nav, operation=operation, all_Page=all_Page,current='versions', pagename = '版本号')

##############################
#         caseManage
##############################
# 首页
@app.route('/caseManage')
def caseManage_initial():
    return redirect(url_for('caseManage_login'))

# 登陆页面
@app.route('/caseManage/login', methods=['GET', 'POST'])
def caseManage_login():
    if session.get('logged_in'):
        return redirect(url_for('caseManage_index',current_user = session['username']))
    error = None
    result = selectall('select username,password from user')
    date = []
    for i in list(range(len(result))):
        date.append(result[i][0])
    if request.method == 'POST':
        session['username']=request.form['username']
        if request.form['username'] in date:
            cur = selectone('select username,password from user where username = %s',(request.form['username'],))
            uname,pw = cur[0]
            if request.form['username'] != uname:
                error = '无效的用户名'
            elif request.form['password'] != decrypt(pw):
                error = '无效的密码'
            elif request.form['username'] == 'admin':
                session['logged_in'] = True
                addUpdateDel('update user set last_login = %s where username = %s',[time.strftime('%Y-%m-%d %X', time.localtime(time.time())), session['username']])
                flash('你已经登陆管理员...')
                return redirect(url_for('caseManage_index',current_user = session['username']))
            else:
                session['logged_in'] = True
                addUpdateDel('update user set last_login = %s where username = %s',[time.strftime('%Y-%m-%d %X', time.localtime(time.time())), session['username']])
                flash('你已经登陆...')
                return redirect(url_for('caseManage_index',current_user = session['username']))
        else:
            error = '用户名不存在'
    return render_template('caseManage/login.html', error=error)

@app.route('/caseManage/<current_user>/')
def caseManage_index(current_user):
    if session.get('logged_in'):
        counts = selectall('select count(1) from uicases where activity !="2"')[0][0]
        versions = selectall('SELECT VERSION,COUNT(1) AS COUNT FROM uicases where activity !="2" GROUP BY VERSION ORDER BY COUNT DESC')
        models = selectall('SELECT MODEl,COUNT(1) AS COUNT FROM uicases where activity !="2"  GROUP BY MODEl ORDER BY COUNT DESC')
        return render_template('caseManage/index.html', username=session['username'],caseManage_nav=caseManage_nav, caseManage_sub_nav_ui = caseManage_sub_nav_ui, caseManage_sub_nav_api = caseManage_sub_nav_api, caseManage_set_nav=caseManage_set_nav,counts=counts,versions=versions,models=models,pagename = '主页')
    else:
        return redirect(url_for('caseManage_login'))

# caseManage UI CASES
@app.route('/caseManage/uicases/<category>/<value>/<int:num>', methods=['GET', 'POST'])
def caseManage_uicases(category,value,num):
    if not session.get('logged_in'):
        abort(401)
    else:
        error = None
        if category == 'a.name':
            all_Count = selectall('SELECT count(1) FROM uicases a inner join user b on a.username=b.username where activity="0" and '+category+' like "%'+value+'%"')[0][0]
        else:
            all_Count = selectall('SELECT count(1) FROM uicases a inner join user b on a.username=b.username where activity="0" and '+category+'="'+value+'"')[0][0]
        all_Page = math.ceil(all_Count/page_Count)
        cur_usernames=selectall('SELECT b.zh_name FROM uicases a inner join user b ON a.username=b.username WHERE a.activity="0" GROUP BY a.username')
        usernames=[dict(zh_name=row[0]) for row in cur_usernames]
        cur_versions=selectall('SELECT version FROM uicases WHERE activity="0" group by version')
        versions=[dict(version=row[0]) for row in cur_versions]
        cur_models=selectall('SELECT model FROM uicases WHERE activity="0" group by model')
        models=[dict(model=row[0]) for row in cur_models]
        if request.method == 'POST':
            if request.form['select-model'].strip() == '':
                category = '1'
                value ='1'
            elif request.form['select-model'].strip() == '按名称' and request.form['query-name'].strip() != '':
                category = 'a.name'
                value = request.form['query-name']
            elif request.form['select-model'].strip() == '按版本' and request.form['query-version'].strip() != '':
                category = 'a.version'
                value = request.form['query-version']
            elif request.form['select-model'].strip() == '按模块' and request.form['query-model'].strip() != '':
                category = 'a.model'
                value = request.form['query-model']
            elif request.form['select-model'].strip() == '按用户' and request.form['query-username'].strip() != '':
                category = 'b.zh_name'
                value = request.form['query-username']
            return redirect(url_for('caseManage_uicases',category=category,value=value,num='1'))
        if category == 'a.name':
            cur = selectall('SELECT a.id,a.type,a.version, a.model, a.product, a.name,a.pre_steps, a.steps, a.next_steps,a.description,a.exec_result, b.zh_name, a.create_date FROM uicases a inner join user b on a.username=b.username where activity="0" and '+category+' like "%'+value+'%" order by a.id desc LIMIT '+str((num-1)*page_Count)+','+str(page_Count))
        else:
            cur = selectall('SELECT a.id,a.type,a.version, a.model, a.product, a.name,a.pre_steps, a.steps, a.next_steps,a.description,a.exec_result, b.zh_name, a.create_date FROM uicases a inner join user b on a.username=b.username where activity="0" and '+category+'="'+value+'" order by a.id desc LIMIT '+str((num-1)*page_Count)+','+str(page_Count))
        cases = [dict(id=row[0], type=row[1], version=row[2], model=row[3], product=row[4], name=row[5], pre_steps=row[6], steps=row[7], next_steps=row[8], description=row[9], exec_result=row[10], zh_name=row[11], create_date=row[12]) for row in cur]
        return render_template('caseManage/uicases.html', SITEURL=SITEURL, username=session['username'], cases=cases, caseManage_nav=caseManage_nav, caseManage_sub_nav_ui = caseManage_sub_nav_ui, caseManage_sub_nav_api = caseManage_sub_nav_api, caseManage_set_nav=caseManage_set_nav, operation=operation, all_Page=all_Page,category=category,value=value, num=num,usernames=usernames,versions=versions,models=models,current='uicases',error=error,pagename = '测试用例')

# caseManage UI CASE EDIT
@app.route('/caseManage/uicase_edit/<int:id>', methods=['GET', 'POST'])
def caseManage_uicase_edit(id):
    error = None
    if not session.get('logged_in'):
        abort(401)
    else:
        issuetype = selectall('select name from uicases where type="公共用例"')
        issuetypes = [dict(name=row[0]) for row in issuetype]

        nexttype = selectall('select name from uicases where type="后置用例"')
        nexttypes = [dict(name=row[0]) for row in nexttype]

        cur = selectall('SELECT keyword FROM uiset')
        list_steps = [dict(keyword=row[0]) for row in cur]

        cur = selectone('SELECT type,version, model, product, name,pre_steps, steps, description,next_steps, username, create_date FROM uicases where id=%s',[id])
        cases = [dict(type=row[0], version=row[1], model=row[2], product=row[3], name=row[4], pre_steps=row[5], steps=row[6], description=row[7], next_steps=row[8], username=row[9], create_date=row[10]) for row in cur]
        if request.method == 'POST':
            uiname = selectone('select name from uicases where name !=%s',[cases[0]['name']])
            uinames = [dict(name=row[0]) for row in uiname]
            uinames = [uiname['name'] for uiname in uinames]
            if request.form['steps'].strip() == '' or request.form['name'] == '':
                error = '必输项不能为空'
            elif request.form['name'].strip() in uinames:
                error = "该用例已经存在"
            elif request.form['type'].strip() in ('公共用例','后置用例'):
                addUpdateDel('update uicases set name=%s, steps=%s, description=%s where id=%s',[request.form['name'], request.form['steps'], request.form['description'],id])

                cur_edit= selectone("SELECT name,steps,description FROM uicases WHERE id = %s",[id])
                uicases_edit = [dict(name=row[0],steps=row[1],description=row[2]) for row in cur_edit]
                uicase_name = uicases_edit[0]['name']
                uicases_steps = uicases_edit[0]['steps']
                uicases_description = uicases_edit[0]['description']
                if request.form['name'] == uicase_name and request.form['steps'] == uicases_steps and request.form['description'] == uicases_description:
                    flash('编辑成功...')
                else:
                    flash('编辑失败...')

                return redirect(url_for('caseManage_uicases',category='a.username',value=session['username'],num=1))
            else:
                addUpdateDel('update uicases set name=%s, pre_steps=%s, steps=%s, next_steps=%s, description=%s where id=%s',[request.form['name'], request.form['pre-steps'], request.form['steps'], request.form['next-steps'],request.form['description'],id])

                cur_edit= selectone("SELECT name,pre_steps,steps,next_steps,description FROM uicases WHERE id = %s",[id])
                uicases_edit = [dict(name=row[0],pre_steps=row[1],steps=row[2],next_steps=row[3],description=row[4]) for row in cur_edit]
                uicase_name = uicases_edit[0]['name']
                uicases_pre_steps = uicases_edit[0]['pre_steps']
                uicases_steps = uicases_edit[0]['steps']
                uicases_next_steps = uicases_edit[0]['next_steps']
                uicases_description = uicases_edit[0]['description']
                if request.form['name'] == uicase_name and request.form['pre-steps'] == uicases_pre_steps and request.form['steps'] == uicases_steps and request.form['next-steps'] == uicases_next_steps and request.form['description'] == uicases_description:
                    flash('编辑成功...')
                else:
                    flash('编辑失败...')

                return redirect(url_for('caseManage_uicases',category='a.username',value=session['username'],num=1))
        return render_template('caseManage/uicase_edit.html',SITEURL=SITEURL, username=session['username'],list_steps=list_steps, case=cases[0], caseManage_nav=caseManage_nav, caseManage_sub_nav_ui = caseManage_sub_nav_ui, caseManage_sub_nav_api = caseManage_sub_nav_api, caseManage_set_nav=caseManage_set_nav, operation=operation,issuetypes=issuetypes,nexttypes=nexttypes,current='uicases', pagename = '测试用例编辑',error=error,id=id)

# caseManage UI CASE QUERY
@app.route('/caseManage/uicase_query/<int:id>', methods=['GET', 'POST'])
def caseManage_uicase_query(id):
    if not session.get('logged_in'):
        abort(401)
    else:
        cur = selectone('SELECT type,version, model, product, name,pre_steps, steps, description,next_steps, username, create_date FROM uicases where id=%s',[id])
        cases = [dict(type=row[0], version=row[1], model=row[2], product=row[3], name=row[4], pre_steps=row[5], steps=row[6], description=row[7], next_steps=row[8], username=row[9], create_date=row[10]) for row in cur]
        return render_template('caseManage/uicase_query.html', SITEURL=SITEURL, username=session['username'], case=cases[0], caseManage_nav=caseManage_nav, caseManage_sub_nav_ui = caseManage_sub_nav_ui, caseManage_sub_nav_api = caseManage_sub_nav_api, caseManage_set_nav=caseManage_set_nav, operation=operation,current='uicases', pagename = '测试用例查看')

# caseManage UI CASE DELETE
@app.route('/caseManage/uicase_delete/<int:id>', methods=['GET', 'POST'])
def caseManage_uicase_delete(id):
    if not session.get('logged_in'):
        abort(401)
    else:
        uisitue = selectall('select steps from uisitues')
        uisitues = [dict(steps=row[0]) for row in uisitue]
        uisitues = [uisitue['steps'] for uisitue in uisitues]
        uisitues_all=[]
        for uisitue in uisitues:
            uisitues_all.extend(uisitue.split('\r\n'))

        uicase = selectone('select name from uicases where id=%s',[id])
        uicases = [dict(name=row[0]) for row in uicase]
        uicase_name = uicases[0]['name']
        
        uicase_pre_step = selectall('select pre_steps from uicases')
        uicase_pre_steps = [dict(pre_steps=row[0]) for row in uicase_pre_step]
        uicase_pre_steps = [uicase_pre_step['pre_steps'] for uicase_pre_step in uicase_pre_steps]
        uicase_pre_steps_all=[]
        for uicase_pre in uicase_pre_steps:
            if uicase_pre != '':
                uicase_pre_steps_all.extend(uicase_pre.split('\r\n'))

        uicase_next_step = selectall('select next_steps from uicases')
        uicase_next_steps = [dict(next_steps=row[0]) for row in uicase_next_step]
        uicase_next_steps = [uicase_next_step['next_steps'] for uicase_next_step in uicase_next_steps]
        uicase_next_steps_all=[]
        for uicase_next in uicase_next_steps:
            if uicase_next != '':
                uicase_next_steps_all.extend(uicase_next.split('\r\n'))

        if uicase_name in uisitues_all:
            flash("该用例被测试集引用，不能删除~！")
        elif uicase_name in uicase_pre_steps_all or uicase_name in uicase_next_steps_all:
            flash("该案例被其他用例前置/后置事务引用，不能删除~！")
        else:
            cur = addUpdateDel('update uicases set activity = "2" where id=%s',[id])

            cur_uicases_del= selectone("SELECT * FROM uicases where id=%s and activity !=2",[id])
            if cur_uicases_del == ():
                flash('删除成功...')
            else:
                flash('删除失败...')

        return redirect(url_for('caseManage_uicases',category='a.username',value=session['username'],num=1))

# caseManage UI CASE EXEC
@app.route('/caseManage/uicase_exec/<int:id>', methods=['GET', 'POST'])
def caseManage_uicase_exec(id):
    if not session.get('logged_in'):
        abort(401)
    else:
        error = None
        newrun = RunUiTests(id,session['username'])
        res = newrun.getTestCases()
        return render_template('caseManage/uicase_exec.html',res=res,SITEURL=SITEURL, username=session['username'], caseManage_nav=caseManage_nav, caseManage_sub_nav_ui = caseManage_sub_nav_ui, caseManage_sub_nav_api = caseManage_sub_nav_api, caseManage_set_nav=caseManage_set_nav, operation=operation,current='uicases', pagename = '用例执行结果')

# caseManage UI CASES recyclebin
@app.route('/caseManage/uirecyclebin/<category>/<value>/<int:num>', methods=['GET', 'POST'])
def caseManage_uirecyclebin(category,value,num):
    if not session.get('logged_in'):
        abort(401)
    else:
        error = None
        if category == 'a.name':
            all_Count = selectall('SELECT count(1) FROM uicases a inner join user b on a.username=b.username where activity="2" and '+category+' like "%'+value+'%"')[0][0]
        else:
            all_Count = selectall('SELECT count(1) FROM uicases a inner join user b on a.username=b.username where activity="2" and '+category+'="'+value+'"')[0][0]
        all_Page = math.ceil(all_Count/page_Count)
        cur_usernames=selectall('SELECT b.zh_name FROM uicases a inner join user b ON a.username=b.username WHERE a.activity="2" GROUP BY a.username')
        usernames=[dict(zh_name=row[0]) for row in cur_usernames]
        cur_versions=selectall('SELECT version FROM uicases WHERE activity="2" group by version')
        versions=[dict(version=row[0]) for row in cur_versions]
        cur_models=selectall('SELECT model FROM uicases WHERE activity="2" group by model')
        models=[dict(model=row[0]) for row in cur_models]
        if request.method == 'POST':
            if request.form['select-model'].strip() == '':
                category = '1'
                value ='1'
            elif request.form['select-model'].strip() == '按名称' and request.form['query-name'].strip() != '':
                category = 'a.name'
                value = request.form['query-name']
            elif request.form['select-model'].strip() == '按版本' and request.form['query-version'].strip() != '':
                category = 'a.version'
                value = request.form['query-version']
            elif request.form['select-model'].strip() == '按模块' and request.form['query-model'].strip() != '':
                category = 'a.model'
                value = request.form['query-model']
            elif request.form['select-model'].strip() == '按用户' and request.form['query-username'].strip() != '':
                category = 'b.zh_name'
                value = request.form['query-username']
            return redirect(url_for('caseManage_uirecyclebin',category=category,value=value,num='1'))
        if category == 'a.name':
            cur = selectall('SELECT a.id,a.type,a.version, a.model, a.product, a.name,a.pre_steps, a.steps, a.next_steps,a.description,a.exec_result, b.zh_name, a.create_date FROM uicases a inner join user b on a.username=b.username where activity="2" and '+category+' like "%'+value+'%" order by a.id desc LIMIT '+str((num-1)*page_Count)+','+str(page_Count))
        else:
            cur = selectall('SELECT a.id,a.type,a.version, a.model, a.product, a.name,a.pre_steps, a.steps, a.next_steps,a.description,a.exec_result, b.zh_name, a.create_date FROM uicases a inner join user b on a.username=b.username where activity="2" and '+category+'="'+value+'" order by a.id desc LIMIT '+str((num-1)*page_Count)+','+str(page_Count))
        cases = [dict(id=row[0], type=row[1], version=row[2], model=row[3], product=row[4], name=row[5], pre_steps=row[6], steps=row[7], next_steps=row[8], description=row[9], exec_result=row[10], zh_name=row[11], create_date=row[12]) for row in cur]
        return render_template('caseManage/uicases_recyclebin.html', SITEURL=SITEURL, username=session['username'], cases=cases, caseManage_nav=caseManage_nav, caseManage_sub_nav_ui = caseManage_sub_nav_ui, caseManage_sub_nav_api = caseManage_sub_nav_api, caseManage_set_nav=caseManage_set_nav, recyclebin=recyclebin, all_Page=all_Page,category=category,value=value, num=num,usernames=usernames,versions=versions,models=models,current='uirecyclebin',error=error,pagename = '测试用例回收站')

# caseManage UI CASE DELETE forever
@app.route('/caseManage/uicase_recyclebin_delete/<int:id>', methods=['GET', 'POST'])
def caseManage_uicase_recyclebin_delete(id):
    if not session.get('logged_in'):
        abort(401)
    else:
        uicase = selectone('select name from uicases where id=%s',[id])
        uicases = [dict(name=row[0]) for row in uicase]
        uicase_name = uicases[0]['name']
        
        cur = addUpdateDel('delete from uicases where id=%s and activity=2',[id])

        cur_uicases_del= selectone("SELECT * FROM uicases where id=%s and activity=2",[id])
        if cur_uicases_del == ():
            flash('删除成功...')
        else:
            flash('删除失败...')

        return redirect(url_for('caseManage_uirecyclebin',category='a.username',value=session['username'],num=1))

# caseManage UI CASE submmit
@app.route('/caseManage/uicase_submit/<int:id>', methods=['GET', 'POST'])
def caseManage_uicase_submit(id):
    if not session.get('logged_in'):
        abort(401)
    else:
        uicase = selectone('select name from uicases where id=%s',[id])
        uicases = [dict(name=row[0]) for row in uicase]
        uicase_name = uicases[0]['name']
        
        cur = addUpdateDel('update uicases set activity=3 where id=%s',[id])

        cur_uicases_submint= selectone("SELECT * FROM uicases where id=%s and activity=3",[id])
        if cur_uicases_submint == ():
            flash('提交成功...')
        else:
            flash('提交失败...')

        return redirect(url_for('caseManage_uicases',category='a.username',value=session['username'],num=1))

# caseManage UI CASE DELETE restore
@app.route('/caseManage/uicase_recyclebin_restore/<int:id>', methods=['GET', 'POST'])
def caseManage_uicase_recyclebin_restore(id):
    if not session.get('logged_in'):
        abort(401)
    else:
        cur = addUpdateDel('update uicases set activity=0 where id=%s and activity=2',[id])

        cur_uicases_del= selectone("SELECT * FROM uicases where id=%s and activity=0",[id])
        if cur_uicases_del == ():
            flash('恢复失败...')
        else:
            flash('恢复成功...')

        return redirect(url_for('caseManage_uirecyclebin',category='a.username',value=session['username'],num=1))

# caseManage NEW UI CASE
@app.route('/caseManage/new_uicase', methods=['GET', 'POST'])
def caseManage_new_uicase():
    if not session.get('logged_in'):
        abort(401)
    error = None

    version = selectall('select version from versions')
    versions = [dict(version=row[0]) for row in version]
    versions = [version['version'] for version in versions]

    issuetype = selectall('select name from uicases where type="公共用例"')
    issuetypes = [dict(name=row[0]) for row in issuetype]

    nexttype = selectall('select name from uicases where type="后置用例"')
    nexttypes = [dict(name=row[0]) for row in nexttype]

    cur = selectall('SELECT keyword FROM uiset')
    list_steps = [dict(keyword=row[0]) for row in cur]
    if request.method == 'POST':
        uiname = selectall('select name from uicases')
        uinames = [dict(name=row[0]) for row in uiname]
        uinames = [uiname['name'] for uiname in uinames]

        if request.form['version'].strip() == '' or request.form['product'].strip() == '' or request.form['model'].strip() == '' or request.form['name'].strip() == '' or request.form['steps'].strip == '':
            error = '必输项不能为空'
        elif request.form['name'].strip() in uinames:
            error = "该用例已经存在"
        elif request.form['version'].strip() not in versions:
            error = "请选择正确的版本号"
        else:
            addUpdateDel('insert into uicases (type,version, model, product, name, pre_steps,steps,next_steps, description,activity, username, create_date) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                         [request.form['type'],request.form['version'], request.form['model'], request.form['product'], request.form['name'],request.form['pre-steps'], request.form['steps'],request.form['next-steps'], request.form['description'], '0', session['username'], time.strftime('%Y-%m-%d %X', time.localtime(time.time()))])

            cur_new= selectone("SELECT * FROM uicases WHERE name = %s",[request.form['name']])
            if cur_new != ():
                flash('创建成功...')
            else:
                flash('创建失败...')

            return redirect(url_for('caseManage_uicases',category='a.username',value=session['username'],num=1))
    return render_template('caseManage/new_uicase.html', list_steps=list_steps, SITEURL=SITEURL, username=session['username'], versions=versions, caseManage_nav=caseManage_nav, caseManage_sub_nav_ui = caseManage_sub_nav_ui, caseManage_sub_nav_api = caseManage_sub_nav_api, caseManage_set_nav=caseManage_set_nav,current='uicases', pagename = '新增测试用例', product=product, model_oma=model_oma, model_sicap=model_sicap, issuetypes=issuetypes,nexttypes=nexttypes, error=error)

# caseManage api CASES
@app.route('/caseManage/apicases/<category>/<value>/<int:num>', methods=['GET', 'POST'])
def caseManage_apicases(category,value,num):
    if not session.get('logged_in'):
        abort(401)
    else:
        error = None
        if category == 'a.name':
            all_Count = selectall('SELECT count(1) FROM apicases a inner join user b on a.username=b.username where activity="0" and '+category+' like "%'+value+'%"')[0][0]
        else:
            all_Count = selectall('SELECT count(1) FROM apicases a inner join user b on a.username=b.username where activity="0" and '+category+'="'+value+'"')[0][0]
        all_Page = math.ceil(all_Count/page_Count)
        cur_usernames=selectall('SELECT b.zh_name FROM apicases a inner join user b ON a.username=b.username WHERE a.activity="0" GROUP BY a.username')
        usernames=[dict(zh_name=row[0]) for row in cur_usernames]
        cur_versions=selectall('SELECT version FROM apicases WHERE activity="0" group by version')
        versions=[dict(version=row[0]) for row in cur_versions]
        cur_models=selectall('SELECT model FROM apicases WHERE activity="0" group by model')
        models=[dict(model=row[0]) for row in cur_models]
        if request.method == 'POST':
            if request.form['select-model'].strip() == '':
                category = '1'
                value ='1'
            elif request.form['select-model'].strip() == '按名称' and request.form['query-name'].strip() != '':
                category = 'a.name'
                value = request.form['query-name']
            elif request.form['select-model'].strip() == '按版本' and request.form['query-version'].strip() != '':
                category = 'a.version'
                value = request.form['query-version']
            elif request.form['select-model'].strip() == '按模块' and request.form['query-model'].strip() != '':
                category = 'a.model'
                value = request.form['query-model']
            elif request.form['select-model'].strip() == '按用户' and request.form['query-username'].strip() != '':
                category = 'b.zh_name'
                value = request.form['query-username']
            return redirect(url_for('caseManage_apicases',category=category,value=value,num='1'))
        if category == 'a.name':
            cur = selectall('SELECT a.id,a.type,a.version, a.model, a.product, a.name,a.pre_steps, a.steps, a.next_steps,a.description,a.exec_result, b.zh_name, a.create_date FROM apicases a inner join user b on a.username=b.username where activity="0" and '+category+' like "%'+value+'%" order by a.id desc LIMIT '+str((num-1)*page_Count)+','+str(page_Count))
        else:
            cur = selectall('SELECT a.id,a.type,a.version, a.model, a.product, a.name,a.pre_steps, a.steps, a.next_steps,a.description,a.exec_result, b.zh_name, a.create_date FROM apicases a inner join user b on a.username=b.username where activity="0" and '+category+'="'+value+'" order by a.id desc LIMIT '+str((num-1)*page_Count)+','+str(page_Count))
        cases = [dict(id=row[0], type=row[1], version=row[2], model=row[3], product=row[4], name=row[5], pre_steps=row[6], steps=row[7], next_steps=row[8], description=row[9], exec_result=row[10], zh_name=row[11], create_date=row[12]) for row in cur]
        return render_template('caseManage/apicases.html', SITEURL=SITEURL, username=session['username'], cases=cases, caseManage_nav=caseManage_nav, caseManage_sub_nav_api = caseManage_sub_nav_api, caseManage_sub_nav_ui = caseManage_sub_nav_ui, caseManage_set_nav=caseManage_set_nav, operation=operation, all_Page=all_Page,category=category,value=value, num=num,usernames=usernames,versions=versions,models=models,current='apicases',error=error,pagename = '测试用例')

# caseManage API CASE EDIT
@app.route('/caseManage/apicase_edit/<int:id>', methods=['GET', 'POST'])
def caseManage_apicase_edit(id):
    if not session.get('logged_in'):
        abort(401)
    else:
        error = None
        cur = selectall('SELECT name,request FROM apiset')
        apisets = [dict(name=row[0],request=row[1]) for row in cur]
        cur = selectone('SELECT type, version, name, product, model, pre_steps, steps, next_steps,description FROM apicases where id=%s',[id])
        cases = [dict(type=row[0], version=row[1], name=row[2], product=row[3], model=row[4], pre_steps=row[5], steps=row[6], next_steps=row[7], description=row[8]) for row in cur]
    return render_template('caseManage/apicase_edit.html',SITEURL=SITEURL, username=session['username'], case=cases[0], caseManage_nav=caseManage_nav, caseManage_sub_nav_ui = caseManage_sub_nav_ui, caseManage_sub_nav_api = caseManage_sub_nav_api, caseManage_set_nav=caseManage_set_nav, operation=operation,current='apicases', pagename = '接口编辑', id=id)

# caseManage API CASE QUERY
@app.route('/caseManage/apicase_query/<int:id>', methods=['GET', 'POST'])
def caseManage_apicase_query(id):
    if not session.get('logged_in'):
        abort(401)
    else:
        cur = selectone('SELECT type, version, name, product, model, pre_steps, steps, next_steps, description FROM apicases where id=%s',[id])
        cases = [dict(type=row[0], version=row[1], name=row[2], product=row[3], model=row[4], pre_steps=row[5],steps=row[6],next_steps=row[7], description=row[8]) for row in cur]
        steps = cases[0]['steps'].split('\r\n')
        case_name = cases[0]['name']
        case_details = []
        for i in range(len(steps)):
            cur = selectone('select name,path,method,request,checks,parameter from apidates where case_name=%s and name=%s',[case_name,str(i)+'_'+steps[i]])
            case_detail = [dict(name=row[0], path=row[1], method=row[2], request=row[3], checks=row[4], parameter=row[5]) for row in cur]
            case_details.append(case_detail[0])
        return render_template('caseManage/apicase_query.html',SITEURL=SITEURL, username=session['username'], case_details=case_details, case=cases[0], caseManage_nav=caseManage_nav, caseManage_sub_nav_ui = caseManage_sub_nav_ui, caseManage_sub_nav_api = caseManage_sub_nav_api, caseManage_set_nav=caseManage_set_nav, operation=operation,current='apicases', pagename = '接口查看')

# caseManage api CASE DELETE
@app.route('/caseManage/apicase_delete/<int:id>', methods=['GET', 'POST'])
def caseManage_apicase_delete(id):
    if not session.get('logged_in'):
        abort(401)
    else:
        apisitue = selectall('select steps from apisitues')
        apisitues = [dict(steps=row[0]) for row in apisitue]
        apisitues = [apisitue['steps'] for apisitue in apisitues]
        apisitues_all=[]
        for apisitue in apisitues:
            apisitues_all.extend(apisitue.split('\r\n'))

        apicase = selectone('select name from apicases where id=%s',[id])
        apicases = [dict(name=row[0]) for row in apicase]
        apicase_name = apicases[0]['name']
        
        apicase_pre_step = selectall('select pre_steps from apicases')
        apicase_pre_steps = [dict(pre_steps=row[0]) for row in apicase_pre_step]
        apicase_pre_steps = [apicase_pre_step['pre_steps'] for apicase_pre_step in apicase_pre_steps]
        apicase_pre_steps_all=[]
        for apicase_pre in apicase_pre_steps:
            if apicase_pre != '':
                apicase_pre_steps_all.extend(apicase_pre.split('\r\n'))

        apicase_next_step = selectall('select next_steps from apicases')
        apicase_next_steps = [dict(next_steps=row[0]) for row in apicase_next_step]
        apicase_next_steps = [apicase_next_step['next_steps'] for apicase_next_step in apicase_next_steps]
        apicase_next_steps_all=[]
        for apicase_next in apicase_next_steps:
            if apicase_next != '':
                apicase_next_steps_all.extend(apicase_next.split('\r\n'))

        if apicase_name in apisitues_all:
            flash("该用例被测试集引用，不能删除~！")
        elif apicase_name in apicase_pre_steps_all or apicase_name in apicase_next_steps_all:
            flash("该案例被其他用例前置/后置事务引用，不能删除~！")
        else:
            cur = addUpdateDel('update apicases set activity = "2" where id=%s',[id])

            cur_apicases_del= selectone("SELECT * FROM apicases where id=%s and activity !=2",[id])
            if cur_apicases_del == ():
                flash('删除成功...')
            else:
                flash('删除失败...')

        return redirect(url_for('caseManage_apicases',category='a.username',value=session['username'],num=1))

# caseManage API CASE EXEC
@app.route('/caseManage/apicase_exec/<int:id>', methods=['GET', 'POST'])
def caseManage_apicase_exec(id):
    if not session.get('logged_in'):
        abort(401)
    else:
        error = None
        newrun = RunTests(id,session['username'])
        res=newrun.getTestCases()

        return render_template('caseManage/apicase_exec.html',SITEURL=SITEURL, username=session['username'], res=res,caseManage_nav=caseManage_nav, caseManage_sub_nav_ui = caseManage_sub_nav_ui, caseManage_sub_nav_api = caseManage_sub_nav_api, caseManage_set_nav=caseManage_set_nav, operation=operation, pagename = '接口执行结果')

# caseManage API CASES recyclebin
@app.route('/caseManage/apirecyclebin/<category>/<value>/<int:num>', methods=['GET', 'POST'])
def caseManage_apirecyclebin(category,value,num):
    if not session.get('logged_in'):
        abort(401)
    else:
        error = None
        if category == 'a.name':
            all_Count = selectall('SELECT count(1) FROM apicases a inner join user b on a.username=b.username where activity="2" and '+category+' like "%'+value+'%"')[0][0]
        else:
            all_Count = selectall('SELECT count(1) FROM apicases a inner join user b on a.username=b.username where activity="2" and '+category+'="'+value+'"')[0][0]
        all_Page = math.ceil(all_Count/page_Count)
        cur_usernames=selectall('SELECT b.zh_name FROM apicases a inner join user b ON a.username=b.username WHERE a.activity="2" GROUP BY a.username')
        usernames=[dict(zh_name=row[0]) for row in cur_usernames]
        cur_versions=selectall('SELECT version FROM apicases WHERE activity="2" group by version')
        versions=[dict(version=row[0]) for row in cur_versions]
        cur_models=selectall('SELECT model FROM apicases WHERE activity="2" group by model')
        models=[dict(model=row[0]) for row in cur_models]
        if request.method == 'POST':
            if request.form['select-model'].strip() == '':
                category = '1'
                value ='1'
            elif request.form['select-model'].strip() == '按名称' and request.form['query-name'].strip() != '':
                category = 'a.name'
                value = request.form['query-name']
            elif request.form['select-model'].strip() == '按版本' and request.form['query-version'].strip() != '':
                category = 'a.version'
                value = request.form['query-version']
            elif request.form['select-model'].strip() == '按模块' and request.form['query-model'].strip() != '':
                category = 'a.model'
                value = request.form['query-model']
            elif request.form['select-model'].strip() == '按用户' and request.form['query-username'].strip() != '':
                category = 'b.zh_name'
                value = request.form['query-username']
            return redirect(url_for('caseManage_apirecyclebin',category=category,value=value,num='1'))
        if category == 'a.name':
            cur = selectall('SELECT a.id,a.type,a.version, a.model, a.product, a.name,a.pre_steps, a.steps, a.next_steps,a.description,a.exec_result, b.zh_name, a.create_date FROM apicases a inner join user b on a.username=b.username where activity="2" and '+category+' like "%'+value+'%" order by a.id desc LIMIT '+str((num-1)*page_Count)+','+str(page_Count))
        else:
            cur = selectall('SELECT a.id,a.type,a.version, a.model, a.product, a.name,a.pre_steps, a.steps, a.next_steps,a.description,a.exec_result, b.zh_name, a.create_date FROM apicases a inner join user b on a.username=b.username where activity="2" and '+category+'="'+value+'" order by a.id desc LIMIT '+str((num-1)*page_Count)+','+str(page_Count))
        cases = [dict(id=row[0], type=row[1], version=row[2], model=row[3], product=row[4], name=row[5], pre_steps=row[6], steps=row[7], next_steps=row[8], description=row[9], exec_result=row[10], zh_name=row[11], create_date=row[12]) for row in cur]
        return render_template('caseManage/apicases_recyclebin.html', SITEURL=SITEURL, username=session['username'], cases=cases, caseManage_nav=caseManage_nav, caseManage_sub_nav_api = caseManage_sub_nav_api, caseManage_sub_nav_ui = caseManage_sub_nav_ui, caseManage_set_nav=caseManage_set_nav, recyclebin=recyclebin, all_Page=all_Page,category=category,value=value, num=num,usernames=usernames,versions=versions,models=models,current='apirecyclebin',error=error,pagename = '测试用例回收站')

# caseManage api CASE DELETE forever
@app.route('/caseManage/apicase_recyclebin_delete/<int:id>', methods=['GET', 'POST'])
def caseManage_apicase_recyclebin_delete(id):
    if not session.get('logged_in'):
        abort(401)
    else:
        apicase = selectone('select name from apicases where id=%s',[id])
        apicases = [dict(name=row[0]) for row in apicase]
        apicase_name = apicases[0]['name']
        
        addUpdateDel('delete from apicases where id=%s and activity=2',[id])
        addUpdateDel('delete from apidates where case_name=%s',[apicase_name])

        cur_apidates_del= selectone("SELECT * FROM apidates where case_name=%s",[apicase_name])
        cur_apicases_del= selectone("SELECT * FROM apicases where id=%s and activity=2",[id])
        if cur_apidates_del == () and cur_apidates_del == ():
            flash('删除成功...')
        else:
            flash('删除失败...')

        return redirect(url_for('caseManage_apirecyclebin',category='a.username',value=session['username'],num=1))

# caseManage api CASE DELETE restore
@app.route('/caseManage/apicase_recyclebin_restore/<int:id>', methods=['GET', 'POST'])
def caseManage_apicase_recyclebin_restore(id):
    if not session.get('logged_in'):
        abort(401)
    else:
        cur = addUpdateDel('update apicases set activity=0 where id=%s and activity=2',[id])

        cur_apicases_del= selectone("SELECT * FROM apicases where id=%s and activity=0",[id])
        if cur_apicases_del == ():
            flash('恢复失败...')
        else:
            flash('恢复成功...')

        return redirect(url_for('caseManage_apirecyclebin',category='a.username',value=session['username'],num=1))

# caseManage API CASE submmit
@app.route('/caseManage/apicase_submit/<int:id>', methods=['GET', 'POST'])
def caseManage_apicase_submit(id):
    if not session.get('logged_in'):
        abort(401)
    else:
        apicase = selectone('select name from apicases where id=%s',[id])
        apicases = [dict(name=row[0]) for row in apicase]
        apicase_name = apicases[0]['name']
        
        cur = addUpdateDel('update apicases set activity=3 where id=%s',[id])

        cur_apicases_submint= selectone("SELECT * FROM apicases where id=%s and activity=3",[id])
        if cur_apicases_submint == ():
            flash('提交失败...')
        else:
            flash('提交成功...')

        return redirect(url_for('caseManage_apicases',category='a.username',value=session['username'],num=1))

# caseManage NEW API CASE
@app.route('/caseManage/new_apicase', methods=['GET', 'POST'])
def caseManage_new_apicase():
    if not session.get('logged_in'):
        abort(401)
    cur = selectall('SELECT name,request FROM apiset')
    apisets = [dict(name=row[0],request=row[1]) for row in cur]
    error = None

    version = selectall('select version from versions')
    versions = [dict(version=row[0]) for row in version]
    versions = [version['version'] for version in versions]

    issuetype = selectall('select name from apicases where type="公共用例"')
    issuetypes = [dict(name=row[0]) for row in issuetype]

    nexttype = selectall('select name from apicases where type="后置用例"')
    nexttypes = [dict(name=row[0]) for row in nexttype]

    if request.method == 'POST':
        apiname = selectall('select name from apicases')
        apinames = [dict(name=row[0]) for row in apiname]
        apinames = [apiname['name'] for apiname in apinames]

        if request.form['version'].strip() == '' or request.form['product'].strip() == '' or request.form['model'].strip() == '' or request.form['name'].strip() == '':
            error = '必输项不能为空'
        elif request.form['name'].strip() in apinames:
            error = "该用例已经存在"
        elif request.form['version'].strip() not in versions:
            error = "请选择正确的版本号"
        else:
            addUpdateDel('insert into apicases (type, version, model, product, name, pre_steps, steps, next_steps, description,activity, username, create_date) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                         [request.form['type'], request.form['version'], request.form['model'], request.form['product'], request.form['name'], request.form['pre-steps'], request.form['steps'], request.form['next-steps'], request.form['description'], '0', session['username'], time.strftime('%Y-%m-%d %X', time.localtime(time.time()))])

            pre_step = selectone('SELECT name FROM apidates WHERE case_name in %s',[request.form['pre-steps'].split('\r\n')])
            pre_steps = [dict(pre_step=row[0]) for row in pre_step]
            pre_steps = [pre_step['pre_step'] for pre_step in pre_steps]
            pre_steps = deline(pre_steps)

            next_step = selectone('SELECT name FROM apidates WHERE case_name in %s',[request.form['next-steps'].split('\r\n')])
            next_steps = [dict(next_step=row[0]) for row in next_step]
            next_steps = [next_step['next_step'] for next_step in next_steps]
            next_steps = deline(next_steps)

            steps = pre_steps+request.form['steps'].split('\r\n')+next_steps

            for i in range(len(steps)):
                cur = selectone('select name,path,method,request,checks from apiset where name = %s',[steps[i]])
                cases = [dict(name=row[0], path=row[1], method=row[2], request=row[3], checks=row[4]) for row in cur]
                addUpdateDel('insert into apidates (case_name,name,path,method,request,checks,username,create_date) values (%s,%s,%s,%s,%s,%s,%s,%s)',[request.form['name'], str(i)+'_'+steps[i], cn_to_uk(cases[0]['path']), cases[0]['method'], cn_to_uk(cases[0]['request']), cn_to_uk(cases[0]['checks']), session['username'], time.strftime('%Y-%m-%d %X', time.localtime(time.time()))])

            cur_apicases_new= selectone("SELECT * FROM apicases WHERE name = %s",[request.form['name']])
            cur_apidates_new= selectone("SELECT * FROM apidates WHERE case_name = %s,name = %s",[request.form['name'],steps[-1]])
            if cur_apicases_new != () and cur_apidates_new !=():
                flash('创建成功...')
            else:
                flash('创建失败...')

            return redirect(url_for('caseManage_apidate_edit_cases_query',case_name=request.form["name"]))
    return render_template('caseManage/new_apicase.html', SITEURL=SITEURL, username=session['username'], apisets=apisets, model_sicap=model_sicap, model_oma=model_oma, versions=versions, caseManage_nav=caseManage_nav, caseManage_sub_nav_ui = caseManage_sub_nav_ui, caseManage_sub_nav_api = caseManage_sub_nav_api, caseManage_set_nav=caseManage_set_nav, product=product, issuetypes=issuetypes,nexttypes=nexttypes, current='apicases',pagename = '新增用例',error=error)

@app.route('/caseManage/apidate_edit_cases_query/<case_name>', methods=['GET', 'POST'])
def caseManage_apidate_edit_cases_query(case_name):
    if not session.get('logged_in'):
        abort(401)
    error = None
    cur = selectone('SELECT name from apidates WHERE case_name = %s',[case_name])
    names = [dict(name=row[0]) for row in cur]
    if request.method == 'POST':
        if request.form['choice'].strip() == '':
            error = '必输项不能为空'
        else:
            cur = selectone('select name,path,method,request,checks,parameter from apidates where case_name=%s and name=%s',[case_name,request.form['choice']])
            cases = [dict(name=row[0], path=row[1], method=row[2], request=row[3], checks=row[4], parameter=row[5]) for row in cur]
            return render_template('caseManage/apidate_edit_cases.html',SITEURL=SITEURL, username=session['username'], case=cases[0], names=names, case_name=case_name, caseManage_nav=caseManage_nav, caseManage_sub_nav_ui = caseManage_sub_nav_ui, caseManage_sub_nav_api = caseManage_sub_nav_api, caseManage_set_nav=caseManage_set_nav, pagename = '编辑接口数据')
    return render_template('caseManage/apidate_edit_cases.html',SITEURL=SITEURL, username=session['username'], names=names, case_name=case_name, caseManage_nav=caseManage_nav, caseManage_sub_nav_ui = caseManage_sub_nav_ui, caseManage_sub_nav_api = caseManage_sub_nav_api, caseManage_set_nav=caseManage_set_nav, pagename = '编辑接口数据')

@app.route('/caseManage/apidate_edit_cases_save/<case_name>', methods=['GET', 'POST'])
def caseManage_apidate_edit_cases_save(case_name):
    if not session.get('logged_in'):
        abort(401)
    error=None
    if request.method == 'POST':
        if request.form['request'].strip() == '' or request.form['checks'].strip() == '':
            error = '必输项不能为空'
        elif is_dict(request.form['request'].strip()) == False:
            error = '请求格式不对'
        elif is_dict(request.form['checks'].strip()) == False:
            error = '检查项格式不对'
        elif request.form['parameter'].strip() != '':
            if is_list(request.form['parameter'].strip()) == False:
                error = '参数格式不对'
        else:
            addUpdateDel('update apidates set request=%s, checks=%s, parameter=%s where case_name=%s and name=%s',[cn_to_uk(request.form['request']),cn_to_uk(request.form['checks']),cn_to_uk(request.form['parameter']),case_name,request.form['name']])

            cur_edit= selectone("SELECT request,checks,parameter FROM apidates where case_name=%s and name=%s",[case_name,request.form['name']])
            apidates_edit = [dict(request=row[0],checks=row[1],parameter=row[2]) for row in cur_edit]
            apidates_request = apidates_edit[0]['request']
            apidates_checks = apidates_edit[0]['checks']
            apidates_parameter = apidates_edit[0]['parameter']
            if request.form['request'] == apidates_request and request.form['checks'] == apidates_checks and request.form['parameter'] == apidates_parameter:
                flash('编辑成功...')
            else:
                flash('编辑失败...')

    return render_template('caseManage/apidate_edit_cases.html',SITEURL=SITEURL, username=session['username'], case_name=case_name, caseManage_nav=caseManage_nav, caseManage_sub_nav_ui = caseManage_sub_nav_ui, caseManage_sub_nav_api = caseManage_sub_nav_api, caseManage_set_nav=caseManage_set_nav,error=error,current='apicases', pagename = '编辑接口数据')

# 密码修改
@app.route('/caseManage/modify_passwd', methods=['GET', 'POST'])
def caseManage_modify_passwd():
    if not session.get('logged_in'):
        abort(401)
    error = None
    if request.method == 'POST':
        cur = selectone('select password from user where username = %s',(session['username'],))
        pw = cur[0][0]
        if request.form['pw_old'].strip() == '' or request.form['pw_new_o'].strip() == '' or request.form['pw_new_t'].strip() == '':
            error = '请输入密码'
        elif request.form['pw_old'].strip() != decrypt(pw):
            error = '当前密码不正确'
        elif request.form['pw_new_o'].strip() != request.form['pw_new_t'].strip():
            error = '新密码和确认密码不一致'
        else:
            addUpdateDel('update user set password = %s where username = %s',(encrypt(request.form['pw_new_o'].strip()),session['username'],))
            flash('密码修改成功...')
    return render_template('caseManage/modify_passwd.html',SITEURL=SITEURL, username=session['username'],  caseManage_nav=caseManage_nav, caseManage_sub_nav_ui = caseManage_sub_nav_ui, caseManage_sub_nav_api = caseManage_sub_nav_api, caseManage_set_nav=caseManage_set_nav, operation=operation, pagename = '修改密码', error=error)


# 退出页面
@app.route('/caseManage/logout')
def caseManage_logout():
    session.pop('logged_in', None)
    flash('你已经退出...')
    return redirect(url_for('caseManage_login'))

###############################
#           review
###############################
# 首页
@app.route('/review')
def review_initial():
    return redirect(url_for('review_login'))

# 登陆页面
@app.route('/review/login', methods=['GET', 'POST'])
def review_login():
    if session.get('logged_in'):
        return redirect(url_for('review_index',current_user = session['username']))
    error = None
    result = selectall('select username,password from user')
    date = []
    for i in list(range(len(result))):
        date.append(result[i][0])
    if request.method == 'POST':
        session['username']=request.form['username']
        if request.form['username'] in date:
            cur = selectone('select username,password from user where username = %s',(request.form['username'],))
            uname,pw = cur[0]
            if request.form['username'] != uname:
                error = '无效的用户名'
            elif request.form['password'] != decrypt(pw):
                error = '无效的密码'
            elif request.form['username'] not in review_user:
                error = '该用户没有审核权限'
            else:
                session['logged_in'] = True
                addUpdateDel('update user set last_login = %s where username = %s',[time.strftime('%Y-%m-%d %X', time.localtime(time.time())), session['username']])
                flash('你已经登陆...')
                return redirect(url_for('review_index',current_user = session['username']))
        else:
            error = '用户名不存在'
    return render_template('review/login.html', error=error)

@app.route('/review/<current_user>/')
def review_index(current_user):
    if session.get('logged_in'):
        return render_template('review/index.html', username=session['username'], review_nav=review_nav, review_sub_nav_ui = review_sub_nav_ui, review_sub_nav_api = review_sub_nav_api, pagename = '主页')
    else:
        return redirect(url_for('review_login'))

# REVIEW UI CASES
@app.route('/review/uicases/<category>/<value>/<int:num>', methods=['GET', 'POST'])
def review_uicases(category,value,num):
    if not session.get('logged_in') or session['username'] not in review_user:
        abort(401)
    else:
        error = None
        if category == 'a.name':
            all_Count = selectall('SELECT count(1) FROM uicases a inner join user b on a.username=b.username where activity="3" and '+category+' like "%'+value+'%"')[0][0]
        else:
            all_Count = selectall('SELECT count(1) FROM uicases a inner join user b on a.username=b.username where activity="3" and '+category+'="'+value+'"')[0][0]
        all_Page = math.ceil(all_Count/page_Count)
        cur_usernames=selectall('SELECT b.zh_name FROM uicases a inner join user b ON a.username=b.username WHERE a.activity="3" GROUP BY a.username')
        usernames=[dict(zh_name=row[0]) for row in cur_usernames]
        cur_versions=selectall('SELECT version FROM uicases WHERE activity="3" group by version')
        versions=[dict(version=row[0]) for row in cur_versions]
        cur_models=selectall('SELECT model FROM uicases WHERE activity="3" group by model')
        models=[dict(model=row[0]) for row in cur_models]
        if request.method == 'POST':
            if request.form['select-model'].strip() == '':
                category = '1'
                value ='1'
            elif request.form['select-model'].strip() == '按名称' and request.form['query-name'].strip() != '':
                category = 'a.name'
                value = request.form['query-name']
            elif request.form['select-model'].strip() == '按版本' and request.form['query-version'].strip() != '':
                category = 'a.version'
                value = request.form['query-version']
            elif request.form['select-model'].strip() == '按模块' and request.form['query-model'].strip() != '':
                category = 'a.model'
                value = request.form['query-model']
            elif request.form['select-model'].strip() == '按用户' and request.form['query-username'].strip() != '':
                category = 'b.zh_name'
                value = request.form['query-username']
            return redirect(url_for('review_uicases',category=category,value=value,num='1'))
        if category == 'a.name':
            cur = selectall('SELECT a.id,a.type,a.version, a.model, a.product, a.name,a.pre_steps, a.steps, a.next_steps,a.description,a.exec_result, b.zh_name, a.create_date FROM uicases a inner join user b on a.username=b.username where activity="3" and '+category+' like "%'+value+'%" order by a.id desc LIMIT '+str((num-1)*page_Count)+','+str(page_Count))
        else:
            cur = selectall('SELECT a.id,a.type,a.version, a.model, a.product, a.name,a.pre_steps, a.steps, a.next_steps,a.description,a.exec_result, b.zh_name, a.create_date FROM uicases a inner join user b on a.username=b.username where activity="3" and '+category+'="'+value+'" order by a.id desc LIMIT '+str((num-1)*page_Count)+','+str(page_Count))
        cases = [dict(id=row[0], type=row[1], version=row[2], model=row[3], product=row[4], name=row[5], pre_steps=row[6], steps=row[7], next_steps=row[8], description=row[9], exec_result=row[10], zh_name=row[11], create_date=row[12]) for row in cur]
        return render_template('review/uireview.html', SITEURL=SITEURL, username=session['username'], cases=cases, review_nav=review_nav, review_sub_nav_ui = review_sub_nav_ui, review_sub_nav_api = review_sub_nav_api, review_operation=review_operation, all_Page=all_Page,usernames=usernames,versions=versions,models=models,category=category,value=value,num=num,current='uicases', pagename = '测试用例')

# REVIEW UI CASE QUERY
@app.route('/review/uicase_query/<int:id>', methods=['GET', 'POST'])
def review_uicase_query(id):
    if not session.get('logged_in'):
        abort(401)
    else:
        cur = selectone('SELECT type,version, model, product, name,pre_steps, steps, description,next_steps, username, create_date FROM uicases where id=%s',[id])
        cases = [dict(type=row[0], version=row[1], model=row[2], product=row[3], name=row[4], pre_steps=row[5], steps=row[6], description=row[7], next_steps=row[8], username=row[9], create_date=row[10]) for row in cur]
    return render_template('review/uicase_review.html', SITEURL=SITEURL, username=session['username'], case=cases[0], review_nav=review_nav, review_sub_nav_ui = review_sub_nav_ui, review_sub_nav_api = review_sub_nav_api, review_operation=review_operation, id=id, current='uicases',pagename = '用例审核')


# UI CASE REVIEW
@app.route('/review/uicase_review/<int:id>', methods=['GET', 'POST'])
def uicase_review(id):
    if not session.get('logged_in') or session['username'] not in review_user:
        abort(401)
    else:
        cur = addUpdateDel('update uicases set activity="1" where id=%s',[id])

        cur_new= selectone("SELECT * FROM uicases WHERE id = %s activity='1'",[id])
        if cur_new != ():
            flash('审核成功...')
        else:
            flash('审核失败...')
        return redirect(url_for('review_uicases',category='a.username',value=session['username'],num=1))

# UI CASE EXEC
@app.route('/review/uicase_exec/<int:id>', methods=['GET', 'POST'])
def review_uicase_exec(id):
    if not session.get('logged_in') or session['username'] not in review_user:
        abort(401)
    else:
        error = None
        newrun = RunUiTests(id,session['username'])
        res = newrun.getTestCases()
        return render_template('review/uicase_exec.html',res=res,SITEURL=SITEURL, username=session['username'], nav=nav, sub_nav_ui = sub_nav_ui, sub_nav_api = sub_nav_api, set_nav=set_nav, operation=operation, pagename = '用例执行结果')

# REVIEW API CASE
@app.route('/review/apicases/<category>/<value>/<int:num>', methods=['GET', 'POST'])
def review_apicases(category,value,num):
    if not session.get('logged_in') or session['username'] not in review_user:
        abort(401)
    else:
        error = None
        if category == 'a.name':
            all_Count = selectall('SELECT count(1) FROM apicases a inner join user b on a.username=b.username where activity="3" and '+category+' like "%'+value+'%"')[0][0]
        else:
            all_Count = selectall('SELECT count(1) FROM apicases a inner join user b on a.username=b.username where activity="3" and '+category+'="'+value+'"')[0][0]
        all_Page = math.ceil(all_Count/page_Count)
        cur_usernames=selectall('SELECT b.zh_name FROM apicases a inner join user b ON a.username=b.username WHERE a.activity="3" GROUP BY a.username')
        usernames=[dict(zh_name=row[0]) for row in cur_usernames]
        cur_versions=selectall('SELECT version FROM apicases WHERE activity="3" group by version')
        versions=[dict(version=row[0]) for row in cur_versions]
        cur_models=selectall('SELECT model FROM apicases WHERE activity="3" group by model')
        models=[dict(model=row[0]) for row in cur_models]
        if request.method == 'POST':
            if request.form['select-model'].strip() == '':
                category = '1'
                value ='1'
            elif request.form['select-model'].strip() == '按名称' and request.form['query-name'].strip() != '':
                category = 'a.name'
                value = request.form['query-name']
            elif request.form['select-model'].strip() == '按版本' and request.form['query-version'].strip() != '':
                category = 'a.version'
                value = request.form['query-version']
            elif request.form['select-model'].strip() == '按模块' and request.form['query-model'].strip() != '':
                category = 'a.model'
                value = request.form['query-model']
            elif request.form['select-model'].strip() == '按用户' and request.form['query-username'].strip() != '':
                category = 'b.zh_name'
                value = request.form['query-username']
            return redirect(url_for('review_apicases',category=category,value=value,num='1'))
        if category == 'a.name':
            cur = selectall('SELECT a.id,a.type,a.version, a.model, a.product, a.name,a.pre_steps, a.steps, a.next_steps,a.description,a.exec_result, b.zh_name, a.create_date FROM apicases a inner join user b on a.username=b.username where activity="3" and '+category+' like "%'+value+'%" order by a.id desc LIMIT '+str((num-1)*page_Count)+','+str(page_Count))
        else:
            cur = selectall('SELECT a.id,a.type,a.version, a.model, a.product, a.name,a.pre_steps, a.steps, a.next_steps,a.description,a.exec_result, b.zh_name, a.create_date FROM apicases a inner join user b on a.username=b.username where activity="3" and '+category+'="'+value+'" order by a.id desc LIMIT '+str((num-1)*page_Count)+','+str(page_Count))
        cases = [dict(id=row[0], type=row[1], version=row[2], model=row[3], product=row[4], name=row[5], pre_steps=row[6], steps=row[7], next_steps=row[8], description=row[9], exec_result=row[10], zh_name=row[11], create_date=row[12]) for row in cur]
        return render_template('review/apireview.html', SITEURL=SITEURL, username=session['username'], cases=cases, review_nav=review_nav, review_sub_nav_ui = review_sub_nav_ui, review_sub_nav_api = review_sub_nav_api, review_operation=review_operation, all_Page=all_Page,usernames=usernames,versions=versions,models=models,category=category,value=value,num=num,current='apicases', pagename = '接口测试用例')

# REVIEW API CASE QUERY
@app.route('/review/apicase_query/<int:id>', methods=['GET', 'POST'])
def review_apicase_query(id):
    if not session.get('logged_in') or session['username'] not in review_user:
        abort(401)
    else:
        cur = selectone('SELECT type, version, name, product, model, pre_steps, steps, next_steps, description FROM apicases where id=%s',[id])
        cases = [dict(type=row[0], version=row[1], name=row[2], product=row[3], model=row[4], pre_steps=row[5], steps=row[6], next_steps=row[7], description=row[8]) for row in cur]
        steps = cases[0]['steps'].split('\r\n')
        case_name = cases[0]['name']
        case_details = []
        for i in range(len(steps)):
            cur = selectone('select name,path,method,request,checks,parameter from apidates where case_name=%s and name=%s',[case_name,str(i)+'_'+steps[i]])
            case_detail = [dict(name=row[0], path=row[1], method=row[2], request=row[3], checks=row[4], parameter=row[5]) for row in cur]
            case_details.append(case_detail[0])
        return render_template('review/apicase_review.html',SITEURL=SITEURL, username=session['username'], case_details=case_details, case=cases[0], review_nav=review_nav, review_sub_nav_ui = review_sub_nav_ui, review_sub_nav_api = review_sub_nav_api, review_operation=review_operation, id=id,current='apicases', pagename = '用例审核')

# API CASE REVIEW
@app.route('/review/apicase_review/<int:id>', methods=['GET', 'POST'])
def apicase_review(id):
    if not session.get('logged_in') or session['username'] not in review_user:
        abort(401)
    else:
        cur = addUpdateDel('update apicases set activity="1" where id=%s',[id])

        cur_new= selectone("SELECT * FROM apicases WHERE id = %s activity='1'",[id])
        if cur_new != ():
            flash('审核成功...')
        else:
            flash('审核失败...')

        return redirect(url_for('review_apicases',category='a.username',value=session['username'],num=1))

# API CASE EXEC
@app.route('/review/apicase_exec/<int:id>', methods=['GET', 'POST'])
def review_apicase_exec(id):
    if not session.get('logged_in') or session['username'] not in review_user:
        abort(401)
    else:
        error = None
        newrun = RunTests(id,session['username'])
        res=newrun.getTestCases()

        return render_template('review/apicase_exec.html',SITEURL=SITEURL, username=session['username'], res=res, review_nav=review_nav, review_sub_nav_ui = review_sub_nav_ui, review_sub_nav_api = review_sub_nav_api, review_operation=review_operation,current='apicases', pagename = '接口执行结果')

# 密码修改
@app.route('/review/modify_passwd', methods=['GET', 'POST'])
def review_modify_passwd():
    if not session.get('logged_in'):
        abort(401)
    error = None
    if request.method == 'POST':
        cur = selectone('select password from user where username = %s',(session['username'],))
        pw = cur[0][0]
        if request.form['pw_old'].strip() == '' or request.form['pw_new_o'].strip() == '' or request.form['pw_new_t'].strip() == '':
            error = '请输入密码'
        elif request.form['pw_old'].strip() != decrypt(pw):
            error = '当前密码不正确'
        elif request.form['pw_new_o'].strip() != request.form['pw_new_t'].strip():
            error = '新密码和确认密码不一致'
        else:
            addUpdateDel('update user set password = %s where username = %s',(encrypt(request.form['pw_new_o'].strip()),session['username'],))
            flash('密码修改成功...')
    return render_template('review/modify_passwd.html',SITEURL=SITEURL, username=session['username'],  review_nav=review_nav, review_sub_nav_ui = review_sub_nav_ui, review_sub_nav_api = review_sub_nav_api, operation=operation, pagename = '修改密码', error=error)


# 退出页面
@app.route('/review/logout')
def review_logout():
    session.pop('logged_in', None)
    flash('你已经退出...')
    return redirect(url_for('review_login'))

##############################
#         admin
##############################
# 重置密码
@app.route('/reset_passwd', methods=['GET', 'POST'])
def reset_passwd():
    if not session.get('logged_in') or (session.get('logged_in') and session['username'] != 'admin'):
        abort(401)
    try:
        error =None
        cur = selectall('select username from user')
        usernames = [dict(username=row[0]) for row in cur]

        if request.form['username'].strip() == '' or request.form['pw_new_o'].strip == '' or request.form['pw_new_t'].strip == '':
            error = '必输项不能为空'
        elif request.form['pw_new_o'].strip != request.form['pw_new_t'].strip:
            error = '两次密码输入不一致'
        else:
            addUpdateDel('update user set password = %s where username = %s',[encrypt(request.form['pw_new_o']),request.form['username']])
            flash("重置密码成功...")
    except Exception as e:
        error = str(err)
    finally:
        return render_template('admin/reset_passwd.html', username=session['username'], usernames=usernames, nav=nav, sub_nav_ui = sub_nav_ui, sub_nav_api = sub_nav_api, set_nav=set_nav, operation=operation, error=error, pagename = '重置密码')


# 用户注册页面
@app.route('/register', methods=['GET', 'POST'])
def register():
    if not session.get('logged_in'):
        abort(401)
    try:
        error = None
        cur = selectall('select username from user')
        users = [dict(username=row[0]) for row in cur]
        users = [user['username'] for user in users]
        if request.method == 'POST':
            if request.form['username'].strip() == '' and request.form['password_o'].strip() == '' and request.form['password_t'].strip() == '' and request.form['fullname'].strip() == '':
                error = '用户名/密码/全名不能为空'
            elif request.form['username'].strip() in users:
                error = '用户已存在'
            elif request.form['password_o'].strip() != request.form['password_t'].strip():
                error = '密码和确认密码不一致'
            else:
                addUpdateDel('insert into user (username, password, zh_name, email, create_date) values (%s, %s, %s, %s, %s)',
                         [request.form['username'], encrypt(request.form['password_o']), request.form['fullname'], request.form['email'], time.strftime('%Y-%m-%d %X', time.localtime(time.time()))])
                flash('注册成功...')
    except Exception as e:
        error = str(err)
    finally:
        return render_template('admin/register.html', username=session['username'],nav=nav, sub_nav_ui = sub_nav_ui, sub_nav_api = sub_nav_api, set_nav=set_nav, operation=operation, error=error, pagename = '注册')

# 密码修改
@app.route('/modify_passwd', methods=['GET', 'POST'])
def modify_passwd():
    if not session.get('logged_in'):
        abort(401)
    error = None
    if request.method == 'POST':
        cur = selectone('select password from user where username = %s',(session['username']))
        pw = cur[0][0]
        if request.form['pw_old'].strip() == '' or request.form['pw_new_o'].strip() == '' or request.form['pw_new_t'].strip() == '':
            error = '请输入密码'
        elif request.form['pw_old'].strip() != decrypt(pw):
            error = '当前密码不正确'
        elif request.form['pw_new_o'].strip() != request.form['pw_new_t'].strip():
            error = '新密码和确认密码不一致'
        else:
            addUpdateDel('update user set password = %s where username = %s',(encrypt(request.form['pw_new_o'].strip()),session['username'],))
            flash('密码修改成功...')
    return render_template('modify_passwd.html',SITEURL=SITEURL, username=session['username'],  nav=nav, sub_nav_ui = sub_nav_ui, sub_nav_api = sub_nav_api, set_nav=set_nav, operation=operation, pagename = '修改密码', error=error)

# 404页面
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

# 退出页面
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('你已经退出...')
    return redirect(url_for('login'))

if __name__ == '__main__':
    #app.run()
    app.run(host='192.168.213.110',port=8000)