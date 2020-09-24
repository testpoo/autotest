#!/usr/local/python  
# coding=UTF-8 

from datetime import datetime

#change time to str
def getCurrentTime():
    #format = "%a %b %d %H:%M:%S %Y"
    format = "%Y-%m-%d %H:%M:%S"
    return datetime.now().strftime(format)

# Get time diff
def timeDiff(starttime,endtime):
    #format = "%a %b %d %H:%M:%S %Y"
    format = "%Y-%m-%d %H:%M:%S"
    return datetime.strptime(endtime,format) - datetime.strptime(starttime,format)