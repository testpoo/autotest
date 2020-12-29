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

# jinja2过滤器
@app.template_filter('split')
def split(str):
    temp = ''
    first = str.split('|')
    for sec in first:
        temp +=sec.split('-')[0]+'|'
    temp = temp[:-1]
    return temp

# 导入time
#@app.context_processor
#def get_current_time():
#    def get_time(timeFormat="%b %d, %Y - %H:%M:%S"):
#        return time.strftime(timeFormat)
#    return dict(current_time=get_time)

# 获取中文名
@app.context_processor
def get_zh_name():
    def get_name(username):
        zname = selectone('select zh_name from user where username = %s',(username,))
        return zname[0][0]
    return dict(get_name=get_name)

# 获取siteurl
@app.context_processor
def get_siteurl():
    return dict(SITEURL=SITEURL)

# 获取username
@app.context_processor
def get_user():
    def get_user(username):
        return username
    return dict(username=get_user)

# 获取用户导航菜单
@app.context_processor
def get_navs():
    def get_nav(username,sub_nav): 
        auths = selectone('select auth from user where username = %s',(username,))[0][0].split('|')
        sql = 'SELECT name,url,status FROM auth WHERE TYPE = "'+sub_nav+'" and ('

        for auth in auths:
            sql+='auth like "%'+auth+'%" or '
        sql = sql[:-4]+') order by `order`'

        navs = selectall(sql)
        return navs
    return dict(nav=get_nav)

# 获取页面操作项目
@app.context_processor
def get_operation():
    def get_buttons(menu,type):
        auths = selectone('SELECT operation FROM auth WHERE NAME = %s and type=%s',[menu,type])[0][0].split('|')
        buttons = []
        for auth in auths:
            buttons.append(auth.split('-'))
        return buttons
    return dict(operation=get_buttons)

# 获取用户权限
@app.context_processor
def get_auth():
    def get_auths(user):
        auths = selectone('SELECT auth FROM user WHERE username = %s',[user])[0][0]
        return auths
    return dict(role=get_auths)

# 获取产品
@app.context_processor
def get_product():
    return dict(product=product)

# 获取oma模块
@app.context_processor
def get_model_oma():
    return dict(model_oma=model_oma)

# 获取sicap模块
@app.context_processor
def get_model_sicap():
    return dict(model_sicap=model_sicap)

# 页面权限控制
def get_auths_control(user,url,category,status,operation,opera):
    user_auths = selectone('SELECT auth FROM user WHERE username = %s',[user])[0][0].split('|')
    page_auths = selectall('SELECT auth FROM auth WHERE url = "'+url+'" AND '+category+' = '+str(status)+' and '+operation+' like "%'+opera+'%"')[0][0].split('|')
    if list(set(page_auths) & set(user_auths)) != []:
        return True
    else:
        return False

# 获取案例状态
def activity(category,cases,id):
    activity = selectall("select activity from "+cases+" where id = '"+str(id)+"'")[0][0]
    return str(activity)

###############################
#             公共
###############################
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
        counts = selectall('select count(1) from uicases where activity !="2"')[0][0]
        versions = selectall('SELECT VERSION,COUNT(1) AS COUNT FROM uicases where activity !="2" GROUP BY VERSION ORDER BY COUNT DESC')
        models = selectall('SELECT MODEl,COUNT(1) AS COUNT FROM uicases where activity !="2"  GROUP BY MODEl ORDER BY COUNT DESC')
        return render_template('index.html', current_user = session['username'],counts=counts,versions=versions,models=models,pagename = '主页')
    else:
        return redirect(url_for('login'))

# 密码修改
@app.route('/modify_passwd', methods=['GET', 'POST'])
def modify_passwd():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
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
    return render_template('modify_passwd.html',pagename = '修改密码', error=error)

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

###############################
#             UI
###############################
# UI案例展示
@app.route('/uicases/<category>/<value>/<int:status>/<int:num>', methods=['GET', 'POST'])
def uicases(category,value,status,num):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    elif get_auths_control(session['username'],'uicases','status',status,'1','1') == False:
        return render_template('invalid.html')
    else:
        error = None
        if category == 'a.name':
            all_Count = selectall('SELECT count(1) FROM uicases a inner join user b on a.username=b.username where activity="'+str(status)+'" and '+category+' like "%'+value+'%"')[0][0]
        else:
            all_Count = selectall('SELECT count(1) FROM uicases a inner join user b on a.username=b.username where activity="'+str(status)+'" and '+category+'="'+value+'"')[0][0]
        all_Page = math.ceil(all_Count/page_Count)
        cur_usernames=selectall('SELECT b.zh_name FROM uicases a inner join user b ON a.username=b.username WHERE a.activity="'+str(status)+'" GROUP BY a.username')
        usernames=[dict(zh_name=row[0]) for row in cur_usernames]
        cur_versions=selectall('SELECT version FROM uicases WHERE activity="'+str(status)+'" group by version')
        versions=[dict(version=row[0]) for row in cur_versions]
        cur_models=selectall('SELECT model FROM uicases WHERE activity="'+str(status)+'" group by model')
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
            return redirect(url_for('uicases',category=category,value=changeWord(value),status=status,num='1'))
        if category == 'a.name':
            cur = selectall('SELECT a.id,a.type,a.version, a.model, a.product, a.name,a.pre_steps, a.steps, a.next_steps,a.description,a.exec_result, b.zh_name, a.create_date FROM uicases a inner join user b on a.username=b.username where activity="'+str(status)+'" and '+category+' like "%'+wordChange(value)+'%" order by a.id desc LIMIT '+str((num-1)*page_Count)+','+str(page_Count))
        else:
            cur = selectall('SELECT a.id,a.type,a.version, a.model, a.product, a.name,a.pre_steps, a.steps, a.next_steps,a.description,a.exec_result, b.zh_name, a.create_date FROM uicases a inner join user b on a.username=b.username where activity="'+str(status)+'" and '+category+'="'+wordChange(value)+'" order by a.id desc LIMIT '+str((num-1)*page_Count)+','+str(page_Count))
        cases = [dict(id=row[0], type=row[1], version=row[2], model=row[3], product=row[4], name=row[5], pre_steps=row[6], steps=row[7], next_steps=row[8], description=row[9], exec_result=row[10], zh_name=row[11], create_date=row[12]) for row in cur]
        return render_template('ui/uicases.html',cases=cases,all_Page=all_Page,category=category,value=value,status=status,num=num,usernames=usernames,versions=versions,models=models,current='uicases'+str(status),error=error,pagename = 'UI测试用例')

# 新建UI案例
@app.route('/new_uicase/<int:status>', methods=['GET', 'POST'])
def new_uicase(status):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    elif get_auths_control(session['username'],'uicases','status',status,'1','1') == False:
        return render_template('invalid.html')
    error = None

    version = selectall('select version from versions')
    versions = [dict(version=row[0]) for row in version]
    versions = [version['version'] for version in versions]

    issuetype = selectall('select name from uicases where type="前置用例"')
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
                         [request.form['type'],request.form['version'], request.form['model'], request.form['product'], request.form['name'].strip(),request.form['pre-steps'], request.form['steps'],request.form['next-steps'], request.form['description'], '0', session['username'], time.strftime('%Y-%m-%d %X', time.localtime(time.time()))])

            cur_new= selectone("SELECT * FROM uicases WHERE name = %s",[request.form['name']])
            if cur_new != ():
                flash('创建成功...')
            else:
                flash('创建失败...')

            return redirect(url_for('uicases',category='a.username',value=session['username'],status=status,num=1))
    return render_template('ui/new_uicase.html', list_steps=list_steps,versions=versions, current='uicases'+str(status), status=status,pagename = '新增测试用例', issuetypes=issuetypes,nexttypes=nexttypes, error=error)

# UI案例查询
@app.route('/uicase_query/<int:status>/<int:id>', methods=['GET', 'POST'])
def uicase_query(status,id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    elif get_auths_control(session['username'],'uicases','status',status,'operation','查看-query') == False:
        return render_template('invalid.html')
    else:
        cur = selectone('SELECT type,version, model, product, name,pre_steps, steps, description,next_steps, username, create_date FROM uicases where id=%s',[id])
        cases = [dict(type=row[0], version=row[1], model=row[2], product=row[3], name=row[4], pre_steps=row[5], steps=row[6], description=row[7], next_steps=row[8], username=row[9], create_date=row[10]) for row in cur]
        return render_template('ui/uicase_query.html',case=cases[0],current='uicases'+str(status),status=status,id=id,pagename = '测试用例查看')

# UI案例删除
@app.route('/uicase_delete/<int:status>/<int:id>', methods=['GET', 'POST'])
def uicase_delete(status,id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    elif get_auths_control(session['username'],'uicases','status',status,'operation','删除-delete') == False:
        return render_template('invalid.html')
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
        elif activity('delete','uicases',id) not in activity_dict['delete']:
            flash('用例状态不允许执行该操作...')
        else:
            cur = addUpdateDel('update uicases set activity = "2" where id=%s and activity in ("0","1","3")',[id])

            cur_uicases_del= selectone("SELECT * FROM uicases where id=%s and activity =2",[id])
            if cur_uicases_del != ():
                flash('删除成功...')
            else:
                flash('删除失败...')

        return redirect(url_for('uicases',category='a.username',value=session['username'],status=status,num=1))

# UI案例执行
@app.route('/uicase_exec/<int:status>/<int:id>', methods=['GET', 'POST'])
def uicase_exec(status,id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    elif get_auths_control(session['username'],'uicases','status',status,'operation','执行-exec') == False:
        return render_template('invalid.html')
    else:
        error = None
        newrun = RunUiTests(id,session['username'])
        res = newrun.getTestCases()
        return render_template('ui/uicase_exec.html',res=res,current='uicases'+str(status),pagename = '用例执行结果')

# UI案例驳回
@app.route('/uicase_reject/<int:status>/<int:id>', methods=['GET', 'POST'])
def uicase_reject(status,id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    elif get_auths_control(session['username'],'uicases','status',status,'operation','驳回-reject') == False:
        return render_template('invalid.html')
    elif activity('reject','uicases',id) not in activity_dict['reject']:
        flash('用例状态不允许执行该操作...')
    else:
        cur = addUpdateDel('update uicases set activity=0 where id=%s and activity in ("1","3")',[id])

        cur_uicases_reject= selectone("SELECT * FROM uicases where id=%s and activity=0",[id])
        if cur_uicases_reject != ():
            flash('驳回成功...')
        else:
            flash('驳回失败...')

    return redirect(url_for('uicases',category='a.username',value=session['username'],status=status,num=1))

# UI案例编辑
@app.route('/uicase_edit/<int:status>/<int:id>', methods=['GET', 'POST'])
def uicase_edit(status,id):
    error = None
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    elif get_auths_control(session['username'],'uicases','status',status,'operation','编辑-edit') == False:
        return render_template('invalid.html')
    else:
        issuetype = selectall('select name from uicases where type="前置用例"')
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
            elif request.form['type'].strip() in ('前置用例','后置用例'):
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

                return redirect(url_for('uicases',category='a.username',value=session['username'],status=status,num=1))
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

                return redirect(url_for('uicases',category='a.username',value=session['username'],status=status,num=1))
        return render_template('ui/uicase_edit.html', list_steps=list_steps, case=cases[0],issuetypes=issuetypes,nexttypes=nexttypes,current='uicases'+str(status),status=status,pagename = '测试用例编辑',error=error,id=id)

# UI案例删除后恢复
@app.route('/uicase_restore/<int:status>/<int:id>', methods=['GET', 'POST'])
def uicase_restore(status,id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    elif get_auths_control(session['username'],'uicases','status',status,'operation','恢复-restore') == False:
        return render_template('invalid.html')
    elif activity('restore','uicases',id) not in activity_dict['restore']:
        flash('用例状态不允许执行该操作...')
    else:
        cur = addUpdateDel('update uicases set activity=0 where id=%s and activity=2',[id])

        cur_uicases_del= selectone("SELECT * FROM uicases where id=%s and activity=0",[id])
        if cur_uicases_del != ():
            flash('恢复成功...')
        else:
            flash('恢复失败...')

    return redirect(url_for('uicases',category='a.username',value=session['username'],status=status,num=1))

# UI案例彻底删除
@app.route('/uicase_redelete/<int:status>/<int:id>', methods=['GET', 'POST'])
def uicase_redelete(status,id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    elif get_auths_control(session['username'],'uicases','status',status,'operation','彻底删除-redelete') == False:
        return render_template('invalid.html')
    elif activity('redelete','uicases',id) not in activity_dict['redelete']:
        flash('用例状态不允许执行该操作...')
    else:
        uicase = selectone('select name from uicases where id=%s',[id])
        uicases = [dict(name=row[0]) for row in uicase]
        uicase_name = uicases[0]['name']
        
        cur = addUpdateDel('delete from uicases where id=%s',[id])

        cur_uicases_del= selectone("SELECT * FROM uicases where id=%s",[id])
        if cur_uicases_del == ():
            flash('删除成功...')
        else:
            flash('删除失败...')

    return redirect(url_for('uicases',category='a.username',value=session['username'],status=status,num=1))

# UI案例提交
@app.route('/uicase_submit/<int:status>/<int:id>', methods=['GET', 'POST'])
def _uicase_submit(status,id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    elif get_auths_control(session['username'],'uicases','status',status,'operation','提交-submit') == False:
        return render_template('invalid.html')
    elif activity('submit','uicases',id) not in activity_dict['submit']:
        flash('用例状态不允许执行该操作...')
    else:
        uicase = selectone('select name from uicases where id=%s',[id])
        uicases = [dict(name=row[0]) for row in uicase]
        uicase_name = uicases[0]['name']
        
        cur = addUpdateDel('update uicases set activity=1 where id=%s and activity=0',[id])

        cur_uicases_submint= selectone("SELECT * FROM uicases where id=%s and activity=1",[id])
        if cur_uicases_submint != ():
            flash('提交成功...')
        else:
            flash('提交失败...')

    return redirect(url_for('uicases',category='a.username',value=session['username'],status=status,num=1))

###############################
#          UI测试集
###############################
# UI测试集页面展示
@app.route('/uisitues/<name>/<value>/<int:num>', methods=['GET', 'POST'])
def uisitues(name,value,num):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    elif get_auths_control(session['username'],'uisitues','1','1','1','1') == False:
        return render_template('invalid.html')
    else:
        all_Count = selectall('SELECT count(1) FROM uisitues a where '+name+' = "'+value+'" and activity = \'1\'')[0][0]
        all_Page = math.ceil(all_Count/page_Count)
        uisitues_list = selectall('select name from uisitues where activity = \'1\'')
        if request.method == 'POST':
            if request.form['select-interface'] != '':
                name = 'a.name'
                value = request.form['select-interface']
            else:
                name = '1'
                value = '1'
            return redirect(url_for('uisitues',name=name,value=value,num=num))
        cur = selectall('SELECT a.id,a.name,a.exec_mode,a.steps,a.description,b.zh_name,a.create_date FROM uisitues a inner join user b on a.username=b.username where '+name+' = "'+value+'" and activity = \'1\' order by a.id desc LIMIT '+str((num-1)*page_Count)+','+str(page_Count))
        uisitues = [dict(id=row[0], name=row[1], exec_mode=row[2], steps=row[3], description=row[4], username=row[5], create_date=row[6]) for row in cur]
        return render_template('ui/uisitues.html',uisitues=uisitues,name=name,value=value, num=num, uisitues_list=uisitues_list,all_Page=all_Page,current="uisitues", pagename = '测试集')

# 新建UI测试集
@app.route('/new_uisitue', methods=['GET', 'POST'])
def new_uisitue():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    elif get_auths_control(session['username'],'uisitues','1','1','1','1') == False:
        return render_template('invalid.html')
    error = None
    cur_issue = selectall('SELECT name FROM uicases where activity="1"')
    uisitues_issue = [dict(name=row[0]) for row in cur_issue]

    cur_model = selectall('SELECT model FROM uicases where activity="1" group by model')
    uisitues_model = [dict(model=row[0]) for row in cur_model]

    cur_version = selectall('SELECT version FROM uicases where activity="1" group by version')
    uisitues_version = [dict(version=row[0]) for row in cur_version]

    cur_name = selectall('SELECT b.zh_name FROM uicases a inner join user b on a.username=b.username group BY a.username')
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
            addUpdateDel('insert into uisitues (name, exec_mode, steps, activity, description, username, create_date) values (%s, %s, %s, %s, %s, %s, %s)',
                         [request.form['name'], request.form['exec-mode'], request.form['steps'], '1', request.form['description'], session['username'], time.strftime('%Y-%m-%d %X', time.localtime(time.time()))])
            
            cur_new= selectone("SELECT * FROM uisitues WHERE name = %s",[request.form['name']])
            if cur_new != ():
                flash('创建成功...')
            else:
                flash('创建失败...')
            return redirect(url_for('uisitues',name=1,value=1,num=1))
    return render_template('ui/new_uisitue.html',uisitues_issue=uisitues_issue, uisitues_name=uisitues_name, uisitues_model=uisitues_model, uisitues_version=uisitues_version, current="uisitues", pagename = '新增测试集',error=error)

# UI测试集编辑
@app.route('/uisitue_edit/<int:id>', methods=['GET', 'POST'])
def uisitue_edit(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    elif get_auths_control(session['username'],'uisitues','1','1','operation','编辑-edit') == False:
        return render_template('invalid.html')
    else:
        cur_issue = selectall('SELECT name FROM uicases where activity="1"')
        uisitues_issue = [dict(name=row[0]) for row in cur_issue]

        cur_model = selectall('SELECT model FROM uicases where activity="1" group by model')
        uisitues_model = [dict(model=row[0]) for row in cur_model]

        cur_version = selectall('SELECT version FROM uicases where activity="1" group by version')
        uisitues_version = [dict(version=row[0]) for row in cur_version]

        cur_name = selectall('SELECT b.zh_name FROM uicases a inner join user b on a.username=b.username group BY a.username')
        uisitues_name = [dict(username=row[0]) for row in cur_name]

        cur = selectone('SELECT name, steps, description FROM uisitues where id=%s',[id])
        cases = [dict(name=row[0], steps=row[1], description=row[2]) for row in cur]
        if request.method == 'POST':
            if request.form['steps'].strip == '':
                error = '必输项不能为空'
            else:
                addUpdateDel('update uisitues set exec_mode=%s, steps=%s, description=%s where id=%s',[request.form['exec-mode'], request.form['steps'], request.form['description'],id])

                cur_edit= selectone("SELECT steps,description FROM uisitues WHERE id = %s",[id])
                uisitues_edit = [dict(steps=row[0],description=row[1]) for row in cur_edit]
                uisitues_steps = uisitues_edit[0]['steps']
                uisitues_description = uisitues_edit[0]['description']
                if request.form['steps'] == uisitues_steps and request.form['description'] == uisitues_description:
                    flash('编辑成功...')
                else:
                    flash('编辑失败...')
                return redirect(url_for('uisitues',name=1,value=1,num=1))
        return render_template('ui/uisitue_edit.html',uisitues_issue=uisitues_issue, uisitues_model=uisitues_model, uisitues_version=uisitues_version,uisitues_name=uisitues_name, case=cases[0],current="uisitues", pagename = '测试集编辑',id=id)

# UI测试集查询
@app.route('/uisitue_query/<int:id>', methods=['GET', 'POST'])
def uisitue_query(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    elif get_auths_control(session['username'],'uisitues','1','1','operation','查看-query') == False:
        return render_template('invalid.html')
    else:
        cur = selectone('SELECT name,exec_mode, steps, description FROM uisitues where id=%s',[id])
        cases = [dict(name=row[0], exec_mode=row[1], steps=row[2], description=row[3]) for row in cur]
        return render_template('ui/uisitue_query.html',case=cases[0],current="uisitues", pagename = '测试集查看')

# UI测试集删除
@app.route('/uisitue_delete/<int:id>', methods=['GET', 'POST'])
def uisitue_delete(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    elif get_auths_control(session['username'],'uisitues','1','1','operation','删除-delete') == False:
        return render_template('invalid.html')
    else:
        cur = addUpdateDel('update uisitues set activity = \'2\' where id=%s',[id])

        cur_uisitues_del= selectone("SELECT * FROM uisitues where activity != '2' id=%s",[id])
        if cur_uisitues_del == None:
            flash('删除成功...')
        else:
            flash('删除失败...')

        return redirect(url_for('uisitues',name=1,value=1,num=1))

# UI测试集执行
@app.route('/uisitue_exec/<int:id>', methods=['GET', 'POST'])
def uisitue_exec(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    elif get_auths_control(session['username'],'uisitues','1','1','operation','执行-exec') == False:
        return render_template('invalid.html')
    else:
        error = None
        username = session['username']
        newrun = RunUiTests(id,username)
        newrun.getTestSiutes()
        flash('执行完毕...')
        return redirect(url_for('uisitues',name=1,value=1,num=1))

# UI测试集报告
@app.route('/ui_report_list/<int:num>', methods=['GET', 'POST'])
def ui_report_list(num):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    elif get_auths_control(session['username'],'ui_report_list','1','1','1','1') == False:
        return render_template('invalid.html')
    else:
        report_lists = get_file_list(path_ui)
        all_Count = len(report_lists)
        all_Page = math.ceil(all_Count/page_Count)
        report_lists = report_lists[(num-1)*page_Count:num*page_Count]
        return render_template('report_list.html', pagename = '测试报告列表',report_lists=report_lists,path = path_ui,all_Page=all_Page,num=num,page_Count=page_Count,current='ui_report_list',type = 'ui')

# UI执行失败的案例
@app.route('/exec_failed/<type>/0', methods=['GET', 'POST'])
def exec_failed(type):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    elif get_auths_control(session['username'],'uisitues','1','1','1','1') == False:
        return render_template('invalid.html')
    else:
        error = None
        username = session['username']
        if type == 'ui':
            newrun = RunUiTests('0',username)
            newrun.getTestSiutes()
            flash('执行成功...')
            return redirect(url_for('ui_report_list'))
        elif type == 'api':
            newrun = RunTests('0',username)
            newrun.getTestSiutes()
            flash('执行成功...')
            return redirect(url_for('api_report_list'))

###############################
#          API测试集
###############################
# API测试集页面展示
@app.route('/apisitues/<name>/<value>/<int:num>', methods=['GET', 'POST'])
def apisitues(name,value,num):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    elif get_auths_control(session['username'],'apisitues','1','1','1','1') == False:
        return render_template('invalid.html')
    else:
        all_Count = selectall('SELECT count(1) FROM apisitues a where '+name+' = "'+value+'" and  activity = \'1\'')[0][0]
        all_Page = math.ceil(all_Count/page_Count)
        apisitues_list = selectall('select name from apisitues where activity = \'1\'')
        if request.method == 'POST':
            if request.form['select-interface'] != '':
                name = 'a.name'
                value = request.form['select-interface']
            else:
                name = '1'
                value = '1'
            return redirect(url_for('apisitues',name=name,value=value,num=num))
        cur = selectall('SELECT a.id,a.name,a.exec_mode, a.steps,a.description,b.zh_name,a.create_date FROM apisitues a inner join user b on a.username=b.username where '+name+' = "'+value+'" and activity = \'1\' order by a.id desc LIMIT '+str((num-1)*page_Count)+','+str(page_Count))
        apisitues = [dict(id=row[0], name=row[1], exec_mode=row[2], steps=row[3], description=row[4], username=row[5], create_date=row[6]) for row in cur]
        return render_template('api/apisitues.html',apisitues=apisitues, all_Page=all_Page, name=name,value=value, num=num,apisitues_list=apisitues_list,pagename = '测试集',current='apisitues')

# 新建API测试集
@app.route('/new_apisitue', methods=['GET', 'POST'])
def new_apisitue():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    elif get_auths_control(session['username'],'apisitues','1','1','1','1') == False:
        return render_template('invalid.html')
    error = None
    cur_issue = selectall('SELECT name FROM apicases where activity="1"')
    apisitues_issue = [dict(name=row[0]) for row in cur_issue]

    cur_model = selectall('SELECT model FROM apicases where activity="1" group by model')
    apisitues_model = [dict(model=row[0]) for row in cur_model]

    cur_version = selectall('SELECT version FROM apicases where activity="1" group by version')
    apisitues_version = [dict(version=row[0]) for row in cur_version]

    cur_name = selectall('SELECT b.zh_name FROM apicases a inner join user b on a.username=b.username group BY a.username')
    apisitues_name = [dict(username=row[0]) for row in cur_name]

    if request.method == 'POST':
        apiname = selectall('select name from apisitues')
        apinames = [dict(name=row[0]) for row in apiname]
        apinames = [apiname['name'] for apiname in apinames]

        if request.form['name'].strip() == '' or request.form['exec-mode'].strip() == '' or request.form['steps'].strip() == '':
            error = '必输项不能为空'
        elif request.form['name'].strip() in apinames:
            error = "该用例集已经存在"
        else:
            addUpdateDel('insert into apisitues (name, exec_mode, steps, activity, description, username, create_date) values (%s, %s, %s, %s, %s, %s, %s)',
                         [request.form['name'], request.form['exec-mode'], request.form['steps'], '1', request.form['description'], session['username'], time.strftime('%Y-%m-%d %X', time.localtime(time.time()))])

            cur_new= selectone("SELECT * FROM apisitues WHERE name = %s",[request.form['name']])
            if cur_new != ():
                flash('创建成功...')
            else:
                flash('创建失败...')

            return redirect(url_for('apisitues',name=1,value=1,num=1))
    return render_template('api/new_apisitue.html', pagename = '新增测试集',error=error,apisitues_issue=apisitues_issue,apisitues_model=apisitues_model,apisitues_version=apisitues_version,apisitues_name=apisitues_name,current='apisitues')

# API测试集编辑
@app.route('/apisitue_edit/<int:id>', methods=['GET', 'POST'])
def apisitue_edit(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    elif get_auths_control(session['username'],'apisitues','1','1','operation','编辑-edit') == False:
        return render_template('invalid.html')
    else:
        error=None
        cur_issue = selectall('SELECT name FROM apicases where activity="1"')
        apisitues_issue = [dict(name=row[0]) for row in cur_issue]

        cur_model = selectall('SELECT model FROM apicases where activity="1" group by model')
        apisitues_model = [dict(model=row[0]) for row in cur_model]

        cur_version = selectall('SELECT version FROM apicases where activity="1" group by version')
        apisitues_version = [dict(version=row[0]) for row in cur_version]

        cur_name = selectall('SELECT b.zh_name FROM apicases a inner join user b on a.username=b.username group BY a.username')
        apisitues_name = [dict(username=row[0]) for row in cur_name]

        cur = selectone('SELECT name, exec_mode, steps, description FROM apisitues where id=%s',[id])
        cases = [dict(name=row[0], exec_mode=row[1], steps=row[2], description=row[3]) for row in cur]
        if request.method == 'POST':
            if request.form['steps'].strip == '':
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
                return redirect(url_for('apisitues',name=1,value=1,num=1))
        return render_template('api/apisitue_edit.html',case=cases[0], pagename = '测试集编辑',id=id,apisitues_issue=apisitues_issue,apisitues_model=apisitues_model,apisitues_version=apisitues_version,apisitues_name=apisitues_name,error=error,current='apisitues')

# API测试集查询
@app.route('/apisitue_query/<int:id>', methods=['GET', 'POST'])
def apisitue_query(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    elif get_auths_control(session['username'],'apisitues','1','1','operation','查看-query') == False:
        return render_template('invalid.html')
    else:
        cur = selectone('SELECT name, exec_mode, steps, description FROM apisitues where id=%s',[id])
        cases = [dict(name=row[0], exec_mode=row[1], steps=row[2], description=row[3]) for row in cur]
        return render_template('api/apisitue_query.html',case=cases[0],current='apisitues', pagename = '测试集查看')

# API测试集删除
@app.route('/apisitue_delete/<int:id>', methods=['GET', 'POST'])
def apisitue_delete(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    elif get_auths_control(session['username'],'apisitues','1','1','operation','删除-delete') == False:
        return render_template('invalid.html')
    else:
        cur = addUpdateDel('update apisitues set activity = \'2\' where id=%s',[id])

        cur_apisitues_del= selectone("SELECT * FROM apisitues where id=%s and activity != '2'",[id])
        if cur_apisitues_del == ():
            flash('删除成功...')
        else:
            flash('删除失败...')

        return redirect(url_for('apisitues',name=1,value=1,num=1))

# API测试集执行
@app.route('/apisitue_exec/<int:id>', methods=['GET', 'POST'])
def apisitue_exec(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    elif get_auths_control(session['username'],'apisitues','1','1','operation','执行-exec') == False:
        return render_template('invalid.html')
    else:
        error = None
        username = session['username']
        newrun = RunTests(id,username)
        res=newrun.getTestSiutes()
        flash('执行完毕...')
        return redirect(url_for('apisitues',name=1,value=1,num=1))

# API测试集报告
@app.route('/api_report_list/<int:num>', methods=['GET', 'POST'])
def api_report_list(num):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    elif get_auths_control(session['username'],'api_report_list','1','1','1','1') == False:
        return render_template('invalid.html')
    else:
        report_lists = get_file_list(path_api)
        all_Count = len(report_lists)
        all_Page = math.ceil(all_Count/page_Count)
        report_lists = report_lists[(num-1)*page_Count:num*page_Count]
        return render_template('report_list.html', pagename = '测试报告列表',report_lists=report_lists,path = path_api,all_Page=all_Page,num=num,page_Count=page_Count,current='api_report_list',type='api')

###############################
#              API
###############################
# API用例页面展示
@app.route('/apicases/<category>/<value>/<int:status>/<int:num>', methods=['GET', 'POST'])
def apicases(category,value,status,num):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    elif get_auths_control(session['username'],'apicases','status',status,'1','1') == False:
        return render_template('invalid.html')
    else:
        error = None
        if category == 'a.name':
            all_Count = selectall('SELECT count(1) FROM apicases a inner join user b on a.username=b.username where activity="'+str(status)+'" and '+category+' like "%'+value+'%"')[0][0]
        else:
            all_Count = selectall('SELECT count(1) FROM apicases a inner join user b on a.username=b.username where activity="'+str(status)+'" and '+category+'="'+value+'"')[0][0]
        all_Page = math.ceil(all_Count/page_Count)
        cur_usernames=selectall('SELECT b.zh_name FROM apicases a inner join user b ON a.username=b.username WHERE a.activity="'+str(status)+'" GROUP BY a.username')
        usernames=[dict(zh_name=row[0]) for row in cur_usernames]
        cur_versions=selectall('SELECT version FROM apicases WHERE activity="'+str(status)+'" group by version')
        versions=[dict(version=row[0]) for row in cur_versions]
        cur_models=selectall('SELECT model FROM apicases WHERE activity="'+str(status)+'" group by model')
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
            return redirect(url_for('apicases',category=category,value=changeWord(value),status=status,num='1'))
        if category == 'a.name':
            cur = selectall('SELECT a.id,a.type,a.version, a.model, a.product, a.name,a.pre_steps, a.steps, a.next_steps,a.description,a.exec_result, b.zh_name, a.create_date FROM apicases a inner join user b on a.username=b.username where activity="'+str(status)+'" and '+category+' like "%'+wordChange(value)+'%" order by a.id desc LIMIT '+str((num-1)*page_Count)+','+str(page_Count))
        else:
            cur = selectall('SELECT a.id,a.type,a.version, a.model, a.product, a.name,a.pre_steps, a.steps, a.next_steps,a.description,a.exec_result, b.zh_name, a.create_date FROM apicases a inner join user b on a.username=b.username where activity="'+str(status)+'" and '+category+'="'+wordChange(value)+'" order by a.id desc LIMIT '+str((num-1)*page_Count)+','+str(page_Count))
        cases = [dict(id=row[0], type=row[1], version=row[2], model=row[3], product=row[4], name=row[5], pre_steps=row[6], steps=row[7], next_steps=row[8], description=row[9], exec_result=row[10], zh_name=row[11], create_date=row[12]) for row in cur]
        return render_template('api/apicases.html',cases=cases, all_Page=all_Page,category=category,value=value,status=status,num=num,usernames=usernames,versions=versions,models=models,current='apicases'+str(status),error=error,pagename = '接口测试用例')

# 新建API用例
@app.route('/new_apicase/<int:status>', methods=['GET', 'POST'])
def new_apicase(status):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    elif get_auths_control(session['username'],'apicases','status',status,'1','1') == False:
        return render_template('invalid.html')
    cur = selectall('SELECT name,request FROM apiset')
    apisets = [dict(name=row[0],request=row[1]) for row in cur]
    error = None

    version = selectall('select version from versions')
    versions = [dict(version=row[0]) for row in version]
    versions = [version['version'] for version in versions]

    issuetype = selectall('select name from apicases where type="前置用例"')
    issuetypes = [dict(name=row[0]) for row in issuetype]

    for issuetype in issuetypes:
        if selectone('SELECT COUNT(1) FROM apidates a INNER JOIN apicases b ON a.case_name = b.name WHERE a.case_name = %s',[issuetype['name']])[0][0] == 0:
            issuetypes.remove(issuetype)

    nexttype = selectall('select name from apicases where type="后置用例"')
    nexttypes = [dict(name=row[0]) for row in nexttype]
    for nexttype in nexttypes:
        if selectone('SELECT COUNT(1) FROM apidates a INNER JOIN apicases b ON a.case_name = b.name WHERE a.case_name = %s',[nexttype['name']])[0][0] == 0:
            nexttypes.remove(nexttype)

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
                         [request.form['type'], request.form['version'], request.form['model'], request.form['product'], request.form['name'].strip(), request.form['pre-steps'], request.form['steps'], request.form['next-steps'], request.form['description'], '0', session['username'], time.strftime('%Y-%m-%d %X', time.localtime(time.time()))])

            cur_apicases_new= selectone("SELECT * FROM apicases WHERE name = %s",[request.form['name']])
            if cur_apicases_new != ():
                flash('创建成功...')
            else:
                flash('创建失败...')

            return redirect(url_for('apicases',category='a.username',value=session['username'],status=status,num=1))
    return render_template('api/new_apicase.html',apisets=apisets,versions=versions,issuetypes=issuetypes,nexttypes=nexttypes, current='apicases'+str(status),status=status,pagename = '新增用例',error=error)

# API用例查询后编辑
@app.route('/apidate_query/<case_name>/<name>', methods=['GET', 'POST'])
def apidate_query(case_name,name):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    error = None
    apidate_cur = selectone('select name,path,method,request,checks,parameter,description from apidates where case_name = %s and name=%s',[wordChange(case_name),name])
    print('apidate_cur',apidate_cur)

    if apidate_cur != ():
        cur = apidate_cur
    else:
        cur = selectone('select name,path,method,request,checks,parameter,description from apiset where name=%s',[new_name])
    cases = [dict(name=name, path=row[1], method=row[2], request=row[3], checks=row[4], parameter=row[5], description=row[6]) for row in cur]
    return render_template('api/apidate_query.html',case=cases[0],case_name=wordChange(case_name), name=name,pagename = '编辑接口数据')

# API用例查询后保存
@app.route('/apidate_save', methods=['GET', 'POST'])
def apidate_save():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    error = None
    if request.method == 'POST':
        if request.form['request'].strip() == '' or request.form['checks'].strip() == '':
            error = '必输项不能为空'
        elif is_dict(request.form['request'].strip()) == False:
            error = '请求格式不对'
        elif is_dict(request.form['checks'].strip()) == False:
            error = '检查项格式不对'
        elif request.form['parameter'].strip() != '' and is_list(request.form['parameter'].strip()) == False:
                error = '参数格式不对'
        else:
            addUpdateDel('update apidates set request = %s,checks = %s,parameter=%s,description=%s where case_name=%s and name=%s',[cn_to_uk(request.form['request']), cn_to_uk(request.form['checks']),cn_to_uk(request.form['parameter']), cn_to_uk(request.form['description']),request.form['case_name'],request.form['name']])

            cur_edit= selectone("SELECT request,checks,parameter FROM apidates where case_name=%s and name=%s and username=%s",[request.form['case_name'],request.form['name'],session['username']])
            apidates_edit = [dict(request=row[0],checks=row[1],parameter=row[2]) for row in cur_edit]
            apidates_request = apidates_edit[0]['request']
            apidates_checks = apidates_edit[0]['checks']
            apidates_parameter = apidates_edit[0]['parameter']
            if request.form['request'] == apidates_request and request.form['checks'] == apidates_checks and request.form['parameter'] == apidates_parameter:
                flash('编辑成功...')
            else:
                flash('编辑失败...')
            return redirect(url_for('apidate_query',case_name=request.form['case_name'],name=request.form['name']))

    return render_template('api/apidate_query.html',error=error,current='apicases', pagename = '编辑接口数据')

# API用例查询
@app.route('/apicase_query/<int:status>/<int:id>', methods=['GET', 'POST'])
def apicase_query(status,id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    elif get_auths_control(session['username'],'apicases','status',status,'operation','查看-query') == False:
        return render_template('invalid.html')
    else:
        cur = selectone('SELECT type,version, name, product, model, pre_steps, steps, next_steps, description FROM apicases where id=%s',[id])
        cases = [dict(type=row[0], version=row[1], name=row[2], product=row[3], model=row[4], pre_steps=row[5], steps=row[6], next_steps=row[7], description=row[8]) for row in cur]
        steps = cases[0]['steps'].split('\r\n')
        case_name = cases[0]['name']
        case_details = []
        for step in steps:
            cur = selectone('select name,path,method,request,checks,parameter from apidates where case_name=%s and name=%s',[case_name,step])
            if cur == ():
                continue
            case_detail = [dict(name=row[0], path=row[1], method=row[2], request=row[3], checks=row[4], parameter=row[5]) for row in cur]
            case_details.append(case_detail[0])
        return render_template('api/apicase_query.html',case_details=case_details, case=cases[0], pagename = '接口查看',current='apicases'+str(status),status=status)

# API用例查询-接口查询
@app.route('/apidate_apiquery/<case_name>/<name>', methods=['GET', 'POST'])
def apidate_apiquery(case_name,name):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    error = None
    apidate_cur = selectone('select name,path,method,request,checks,parameter,description from apidates where case_name = %s and name=%s and username=%s',[wordChange(case_name),name,session['username']])
    cases = [dict(name=name, path=row[1], method=row[2], request=row[3], checks=row[4], parameter=row[5], description=row[6]) for row in apidate_cur]
    return render_template('api/apidate_apiquery.html',case=cases[0],case_name=wordChange(case_name), name=name,pagename = '编辑接口数据')

# API用例删除
@app.route('/apicase_delete/<int:status>/<int:id>', methods=['GET', 'POST'])
def apicase_delete(status,id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    elif get_auths_control(session['username'],'apicases','status',status,'operation','删除-delete') == False:
        return render_template('invalid.html')
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
        elif activity('delete','apicases',id) not in activity_dict['delete']:
            flash('用例状态不允许执行该操作...')
        else:
            cur = addUpdateDel('update apicases set activity = "2" where id=%s and activity in ("0","1","3")',[id])

            cur_apicases_del= selectone("SELECT * FROM apicases where id=%s and activity ==2",[id])
            if cur_apicases_del != ():
                flash('删除成功...')
            else:
                flash('删除失败...')

        return redirect(url_for('apicases',category='a.username',value=session['username'],status=status,num=1))

# API用例执行
@app.route('/apicase_exec/<int:status>/<int:id>', methods=['GET', 'POST'])
def apicase_exec(status,id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    elif get_auths_control(session['username'],'apicases','status',status,'operation','执行-exec') == False:
        return render_template('invalid.html')

    count_dates = selectone('SELECT COUNT(1) FROM apicases a INNER JOIN apidates b ON a.name = b.case_name WHERE a.id = %s',[id])[0][0]
    if count_dates == 0:
        flash('未生成接口数据，不允许执行！')
        return redirect(url_for('apicases',category='a.username',value=session['username'],status=status,num=1))

    error = None
    newrun = RunTests(id,session['username'])
    res=newrun.getTestCases()

    return render_template('api/apicase_exec.html',res=res,pagename = '接口执行结果',current='apicases'+str(status))

# API用例驳回
@app.route('/apicase_reject/<int:status>/<int:id>', methods=['GET', 'POST'])
def apicase_reject(status,id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    elif get_auths_control(session['username'],'apicases','status',status,'operation','驳回-reject') == False:
        return render_template('invalid.html')
    elif activity('reject','apicases',id) not in activity_dict['reject']:
        flash('用例状态不允许执行该操作...')
    else:
        cur = addUpdateDel('update apicases set activity=0 where id=%s and activity in ("1","3")',[id])

        cur_apicases_reject= selectone("SELECT * FROM apicases where id=%s and activity=0",[id])
        if cur_apicases_reject != ():
            flash('驳回成功...')
        else:
            flash('驳回失败...')

    return redirect(url_for('apicases',category='a.username',value=session['username'],status=status,num=1))

# API用例编辑
@app.route('/apicase_edit/<int:status>/<int:id>', methods=['GET', 'POST'])
def apicase_edit(status,id):
    count_dates = selectone('SELECT COUNT(1) FROM apicases a INNER JOIN apidates b ON a.name = b.case_name WHERE a.id = %s',[id])[0][0]
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    elif get_auths_control(session['username'],'apicases','status',status,'operation','编辑-edit') == False:
        return render_template('invalid.html')
    elif count_dates != 0:
        flash('已生成接口数据，不允许编辑！')
        return redirect(url_for('apicases',category='a.username',value=session['username'],status=status,num=1))

    issuetype = selectall('select name from apicases where type="前置用例"')
    issuetypes = [dict(name=row[0]) for row in issuetype]

    nexttype = selectall('select name from apicases where type="后置用例"')
    nexttypes = [dict(name=row[0]) for row in nexttype]
        
    error = None
    cur = selectall('SELECT name,request FROM apiset')
    apisets = [dict(name=row[0],request=row[1]) for row in cur]
    cur = selectone('SELECT type, version, name, product, model, pre_steps, steps, next_steps,description FROM apicases where id=%s',[id])
    cases = [dict(type=row[0], version=row[1], name=row[2], product=row[3], model=row[4], pre_steps=row[5], steps=row[6], next_steps=row[7], description=row[8]) for row in cur]
    if request.method == 'POST':
        apiname = selectone('select name from apicases where name !=%s',[cases[0]['name']])
        apinames = [dict(name=row[0]) for row in apiname]
        apinames = [apiname['name'] for apiname in apinames]

        if request.form['name'].strip() == '':
            error = '必输项不能为空！'
        elif request.form['name'].strip() in apinames:
            error = "该用例已经存在！"
        elif request.form['type'].strip() in ('前置用例','后置用例'):
            addUpdateDel('update apicases set name=%s, steps=%s, description=%s where id=%s',[request.form['name'], request.form['steps'], request.form['description'],id])

            cur_edit= selectone("SELECT name,steps,description FROM apicases WHERE id = %s",[id])
            apicases_edit = [dict(name=row[0],steps=row[1],description=row[2]) for row in cur_edit]
            apicase_name = apicases_edit[0]['name']
            apicases_steps = apicases_edit[0]['steps']
            apicases_description = apicases_edit[0]['description']
            if request.form['name'] == apicase_name and request.form['steps'] == apicases_steps and request.form['description'] == apicases_description:
                flash('编辑成功...')
            else:
                flash('编辑失败...')

            return redirect(url_for('apicases',category='a.username',value=session['username'],status=status,num=1))
        else:
            addUpdateDel('update apicases set name = %s, pre_steps = %s, steps = %s, next_steps = %s, description = %s', [request.form['name'].strip(), request.form['pre-steps'], request.form['steps'], request.form['next-steps'], request.form['description']])

            cur_edit= selectone("SELECT name,pre_steps,steps,next_steps,description FROM apicases WHERE id = %s",[id])
            apicases_edit = [dict(name=row[0],pre_steps=row[1],steps=row[2],next_steps=row[3],description=row[4]) for row in cur_edit]
            apicase_name = apicases_edit[0]['name']
            apicase_pre_steps = apicases_edit[0]['pre_steps']
            apicases_steps = apicases_edit[0]['steps']
            apicase_next_steps = apicases_edit[0]['next_steps']
            apicases_description = apicases_edit[0]['description']
            if request.form['name'] == apicase_name and request.form['pre-steps'] == apicase_pre_steps and request.form['steps'] == apicases_steps and request.form['next-steps'] == apicase_next_steps and request.form['description'] == apicases_description:
                flash('编辑成功...')
            else:
                flash('编辑失败...')
            return redirect(url_for('apicases',category='a.username',value=session['username'],status=status,num=1))
    return render_template('api/apicase_edit.html',case=cases[0],current='apicases'+str(status),status=status,issuetypes=issuetypes, nexttypes=nexttypes,error=error,pagename = '接口编辑', id=id)

# API用例删除后恢复
@app.route('/apicase_restore/<int:status>/<int:id>', methods=['GET', 'POST'])
def apicase_restore(status,id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    elif get_auths_control(session['username'],'apicases','status',status,'operation','恢复-restore') == False:
        return render_template('invalid.html')
    elif activity('restore','apicases',id) not in activity_dict['restore']:
        flash('用例状态不允许执行该操作...')
    else:
        cur = addUpdateDel('update apicases set activity=0 where id=%s and activity=2',[id])

        cur_apicases_del= selectone("SELECT * FROM apicases where id=%s and activity=0",[id])
        if cur_apicases_del != ():
            flash('恢复成功...')
        else:
            flash('恢复失败...')

    return redirect(url_for('apicases',category='a.username',value=session['username'],status=status,num=1))

# API用例彻底删除
@app.route('/apicase_redelete/<int:status>/<int:id>', methods=['GET', 'POST'])
def apicase_redelete(status,id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    elif get_auths_control(session['username'],'apicases','status',status,'operation','删除-redelete') == False:
        return render_template('invalid.html')
    elif activity('redelete','apicases',id) not in activity_dict['redelete']:
        flash('用例状态不允许执行该操作...')
    else:
        apicase = selectone('select name from apicases where id=%s',[id])
        apicases = [dict(name=row[0]) for row in apicase]
        apicase_name = apicases[0]['name']
        
        addUpdateDel('delete from apicases where id=%s',[id])
        addUpdateDel('delete from apidates where case_name=%s',[apicase_name])

        cur_apidates_del= selectone("SELECT * FROM apidates where case_name=%s",[apicase_name])
        cur_apicases_del= selectone("SELECT * FROM apicases where id=%s",[id])
        if cur_apidates_del == () and cur_apidates_del == ():
            flash('删除成功...')
        else:
            flash('删除失败...')

    return redirect(url_for('apicases',category='a.username',value=session['username'],status=status,num=1))

# API用例提交
@app.route('/apicase_submit/<int:status>/<int:id>', methods=['GET', 'POST'])
def apicase_submit(status,id):
    count_dates = selectone('SELECT COUNT(1) FROM apicases a INNER JOIN apidates b ON a.name = b.case_name WHERE a.id = %s',[id])[0][0]
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    elif get_auths_control(session['username'],'apicases','status',status,'operation','提交-submit') == False:
        return render_template('invalid.html')
    elif activity('submit','apicases',id) not in activity_dict['submit']:
        flash('用例状态不允许执行该操作...')
    elif count_dates == 0:
        flash('未生成接口数据，不允许提交...')
        return redirect(url_for('apicases',category='a.username',value=session['username'],status=status,num=1))
    else:
        apicase = selectone('select name from apicases where id=%s',[id])
        apicases = [dict(name=row[0]) for row in apicase]
        apicase_name = apicases[0]['name']
        
        cur = addUpdateDel('update apicases set activity=1 where id=%s and activity=0',[id])

        cur_apicases_submint= selectone("SELECT * FROM apicases where id=%s and activity=1",[id])
        if cur_apicases_submint != ():
            flash('提交成功...')
        else:
            flash('提交失败...')

    return redirect(url_for('apicases',category='a.username',value=session['username'],status=status,num=1))

# API接口数据生成
@app.route('/apicase_makedate/<int:status>/<int:id>', methods=['GET', 'POST'])
def apicase_makedate(status,id):
    print('1')
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    elif get_auths_control(session['username'],'apicases','status',status,'operation','数据生成-makedate') == False:
        return render_template('invalid.html')
    elif activity('makedate','apicases',id) not in activity_dict['makedate']:
        flash('用例状态不允许执行该操作...')
        return redirect(url_for('apicases',category='a.username',value=session['username'],status=status,num=1))
    else:
        error = None
        cur = selectone('SELECT type, version, name, product, model, pre_steps, steps, next_steps,description FROM apicases where id=%s',[id])
        print(cur)
        case = [dict(type=row[0], version=row[1], name=row[2], product=row[3], model=row[4], pre_steps=row[5], steps=row[6], next_steps=row[7], description=row[8]) for row in cur]

        steps = selectone('SELECT steps FROM apicases WHERE id = %s',[id])[0][0].split('\r\n')
        steps_in_dates = selectone('SELECT count(1) FROM apidates a INNER JOIN apicases b ON a.case_name = b.name WHERE b.id = %s',[id])[0][0]
        if steps_in_dates == 0:
            for step in steps:
                new_step = step.split('-')[1]
                cur = selectone('select name,path,method,request,checks from apiset where name = %s',[new_step])
                api_cases = [dict(name=step, path=row[1], method=row[2], request=row[3], checks=row[4]) for row in cur]
                addUpdateDel('insert into apidates (case_name,name,path,method,request,checks,username,create_date) values (%s,%s,%s,%s,%s,%s,%s,%s)',[case[0]['name'], step, cn_to_uk(api_cases[0]['path']), api_cases[0]['method'], cn_to_uk(api_cases[0]['request']), cn_to_uk(api_cases[0]['checks']), session['username'], time.strftime('%Y-%m-%d %X', time.localtime(time.time()))])
                
    return render_template('api/apicase_makedate.html',case=case[0],current='apicases'+str(status),status=status,error=error,pagename = '数据生成', id=id)

###############################
#             UI封装
###############################
# UI封装
@app.route('/uiset/<keyword>/<value>/<int:num>', methods=['GET', 'POST'])
def uiset(keyword,value,num):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    elif get_auths_control(session['username'],'uiset','1','1','1','1') == False:
        return render_template('invalid.html')
    else:
        #value = value.replace('%27','\'').replace('%2C',',').replace('%29',')').replace('%28','(').replace('%7C','|')
        all_Count = selectall('SELECT count(1) FROM uiset a where '+keyword+' = "'+value+'"')[0][0]
        all_Page = math.ceil(all_Count/page_Count)
        uiset_list = selectall('select keyword from uiset')
        if request.method == 'POST':
            if request.form['select-interface'] != '':
                keyword = 'a.keyword'
                value = request.form['select-interface']
            else:
                keyword = '1'
                value = '1'
            return redirect(url_for('uiset',keyword=keyword,value=value,num=num))
        cur = selectall('SELECT a.id,a.keyword,a.description,a.template,a.example,b.zh_name,a.create_date FROM uiset a inner join user b on a.username=b.username where '+keyword+' = "'+value+'" order by a.id desc LIMIT '+str((num-1)*page_Count)+','+str(page_Count))
        uisets = [dict(id=row[0], keyword=row[1], description=row[2], template=row[3], example=row[4], username=row[5], create_date=row[6]) for row in cur]
        return render_template('set/uiset.html',uisets=uisets,all_Page=all_Page,keyword=keyword,value=value,num=num, current='uiset',uiset_list=uiset_list,pagename = 'UI封装')

# 新建UI封装
@app.route('/new_uiset', methods=['GET', 'POST'])
def new_uiset():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    elif get_auths_control(session['username'],'uiset','1','1','1','1') == False:
        return render_template('invalid.html')
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

            return redirect(url_for('uiset',keyword=1,value=1,num=1))
    return render_template('set/new_uiset.html',current='uiset', pagename = '新建UI封装',error=error)

# UI封装编辑
@app.route('/uiset_edit/<int:id>', methods=['GET', 'POST'])
def uiset_edit(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    elif get_auths_control(session['username'],'uiset','1','1','operation','编辑-edit') == False:
        return render_template('invalid.html')
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

                return redirect(url_for('uiset',keyword=1,value=1,num=1))
        return render_template('set/uiset_edit.html',case=cases[0],current='uiset', pagename = 'UI封装编辑',id=id)

# UI封装查询
@app.route('/uiset_query/<int:id>', methods=['GET', 'POST'])
def uiset_query(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    elif get_auths_control(session['username'],'uiset','1','1','operation','查看-query') == False:
        return render_template('invalid.html')
    else:
        cur = selectone('SELECT id,keyword,description,template,example FROM uiset where id=%s',[id])
        cases = [dict(id=row[0], keyword=row[1], description=row[2], template=row[3], example=row[4]) for row in cur]
        return render_template('set/uiset_query.html',case=cases[0],current='uiset', pagename = 'UI封装查看')

# UI封装删除
@app.route('/uiset_delete/<int:id>', methods=['GET', 'POST'])
def uiset_delete(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    elif get_auths_control(session['username'],'uiset','1','1','operation','删除-delete') == False:
        return render_template('invalid.html')
    else:
        addUpdateDel('delete from uiset where id=%s',[id])

        cur_uiset_del= selectone("SELECT * FROM uiset where id=%s",[id])
        if cur_uiset_del == ():
            flash('删除成功...')
        else:
            flash('删除失败...')

        return redirect(url_for('uiset',keyword=1,value=1,num=1))

###############################
#             接口
###############################
# 接口
@app.route('/apiset/<name>/<value>/<int:num>', methods=['GET', 'POST'])
def apiset(name,value,num):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    elif get_auths_control(session['username'],'apiset','1','1','1','1') == False:
        return render_template('invalid.html')
    else:
        all_Count = selectall('SELECT count(1) FROM apiset a where '+name+' = "'+value+'"')[0][0]
        all_Page = math.ceil(all_Count/page_Count)
        apiset_list = selectall('select name from apiset')
        if request.method == 'POST':
            if request.form['select-interface'] != '':
                name = 'a.name'
                value = request.form['select-interface']
            else:
                name = '1'
                value = '1'
            return redirect(url_for('apiset',name=name,value=value,num=num))
        cur = selectall('SELECT a.id,a.name,a.path,a.method,a.request,a.checks,a.description,b.zh_name,a.create_date FROM apiset a inner join user b on a.username=b.username where '+name+' = "'+value+'" order by a.id desc LIMIT '+str((num-1)*page_Count)+','+str(page_Count))
        apisets = [dict(id=row[0], name=row[1], path=row[2], method=row[3], request=row[4], checks=row[5], description=row[6], username=row[7], create_date=row[8]) for row in cur]
        return render_template('set/apiset.html',apisets=apisets,all_Page=all_Page,name=name,value=value, num=num, current='apiset',apiset_list=apiset_list,pagename = '全部接口')

# 新建接口
@app.route('/new_apiset', methods=['GET', 'POST'])
def new_apiset():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    elif get_auths_control(session['username'],'apiset','1','1','1','1') == False:
        return render_template('invalid.html')
    error = None
    if request.method == 'POST':
        apiset = selectall('select name from apiset')
        apisets = [dict(name=row[0]) for row in apiset]
        apisets = [apiset['name'] for apiset in apisets]

        if request.form['name'].strip() == '' or request.form['path'].strip == '' or request.form['method'].strip == '' or request.form['request'].strip == '':
            error = '必输项不能为空'
        elif request.form['name'].strip() in apisets:
            error = "该API已经存在"
        elif request.form['path'][0:7] not in ('http://','https:/'):
            error = '路径格式不对'
        elif is_dict(request.form['request'].strip()) == False:
            error = '请求项格式不对'
        elif request.form['checks'].strip() != '' and is_dict(request.form['checks'].strip()) == False:
            error = '检查项格式不对'
        else:
            addUpdateDel('insert into apiset (name, description, path, method, request, checks, username, create_date) values (%s, %s, %s, %s, %s, %s, %s, %s)',
                         [request.form['name'], request.form['description'], cn_to_uk(request.form['path']), request.form['method'], cn_to_uk(request.form['request']), cn_to_uk(request.form['checks']), session['username'], time.strftime('%Y-%m-%d %X', time.localtime(time.time()))])

            cur_new= selectone("SELECT * FROM apiset WHERE name = %s",[request.form['name']])
            if cur_new != ():
                flash('创建成功...')
            else:
                flash('创建失败...')

            return redirect(url_for('apiset',name=1,value=1,num=1))
    return render_template('set/new_apiset.html',pagename = '新增接口',error=error,current='apiset', methods=http_methods)

# 接口编辑
@app.route('/apiset_edit/<int:id>', methods=['GET', 'POST'])
def apiset_edit(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    elif get_auths_control(session['username'],'apiset','1','1','operation','编辑-edit') == False:
        return render_template('invalid.html')
    else:
        error=None
        cur = selectone('SELECT id,name,path,method,request,checks,description FROM apiset where id=%s',[id])
        cases = [dict(id=row[0], name=row[1], path=row[2], method=row[3], request=row[4], checks=row[5], description=row[6]) for row in cur]

        if request.method == 'POST':
            if request.form['path'].strip() == '' or request.form['request'].strip() == '':
                error = '必输项不能为空'
            elif request.form['path'][0:7] not in ('http://','https:/'):
                error = '路径格式不对'
            elif is_dict(request.form['request'].strip()) == False:
                error = '请求项格式不对'
            elif request.form['checks'].strip() != '' and is_dict(request.form['checks'].strip()) == False:
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

                return redirect(url_for('apiset',name=1,value=1,num=1))
        return render_template('set/apiset_edit.html',case=cases[0],error=error,current='apiset', pagename = '接口编辑', id=id)

# 接口查询
@app.route('/apiset_query/<int:id>', methods=['GET', 'POST'])
def apiset_query(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    elif get_auths_control(session['username'],'apiset','1','1','operation','查看-query') == False:
        return render_template('invalid.html')
    else:
        cur = selectone('SELECT id,name,path,method,request,checks,description FROM apiset where id=%s',[id])
        cases = [dict(id=row[0], name=row[1], path=row[2], method=row[3], request=row[4], checks=row[5], description=row[6]) for row in cur]
        return render_template('set/apiset_query.html',case=cases[0],current='apiset', pagename = '接口查看')

# 接口删除
@app.route('/apiset_delete/<int:id>', methods=['GET', 'POST'])
def apiset_delete(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    elif get_auths_control(session['username'],'apiset','1','1','operation','删除-delete') == False:
        return render_template('invalid.html')
    else:
        addUpdateDel('delete from apiset where id=%s',[id])

        cur_apiset_del= selectone("SELECT * FROM apiset where id=%s",[id])
        if cur_apiset_del == ():
            flash('删除成功...')
        else:
            flash('删除失败...')

        return redirect(url_for('apiset',name=1,value=1,num=1))

# 接口执行
@app.route('/apiset_exec/<int:id>', methods=['GET', 'POST'])
def apiset_exec(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    elif get_auths_control(session['username'],'apiset','1','1','operation','执行-exec') == False:
        return render_template('invalid.html')
    else:
        error = None
        newrun = RunTests(id,session['username'])
        res=newrun.getApis()
        flash('执行成功...')
        return render_template('set/apiset_exec.html',res=res, current="apiset", pagename = '接口执行结果')

##############################
#         版本
##############################
# 版本展示
@app.route('/versions/<version>/<value>/<int:num>', methods=['GET', 'POST'])
def versions(version,value,num):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    elif get_auths_control(session['username'],'versions','1','1','1','1') == False:
        return render_template('invalid.html')
    else:
        all_Count = selectall('SELECT count(1) FROM versions a where '+version+' = "'+value+'"')[0][0]
        all_Page = math.ceil(all_Count/page_Count)
        version_list = selectall('select version from versions')
        if request.method == 'POST':
            if request.form['select-version'] != '':
                version = 'a.version'
                value = request.form['select-version']
            else:
                version = '1'
                value = '1'
            return redirect(url_for('versions',version=version,value=value,num=num))
        cur = selectall('SELECT a.id,a.version,b.zh_name,a.create_date FROM versions a inner join user b on a.username=b.username where '+version+' = "'+value+'" order by a.id desc LIMIT '+str((num-1)*page_Count)+','+str(page_Count))
        versions = [dict(id=row[0], version=row[1], username=row[2], create_date=row[3]) for row in cur]
        return render_template('version/versions.html',versions=versions,version=version,value=value,num=num,version_list=version_list,all_Page=all_Page,current='versions', pagename = '版本号')

# 新建版本
@app.route('/new_version', methods=['GET', 'POST'])
def new_version():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    elif get_auths_control(session['username'],'versions','1','1','1','1') == False:
        return render_template('invalid.html')
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

            return redirect(url_for('versions',version=1,value=1,num=1))
    return render_template('version/new_version.html', pagename = '新增版本号',current='versions',error=error)

# 版本删除
@app.route('/version_delete/<int:id>', methods=['GET', 'POST'])
def version_delete(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    elif get_auths_control(session['username'],'versions','1','1','operation','删除-delete') == False:
        return render_template('invalid.html')
    else:
        cur = addUpdateDel('delete from versions where id=%s',[id])

        cur_versions_del= selectone("SELECT * FROM versions where id=%s",[id])
        if cur_versions_del == ():
            flash('删除成功...')
        else:
            flash('删除失败...')

        return redirect(url_for('versions',version=1,value=1,num=1))
###############################
#           审核
###############################
# UI用例审核
@app.route('/uicase_review/<int:status>/<int:id>', methods=['GET', 'POST'])
def uicase_review(status,id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    elif get_auths_control(session['username'],'uicases','status',status,'operation','审核-review') == False:
        return render_template('invalid.html')
    elif activity('review','uicases',id) not in activity_dict['review']:
        flash('用例状态不允许执行该操作...')
    else:
        cur = addUpdateDel('update uicases set activity="3" where id=%s and activity="1"',[id])

        cur_new= selectone("SELECT * FROM uicases WHERE id = %s and activity=3",[id])
        if cur_new != ():
            flash('审核成功...')
        else:
            flash('审核失败...')
    return redirect(url_for('uicases',category='a.username',value=session['username'],status=status,num=1))

# API用例审核
@app.route('/apicase_review/<int:status>/<int:id>', methods=['GET', 'POST'])
def apicase_review(status,id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    elif get_auths_control(session['username'],'apicases','status',status,'operation','审核-review') == False:
        return render_template('invalid.html')
    elif activity('review','apicases',id) not in activity_dict['review']:
        flash('用例状态不允许执行该操作...')
    else:
        cur = addUpdateDel('update apicases set activity="3" where id=%s and activity="1"',[id])

        cur_new= selectone("SELECT * FROM apicases WHERE id = %s and activity=3",[id])
        if cur_new != ():
            flash('审核成功...')
        else:
            flash('审核失败...')

    return redirect(url_for('apicases',category='a.username',value=session['username'],status=status,num=1))

##############################
#         管理员
##############################
# 重置密码
@app.route('/reset_passwd', methods=['GET', 'POST'])
def reset_passwd():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    elif get_auths_control(session['username'],'reset_passwd','1','1','1','1') == False:
        return render_template('invalid.html')
    try:
        error =None
        cur = selectall('select username from user')
        usernames = [dict(username=row[0]) for row in cur]

        if request.form['username'].strip() == '' or request.form['pw_new_o'].strip() == '' or request.form['pw_new_t'].strip() == '':
            error = '必输项不能为空'
        elif request.form['pw_new_o'].strip() != request.form['pw_new_t'].strip():
            error = '两次密码输入不一致'
        else:
            addUpdateDel('update user set password = %s where username = %s',[encrypt(request.form['pw_new_o']),request.form['username']])
            flash("重置密码成功...")
    except Exception as e:
        error = str(err)
    finally:
        return render_template('admin/reset_passwd.html',usernames=usernames,current="reset_passwd", error=error, pagename = '重置密码')

# 用户注册页面
@app.route('/register', methods=['GET', 'POST'])
def register():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    elif get_auths_control(session['username'],'register','1','1','1','1') == False:
        return render_template('invalid.html')
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
        return render_template('admin/register.html', error=error,current="register", pagename = '注册')

# 页面权限
@app.route('/page_auth', methods=['GET', 'POST'])
def page_auth():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    elif get_auths_control(session['username'],'page_auth','1','1','1','1') == False:
        return render_template('invalid.html')
    error = None
    if request.method == 'POST':
        if request.form['select-page'].strip() == '':
            error = '授权页面不能为空'
        else:
            temp = request.form['select-page'].split('-')
            addUpdateDel('update auth set auth=%s where type=%s and name=%s',[request.form['auth'][:-1],temp[0],temp[1]])
            flash('权限更新成功...')
    page_auths = selectall("SELECT TYPE,NAME,auth FROM auth")
    return render_template('admin/page_auth.html', error=error,page_auths=page_auths,current='page_auth', pagename = '页面权限设置')

# 页面操作权限
@app.route('/opera_auth', methods=['GET', 'POST'])
def opera_auth():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    elif get_auths_control(session['username'],'opera_auth','1','1','1','1') == False:
        return render_template('invalid.html')
    error = None
    if request.method == 'POST':
        if request.form['select-page'].strip() == '':
            error = '授权页面不能为空'
        else:
            temp = request.form['select-page'].split('-')
            addUpdateDel('update auth set operation=%s where type=%s and name=%s',[request.form['auth'][:-1],temp[0],temp[1]])
            flash('权限更新成功...')
    opera_auths = selectall("SELECT TYPE,NAME,operation FROM auth")
    return render_template('admin/opera_auth.html', error=error,opera_auths=opera_auths, current='opera_auth',pagename = '操作权限设置')

# 用户权限
@app.route('/user_auth', methods=['GET', 'POST'])
def user_auth():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    elif get_auths_control(session['username'],'user_auth','1','1','1','1') == False:
        return render_template('invalid.html')
    error = None
    if request.method == 'POST':
        if request.form['select-user'].strip() == '':
            error = '用户名不能为空'
        else:
            addUpdateDel('update user set auth=%s where zh_name=%s',[request.form['auth'][:-1],request.form['select-user']])
            flash('权限更新成功...')
    user_auths = selectall("SELECT username,zh_name,auth FROM user")
    return render_template('admin/user_auth.html', error=error,user_auths=user_auths,current='user_auth', pagename = '用户权限设置')

if __name__ == '__main__':
    app.run()
    #app.run(host='192.168.213.110',port=8000)