# coding=UTF-8 

import smtplib
import os
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE,formatdate
from datetime import datetime

from Common import Report,GetFileName


def sendEmail(send_from,send_to,subject,text,files=None,server=None,username=None,password=None):

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = send_to
    msg['Date'] = formatdate(localtime = True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text,'html'))

    with open(files,"rb") as f:
        part = MIMEApplication(f.read(),Name=basename(files))
        msg.attach(part)
    smtp = smtplib.SMTP()
    smtp.connect(server)
    smtp.login(username,password)
    smtp.sendmail(send_from,send_to,msg.as_string())
    smtp.quit()

def sendReport():
    send_f = "xxxx@xxxx.com.cn"
    send_t = "xxxx@xxxx.com.cn"

    server = "smtp.xxxx.com"
    username="xxxx@xxxx.com.cn"
    password="xxxxxxxx"
    
    subject = "[自动化测试结果]TestReport_"+str(datetime.today())
    
    files = "TestResult\\"+GetFileName.getFilename(os.path.dirname(os.getcwd()),".log")+".html" 
    with open(files,'r',encoding='utf-8') as f:
        text = f.read()

    sendEmail(send_f,send_t,subject,text,files,server,username,password)