#coding=utf-8

import os
import jinja2
import time

jinja_environment = jinja2.Environment(autoescape=True,
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), '../templates')))

# 生成测试报告
def report(content,path):
    report_date = time.strftime("%Y_%m_%d_%H_%M_%S")
    template = jinja_environment.get_template('report.html')
    if not os.path.exists(path+"/"):
        os.makedirs(path+"/")
    f = open(path+"/report_"+report_date+".html", "w",encoding="utf-8")
    f.write(template.render(content=content))
    f.close()