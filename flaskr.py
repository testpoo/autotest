# coding=utf-8

import os
import pymysql
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
import time
from contextlib import closing
from encrypt import *
from parm import *

from db_config import *
import requests
from api_test import RunTests
from ui_test import RunUiTests

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

def connect_db():
    return pymysql.connect("127.0.0.1","test","123456","autotest",charset = 'utf8')

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

#@app.before_request
#def before_request():
#    g.db = connect_db()

#@app.teardown_request
#def teardown_request(exception):
#    db = getattr(g, 'db', None)
#    if db is not None:
#        db.close()

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
        return render_template('index.html', nav=nav, sub_nav_ui = sub_nav_ui, sub_nav_api = sub_nav_api, set_nav=set_nav,pagename = '主页')
    else:
        return redirect(url_for('login'))

###############################
#             UI
###############################

# UI CASES
@app.route('/uicases', methods=['GET', 'POST'])
def uicases():
    if not session.get('logged_in'):
        abort(401)
    else:
        cur = selectall('SELECT id,type, model, product, name, steps, description, username, create_date FROM uicases')
        cases = [dict(id=row[0], type=row[1], model=row[2], product=row[3], name=row[4], steps=row[5], description=row[6], username=row[7], create_date=row[8]) for row in cur]
        return render_template('ui/uicases.html', SITEURL=SITEURL, username=session['username'], cases=cases, nav=nav, sub_nav_ui = sub_nav_ui, sub_nav_api = sub_nav_api, set_nav=set_nav, operation=operation, pagename = '测试案例')

# UI EDIT
@app.route('/uicase_edit/<int:id>', methods=['GET', 'POST'])
def uicase_edit(id):
    error = None
    if not session.get('logged_in'):
        abort(401)
    else:
        cur = selectall('SELECT keyword FROM uiset')
        list_steps = [dict(keyword=row[0]) for row in cur]

        cur = selectone('SELECT type, model, product, name, steps, description, username, create_date FROM uicases where id=%s',[id])
        cases = [dict(type=row[0], model=row[1], product=row[2], name=row[3], steps=row[4], description=row[5], username=row[6], create_date=row[7]) for row in cur]
        if request.method == 'POST':
            if request.form['steps'].strip == '':
                error = '必输项不能为空'
            else:
                addUpdateDel('update uicases set steps=%s, description=%s where id=%s',[request.form['steps'], request.form['description'],id])
                flash('编辑成功...')
                #return redirect(url_for('uicases'))
        return render_template('ui/uicase_edit.html',SITEURL=SITEURL, username=session['username'],list_steps=list_steps, case=cases[0], nav=nav, sub_nav_ui = sub_nav_ui, sub_nav_api = sub_nav_api, set_nav=set_nav, operation=operation, pagename = '测试案例编辑',error=error,id=id)

# UI QUERY
@app.route('/uicase_query/<int:id>', methods=['GET', 'POST'])
def uicase_query(id):
    if not session.get('logged_in'):
        abort(401)
    else:
        cur = selectone('SELECT type, model, product, name, steps, description, username, create_date FROM uicases where id=%s',[id])
        cases = [dict(type=row[0], model=row[1], product=row[2], name=row[3], steps=row[4], description=row[5], username=row[6], create_date=row[7]) for row in cur]
        return render_template('ui/uicase_query.html', SITEURL=SITEURL, username=session['username'], case=cases[0], nav=nav, sub_nav_ui = sub_nav_ui, sub_nav_api = sub_nav_api, set_nav=set_nav, operation=operation, pagename = '测试案例查看')

# UI CASE DELETE
@app.route('/uicase_delete/<int:id>', methods=['GET', 'POST'])
def uicase_delete(id):
    if not session.get('logged_in'):
        abort(401)
    else:
        cur = addUpdateDel('delete from uicases where id=%s',[id])
        flash('删除成功...')
        return redirect(url_for('uicases'))

# UI CASE EXEC
@app.route('/uicase_exec/<int:id>', methods=['GET', 'POST'])
def uicase_exec(id):
    if not session.get('logged_in'):
        abort(401)
    else:
        error = None
        newrun = RunUiTests(id,session['username'])
        res = newrun.getTestCases()
        return render_template('ui/uicase_exec.html',res=res,SITEURL=SITEURL, username=session['username'], nav=nav, sub_nav_ui = sub_nav_ui, sub_nav_api = sub_nav_api, set_nav=set_nav, operation=operation, pagename = '接口执行结果')

# NEW UI CASE
@app.route('/new_uicase', methods=['GET', 'POST'])
def new_uicase():
    if not session.get('logged_in'):
        abort(401)
    error = None
    cur = selectall('SELECT keyword FROM uiset')
    list_steps = [dict(keyword=row[0]) for row in cur]
    if request.method == 'POST':
        uiname = selectall('select name from uicases')
        uinames = [dict(name=row[0]) for row in uiname]
        uinames = [uiname['name'] for uiname in uinames]

        if request.form['type'].strip() == '' or request.form['product'].strip() == '' or request.form['model'].strip() == '' or request.form['name'].strip() == '' or request.form['steps'].strip == '':
            error = '必输项不能为空'
        elif request.form['name'].strip() in uinames:
            error = "该案例已经存在"
        else:
            addUpdateDel('insert into uicases (type, model, product, name, steps, description, username, create_date) values (%s, %s, %s, %s, %s, %s, %s, %s)',
                         [request.form['type'], request.form['model'], request.form['product'], request.form['name'], request.form['steps'], request.form['description'], session['username'], time.strftime('%Y-%m-%d %X', time.localtime(time.time()))])
            flash('创建成功...')
            #return redirect(url_for('uicases'))
    return render_template('ui/new_uicase.html', list_steps=list_steps, SITEURL=SITEURL, username=session['username'], nav=nav, sub_nav_ui = sub_nav_ui, sub_nav_api = sub_nav_api, set_nav=set_nav, pagename = '新增测试用例', product=product, model_oma=model_oma, error=error)

# UI SITUES
@app.route('/uisitues', methods=['GET', 'POST'])
def uisitues():
    if not session.get('logged_in'):
        abort(401)
    else:
        cur = selectall('SELECT id,name,steps,description,username,create_date FROM uisitues')
        uisitues = [dict(id=row[0], name=row[1], steps=row[2], description=row[3], username=row[4], create_date=row[5]) for row in cur]
        return render_template('ui/uisitues.html', SITEURL=SITEURL, username=session['username'], uisitues=uisitues, nav=nav, sub_nav_ui = sub_nav_ui, sub_nav_api = sub_nav_api, set_nav=set_nav, operation=operation, pagename = '测试集')

# UI SITUES EDIT
@app.route('/uisitue_edit/<int:id>', methods=['GET', 'POST'])
def uisitue_edit(id):
    if not session.get('logged_in'):
        abort(401)
    else:
        cur = selectone('SELECT name, steps, description FROM uisitues where id=%s',[id])
        cases = [dict(name=row[0], steps=row[1], description=row[2]) for row in cur]
        if request.method == 'POST':
            if request.form['steps'].strip == '':
                error = '必输项不能为空'
            else:
                addUpdateDel('update uisitues set steps=%s, description=%s where id=%s',[request.form['steps'], request.form['description'],id])
                flash('编辑成功...')
                #return redirect(url_for('uisitues'))
        return render_template('ui/uisitue_edit.html',SITEURL=SITEURL, username=session['username'],  case=cases[0], nav=nav, sub_nav_ui = sub_nav_ui, sub_nav_api = sub_nav_api, set_nav=set_nav, operation=operation, pagename = '测试集编辑',id=id)

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
        return redirect(url_for('uisitues'))

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
        return redirect(url_for('uisitues'))

# NEW UI SITUE
@app.route('/new_uisitue', methods=['GET', 'POST'])
def new_uisitue():
    if not session.get('logged_in'):
        abort(401)
    error = None
    cur = selectall('SELECT name FROM uicases')
    uisitues = [dict(name=row[0]) for row in cur]
    if request.method == 'POST':
        uiname = selectall('select name from uisitues')
        uinames = [dict(name=row[0]) for row in uiname]
        uinames = [uiname['name'] for uiname in uinames]

        if request.form['name'].strip() == '' or request.form['steps'].strip() == '':
            error = '必输项不能为空'
        elif request.form['name'].strip() in uinames:
            error = "该案例集已经存在"
        else:
            addUpdateDel('insert into uisitues (name, steps, description, username, create_date) values (%s, %s, %s, %s, %s)',
                         [request.form['name'], request.form['steps'], request.form['description'], session['username'], time.strftime('%Y-%m-%d %X', time.localtime(time.time()))])
            flash('创建成功...')
            #return redirect(url_for('uisitues'))
    return render_template('ui/new_uisitue.html',SITEURL=SITEURL, username=session['username'], uisitues=uisitues, nav=nav, sub_nav_ui = sub_nav_ui, sub_nav_api = sub_nav_api, set_nav=set_nav, pagename = '新增测试集',error=error)

# UI SIUTE REPORT
@app.route('/ui_report_list', methods=['GET', 'POST'])
def ui_report_list():
    if not session.get('logged_in'):
        abort(401)
    else:
        for root,dirs,files in os.walk(path_ui):
            report_lists = files
        return render_template('report_list.html',SITEURL=SITEURL, username=session['username'], nav=nav, sub_nav_ui = sub_nav_ui, sub_nav_api = sub_nav_api, set_nav=set_nav, pagename = '测试报告列表',report_lists=report_lists,path = path_ui)


###############################
#             API
###############################
# API SITUES
@app.route('/apisitues', methods=['GET', 'POST'])
def apisitues():
    if not session.get('logged_in'):
        abort(401)
    else:
        cur = selectall('SELECT id,name,steps,description,username,create_date FROM apisitues')
        apisitues = [dict(id=row[0], name=row[1], steps=row[2], description=row[3], username=row[4], create_date=row[5]) for row in cur]
        return render_template('api/apisitues.html', SITEURL=SITEURL, username=session['username'], apisitues=apisitues, nav=nav, sub_nav_ui = sub_nav_ui, sub_nav_api = sub_nav_api, set_nav=set_nav, operation=operation, pagename = '测试集')

# API SITUES EDIT
@app.route('/apisitue_edit/<int:id>', methods=['GET', 'POST'])
def apisitue_edit(id):
    if not session.get('logged_in'):
        abort(401)
    else:
        cur = selectall('SELECT name FROM apicases')
        apisitues = [dict(name=row[0]) for row in cur]
        cur = selectone('SELECT name, steps, description FROM apisitues where id=%s',[id])
        cases = [dict(name=row[0], steps=row[1], description=row[2]) for row in cur]
        if request.method == 'POST':
            if request.form['steps'].strip == '':
                error = '必输项不能为空'
            else:
                addUpdateDel('update apisitues set steps=%s, description=%s where id=%s',[request.form['steps'], request.form['description'],id])
                flash('编辑成功...')
                #return redirect(url_for('apisitues'))
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
        return redirect(url_for('apisitues'))

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
        return redirect(url_for('apisitues'))

# NEW API SITUE
@app.route('/new_apisitue', methods=['GET', 'POST'])
def new_apisitue():
    if not session.get('logged_in'):
        abort(401)
    error = None
    cur = selectall('SELECT name FROM apicases')
    apisitues = [dict(name=row[0]) for row in cur]
    if request.method == 'POST':
        apiname = selectall('select name from apisitues')
        apinames = [dict(name=row[0]) for row in apiname]
        apinames = [apiname['name'] for apiname in apinames]

        if request.form['name'].strip() == '' or request.form['steps'].strip() == '':
            error = '必输项不能为空'
        elif request.form['name'].strip() in apinames:
            error = "该案例集已经存在"
        else:
            addUpdateDel('insert into apisitues (name, steps, description, username, create_date) values (%s, %s, %s, %s, %s)',
                         [request.form['name'], request.form['steps'], request.form['description'], session['username'], time.strftime('%Y-%m-%d %X', time.localtime(time.time()))])
            flash('创建成功...')
            #return redirect(url_for('apisitues'))
    return render_template('api/new_apisitue.html',SITEURL=SITEURL, username=session['username'], nav=nav, sub_nav_ui = sub_nav_ui, sub_nav_api = sub_nav_api, set_nav=set_nav, pagename = '新增测试集',error=error,apisitues=apisitues)

# API SIUTE REPORT
@app.route('/api_report_list', methods=['GET', 'POST'])
def api_report_list():
    if not session.get('logged_in'):
        abort(401)
    else:
        for root,dirs,files in os.walk(path_api):
            report_lists = files
        return render_template('report_list.html',SITEURL=SITEURL, username=session['username'], nav=nav, sub_nav_ui = sub_nav_ui, sub_nav_api = sub_nav_api, set_nav=set_nav, pagename = '测试报告列表',report_lists=report_lists,path = path_api)

# API CASE
@app.route('/apicases', methods=['GET', 'POST'])
def apicases():
    if not session.get('logged_in'):
        abort(401)
    else:
        cur = selectall('SELECT id,type,product,model,name,description,username,create_date, steps FROM apicases')
        apicases = [dict(id=row[0], type=row[1], product=row[2], model=row[3], name=row[4], description=row[5], username=row[6], create_date=row[7], steps=row[8]) for row in cur]
        return render_template('api/apicases.html',SITEURL=SITEURL, username=session['username'], apicases=apicases, nav=nav, sub_nav_ui = sub_nav_ui, sub_nav_api = sub_nav_api, set_nav=set_nav, operation=operation, pagename = '接口测试案例')

# API CASE EDIT
@app.route('/apicase_edit/<int:id>', methods=['GET', 'POST'])
def apicase_edit(id):
    if not session.get('logged_in'):
        abort(401)
    else:
        error = None
        cur = selectall('SELECT name,request FROM apiset')
        apisets = [dict(name=row[0],request=row[1]) for row in cur]
        cur = selectone('SELECT type, name, product, model, steps, description FROM apicases where id=%s',[id])
        cases = [dict(type=row[0], name=row[1], product=row[2], model=row[3], steps=row[4], description=row[5]) for row in cur]
    '''
        if request.method == 'POST':
            if request.form['steps'].strip == '':
                error = '必输项不能为空'
            else:
                addUpdateDel('update apicases set steps=%s where id=%s',[request.form['steps'],id])
                flash('创建成功...')
                return redirect(url_for('new_apicase_edit',case_name=request.form["name"]))
    '''
    return render_template('api/apicase_edit.html',SITEURL=SITEURL, username=session['username'], case=cases[0], nav=nav, sub_nav_ui = sub_nav_ui, sub_nav_api = sub_nav_api, set_nav=set_nav, operation=operation, pagename = '接口编辑', id=id)

# API CASE QUERY
@app.route('/apicase_query/<int:id>', methods=['GET', 'POST'])
def apicase_query(id):
    if not session.get('logged_in'):
        abort(401)
    else:
        cur = selectone('SELECT type, name, product, model, steps, description FROM apicases where id=%s',[id])
        cases = [dict(type=row[0], name=row[1], product=row[2], model=row[3], steps=row[4], description=row[5]) for row in cur]
        steps = cases[0]['steps'].split(';')
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
        addUpdateDel('delete from apicases where id=%s',[id])
        flash('删除成功...')
        return redirect(url_for('apicases'))

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

# NEW API CASE
@app.route('/new_apicase', methods=['GET', 'POST'])
def new_apicase():
    if not session.get('logged_in'):
        abort(401)
    cur = selectall('SELECT name,request FROM apiset')
    apisets = [dict(name=row[0],request=row[1]) for row in cur]
    error = None
    if request.method == 'POST':
        apiname = selectall('select name from apicases')
        apinames = [dict(name=row[0]) for row in apiname]
        apinames = [apiname['name'] for apiname in apinames]

        if request.form['type'].strip() == '' or request.form['product'].strip() == '' or request.form['model'].strip() == '' or request.form['name'].strip() == '':
            error = '必输项不能为空'
        elif request.form['name'].strip() in apinames:
            error = "该案例已经存在"
        else:
            addUpdateDel('insert into apicases (type, model, product, name, steps, description, username, create_date) values (%s, %s, %s, %s, %s, %s, %s, %s)',
                         [request.form['type'], request.form['model'], request.form['product'], request.form['name'], request.form['steps'], request.form['description'], session['username'], time.strftime('%Y-%m-%d %X', time.localtime(time.time()))])
            steps = request.form['steps'].split(';')
            for i in range(len(steps)):
                    cur = selectone('select name,path,method,request,checks from apiset where name = %s',[steps[i]])
                    cases = [dict(name=row[0], path=row[1], method=row[2], request=row[3], checks=row[4]) for row in cur]
                    addUpdateDel('insert into apidates (case_name,name,path,method,request,checks,username,create_date) values (%s,%s,%s,%s,%s,%s,%s,%s)',[request.form['name'], steps[i]+'_'+str(i), cases[0]['path'], cases[0]['method'], cases[0]['request'], cases[0]['checks'], session['username'], time.strftime('%Y-%m-%d %X', time.localtime(time.time()))])
            flash('创建成功...')
            return redirect(url_for('apidate_edit_cases_query',case_name=request.form["name"]))
    return render_template('api/new_apicase.html', SITEURL=SITEURL, username=session['username'], apisets=apisets, model_sicap=model_sicap, nav=nav, sub_nav_ui = sub_nav_ui, sub_nav_api = sub_nav_api, set_nav=set_nav, pagename = '新增用例',error=error)

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


###############################
#             SET
###############################
# UI SET
@app.route('/uiset', methods=['GET', 'POST'])
def uiset():
    if not session.get('logged_in'):
        abort(401)
    else:
        cur = selectall('SELECT id,keyword,description,template,example FROM uiset')
        uisets = [dict(id=row[0], keyword=row[1], description=row[2], template=row[3], example=row[4]) for row in cur]
        return render_template('set/uiset.html',SITEURL=SITEURL, username=session['username'],  uisets=uisets, nav=nav, sub_nav_ui = sub_nav_ui, sub_nav_api = sub_nav_api, set_nav=set_nav, operation=operation, pagename = 'UI步骤说明')

# UI SET EDIT
@app.route('/uiset_edit/<int:id>', methods=['GET', 'POST'])
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
                flash('创建成功...')
                return redirect(url_for('uiset'))
        return render_template('set/uiset_edit.html', SITEURL=SITEURL, username=session['username'], case=cases[0], nav=nav, sub_nav_ui = sub_nav_ui, sub_nav_api = sub_nav_api, set_nav=set_nav, operation=operation, pagename = 'UI步骤说明编辑',id=id)

# UI SET QUERY
@app.route('/uiset_query/<int:id>', methods=['GET', 'POST'])
def uiset_query(id):
    if not session.get('logged_in'):
        abort(401)
    else:
        cur = selectone('SELECT id,keyword,description,template,example FROM uiset where id=%s',[id])
        cases = [dict(id=row[0], keyword=row[1], description=row[2], template=row[3], example=row[4]) for row in cur]
        return render_template('set/uiset_query.html', SITEURL=SITEURL, username=session['username'], case=cases[0], nav=nav, sub_nav_ui = sub_nav_ui, sub_nav_api = sub_nav_api, set_nav=set_nav, operation=operation, pagename = 'UI步骤说明查看')

# UI SET DELETE
@app.route('/uiset_delete/<int:id>', methods=['GET', 'POST'])
def uiset_delete(id):
    if not session.get('logged_in'):
        abort(401)
    else:
        addUpdateDel('delete from uiset where id=%s',[id])
        flash('删除成功...')
        return redirect(url_for('uiset'))

# NEW UI SET
@app.route('/new_uiset', methods=['GET', 'POST'])
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
            return redirect(url_for('uiset'))
    return render_template('set/new_uiset.html', SITEURL=SITEURL, username=session['username'], nav=nav, sub_nav_ui = sub_nav_ui, sub_nav_api = sub_nav_api, set_nav=set_nav, pagename = '新建UI步骤说明',error=error)

# API SET
@app.route('/apiset', methods=['GET', 'POST'])
def apiset():
    if not session.get('logged_in'):
        abort(401)
    else:
        cur = selectall('SELECT id,name,path,method,request,checks,description FROM apiset')
        apisets = [dict(id=row[0], name=row[1], path=row[2], method=row[3], request=row[4], checks=row[5], description=row[6]) for row in cur]
        return render_template('set/apiset.html',SITEURL=SITEURL, username=session['username'], apisets=apisets, nav=nav, sub_nav_ui = sub_nav_ui, sub_nav_api = sub_nav_api, set_nav=set_nav, operation=operation, pagename = '全部接口')

# API SET EDIT
@app.route('/apiset_edit/<int:id>', methods=['GET', 'POST'])
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
                flash('创建成功...')
                return redirect(url_for('apiset'))
        return render_template('set/apiset_edit.html',SITEURL=SITEURL, username=session['username'], case=cases[0], nav=nav, sub_nav_ui = sub_nav_ui, sub_nav_api = sub_nav_api, set_nav=set_nav, operation=operation, pagename = '接口编辑', id=id)

# API SET QUERY
@app.route('/apiset_query/<int:id>', methods=['GET', 'POST'])
def apiset_query(id):
    if not session.get('logged_in'):
        abort(401)
    else:
        cur = selectone('SELECT id,name,path,method,request,checks,description FROM apiset where id=%s',[id])
        cases = [dict(id=row[0], name=row[1], path=row[2], method=row[3], request=row[4], checks=row[5], description=row[6]) for row in cur]
        return render_template('set/apiset_query.html',SITEURL=SITEURL, username=session['username'],  case=cases[0], nav=nav, sub_nav_ui = sub_nav_ui, sub_nav_api = sub_nav_api, set_nav=set_nav, operation=operation, pagename = '接口查看')

# API SET DELETE
@app.route('/apiset_delete/<int:id>', methods=['GET', 'POST'])
def apiset_delete(id):
    if not session.get('logged_in'):
        abort(401)
    else:
        addUpdateDel('delete from apiset where id=%s',[id])
        flash('删除成功...')
        return redirect(url_for('apiset'))

# API SET EXEC
@app.route('/apiset_exec/<int:id>', methods=['GET', 'POST'])
def apiset_exec(id):
    if not session.get('logged_in'):
        abort(401)
    else:
        error = None
        newrun = RunTests(id,session['username'])
        res=newrun.getApis()
        if res[0:4] == '执行失败':
            flash('执行失败...')
            return redirect(url_for('apiset'))
        else:
            flash('执行成功...')
        return render_template('set/apiset_exec.html',SITEURL=SITEURL, username=session['username'], res=res,nav=nav, sub_nav_ui = sub_nav_ui, sub_nav_api = sub_nav_api, set_nav=set_nav, operation=operation, pagename = '接口执行结果')

# NEW API
@app.route('/new_apiset', methods=['GET', 'POST'])
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
            return redirect(url_for('apiset'))
    return render_template('set/new_apiset.html',SITEURL=SITEURL, username=session['username'],  nav=nav, sub_nav_ui = sub_nav_ui, sub_nav_api = sub_nav_api, set_nav=set_nav, pagename = '新增接口', product=product, model_sicap=model_sicap, error=error, methods=http_methods)

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
        print(usernames)
        if request.form['username'].strip() == '' or request.form['pw_new_o'].strip == '' or request.form['pw_new_t'].strip == '':
            error = '必输项不能为空'
        elif request.form['pw_new_o'].strip != request.form['pw_new_t'].strip:
            error = '两次密码输入不一致'
        else:
            addUpdateDel('update user set password = %s where username = %s',[encrypt(request.form['pw_new_o']),request.form['username']])
            flash("重置密码成功...")
    except Exception as e:
        print(str(e))
    finally:
        return render_template('admin/reset_passwd.html', usernames=usernames, nav=nav, sub_nav_ui = sub_nav_ui, sub_nav_api = sub_nav_api, set_nav=set_nav, operation=operation, error=error, pagename = '重置密码')


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
        print(str(e))
    finally:
        return render_template('admin/register.html', nav=nav, sub_nav_ui = sub_nav_ui, sub_nav_api = sub_nav_api, set_nav=set_nav, operation=operation, error=error, pagename = '注册')

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
    #app.run(host='10.43.2.225')