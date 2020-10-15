### autotest
接口UI自动化合一框架

### 依赖
- Python    3.8.5
- Flask     1.1.2
- PyMySQL   0.10.1
- requests  2.24.0
- selenium  3.141.0

### 安装
- 安装依赖
- 执行初始化脚本init.sql

### 修改参数
- 修改Common/Config中的SITEURL和dblink,SITEURL为主页地址，dblink为数据库链接
- 修改autotest最后一行app.run()为自己对应的ip和端口

### 启动
- 执行autotest.py
