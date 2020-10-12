# coding=utf-8

import os
import math
import pymysql
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
import time
from contextlib import closing

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
@app.route('/uicases/<int:num>', methods=['GET', 'POST'])
def uicases(num):
    if not session.get('logged_in'):
        abort(401)
    else:
        all_Count = selectall('SELECT count(1) FROM uicases where activity = "1"')[0][0]
        all_Page = math.ceil(all_Count/page_Count)
        cur = selectone('SELECT a.id,a.type,a.version, a.model, a.product, a.name,a.pre_steps, a.steps, a.next_steps,a.description, b.zh_name, a.create_date FROM uicases a inner join user b on a.username=b.username where activity="1" LIMIT %s,%s',[(num-1)*page_Count,page_Count])
        cases = [dict(id=row[0], type=row[1], version=row[2], model=row[3], product=row[4], name=row[5], pre_steps=row[6], steps=row[7], next_steps=row[8], description=row[9], zh_name=row[10], create_date=row[11]) for row in cur]
        return render_template('ui/uicases.html', SITEURL=SITEURL, username=session['username'], cases=cases, nav=nav, sub_nav_ui = sub_nav_ui, sub_nav_api = sub_nav_api, set_nav=set_nav, operation=operation, all_Page=all_Page, pagename = '测试用例')
'''
# UI CASE EDIT
@app.route('/uicase_edit/<int:id>', methods=['GET', 'POST'])
def uicase_edit(id):
    error = None
    if not session.get('logged_in'):
        abort(401)
    else:
        cur = selectall('SELECT keyword FROM uiset')
        list_steps = [dict(keyword=row[0]) for row in cur]

        cur = selectone('SELECT version, model, product, name, steps, description, username, create_date FROM uicases where id=%s',[id])
        cases = [dict(version=row[0], model=row[1], product=row[2], name=row[3], steps=row[4], description=row[5], username=row[6], create_date=row[7]) for row in cur]
        if request.method == 'POST':
            if request.form['steps'].strip == '':
                error = '必输项不能为空'
            else:
                addUpdateDel('update uicases set steps=%s, description=%s where id=%s',[request.form['steps'], request.form['description'],id])
                flash('编辑成功...')
                return redirect(url_for('uicases',num=1))
        return render_template('ui/uicase_edit.html',SITEURL=SITEURL, username=session['username'],list_steps=list_steps, case=cases[0], nav=nav, sub_nav_ui = sub_nav_ui, sub_nav_api = sub_nav_api, set_nav=set_nav, operation=operation, pagename = '测试用例编辑',error=error,id=id)
'''
# UI CASE QUERY
@app.route('/uicase_query/<int:id>', methods=['GET', 'POST'])
def uicase_query(id):
    if not session.get('logged_in'):
        abort(401)
    else:
        cur = selectone('SELECT type,version, model, product, name,pre_steps, steps, description,next_steps, username, create_date FROM uicases where id=%s',[id])
        cases = [dict(type=row[0], version=row[1], model=row[2], product=row[3], name=row[4], pre_steps=row[5], steps=row[6], description=row[7], next_steps=row[8], username=row[9], create_date=row[10]) for row in cur]
        return render_template('ui/uicase_query.html', SITEURL=SITEURL, username=session['username'], case=cases[0], nav=nav, sub_nav_ui = sub_nav_ui, sub_nav_api = sub_nav_api, set_nav=set_nav, operation=operation, pagename = '测试用例查看')

# UI CASE DELETE
@app.route('/uicase_delete/<int:id>', methods=['GET', 'POST'])
def uicase_delete(id):
    if not session.get('logged_in'):
        abort(401)
    else:
        uisitue = selectall('select steps from uisitues')
        uisitues = [dict(steps=row[0]) for row in uisitue]
        uisitues = [uisitue['steps'] for uisitue in uisitues]

        uicase = selectone('select name from uicases where id=%s',[id])
        uicases = [dict(name=row[0]) for row in uicase]
        uicase_name = uicases[0]['name']
        
        if uicase_name in uisitues:
            error = "该用例被测试集引用，不能删除~！"
        else:
            cur = addUpdateDel('delete from uicases where id=%s',[id])
            flash('删除成功...')
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
'''
# NEW UI CASE
@app.route('/new_uicase', methods=['GET', 'POST'])
def new_uicase():
    if not session.get('logged_in'):
        abort(401)
    error = None

    version = selectall('select version from versions')
    versions = [dict(version=row[0]) for row in version]
    versions = [version['version'] for version in versions]

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
        else:
            addUpdateDel('insert into uicases (version, model, product, name, steps, description, username, create_date) values (%s, %s, %s, %s, %s, %s, %s, %s)',
                         [request.form['version'], request.form['model'], request.form['product'], request.form['name'], request.form['steps'], request.form['description'], session['username'], time.strftime('%Y-%m-%d %X', time.localtime(time.time()))])
            flash('创建成功...')
            return redirect(url_for('uicases',num=1))
    return render_template('ui/new_uicase.html', list_steps=list_steps, SITEURL=SITEURL, username=session['username'], versions=versions, nav=nav, sub_nav_ui = sub_nav_ui, sub_nav_api = sub_nav_api, set_nav=set_nav, pagename = '新增测试用例', product=product, model_oma=model_oma, error=error)
'''
# UI SITUES
@app.route('/uisitues/<int:num>', methods=['GET', 'POST'])
def uisitues(num):
    if not session.get('logged_in'):
        abort(401)
    else:
        all_Count = selectall('SELECT count(1) FROM uisitues')[0][0]
        all_Page = math.ceil(all_Count/page_Count)
        cur = selectone('SELECT a.id,a.name,a.steps,a.description,b.zh_name,a.create_date FROM uisitues a inner join user b on a.username=b.username LIMIT %s,%s',[(num-1)*page_Count,page_Count])
        uisitues = [dict(id=row[0], name=row[1], steps=row[2], description=row[3], username=row[4], create_date=row[5]) for row in cur]
        return render_template('ui/uisitues.html', SITEURL=SITEURL, username=session['username'], uisitues=uisitues, nav=nav, sub_nav_ui = sub_nav_ui, sub_nav_api = sub_nav_api, set_nav=set_nav, operation=operation, all_Page=all_Page, pagename = '测试集')

# UI SITUES EDIT
@app.route('/uisitue_edit/<int:id>', methods=['GET', 'POST'])
def uisitue_edit(id):
    if not session.get('logged_in'):
        abort(401)
    else:
        cur = selectall('SELECT name FROM uicases where activity="1"')
        uisitues = [dict(name=row[0]) for row in cur]

        cur = selectone('SELECT name, steps, description FROM uisitues where id=%s',[id])
        cases = [dict(name=row[0], steps=row[1], description=row[2]) for row in cur]
        if request.method == 'POST':
            if request.form['steps'].strip == '':
                error = '必输项不能为空'
            else:
                addUpdateDel('update uisitues set steps=%s, description=%s where id=%s',[request.form['steps'], request.form['description'],id])
                flash('编辑成功...')
                return redirect(url_for('uisitues',num=1))
        return render_template('ui/uisitue_edit.html',SITEURL=SITEURL, username=session['username'], uisitues=uisitues, case=cases[0], nav=nav, sub_nav_ui = sub_nav_ui, sub_nav_api = sub_nav_api, set_nav=set_nav, operation=operation, pagename = '测试集编辑',id=id)

# UI SITUES QUERY
@app.route('/uisitue_query/<int:id>', methods=['GET', 'POST'])
def uisitue_query(id):
    if not session.get('logged_in'):
        abort(401)
    else:
        cur = selectone('SELECT name, steps, description FROM uisitues where id=%s',[id])
        cases = [dict(name=row[0], steps=row[1], description=row[2]) for row in cur]
        return render_template('ui/uisitue_query.html',SITEURL=SITEURL, username=session['username'],  case=cases[0], nav=nav, sub_nav_ui = sub_nav_ui, sub_nav_api = sub_nav_api, set_nav=set_nav, operation=operation, pagename = '测试集查看')

# UI SITUES DELETE
@app.route('/uisitue_delete/<int:id>', methods=['GET', 'POST'])
def uisitue_delete(id):
    if not session.get('logged_in'):
        abort(401)
    else:
        cur = addUpdateDel('delete from uisitues where id=%s',[id])
        flash('删除成功...')
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
    cur = selectall('SELECT name FROM uicases where activity="1"')
    uisitues = [dict(name=row[0]) for row in cur]
    if request.method == 'POST':
        uiname = selectall('select name from uisitues')
        uinames = [dict(name=row[0]) for row in uiname]
        uinames = [uiname['name'] for uiname in uinames]

        if request.form['name'].strip() == '' or request.form['steps'].strip() == '':
            error = '必输项不能为空'
        elif request.form['name'].strip() in uinames:
            error = "该用例集已经存在"
        else:
            addUpdateDel('insert into uisitues (name, steps, description, username, create_date) values (%s, %s, %s, %s, %s)',
                         [request.form['name'], request.form['steps'], request.form['description'], session['username'], time.strftime('%Y-%m-%d %X', time.localtime(time.time()))])
            flash('创建成功...')
            return redirect(url_for('uisitues',num=1))
    return render_template('ui/new_uisitue.html',SITEURL=SITEURL, username=session['username'], uisitues=uisitues, nav=nav, sub_nav_ui = sub_nav_ui, sub_nav_api = sub_nav_api, set_nav=set_nav, pagename = '新增测试集',error=error)

# UI SIUTE REPORT
@app.route('/ui_report_list/1', methods=['GET', 'POST'])
def ui_report_list():
    if not session.get('logged_in'):
        abort(401)
    else:
        for root,dirs,files in os.walk(path_ui):
            report_lists = files[::-1][0:18]
        return render_template('report_list.html',SITEURL=SITEURL, username=session['username'], nav=nav, sub_nav_ui = sub_nav_ui, sub_nav_api = sub_nav_api, set_nav=set_nav, pagename = '测试报告列表',report_lists=report_lists,path = path_ui)


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
        cur = selectone('SELECT a.id,a.name,a.steps,a.description,b.zh_name,a.create_date FROM apisitues a inner join user b on a.username=b.username LIMIT %s,%s',[(num-1)*page_Count,page_Count])
        apisitues = [dict(id=row[0], name=row[1], steps=row[2], description=row[3], username=row[4], create_date=row[5]) for row in cur]
        return render_template('api/apisitues.html', SITEURL=SITEURL, username=session['username'], apisitues=apisitues, nav=nav, sub_nav_ui = sub_nav_ui, sub_nav_api = sub_nav_api, set_nav=set_nav, operation=operation, all_Page=all_Page, pagename = '测试集')

# API SITUES EDIT
@app.route('/apisitue_edit/<int:id>', methods=['GET', 'POST'])
def apisitue_edit(id):
    if not session.get('logged_in'):
        abort(401)
    else:
        cur = selectall('SELECT name FROM apicases where activity="1"')
        apisitues = [dict(name=row[0]) for row in cur]
        cur = selectone('SELECT name, steps, description FROM apisitues where id=%s',[id])
        cases = [dict(name=row[0], steps=row[1], description=row[2]) for row in cur]
        if request.method == 'POST':
            if request.form['steps'].strip == '':
                error = '必输项不能为空'
            else:
                addUpdateDel('update apisitues set steps=%s, description=%s where id=%s',[request.form['steps'], request.form['description'],id])
                flash('编辑成功...')
                return redirect(url_for('apisitues',num=1))
        return render_template('api/apisitue_edit.html',SITEURL=SITEURL, username=session['username'], case=cases[0], nav=nav, sub_nav_ui = sub_nav_ui, sub_nav_api = sub_nav_api, set_nav=set_nav, operation=operation, pagename = '测试集编辑',id=id,apisitues=apisitues)

# API SITUES QUERY
@app.route('/apisitue_query/<int:id>', methods=['GET', 'POST'])
def apisitue_query(id):
    if not session.get('logged_in'):
        abort(401)
    else:
        cur = selectone('SELECT name, steps, description FROM apisitues where id=%s',[id])
        cases = [dict(name=row[0], steps=row[1], description=row[2]) for row in cur]
        return render_template('api/apisitue_query.html',SITEURL=SITEURL, username=session['username'], case=cases[0], nav=nav, sub_nav_ui = sub_nav_ui, sub_nav_api = sub_nav_api, set_nav=set_nav, operation=operation, pagename = '测试集查看')

# API SITUES DELETE
@app.route('/apisitue_delete/<int:id>', methods=['GET', 'POST'])
def apisitue_delete(id):
    if not session.get('logged_in'):
        abort(401)
    else:
        cur = addUpdateDel('delete from apisitues where id=%s',[id])
        flash('删除成功...')
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
    cur = selectall('SELECT name FROM apicases where activity="1"')
    apisitues = [dict(name=row[0]) for row in cur]
    if request.method == 'POST':
        apiname = selectall('select name from apisitues')
        apinames = [dict(name=row[0]) for row in apiname]
        apinames = [apiname['name'] for apiname in apinames]

        if request.form['name'].strip() == '' or request.form['steps'].strip() == '':
            error = '必输项不能为空'
        elif request.form['name'].strip() in apinames:
            error = "该用例集已经存在"
        else:
            addUpdateDel('insert into apisitues (name, steps, description, username, create_date) values (%s, %s, %s, %s, %s)',
                         [request.form['name'], request.form['steps'], request.form['description'], session['username'], time.strftime('%Y-%m-%d %X', time.localtime(time.time()))])
            flash('创建成功...')
            return redirect(url_for('apisitues',num=1))
    return render_template('api/new_apisitue.html',SITEURL=SITEURL, username=session['username'], nav=nav, sub_nav_ui = sub_nav_ui, sub_nav_api = sub_nav_api, set_nav=set_nav, pagename = '新增测试集',error=error,apisitues=apisitues)

# API SIUTE REPORT
@app.route('/api_report_list/1', methods=['GET', 'POST'])
def api_report_list():
    if not session.get('logged_in'):
        abort(401)
    else:
        for root,dirs,files in os.walk(path_api):
            report_lists = files[::-1][0:18]
        return render_template('report_list.html',SITEURL=SITEURL, username=session['username'], nav=nav, sub_nav_ui = sub_nav_ui, sub_nav_api = sub_nav_api, set_nav=set_nav, pagename = '测试报告列表',report_lists=report_lists,path = path_api)

# API CASE
@app.route('/apicases/<int:num>', methods=['GET', 'POST'])
def apicases(num):
    if not session.get('logged_in'):
        abort(401)
    else:
        all_Count = selectall('SELECT count(1) FROM apicases where activity="1"')[0][0]
        all_Page = math.ceil(all_Count/page_Count)
        cur = selectone('SELECT a.id,a.version,a.product,a.model,a.name,a.description,b.zh_name,a.create_date, steps FROM apicases a inner join user b on a.username=b.username where activity="1" LIMIT %s,%s',[(num-1)*page_Count,page_Count])
        apicases = [dict(id=row[0], version=row[1], product=row[2], model=row[3], name=row[4], description=row[5], username=row[6], create_date=row[7], steps=row[8]) for row in cur]
        return render_template('api/apicases.html',SITEURL=SITEURL, username=session['username'], apicases=apicases, nav=nav, sub_nav_ui = sub_nav_ui, sub_nav_api = sub_nav_api, set_nav=set_nav, operation=operation, all_Page=all_Page, pagename = '接口测试用例')
'''
# API CASE EDIT
@app.route('/apicase_edit/<int:id>', methods=['GET', 'POST'])
def apicase_edit(id):
    if not session.get('logged_in'):
        abort(401)
    else:
        error = None
        cur = selectall('SELECT name,request FROM apiset')
        apisets = [dict(name=row[0],request=row[1]) for row in cur]
        cur = selectone('SELECT version, name, product, model, steps, description FROM apicases where id=%s',[id])
        cases = [dict(version=row[0], name=row[1], product=row[2], model=row[3], steps=row[4], description=row[5]) for row in cur]
    return render_template('api/apicase_edit.html',SITEURL=SITEURL, username=session['username'], case=cases[0], nav=nav, sub_nav_ui = sub_nav_ui, sub_nav_api = sub_nav_api, set_nav=set_nav, operation=operation, pagename = '接口编辑', id=id)
'''
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
            cur = selectone('select name,path,method,request,checks,parameter from apidates where case_name=%s and name=%s',[case_name,steps[i]+'_'+str(i)])
            case_detail = [dict(name=row[0], path=row[1], method=row[2], request=row[3], checks=row[4], parameter=row[5]) for row in cur]
            case_details.append(case_detail[0])
        return render_template('api/apicase_query.html',SITEURL=SITEURL, username=session['username'], case_details=case_details, case=cases[0], nav=nav, sub_nav_ui = sub_nav_ui, sub_nav_api = sub_nav_api, set_nav=set_nav, operation=operation, pagename = '接口查看')

# API CASE DELETE
@app.route('/apicase_delete/<int:id>', methods=['GET', 'POST'])
def apicase_delete(id):
    if not session.get('logged_in'):
        abort(401)
    else:
        apisitue = selectall('select steps from apisitues')
        apisitues = [dict(steps=row[0]) for row in apisitue]
        apisitues = [apisitue['steps'] for apisitue in apisitues]

        apicase = selectone('select name from apicases where id=%s',[id])
        apicases = [dict(name=row[0]) for row in apicase]
        apicase_name = apicases[0]['name']
        
        if apicase_name in apisitues:
            error = "该用例被测试集引用，不能删除~！"
        else:
            addUpdateDel('delete from apicases where id=%s',[id])
            addUpdateDel('delete from apidates where case_name=%s',[apicase_name])
            flash('删除成功...')
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

        return render_template('api/apicase_exec.html',SITEURL=SITEURL, username=session['username'], res=res,nav=nav, sub_nav_ui = sub_nav_ui, sub_nav_api = sub_nav_api, set_nav=set_nav, operation=operation, pagename = '接口执行结果')
'''
# NEW API CASE
@app.route('/new_apicase', methods=['GET', 'POST'])
def new_apicase():
    if not session.get('logged_in'):
        abort(401)
    cur = selectall('SELECT name,request FROM apiset')
    apisets = [dict(name=row[0],request=row[1]) for row in cur]
    error = None

    version = selectall('select version from versions')
    versions = [dict(version=row[0]) for row in version]
    versions = [version['version'] for version in versions]

    if request.method == 'POST':
        apiname = selectall('select name from apicases')
        apinames = [dict(name=row[0]) for row in apiname]
        apinames = [apiname['name'] for apiname in apinames]

        if request.form['version'].strip() == '' or request.form['product'].strip() == '' or request.form['model'].strip() == '' or request.form['name'].strip() == '':
            error = '必输项不能为空'
        elif request.form['name'].strip() in apinames:
            error = "该用例已经存在"
        else:
            addUpdateDel('insert into apicases (version, model, product, name, steps, description, username, create_date) values (%s, %s, %s, %s, %s, %s, %s, %s)',
                         [request.form['version'], request.form['model'], request.form['product'], request.form['name'], request.form['steps'], request.form['description'], session['username'], time.strftime('%Y-%m-%d %X', time.localtime(time.time()))])
            steps = request.form['steps'].split('\r\n')
            for i in range(len(steps)):
                    cur = selectone('select name,path,method,request,checks from apiset where name = %s',[steps[i]])
                    cases = [dict(name=row[0], path=row[1], method=row[2], request=row[3], checks=row[4]) for row in cur]
                    addUpdateDel('insert into apidates (case_name,name,path,method,request,checks,username,create_date) values (%s,%s,%s,%s,%s,%s,%s,%s)',[request.form['name'], steps[i]+'_'+str(i), cases[0]['path'], cases[0]['method'], cases[0]['request'], cases[0]['checks'], session['username'], time.strftime('%Y-%m-%d %X', time.localtime(time.time()))])
            flash('创建成功...')
            return redirect(url_for('apidate_edit_cases_query',case_name=request.form["name"]))
    return render_template('api/new_apicase.html', SITEURL=SITEURL, username=session['username'], apisets=apisets, model_sicap=model_sicap, versions=versions, nav=nav, sub_nav_ui = sub_nav_ui, sub_nav_api = sub_nav_api, set_nav=set_nav, pagename = '新增用例',error=error)

@app.route('/apidate_edit_cases_query/<case_name>', methods=['GET', 'POST'])
def apidate_edit_cases_query(case_name):
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
            return render_template('api/apidate_edit_cases.html',SITEURL=SITEURL, username=session['username'], case=cases[0], names=names, case_name=case_name, nav=nav, sub_nav_ui = sub_nav_ui, sub_nav_api = sub_nav_api, set_nav=set_nav, pagename = '编辑接口数据')
    return render_template('api/apidate_edit_cases.html',SITEURL=SITEURL, username=session['username'], names=names, case_name=case_name, nav=nav, sub_nav_ui = sub_nav_ui, sub_nav_api = sub_nav_api, set_nav=set_nav, pagename = '编辑接口数据')

@app.route('/apidate_edit_cases_save/<case_name>', methods=['GET', 'POST'])
def apidate_edit_cases_save(case_name):
    if not session.get('logged_in'):
        abort(401)
    if request.method == 'POST':
        if request.form['request'].strip() == '' or request.form['checks'].strip() == '' or request.form['parameter'].strip() == '':
            error = '必输项不能为空'
        else:
            addUpdateDel('update apidates set request=%s, checks=%s, parameter=%s where case_name=%s and name=%s',[request.form['request'],request.form['checks'],request.form['parameter'],case_name,request.form['name']])
            flash('更新成功...')
    return render_template('api/apidate_edit_cases.html',SITEURL=SITEURL, username=session['username'], case_name=case_name, nav=nav, sub_nav_ui = sub_nav_ui, sub_nav_api = sub_nav_api, set_nav=set_nav, pagename = '编辑接口数据')
'''
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
        cur = selectone('SELECT a.id,a.keyword,a.description,a.template,a.example,b.zh_name,a.create_date FROM uiset a inner join user b on a.username=b.username LIMIT %s,%s',[(num-1)*page_Count,page_Count])
        uisets = [dict(id=row[0], keyword=row[1], description=row[2], template=row[3], example=row[4], username=row[5], create_date=row[6]) for row in cur]
        return render_template('set/uiset.html',SITEURL=SITEURL, username=session['username'],  uisets=uisets, caseManage_nav=caseManage_nav, caseManage_sub_nav_ui = caseManage_sub_nav_ui, caseManage_sub_nav_api = caseManage_sub_nav_api, caseManage_set_nav=caseManage_set_nav, operation=operation, all_Page=all_Page, pagename = 'UI步骤说明')

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
                flash('编辑成功...')
                return redirect(url_for('uiset',num=1))
        return render_template('set/uiset_edit.html', SITEURL=SITEURL, username=session['username'], case=cases[0], caseManage_nav=caseManage_nav, caseManage_sub_nav_ui = caseManage_sub_nav_ui, caseManage_sub_nav_api = caseManage_sub_nav_api, caseManage_set_nav=caseManage_set_nav, operation=operation, pagename = 'UI步骤说明编辑',id=id)

# UI SET QUERY
@app.route('/caseManage/uiset_query/<int:id>', methods=['GET', 'POST'])
def uiset_query(id):
    if not session.get('logged_in'):
        abort(401)
    else:
        cur = selectone('SELECT id,keyword,description,template,example FROM uiset where id=%s',[id])
        cases = [dict(id=row[0], keyword=row[1], description=row[2], template=row[3], example=row[4]) for row in cur]
        return render_template('set/uiset_query.html', SITEURL=SITEURL, username=session['username'], case=cases[0], caseManage_nav=caseManage_nav, caseManage_sub_nav_ui = caseManage_sub_nav_ui, caseManage_sub_nav_api = caseManage_sub_nav_api, caseManage_set_nav=caseManage_set_nav, operation=operation, pagename = 'UI步骤说明查看')

# UI SET DELETE
@app.route('/caseManage/uiset_delete/<int:id>', methods=['GET', 'POST'])
def uiset_delete(id):
    if not session.get('logged_in'):
        abort(401)
    else:
        addUpdateDel('delete from uiset where id=%s',[id])
        flash('删除成功...')
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
                         [request.form['keyword'], request.form['description'], request.form['template'], request.form['example'], session['username'], time.strftime('%Y-%m-%d %X', time.localtime(time.time()))])
            flash('创建成功...')
            return redirect(url_for('uiset',num=1))
    return render_template('set/new_uiset.html', SITEURL=SITEURL, username=session['username'], caseManage_nav=caseManage_nav, caseManage_sub_nav_ui = caseManage_sub_nav_ui, caseManage_sub_nav_api = caseManage_sub_nav_api, caseManage_set_nav=caseManage_set_nav, pagename = '新建UI步骤说明',error=error)

# API SET
@app.route('/caseManage/apiset/<int:num>', methods=['GET', 'POST'])
def apiset(num):
    if not session.get('logged_in'):
        abort(401)
    else:
        all_Count = selectall('SELECT count(1) FROM apiset')[0][0]
        all_Page = math.ceil(all_Count/page_Count)
        cur = selectone('SELECT a.id,a.name,a.path,a.method,a.request,a.checks,a.description,b.zh_name,a.create_date FROM apiset a inner join user b on a.username=b.username LIMIT %s,%s',[(num-1)*page_Count,page_Count])
        apisets = [dict(id=row[0], name=row[1], path=row[2], method=row[3], request=row[4], checks=row[5], description=row[6], username=row[7], create_date=row[8]) for row in cur]
        return render_template('set/apiset.html',SITEURL=SITEURL, username=session['username'], apisets=apisets, caseManage_nav=caseManage_nav, caseManage_sub_nav_ui = caseManage_sub_nav_ui, caseManage_sub_nav_api = caseManage_sub_nav_api, caseManage_set_nav=caseManage_set_nav, operation=operation, all_Page=all_Page, pagename = '全部接口')

# API SET EDIT
@app.route('/caseManage/apiset_edit/<int:id>', methods=['GET', 'POST'])
def apiset_edit(id):
    if not session.get('logged_in'):
        abort(401)
    else:
        cur = selectone('SELECT id,name,path,method,request,checks,description FROM apiset where id=%s',[id])
        cases = [dict(id=row[0], name=row[1], path=row[2], method=row[3], request=row[4], checks=row[5], description=row[6]) for row in cur]
        if request.method == 'POST':
            if request.form['path'].strip == '' or request.form['request'].strip == '':
                error = '必输项不能为空'
            else:
                addUpdateDel('update apiset set path=%s, request=%s, checks=%s, description=%s where id=%s',[request.form['path'], request.form['request'], request.form['checks'], request.form['description'],id])
                flash('编辑成功...')
                return redirect(url_for('apiset',num=1))
        return render_template('set/apiset_edit.html',SITEURL=SITEURL, username=session['username'], case=cases[0], caseManage_nav=caseManage_nav, caseManage_sub_nav_ui = caseManage_sub_nav_ui, caseManage_sub_nav_api = caseManage_sub_nav_api, caseManage_set_nav=caseManage_set_nav, operation=operation, pagename = '接口编辑', id=id)

# API SET QUERY
@app.route('/caseManage/apiset_query/<int:id>', methods=['GET', 'POST'])
def apiset_query(id):
    if not session.get('logged_in'):
        abort(401)
    else:
        cur = selectone('SELECT id,name,path,method,request,checks,description FROM apiset where id=%s',[id])
        cases = [dict(id=row[0], name=row[1], path=row[2], method=row[3], request=row[4], checks=row[5], description=row[6]) for row in cur]
        return render_template('set/apiset_query.html',SITEURL=SITEURL, username=session['username'],  case=cases[0], caseManage_nav=caseManage_nav, caseManage_sub_nav_ui = caseManage_sub_nav_ui, caseManage_sub_nav_api = caseManage_sub_nav_api, caseManage_set_nav=caseManage_set_nav, operation=operation, pagename = '接口查看')

# API SET DELETE
@app.route('/caseManage/apiset_delete/<int:id>', methods=['GET', 'POST'])
def apiset_delete(id):
    if not session.get('logged_in'):
        abort(401)
    else:
        addUpdateDel('delete from apiset where id=%s',[id])
        flash('删除成功...')
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
        return render_template('set/apiset_exec.html',SITEURL=SITEURL, username=session['username'], res=res,caseManage_nav=caseManage_nav, caseManage_sub_nav_ui = caseManage_sub_nav_ui, caseManage_sub_nav_api = caseManage_sub_nav_api, caseManage_set_nav=caseManage_set_nav, operation=operation, pagename = '接口执行结果')

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
        else:
            addUpdateDel('insert into apiset (name, description, path, method, request, checks, username, create_date) values (%s, %s, %s, %s, %s, %s, %s, %s)',
                         [request.form['name'], request.form['description'], request.form['path'], request.form['method'], request.form['request'], request.form['checks'], session['username'], time.strftime('%Y-%m-%d %X', time.localtime(time.time()))])
            flash('创建成功...')
            return redirect(url_for('apiset',num=1))
    return render_template('set/new_apiset.html',SITEURL=SITEURL, username=session['username'], caseManage_nav=caseManage_nav, caseManage_sub_nav_ui = caseManage_sub_nav_ui, caseManage_sub_nav_api = caseManage_sub_nav_api, caseManage_set_nav=caseManage_set_nav, pagename = '新增接口', product=product, model_sicap=model_sicap, error=error, methods=http_methods)

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
        flash('删除成功...')
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
            flash('创建成功...')
            return redirect(url_for('versions',num=1))
    return render_template('version/new_version.html',  SITEURL=SITEURL, username=session['username'], caseManage_nav=caseManage_nav, caseManage_sub_nav_ui = caseManage_sub_nav_ui, caseManage_sub_nav_api = caseManage_sub_nav_api, caseManage_set_nav=caseManage_set_nav, pagename = '新增版本号', product=product, model_oma=model_oma, error=error)

# VERSION
@app.route('/caseManage/versions/<int:num>', methods=['GET', 'POST'])
def versions(num):
    if not session.get('logged_in'):
        abort(401)
    else:
        all_Count = selectall('SELECT count(1) FROM versions')[0][0]
        all_Page = math.ceil(all_Count/page_Count)
        cur = selectone('SELECT a.id,a.version,b.zh_name,a.create_date FROM versions a inner join user b on a.username=b.username LIMIT %s,%s',[(num-1)*page_Count,page_Count])
        versions = [dict(id=row[0], version=row[1], username=row[2], create_date=row[3]) for row in cur]
        return render_template('version/versions.html', SITEURL=SITEURL, username=session['username'], versions=versions, caseManage_nav=caseManage_nav, caseManage_sub_nav_ui = caseManage_sub_nav_ui, caseManage_sub_nav_api = caseManage_sub_nav_api, caseManage_set_nav=caseManage_set_nav, operation=operation, all_Page=all_Page, pagename = '版本号')

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
        return render_template('caseManage/index.html', username=session['username'],caseManage_nav=caseManage_nav, caseManage_sub_nav_ui = caseManage_sub_nav_ui, caseManage_sub_nav_api = caseManage_sub_nav_api, caseManage_set_nav=caseManage_set_nav,pagename = '主页')
    else:
        return redirect(url_for('caseManage_login'))

# caseManage UI CASES
@app.route('/caseManage/uicases/<int:num>', methods=['GET', 'POST'])
def caseManage_uicases(num):
    if not session.get('logged_in'):
        abort(401)
    else:
        all_Count = selectall('SELECT count(1) FROM uicases where activity="0"')[0][0]
        all_Page = math.ceil(all_Count/page_Count)
        cur = selectone('SELECT a.id,a.type,a.version, a.model, a.product, a.name,a.pre_steps, a.steps, a.next_steps,a.description, b.zh_name, a.create_date FROM uicases a inner join user b on a.username=b.username where activity="0" LIMIT %s,%s',[(num-1)*page_Count,page_Count])
        cases = [dict(id=row[0], type=row[1], version=row[2], model=row[3], product=row[4], name=row[5], pre_steps=row[6], steps=row[7], next_steps=row[8], description=row[9], zh_name=row[10], create_date=row[11]) for row in cur]
        return render_template('caseManage/uicases.html', SITEURL=SITEURL, username=session['username'], cases=cases, caseManage_nav=caseManage_nav, caseManage_sub_nav_ui = caseManage_sub_nav_ui, caseManage_sub_nav_api = caseManage_sub_nav_api, caseManage_set_nav=caseManage_set_nav, operation=operation, all_Page=all_Page, pagename = '测试用例')

# caseManage UI CASE EDIT
@app.route('/caseManage/uicase_edit/<int:id>', methods=['GET', 'POST'])
def caseManage_uicase_edit(id):
    error = None
    if not session.get('logged_in'):
        abort(401)
    else:
        issuetype = selectall('select name from uicases where type="公共用例"')
        issuetypes = [dict(name=row[0]) for row in issuetype]

        cur = selectall('SELECT keyword FROM uiset')
        list_steps = [dict(keyword=row[0]) for row in cur]

        cur = selectone('SELECT type,version, model, product, name,pre_steps, steps, description,next_steps, username, create_date FROM uicases where id=%s',[id])
        cases = [dict(type=row[0], version=row[1], model=row[2], product=row[3], name=row[4], pre_steps=row[5], steps=row[6], description=row[7], next_steps=row[8], username=row[9], create_date=row[10]) for row in cur]
        if request.method == 'POST':
            if request.form['steps'].strip() == '':
                error = '必输项不能为空'
            elif request.form['type'].strip() == '公共用例':
                addUpdateDel('update uicases set steps=%s, description=%s where id=%s',[request.form['steps'], request.form['description'],id])
                flash('编辑成功...')
                return redirect(url_for('caseManage_uicases',num=1))
            else:
                addUpdateDel('update uicases set pre_steps=%s, steps=%s, next_steps=%s, description=%s where id=%s',[request.form['pre-steps'], request.form['steps'], request.form['next-steps'],request.form['description'],id])
                flash('编辑成功...')
                return redirect(url_for('caseManage_uicases',num=1))
        return render_template('caseManage/uicase_edit.html',SITEURL=SITEURL, username=session['username'],list_steps=list_steps, case=cases[0], caseManage_nav=caseManage_nav, caseManage_sub_nav_ui = caseManage_sub_nav_ui, caseManage_sub_nav_api = caseManage_sub_nav_api, caseManage_set_nav=caseManage_set_nav, operation=operation,issuetypes=issuetypes, pagename = '测试用例编辑',error=error,id=id)

# caseManage UI CASE QUERY
@app.route('/caseManage/uicase_query/<int:id>', methods=['GET', 'POST'])
def caseManage_uicase_query(id):
    if not session.get('logged_in'):
        abort(401)
    else:
        cur = selectone('SELECT type,version, model, product, name,pre_steps, steps, description,next_steps, username, create_date FROM uicases where id=%s',[id])
        cases = [dict(type=row[0], version=row[1], model=row[2], product=row[3], name=row[4], pre_steps=row[5], steps=row[6], description=row[7], next_steps=row[8], username=row[9], create_date=row[10]) for row in cur]
        return render_template('caseManage/uicase_query.html', SITEURL=SITEURL, username=session['username'], case=cases[0], caseManage_nav=caseManage_nav, caseManage_sub_nav_ui = caseManage_sub_nav_ui, caseManage_sub_nav_api = caseManage_sub_nav_api, caseManage_set_nav=caseManage_set_nav, operation=operation, pagename = '测试用例查看')

# caseManage UI CASE DELETE
@app.route('/caseManage/uicase_delete/<int:id>', methods=['GET', 'POST'])
def caseManage_uicase_delete(id):
    if not session.get('logged_in'):
        abort(401)
    else:
        uisitue = selectall('select steps from uisitues')
        uisitues = [dict(steps=row[0]) for row in uisitue]
        uisitues = [uisitue['steps'] for uisitue in uisitues]

        uicase = selectone('select name from uicases where id=%s',[id])
        uicases = [dict(name=row[0]) for row in uicase]
        uicase_name = uicases[0]['name']
        
        if uicase_name in uisitues:
            error = "该用例被测试集引用，不能删除~！"
        else:
            cur = addUpdateDel('delete from uicases where id=%s',[id])
            flash('删除成功...')
        return redirect(url_for('caseManage_uicases',num=1))

# caseManage UI CASE EXEC
@app.route('/caseManage/uicase_exec/<int:id>', methods=['GET', 'POST'])
def caseManage_uicase_exec(id):
    if not session.get('logged_in'):
        abort(401)
    else:
        error = None
        newrun = RunUiTests(id,session['username'])
        res = newrun.getTestCases()
        return render_template('caseManage/uicase_exec.html',res=res,SITEURL=SITEURL, username=session['username'], caseManage_nav=caseManage_nav, caseManage_sub_nav_ui = caseManage_sub_nav_ui, caseManage_sub_nav_api = caseManage_sub_nav_api, caseManage_set_nav=caseManage_set_nav, operation=operation, pagename = '用例执行结果')

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
        else:
            addUpdateDel('insert into uicases (type,version, model, product, name, pre_steps,steps,next_steps, description,activity, username, create_date) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                         [request.form['type'],request.form['version'], request.form['model'], request.form['product'], request.form['name'],request.form['pre-steps'], request.form['steps'],request.form['next-steps'], request.form['description'], '0', session['username'], time.strftime('%Y-%m-%d %X', time.localtime(time.time()))])
            flash('创建成功...')
            return redirect(url_for('caseManage_uicases',num=1))
    return render_template('caseManage/new_uicase.html', list_steps=list_steps, SITEURL=SITEURL, username=session['username'], versions=versions, caseManage_nav=caseManage_nav, caseManage_sub_nav_ui = caseManage_sub_nav_ui, caseManage_sub_nav_api = caseManage_sub_nav_api, caseManage_set_nav=caseManage_set_nav, pagename = '新增测试用例', product=product, model_oma=model_oma, issuetypes=issuetypes, error=error)

# caseManage API CASE
@app.route('/caseManage/apicases/<int:num>', methods=['GET', 'POST'])
def caseManage_apicases(num):
    if not session.get('logged_in'):
        abort(401)
    else:
        all_Count = selectall('SELECT count(1) FROM apicases where activity="0"')[0][0]
        all_Page = math.ceil(all_Count/page_Count)
        cur = selectone('SELECT a.id,a.type,a.version,a.product,a.model,a.name,a.description,b.zh_name,a.create_date, a.steps,a.pre_steps,a.next_steps FROM apicases a inner join user b on a.username=b.username where activity="0" LIMIT %s,%s',[(num-1)*page_Count,page_Count])
        apicases = [dict(id=row[0], type=row[1],version=row[2], product=row[3], model=row[4], name=row[5], description=row[6], username=row[7], create_date=row[8], steps=row[9], pre_steps=row[10], next_steps=row[11]) for row in cur]
        return render_template('caseManage/apicases.html',SITEURL=SITEURL, username=session['username'], apicases=apicases, caseManage_nav=caseManage_nav, caseManage_sub_nav_ui = caseManage_sub_nav_ui, caseManage_sub_nav_api = caseManage_sub_nav_api, caseManage_set_nav=caseManage_set_nav, operation=operation, all_Page=all_Page, pagename = '接口测试用例')

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
        print(cases)
    return render_template('caseManage/apicase_edit.html',SITEURL=SITEURL, username=session['username'], case=cases[0], caseManage_nav=caseManage_nav, caseManage_sub_nav_ui = caseManage_sub_nav_ui, caseManage_sub_nav_api = caseManage_sub_nav_api, caseManage_set_nav=caseManage_set_nav, operation=operation, pagename = '接口编辑', id=id)

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
            cur = selectone('select name,path,method,request,checks,parameter from apidates where case_name=%s and name=%s',[case_name,steps[i]+'_'+str(i)])
            case_detail = [dict(name=row[0], path=row[1], method=row[2], request=row[3], checks=row[4], parameter=row[5]) for row in cur]
            case_details.append(case_detail[0])
        return render_template('caseManage/apicase_query.html',SITEURL=SITEURL, username=session['username'], case_details=case_details, case=cases[0], caseManage_nav=caseManage_nav, caseManage_sub_nav_ui = caseManage_sub_nav_ui, caseManage_sub_nav_api = caseManage_sub_nav_api, caseManage_set_nav=caseManage_set_nav, operation=operation, pagename = '接口查看')

# caseManage API CASE DELETE
@app.route('/caseManage/apicase_delete/<int:id>', methods=['GET', 'POST'])
def caseManage_apicase_delete(id):
    if not session.get('logged_in'):
        abort(401)
    else:
        apicase = selectone('select name from apicases where id=%s',[id])
        apicases = [dict(name=row[0]) for row in apicase]
        apicase_name = apicases[0]['name']
        
        addUpdateDel('delete from apicases where id=%s',[id])
        addUpdateDel('delete from apidates where case_name=%s',[apicase_name])
        flash('删除成功...')
        return redirect(url_for('caseManage_apicases',num=1))

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

    if request.method == 'POST':
        apiname = selectall('select name from apicases')
        apinames = [dict(name=row[0]) for row in apiname]
        apinames = [apiname['name'] for apiname in apinames]

        if request.form['version'].strip() == '' or request.form['product'].strip() == '' or request.form['model'].strip() == '' or request.form['name'].strip() == '':
            error = '必输项不能为空'
        elif request.form['name'].strip() in apinames:
            error = "该用例已经存在"
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
                    addUpdateDel('insert into apidates (case_name,name,path,method,request,checks,username,create_date) values (%s,%s,%s,%s,%s,%s,%s,%s)',[request.form['name'], str(i)+'_'+steps[i], cases[0]['path'], cases[0]['method'], cases[0]['request'], cases[0]['checks'], session['username'], time.strftime('%Y-%m-%d %X', time.localtime(time.time()))])
            flash('创建成功...')
            return redirect(url_for('caseManage_apidate_edit_cases_query',case_name=request.form["name"]))
    return render_template('caseManage/new_apicase.html', SITEURL=SITEURL, username=session['username'], apisets=apisets, model_sicap=model_sicap, versions=versions, caseManage_nav=caseManage_nav, caseManage_sub_nav_ui = caseManage_sub_nav_ui, caseManage_sub_nav_api = caseManage_sub_nav_api, caseManage_set_nav=caseManage_set_nav, product=product, issuetypes=issuetypes, pagename = '新增用例',error=error)

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
    if request.method == 'POST':
        if request.form['request'].strip() == '' or request.form['checks'].strip() == '' or request.form['parameter'].strip() == '':
            error = '必输项不能为空'
        else:
            addUpdateDel('update apidates set request=%s, checks=%s, parameter=%s where case_name=%s and name=%s',[request.form['request'],request.form['checks'],request.form['parameter'],case_name,request.form['name']])
            flash('更新成功...')
    return render_template('caseManage/apidate_edit_cases.html',SITEURL=SITEURL, username=session['username'], case_name=case_name, caseManage_nav=caseManage_nav, caseManage_sub_nav_ui = caseManage_sub_nav_ui, caseManage_sub_nav_api = caseManage_sub_nav_api, caseManage_set_nav=caseManage_set_nav, pagename = '编辑接口数据')

# 密码修改
@app.route('/caseManage/modify_passwd', methods=['GET', 'POST'])
def caseManage_modify_passwd():
    if not session.get('logged_in'):
        abort(401)
    error = None
    if request.method == 'POST':
        cur = selectone('select password from user where username = %s',(session['username'],))
        pw = cur.fetchone()[0]
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
@app.route('/review/uicases/<int:num>', methods=['GET', 'POST'])
def review_uicases(num):
    if not session.get('logged_in') or session['username'] not in review_user:
        abort(401)
    else:
        all_Count = selectall('SELECT count(1) FROM uicases where activity = "0"')[0][0]
        all_Page = math.ceil(all_Count/page_Count)
        cur = selectone('SELECT a.id,a.type,a.version, a.model, a.product, a.name,a.pre_steps, a.steps, a.next_steps,a.description, b.zh_name, a.create_date FROM uicases a inner join user b on a.username=b.username where activity="0" LIMIT %s,%s',[(num-1)*page_Count,page_Count])
        cases = [dict(id=row[0], type=row[1], version=row[2], model=row[3], product=row[4], name=row[5], pre_steps=row[6], steps=row[7], next_steps=row[8], description=row[9], zh_name=row[10], create_date=row[11]) for row in cur]
    return render_template('review/uireview.html', SITEURL=SITEURL, username=session['username'], cases=cases, review_nav=review_nav, review_sub_nav_ui = review_sub_nav_ui, review_sub_nav_api = review_sub_nav_api, review_operation=review_operation, all_Page=all_Page, pagename = '测试用例')

# REVIEW UI CASE QUERY
@app.route('/review/uicase_query/<int:id>', methods=['GET', 'POST'])
def review_uicase_query(id):
    if not session.get('logged_in'):
        abort(401)
    else:
        cur = selectone('SELECT type,version, model, product, name,pre_steps, steps, description,next_steps, username, create_date FROM uicases where id=%s',[id])
        cases = [dict(type=row[0], version=row[1], model=row[2], product=row[3], name=row[4], pre_steps=row[5], steps=row[6], description=row[7], next_steps=row[8], username=row[9], create_date=row[10]) for row in cur]
    return render_template('review/uicase_review.html', SITEURL=SITEURL, username=session['username'], case=cases[0], review_nav=review_nav, review_sub_nav_ui = review_sub_nav_ui, review_sub_nav_api = review_sub_nav_api, review_operation=review_operation, id=id, pagename = '用例审核')


# UI CASE REVIEW
@app.route('/review/uicase_review/<int:id>', methods=['GET', 'POST'])
def uicase_review(id):
    if not session.get('logged_in') or session['username'] not in review_user:
        abort(401)
    else:
        cur = addUpdateDel('update uicases set activity="1" where id=%s',[id])
        flash('审核成功...')
        return redirect(url_for('review_uicases',num=1))

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
@app.route('/review/apicases/<int:num>', methods=['GET', 'POST'])
def review_apicases(num):
    if not session.get('logged_in') or session['username'] not in review_user:
        abort(401)
    else:
        all_Count = selectall('SELECT count(1) FROM apicases where activity="0"')[0][0]
        all_Page = math.ceil(all_Count/page_Count)
        cur = selectone('SELECT a.id,a.version,a.product,a.model,a.name,a.description,b.zh_name,a.create_date, steps FROM apicases a inner join user b on a.username=b.username where activity="0" LIMIT %s,%s',[(num-1)*page_Count,page_Count])
        apicases = [dict(id=row[0], version=row[1], product=row[2], model=row[3], name=row[4], description=row[5], username=row[6], create_date=row[7], steps=row[8]) for row in cur]
        return render_template('review/apireview.html',SITEURL=SITEURL, username=session['username'], apicases=apicases, review_nav=review_nav, review_sub_nav_ui = review_sub_nav_ui, review_sub_nav_api = review_sub_nav_api, review_operation=review_operation, all_Page=all_Page, pagename = '用例审核')

# REVIEW API CASE QUERY
@app.route('/review/apicase_query/<int:id>', methods=['GET', 'POST'])
def review_apicase_query(id):
    if not session.get('logged_in') or session['username'] not in review_user:
        abort(401)
    else:
        cur = selectone('SELECT version, name, product, model, steps, description FROM apicases where id=%s',[id])
        cases = [dict(version=row[0], name=row[1], product=row[2], model=row[3], steps=row[4], description=row[5]) for row in cur]
        steps = cases[0]['steps'].split('\r\n')
        case_name = cases[0]['name']
        print(case_name)
        case_details = []
        for i in range(len(steps)):
            cur = selectone('select name,path,method,request,checks,parameter from apidates where case_name=%s and name=%s',[case_name,steps[i]+'_'+str(i)])
            case_detail = [dict(name=row[0], path=row[1], method=row[2], request=row[3], checks=row[4], parameter=row[5]) for row in cur]
            print(cur)
            case_details.append(case_detail[0])
        return render_template('review/apicase_review.html',SITEURL=SITEURL, username=session['username'], case_details=case_details, case=cases[0], review_nav=review_nav, review_sub_nav_ui = review_sub_nav_ui, review_sub_nav_api = review_sub_nav_api, review_operation=review_operation, id=id, pagename = '用例审核')

# API CASE REVIEW
@app.route('/review/apicase_review/<int:id>', methods=['GET', 'POST'])
def apicase_review(id):
    if not session.get('logged_in') or session['username'] not in review_user:
        abort(401)
    else:
        cur = addUpdateDel('update apicases set activity="1" where id=%s',[id])
        flash('审核成功...')
        return redirect(url_for('review_apicases',num=1))

# API CASE EXEC
@app.route('/review/apicase_exec/<int:id>', methods=['GET', 'POST'])
def review_apicase_exec(id):
    if not session.get('logged_in') or session['username'] not in review_user:
        abort(401)
    else:
        error = None
        newrun = RunTests(id,session['username'])
        res=newrun.getTestCases()

        return render_template('review/apicase_exec.html',SITEURL=SITEURL, username=session['username'], res=res, review_nav=review_nav, review_sub_nav_ui = review_sub_nav_ui, review_sub_nav_api = review_sub_nav_api, review_operation=review_operation, pagename = '接口执行结果')

# 密码修改
@app.route('/review/modify_passwd', methods=['GET', 'POST'])
def review_modify_passwd():
    if not session.get('logged_in'):
        abort(401)
    error = None
    if request.method == 'POST':
        cur = selectone('select password from user where username = %s',(session['username'],))
        pw = cur.fetchone()[0]
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
        cur = selectone('select password from user where username = %s',(session['username'],))
        pw = cur.fetchone()[0]
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
    app.run()
    #app.run(host='192.168.213.110',port=8000)