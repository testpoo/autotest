CREATE TABLE IF NOT EXISTS `apicases` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `type` varchar(50) DEFAULT NULL,
  `version` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `product` varchar(255) NOT NULL,
  `model` varchar(255) NOT NULL,
  `pre_steps` varchar(2550) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '',
  `steps` varchar(2550) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '',
  `next_steps` varchar(2550) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '',
  `activity` int(11) NOT NULL,
  `exec_result` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '',
  `description` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '',
  `username` varchar(255) NOT NULL,
  `create_date` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=112 DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `apidates` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `case_name` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `path` varchar(255) NOT NULL,
  `method` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `request` varchar(2550) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '',
  `checks` varchar(2550) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '',
  `parameter` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '',
  `description` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '',
  `username` varchar(255) NOT NULL,
  `create_date` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`case_name`,`name`)
) ENGINE=InnoDB AUTO_INCREMENT=182 DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `apiset` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `path` varchar(255) NOT NULL,
  `method` varchar(255) NOT NULL,
  `request` varchar(255) NOT NULL,
  `checks` varchar(2550) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '',
  `description` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '',
  `username` varchar(255) NOT NULL,
  `create_date` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `apisitues` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `exec_mode` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `steps` varchar(2550) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '',
  `activity` int(11) DEFAULT NULL,
  `description` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '',
  `username` varchar(255) NOT NULL,
  `create_date` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `auth` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `type` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `order` int(11) DEFAULT NULL,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `url` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `status` int(11) NOT NULL,
  `auth` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `operation` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`type`,`name`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `report` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `case_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `type` varchar(50) NOT NULL,
  `product` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `status` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `Screenshot` longtext CHARACTER SET utf8 COLLATE utf8_general_ci,
  `spenttime` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `error` varchar(1200) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `username` varchar(50) NOT NULL,
  `create_date` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=10419 DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `uicases` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `type` varchar(50) DEFAULT NULL,
  `version` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `model` varchar(255) NOT NULL,
  `product` varchar(255) NOT NULL,
  `pre_steps` varchar(2550) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '',
  `steps` varchar(12500) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '0',
  `next_steps` varchar(2550) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '',
  `description` varchar(2550) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '',
  `activity` int(11) NOT NULL,
  `exec_result` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '',
  `username` varchar(255) NOT NULL,
  `create_date` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=1886 DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `uiset` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `keyword` varchar(255) NOT NULL,
  `template` varchar(255) NOT NULL,
  `example` varchar(255) NOT NULL,
  `description` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '',
  `username` varchar(255) NOT NULL,
  `create_date` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `keyword` (`keyword`)
) ENGINE=InnoDB AUTO_INCREMENT=85 DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `uisitues` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `exec_mode` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `steps` varchar(20000) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '0',
  `activity` int(11) DEFAULT NULL,
  `description` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '',
  `username` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `create_date` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `name` (`name`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=109 DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `user` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `last_login` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '',
  `email` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '',
  `zh_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '',
  `auth` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '',
  `create_date` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `versions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `version` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `username` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `create_date` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `version` (`version`)
) ENGINE=InnoDB AUTO_INCREMENT=159 DEFAULT CHARSET=utf8;

INSERT INTO `user` (`username`, `password`, `last_login`, `email`, `zh_name`, `auth`, `create_date`) VALUES ('admin', 'MQ==', '2021-01-11 14:59:34', 'admin@suninfo.com', '管理员', '管理', '2020-09-18 17:15:44');

INSERT INTO `uiset` (`keyword`, `template`, `example`, `description`, `username`, `create_date`) VALUES ('前往|(\'test_keywordurl\')', 'open', '前往|(\'https://www.baidu.com\')', '前往：打开指定URL网页', 'lvhao', '2020-09-23 15:35:37');
INSERT INTO `uiset` (`keyword`, `template`, `example`, `description`, `username`, `create_date`) VALUES ('最大化|()', 'maximizeWindow', '最大化|()', '最大化：窗口最大化', 'lvhao', '2020-09-23 15:35:37');
INSERT INTO `uiset` (`keyword`, `template`, `example`, `description`, `username`, `create_date`) VALUES ('填写|(\'元素\',\'值\',\'文本\')', 'type', '填写|(\'id\',\'kw\',\'selenium\')', '元素：\'id\'、\'name\'、\'link_text\'、class\'、\'css\'、\'xpath\'\'、\'tag_name\'\r\n值：定位元素对应的值\r\n文本：需要输入的文本信息', 'lvhao', '2020-09-23 15:35:37');
INSERT INTO `uiset` (`keyword`, `template`, `example`, `description`, `username`, `create_date`) VALUES ('点击|(\'元素\',\'值\')', 'click', '点击|(\'id\',\'su\')', '元素：\'id\'、\'name\'、\'link_text\'、class\'、\'css\'、\'xpath\'\'、\'tag_name\'', 'lvhao', '2020-09-23 15:35:37');
INSERT INTO `uiset` (`keyword`, `template`, `example`, `description`, `username`, `create_date`) VALUES ('清除|(\'元素\',\'值\')', 'clear', '清除|(\'id\',\'kw\')', '元素：\'id\'、\'name\'、\'link_text\'、class\'、\'css\'、\'xpath\'\'、\'tag_name\'', 'lvhao', '2020-09-23 15:35:37');
INSERT INTO `uiset` (`keyword`, `template`, `example`, `description`, `username`, `create_date`) VALUES ('验证标题|(\'文本\')', 'assertTitle', '验证标题|(\'首页-上讯信息\')', '文本：需要验证的文本信息', 'lvhao', '2020-09-23 15:35:37');
INSERT INTO `uiset` (`keyword`, `template`, `example`, `description`, `username`, `create_date`) VALUES ('隐式等待|(time)', 'implicitlyWwait', '隐式等待|(20)', 'time：时间(s)', 'lvhao', '2020-09-23 15:35:37');
INSERT INTO `uiset` (`keyword`, `template`, `example`, `description`, `username`, `create_date`) VALUES ('标题|()', 'getTitle', '标题|()', '', 'lvhao', '2020-09-23 15:35:37');
INSERT INTO `uiset` (`keyword`, `template`, `example`, `description`, `username`, `create_date`) VALUES ('等待|(time)', 'wait', '等待|(5)', 'time：时间(s)', 'lvhao', '2020-09-23 15:35:37');
INSERT INTO `uiset` (`keyword`, `template`, `example`, `description`, `username`, `create_date`) VALUES ('验证文本|(\'元素\',\'值\',\'文本\')', 'assertText', '验证文本|(\'class\',\'nums_text\',\'百度为您找到\')', '元素：\'id\'、\'name\'、\'link_text\'、class\'、\'css\'、\'xpath\'\'、\'tag_name\'\r\n值：定位元素对应的值\r\n文本：需要验证的文本信息', 'lvhao', '2020-09-23 15:35:37');
INSERT INTO `uiset` (`keyword`, `template`, `example`, `description`, `username`, `create_date`) VALUES ('截图|(\'路径\')', 'getScreenshot', '截图|(\'D://baidu.png\')', '路径：存放截图的绝对路径；执行失败时会自动截图保存autotest\\static\\Screenshot路径下', 'lvhao', '2020-09-23 15:35:37');
INSERT INTO `uiset` (`keyword`, `template`, `example`, `description`, `username`, `create_date`) VALUES ('前进|()', 'forward', '前进|()', '', 'lvhao', '2020-09-23 15:35:37');
INSERT INTO `uiset` (`keyword`, `template`, `example`, `description`, `username`, `create_date`) VALUES ('后退|()', 'back', '后退|()', '', 'lvhao', '2020-09-23 15:35:37');
INSERT INTO `uiset` (`keyword`, `template`, `example`, `description`, `username`, `create_date`) VALUES ('切换frame|(\'元素\',\'值\')', 'switchToFrame', '切换frame|(\'id\',\'login_frame\')', '元素：\'id\'、\'name\'、\'link_text\'、class\'、\'css\'、\'xpath\'\'、\'tag_name\'', 'lvhao', '2020-09-23 15:35:37');
INSERT INTO `uiset` (`keyword`, `template`, `example`, `description`, `username`, `create_date`) VALUES ('返回主frame|()', 'switchToOuterFrame', '返回主frame|()', '', 'lvhao', '2020-09-23 15:35:37');
INSERT INTO `uiset` (`keyword`, `template`, `example`, `description`, `username`, `create_date`) VALUES ('切换到弹窗|()', 'switchToAlert', '切换到弹窗|()', '', 'lvhao', '2020-09-23 15:35:37');
INSERT INTO `uiset` (`keyword`, `template`, `example`, `description`, `username`, `create_date`) VALUES ('弹窗填写|(‘文本’)', 'tpyeAlert', '弹窗填写|(‘人员管理’)', '文本：需要填写的文本信息', 'lvhao', '2020-09-23 15:35:37');
INSERT INTO `uiset` (`keyword`, `template`, `example`, `description`, `username`, `create_date`) VALUES ('验证弹窗文本|(\'文本\')', 'assertTextAlert', '验证弹窗文本|(\'保存成功\')', '文本：需要验证的文本信息', 'lvhao', '2020-09-23 15:35:37');
INSERT INTO `uiset` (`keyword`, `template`, `example`, `description`, `username`, `create_date`) VALUES ('弹窗确认|()', 'acceptAlert', '弹窗确认|()', '', 'lvhao', '2020-09-23 15:35:37');
INSERT INTO `uiset` (`keyword`, `template`, `example`, `description`, `username`, `create_date`) VALUES ('设置窗口大小|(宽,高)', 'setWindowSize', '设置窗口大小|(800,500)', '', 'lvhao', '2020-09-23 15:35:37');
INSERT INTO `uiset` (`keyword`, `template`, `example`, `description`, `username`, `create_date`) VALUES ('提交表单|(\'元素\',\'值\')', 'submit', '提交表单|(\'xpath\',\'//*[@id="role_search_id"]\')', '', 'lvhao', '2020-09-23 15:35:37');
INSERT INTO `uiset` (`keyword`, `template`, `example`, `description`, `username`, `create_date`) VALUES ('刷新|()', 'refresh', '刷新|()', '', 'lvhao', '2020-09-23 15:35:37');
INSERT INTO `uiset` (`keyword`, `template`, `example`, `description`, `username`, `create_date`) VALUES ('下拉框|(\'元素\',\'值\',\'文本\')', 'findSelect', '下拉框|(\'name\',\'user_gender\',\'男\')', '元素：\'id\'、\'name\'、\'link_text\'、class\'、\'css\'、\'xpath\'\'、\'tag_name\'\r\n值：定位元素对应的值\r\n文本：需要选择的文本信息', 'lvhao', '2020-09-23 15:35:37');
INSERT INTO `uiset` (`keyword`, `template`, `example`, `description`, `username`, `create_date`) VALUES ('上传|(\'元素\',\'值\',\'路径\')', 'uploadFile', '上传|(\'id\',\'fileupload\',\'C:\\\\Users\\\\dell\\\\Desktop\\\\DepartList_2020_10_10_093508.xls\')', '元素：\'id\'、\'name\'、\'link_text\'、class\'、\'css\'、\'xpath\'\'、\'tag_name\'\r\n值：定位元素对应的值\r\n路径：文件的绝对路径；格式：‘C:\\\\*\\\\*’', 'lvhao', '2020-09-23 15:35:37');
INSERT INTO `uiset` (`keyword`, `template`, `example`, `description`, `username`, `create_date`) VALUES ('回车|(\'元素\',\'值\')', 'enter', '回车|(\'id\',\'submit_btn\')', '回车按键\r\n元素：\'id\'、\'name\'、\'link_text\'、class\'、\'css\'、\'xpath\'\'、\'tag_name\'\r\n值：定位元素对应的值', 'lvhao', '2020-09-23 15:35:37');
INSERT INTO `uiset` (`keyword`, `template`, `example`, `description`, `username`, `create_date`) VALUES ('TABLE|(\'元素\',\'值\')', 'table', 'TABLE|(\'id\',\'username\')', '制表按键\r\n元素：\'id\'、\'name\'、\'link_text\'、class\'、\'css\'、\'xpath\'\'、\'tag_name\'\r\n值：定位元素对应的值', 'lvhao', '2020-09-23 15:35:37');
INSERT INTO `uiset` (`keyword`, `template`, `example`, `description`, `username`, `create_date`) VALUES ('验证属性|(\'元素\',\'值\',\'属性\',\'文本\')', 'assertAttribute', '验证属性(\'id\', \'login_name\', \'value\',\'口令认证\')', '元素：\'id\'、\'name\'、\'link_text\'、class\'、\'css\'、\'xpath\'\'、\'tag_name\'\r\n值：定位元素对应的值\r\n属性：‘value’,\'class\'等\r\n文本：需要验证的文本信息', 'lvhao', '2020-09-23 15:35:37');
INSERT INTO `uiset` (`keyword`, `template`, `example`, `description`, `username`, `create_date`) VALUES ('验证下拉框文本|(\'元素\',\'值\',\'文本\')', 'assertSelectOptions', '验证下拉框文本|(\'name\', \'user_gender\',\'保密,男,女\')', '描述：验证下拉框所有选项;\r\n元素：\'id\'、\'name\'、\'link_text\'、class\'、\'css\'、\'xpath\'\'、\'tag_name\';\r\n值：定位元素对应的值;\r\n文本：需要输入下拉框所有文本', 'lvhao', '2020-09-23 15:35:37');
INSERT INTO `uiset` (`keyword`, `template`, `example`, `description`, `username`, `create_date`) VALUES ('返回上层frame|()', 'switchToParentFrame', '返回上层frame|()', '返回上层frame，如果当前已是主文档，则无效果', 'wangting', '2020-10-15 20:44:40');
INSERT INTO `uiset` (`keyword`, `template`, `example`, `description`, `username`, `create_date`) VALUES ('勾选|(\'元素\',\'值\')', 'checkOne', '勾选|(\'id\',\'is_om_log\')', '勾选操作：未勾选的选项勾选;\r\n元素：\'id\'、\'name\'、\'link_text\'、class\'、\'css\'、\'xpath\'\'、\'tag_name\';\r\n值：定位元素对应的值', 'wangting', '2020-10-15 20:44:40');
INSERT INTO `uiset` (`keyword`, `template`, `example`, `description`, `username`, `create_date`) VALUES ('取消勾选|(\'元素\',\'值\')', 'decheckOne', '取消勾选|(\'id\',\'is_om_log\')', '取消勾选操作：勾选的选项去勾选;\r\n元素：\'id\'、\'name\'、\'link_text\'、class\'、\'css\'、\'xpath\'\'、\'tag_name\';\r\n值：定位元素对应的值', 'wangting', '2020-10-15 20:44:40');
INSERT INTO `uiset` (`keyword`, `template`, `example`, `description`, `username`, `create_date`) VALUES ('勾选全部|(\'元素\',\'值\')', 'checkAll', '勾选全部|(\'id\',\'is_om_log\')', '勾选全部操作：未勾选选项全部勾选;\r\n元素：\'id\'、\'name\'、\'link_text\'、class\'、\'css\'、\'xpath\'\'、\'tag_name\';\r\n值：定位元素对应的值', 'wangting', '2020-10-15 20:44:40');
INSERT INTO `uiset` (`keyword`, `template`, `example`, `description`, `username`, `create_date`) VALUES ('取消全部勾选|(\'元素\',\'值\')', 'decheckAll', '取消勾选全部|(\'id\',\'is_om_log\')', '取消全部勾选操作：勾选的选项全部取消勾选;\r\n元素：\'id\'、\'name\'、\'link_text\'、class\'、\'css\'、\'xpath\'\'、\'tag_name\';\r\n值：定位元素对应的值', 'wangting', '2020-10-15 20:44:40');
INSERT INTO `uiset` (`keyword`, `template`, `example`, `description`, `username`, `create_date`) VALUES ('验证下拉框已选项|(\'元素\',\'值\',\'文本\')', 'assertSelectedOptions', '验证下拉框已选项|(\'name\', \'user_gender\',\'保密\')', '描述：验证下拉框所有已选择选项;\r\n元素：\'id\'、\'name\'、\'link_text\'、class\'、\'css\'、\'xpath\'\'、\'tag_name\';\r\n值：定位元素对应的值;\r\n文本：需要验证的所有已选下拉框文本', 'lvhao', '2020-09-23 15:35:37');
INSERT INTO `uiset` (`keyword`, `template`, `example`, `description`, `username`, `create_date`) VALUES ('表格点击|(\'元素\',\'值\',\'列号\',\'文本\',\'属性值\')', 'tableClick', '表格点击|(\'id\',\'archive_log_tb\',\'3\',\'all\',\'编辑\')', '元素：\'id\'、\'name\'、\'link_text\'、class\'、\'css\'、\'xpath\'\'、\'tag_name\'\r\n值：定位元素对应的值，用来定位到表格；\r\n列号：用来匹配文本的列号，xpath定位信息显示的列号\r\n文本：被匹配的文本\r\n属性：表格操作列对象的title属性值', 'lvhao', '2020-09-23 15:35:37');
INSERT INTO `uiset` (`keyword`, `template`, `example`, `description`, `username`, `create_date`) VALUES ('清空填写|(\'元素\',\'值\',\'文本\')', 'clearType', '清空填写|(\'id\',\'kw\',\'selenium\')', '元素：\'id\'、\'name\'、\'link_text\'、class\'、\'css\'、\'xpath\'\'、\'tag_name\'\r\n值：定位元素对应的值\r\n文本：需要输入的文本信息', 'lvhao', '2020-09-23 15:35:37');
INSERT INTO `uiset` (`keyword`, `template`, `example`, `description`, `username`, `create_date`) VALUES ('验证表格操作|(\'元素\',\'值\',\'列号\',\'文本\',\'属性值\')', 'assertTableOp', '验证表格操作|(\'xpath\', \'//*[@id="role_search_id"]\', \'3\', \'AIOPS\',\'编辑,部门成员,查看设备\')', '元素：\'id\'、\'name\'、\'link_text\'、class\'、\'css\'、\'xpath\'\'、\'tag_name\'\r\n值：定位元素对应的值，用来定位到表格；\r\n列号：用来匹配文本的列号，xpath定位信息显示的列号\r\n文本：被匹配的文本\r\n属性：title属性值', 'lvhao', '2020-09-23 15:35:37');
INSERT INTO `uiset` (`keyword`, `template`, `example`, `description`, `username`, `create_date`) VALUES ('验证文本集|(\'元素\',\'值\',\'文本\',\'布尔值\')', 'assertTexts', '验证文本集|(\'xpath\',\'/html/body/div[2]/div[1]/div[2]/div/div/div[4]/ul/li/a\',\'AD域设置,动态口令牌设置,登录属性设置\',\'True\')', '元素：\'id\'、\'name\'、\'link_text\'、class\'、\'css\'、\'xpath\'\'、\'tag_name\'\r\n值：定位元素集对应的值；\r\n文本：要验证的文本\r\n布尔值：默认为\'False\'无序验证，可不填此参数；为\'True\'时有序验证，需填上参数\'True\'\r\n', 'lvhao', '2020-09-23 15:35:37');
INSERT INTO `uiset` (`keyword`, `template`, `example`, `description`, `username`, `create_date`) VALUES ('验证元素勾选|(\'元素\',\'值\',\'布尔值\')', 'assertChecked', '验证元素勾选|(\'xpath\', \'//*[@id="code_form"]/div/table/tbody/tr/td[2]/input[1]\',’False‘)', '描述：验证元素勾选；\r\n参数：默认为\'True\'，验证被勾选；为\'False\'时，验证未被勾选', 'lvhao', '2020-09-23 15:35:37');
INSERT INTO `uiset` (`keyword`, `template`, `example`, `description`, `username`, `create_date`) VALUES ('弹窗取消|()', 'dismissAlert', '弹窗取消|()', '', 'lvhao', '2020-09-23 15:35:37');
INSERT INTO `uiset` (`keyword`, `template`, `example`, `description`, `username`, `create_date`) VALUES ('表格点击操作|(\'元素\',\'值\',\'匹配项\',\'列号\',\'文本\')', 'tableOperate', '表格点击操作|(\'xpath\',\'//*[@id="user_list_cont"]\',\'2,内置-运维人员,3,yunwei\',\'4\',\'AIOPS\')', '元素：\'id\'、\'name\'、\'link_text\'、class\'、\'css\'、\'xpath\'\'、\'tag_name\'；\r\n值：定位元素对应的值，用来定位到表格；\r\n匹配项：列号+文本匹配到指定行，可通过多列匹配，格式：1,\'a\',4,\'b\'；\r\n列号：目标列号，注意列号为1时，表示勾选项，不需要输入文本\r\n文本：目标元素的文本。', 'lvhao', '2020-11-03 18:42:55');
INSERT INTO `uiset` (`keyword`, `template`, `example`, `description`, `username`, `create_date`) VALUES ('验证表格文本|(\'元素\',\'值\',\'匹配项\',\'列号\',\'文本\')', 'assertTableText', '验证表格文本|(\'xpath\',\'//*[@id="user_list_cont"]\',\'2,内置-运维人员,3,yunwei\',\'4\',\'AIOPS\')', '元素：\'id\'、\'name\'、\'link_text\'、class\'、\'css\'、\'xpath\'\'、\'tag_name\'；\r\n值：定位元素对应的值，用来定位到表格；\r\n匹配项：列号+文本匹配到指定行，可通过多列匹配，格式：1,a,3,c；\r\n列号：目标元素所在列号；\r\n文本：待验证单元格文本', 'lvhao', '2020-11-09 15:37:23');
INSERT INTO `uiset` (`keyword`, `template`, `example`, `description`, `username`, `create_date`) VALUES ('验证表格属性|(\'元素\',\'值\',\'匹配项\',\'列号\',\'属性值\')', 'assertTableAttribute', '验证表格属性|(\'xpath\',\'//*[@id="user_list_cont"]\',\'3,内置-linux\',\'8\',\'22,23,23,22,22,5901,5901,177\')', '元素：\'id\'、\'name\'、\'link_text\'、class\'、\'css\'、\'xpath\'\'、\'tag_name\'；\r\n值：定位元素对应的值，用来定位到表格；\r\n匹配项：列号+文本匹配到指定行，可通过一列或者多列匹配，格式：1,a,4,c；\r\n列号：目标元素所在列号；\r\n文本：待验证单元格title属性的值', 'lvhao', '2020-11-09 15:37:23');
INSERT INTO `uiset` (`keyword`, `template`, `example`, `description`, `username`, `create_date`) VALUES ('切换窗口|(\'窗口序号\')', 'switchToWindow', '切换窗口|(\'1\')', '窗口序号:1,2,3....;分别对应第1,2,3...个打开的窗口', 'lvhao', '2020-11-09 15:37:23');
INSERT INTO `uiset` (`keyword`, `template`, `example`, `description`, `username`, `create_date`) VALUES ('验证文本存在|(\'元素\',\'值\',\'布尔值\')', 'assertTextExist', '验证文本存在|(\'xpath\',\'//*[@id="login"]/div[7]/a\',\'False\')', '元素：\'id\'、\'name\'、\'link_text\'、class\'、\'css\'、\'xpath\'\'、\'tag_name\'\r\n值：定位元素对应的值\r\n布尔值：默认为\'True\',验证元素对象的文本为空；为\'False\'时验证元素对象不为空', 'lvhao', '2020-11-12 13:58:23');
INSERT INTO `uiset` (`keyword`, `template`, `example`, `description`, `username`, `create_date`) VALUES ('删除|(\'元素\',\'值\')', 'backSpace', '删除|(\'class\',\'input\')', '删除按键\r\n元素：\'id\'、\'name\'、\'link_text\'、class\'、\'css\'、\'xpath\'\'、\'tag_name\'\r\n值：定位元素对应的值', 'lvhao', '2020-11-12 13:58:23');
INSERT INTO `uiset` (`keyword`, `template`, `example`, `description`, `username`, `create_date`) VALUES ('滚动条|(\'左边距\',\'上边距\')', 'scrollBar', '滚动条|(\'300\',\'500\')', '滑动WINDOWS滚动条；待优化页面嵌套div滚动条、表格滚动条', 'lvhao', '2020-11-12 13:58:23');
INSERT INTO `uiset` (`keyword`, `template`, `example`, `description`, `username`, `create_date`) VALUES ('元素聚焦|(\'元素\',\'值\')', 'focus', '元素聚焦|(\'id\',\'username\')', '设置元素焦点', 'lvhao', '2020-11-12 13:58:23');
INSERT INTO `uiset` (`keyword`, `template`, `example`, `description`, `username`, `create_date`) VALUES ('验证表格勾选|(\'元素\',\'值\',\'匹配项\',\'列号\',\'布尔值\')', 'assertTableChecked', '验证表格勾选|(\'xpath\',\'//*[@id="user_list_cont"]\',\'2,内置-运维人员,3,yunwei\',\'1\',)', '元素：\'id\'、\'name\'、\'link_text\'、class\'、\'css\'、\'xpath\'\'、\'tag_name\'；\r\n值：定位元素对应的值，用来定位到表格；\r\n匹配项：列号+文本匹配到指定行，可通过多列匹配，格式：1,a,3,c；\r\n列号：目标元素所在列号\r\n布尔值：默认为\'True\'，验证被勾选；为\'False\'时，验证未被勾选', 'lvhao', '2020-11-12 13:58:23');
INSERT INTO `uiset` (`keyword`, `template`, `example`, `description`, `username`, `create_date`) VALUES ('表格勾选|(\'元素\',\'值\',\'匹配项\',\'列号\',\'布尔值\')', 'tableCheck', '表格勾选|(\'xpath\',\'//*[@id="user_list_cont"]\',\'2,内置-运维人员,3,yunwei\',\'1\',\'Fasle\')', '元素：\'id\'、\'name\'、\'link_text\'、class\'、\'css\'、\'xpath\'\'、\'tag_name\'；\r\n值：定位元素对应的值，用来定位到表格；\r\n匹配项：列号+文本匹配到指定行，可通过多列匹配，格式：1,a,3,c；\r\n列号：勾选框元素所在列号\r\n布尔值：默认为\'True\'，表示勾选；为\'False\'时，表示去勾选', 'lvhao', '2020-11-12 13:58:23');
INSERT INTO `uiset` (`keyword`, `template`, `example`, `description`, `username`, `create_date`) VALUES ('清空填写时间|(\'值\',\'时间\')', 'clearTypetime', '清空填写时间|(\'start_time\',\'2020-10-25 12:22:33\')', '值：元素Id对应的值\r\n时间：输入符合页面格式的时间', 'lvhao', '2020-11-27 13:58:23');
INSERT INTO `uiset` (`keyword`, `template`, `example`, `description`, `username`, `create_date`) VALUES ('强制删除设备|(\'设备名称\',\'设备IP\')', 'delDevice', '强制删除设备|(\'212.213\',\'192.168.212.213\')', '请勿使用', 'puyawei', '2020-12-10 10:25:10');
INSERT INTO `uiset` (`keyword`, `template`, `example`, `description`, `username`, `create_date`) VALUES ('强制删除设备组|(\'设备组名称\')', 'delDevices', '强制删除设备集|(\'内置106\')', '请勿使用', 'puyawei', '2020-12-10 10:26:01');
INSERT INTO `uiset` (`keyword`, `template`, `example`, `description`, `username`, `create_date`) VALUES ('强制删除存放地|(\'存放地名称\')', 'delPlace', '强制删除存放地|(\'addr_poo\')', '请勿使用', 'puyawei', '2020-12-10 10:36:44');
INSERT INTO `uiset` (`keyword`, `template`, `example`, `description`, `username`, `create_date`) VALUES ('填写不重复文本|(\'元素\',\'值\',\'文本\')', 'typeRandom', '填写不重复文本|(\'id\',\'kw\',\'selenium\')', '元素：\'id\'、\'name\'、\'link_text\'、class\'、\'css\'、\'xpath\'\'、\'tag_name\'\r\n值：定位元素对应的值\r\n文本：需要输入的文本信息', 'lvhao', '2020-12-28 16:36:44');
