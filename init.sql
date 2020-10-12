-- 导出 autotest 的数据库结构
CREATE DATABASE IF NOT EXISTS `autotest` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `autotest`;

-- 导出  表 autotest.apicases 结构
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
  `description` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '',
  `username` varchar(255) NOT NULL,
  `create_date` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=109 DEFAULT CHARSET=utf8;

-- 数据导出被取消选择。

-- 导出  表 autotest.apidates 结构
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
) ENGINE=InnoDB AUTO_INCREMENT=180 DEFAULT CHARSET=utf8;

-- 数据导出被取消选择。

-- 导出  表 autotest.apiset 结构
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
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;

-- 数据导出被取消选择。

-- 导出  表 autotest.apisitues 结构
CREATE TABLE IF NOT EXISTS `apisitues` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `steps` varchar(2550) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '',
  `description` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '',
  `username` varchar(255) NOT NULL,
  `create_date` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;

-- 数据导出被取消选择。

-- 导出  表 autotest.report 结构
CREATE TABLE IF NOT EXISTS `report` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `case_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `type` varchar(50) NOT NULL,
  `product` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `status` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `spenttime` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `error` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `username` varchar(50) NOT NULL,
  `create_date` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=171 DEFAULT CHARSET=utf8;

-- 数据导出被取消选择。

-- 导出  表 autotest.uicases 结构
CREATE TABLE IF NOT EXISTS `uicases` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `type` varchar(50) DEFAULT NULL,
  `version` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `model` varchar(255) NOT NULL,
  `product` varchar(255) NOT NULL,
  `pre_steps` varchar(2550) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '',
  `steps` varchar(2550) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '',
  `next_steps` varchar(2550) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '',
  `description` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '',
  `activity` int(11) NOT NULL,
  `username` varchar(255) NOT NULL,
  `create_date` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=70 DEFAULT CHARSET=utf8;

-- 数据导出被取消选择。

-- 导出  表 autotest.uiset 结构
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
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8;

-- 数据导出被取消选择。

-- 导出  表 autotest.uisitues 结构
CREATE TABLE IF NOT EXISTS `uisitues` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `steps` varchar(2550) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '',
  `description` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '',
  `username` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `create_date` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `name` (`name`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;

-- 数据导出被取消选择。

-- 导出  表 autotest.user 结构
CREATE TABLE IF NOT EXISTS `user` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `last_login` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '',
  `email` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '',
  `zh_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '',
  `create_date` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;

-- 数据导出被取消选择。

-- 导出  表 autotest.versions 结构
CREATE TABLE IF NOT EXISTS `versions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `version` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `username` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `create_date` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `version` (`version`)
) ENGINE=InnoDB AUTO_INCREMENT=157 DEFAULT CHARSET=utf8;

-- 数据导出被取消选择。

-- 正在导出表  autotest.uiset 的数据：~27 rows (大约)
/*!40000 ALTER TABLE `uiset` DISABLE KEYS */;
INSERT INTO `uiset` (`keyword`, `template`, `example`, `description`, `username`, `create_date`) VALUES
	('前往|(\'test_keywordurl\')', 'open', '前往|(\'https://www.baidu.com\')', '前往：打开指定URL网页', 'lvhao', '2020-09-23 15:35:37'),
	('最大化|()', 'maximizeWindow', '最大化|()', '最大化：窗口最大化', 'lvhao', '2020-09-23 15:35:37'),
	('填写|(\'元素\',\'值\',\'文本\')', 'type', '填写|(\'id\',\'kw\',\'selenium\')', '元素：\'id\'、\'name\'、\'link_text\'、class\'、\'css\'、\'xpath\'\'、\'tag_name\'\r\n值：定位元素对应的值\r\n文本：需要输入的文本信息', 'lvhao', '2020-09-23 15:35:37'),
	('点击|(\'元素\',\'值\')', 'click', '点击|(\'id\',\'su\')', '元素：\'id\'、\'name\'、\'link_text\'、class\'、\'css\'、\'xpath\'\'、\'tag_name\'', 'lvhao', '2020-09-23 15:35:37'),
	('清除|(\'元素\',\'值\')', 'clear', '清除|(\'id\',\'kw\')', '元素：\'id\'、\'name\'、\'link_text\'、class\'、\'css\'、\'xpath\'\'、\'tag_name\'', 'lvhao', '2020-09-23 15:35:37'),
	('验证标题|(\'文本\')', 'assertTitle', '验证标题|(\'首页-上讯信息\')', '文本：需要验证的文本信息', 'lvhao', '2020-09-23 15:35:37'),
	('隐式等待|(time)', 'implicitlyWwait', '隐式等待|(20)', 'time：时间(s)', 'lvhao', '2020-09-23 15:35:37'),
	('标题|()', 'getTitle', '标题|()', '', 'lvhao', '2020-09-23 15:35:37'),
	('等待|(time)', 'wait', '等待|(5)', 'time：时间(s)', 'lvhao', '2020-09-23 15:35:37'),
	('验证文本|(\'元素\',\'值\',\'文本\')', 'assertText', '验证文本|(\'class\',\'nums_text\',\'百度为您找到\')', '元素：\'id\'、\'name\'、\'link_text\'、class\'、\'css\'、\'xpath\'\'、\'tag_name\'\r\n值：定位元素对应的值\r\n文本：需要验证的文本信息', 'lvhao', '2020-09-23 15:35:37'),
	('截图|(\'路径\')', 'getScreenshot', '截图|(\'D://baidu.png\')', '路径：存放截图的绝对路径；执行失败时会自动截图保存autotest\\static\\Screenshot路径下', 'lvhao', '2020-09-23 15:35:37'),
	('前进|()', 'forward', '前进|()', '', 'lvhao', '2020-09-23 15:35:37'),
	('后退|()', 'back', '后退|()', '', 'lvhao', '2020-09-23 15:35:37'),
	('切换frame|(\'元素\',\'值\')', 'switchToFrame', '切换frame|(\'id\',\'login_frame\')', '元素：\'id\'、\'name\'、\'link_text\'、class\'、\'css\'、\'xpath\'\'、\'tag_name\'', 'lvhao', '2020-09-23 15:35:37'),
	('切换到最外层frame|()', 'switchToOuterFrame', '切换到最外层frame|()', '', 'lvhao', '2020-09-23 15:35:37'),
	('切换到弹窗|()', 'switchToAlert', '切换到弹窗|()', '', 'lvhao', '2020-09-23 15:35:37'),
	('弹窗填写|(‘文本’)', 'tpyeAlert', '弹窗填写|(‘人员管理’)', '文本：需要填写的文本信息', 'lvhao', '2020-09-23 15:35:37'),
	('验证弹窗文本|(\'文本\')', 'assertTextAlert', '验证弹窗文本|(\'保存成功\')', '文本：需要验证的文本信息', 'lvhao', '2020-09-23 15:35:37'),
	('弹窗确认|()', 'acceptAlert', '弹窗确认|()', '', 'lvhao', '2020-09-23 15:35:37'),
	('设置窗口大小|(宽,高)', 'setWindowSize', '设置窗口大小|(800,500)', '', 'lvhao', '2020-09-23 15:35:37'),
	('提交表单|()', 'submit', '提交表单|()', '', 'lvhao', '2020-09-23 15:35:37'),
	('刷新|()', 'refresh', '刷新|()', '', 'lvhao', '2020-09-23 15:35:37'),
	('下拉框|(\'元素\',\'值\',\'文本\')', 'findSelect', '下拉框|(\'name\',\'user_gender\',\'男\')', '元素：\'id\'、\'name\'、\'link_text\'、class\'、\'css\'、\'xpath\'\'、\'tag_name\'\r\n值：定位元素对应的值\r\n文本：需要选择的文本信息', 'lvhao', '2020-09-23 15:35:37'),
	('上传|(\'元素\',\'值\',\'路径\')', 'uploadFile', '上传|(\'id\',\'fileupload\',\'C:\\\\Users\\dell\\Desktop\\DepartList_2020_10_10_093508.xls\')', '元素：\'id\'、\'name\'、\'link_text\'、class\'、\'css\'、\'xpath\'\'、\'tag_name\'\r\n值：定位元素对应的值\r\n路径：文件的绝对路径；格式：‘C:\\\\*\\*’', 'lvhao', '2020-09-23 15:35:37'),
	('回车|(\'元素\',\'值\')', 'enter', '回车|(\'id\',\'submit_btn\')', '回车按键\r\n元素：\'id\'、\'name\'、\'link_text\'、class\'、\'css\'、\'xpath\'\'、\'tag_name\'\r\n值：定位元素对应的值', 'lvhao', '2020-09-23 15:35:37'),
	('TABLE|(\'元素\',\'值\')', 'table', 'TABLE|(\'id\',\'username\')', '制表按键\r\n元素：\'id\'、\'name\'、\'link_text\'、class\'、\'css\'、\'xpath\'\'、\'tag_name\'\r\n值：定位元素对应的值', 'lvhao', '2020-09-23 15:35:37'),
	('验证属性|(\'元素\',\'值\',\'属性\',\'文本\')', 'assertAttribute', '验证属性(\'id\', \'login_name\', \'value\',\'口令认证\')', '元素：\'id\'、\'name\'、\'link_text\'、class\'、\'css\'、\'xpath\'\'、\'tag_name\'\r\n值：定位元素对应的值\r\n属性：‘value’,\'class\'等\r\n文本：需要验证的文本信息', 'lvhao', '2020-09-23 15:35:37');
/*!40000 ALTER TABLE `uiset` ENABLE KEYS */;

-- 正在导出表  autotest.user 的数据：~9 rows (大约)
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` (`username`, `password`, `last_login`, `email`, `zh_name`, `create_date`) VALUES
	('puyawei', 'MQ==', '2020-10-10 20:55:52', '2', '蒲亚伟', '2020-09-18 17:15:44'),
	('admin', 'MQ==', '2020-09-30 09:15:14', '2', '管理员', '2020-09-18 17:15:44'),
	('lvhao', 'MQ==', '2020-10-10 14:28:18', '2', '吕浩', '2020-09-23 14:50:12'),
	('bailu', 'MQ==', '2020-09-29 16:58:27', 'bailu@suninfo.com', '白露', '2020-09-25 10:26:25'),
	('wangluo', 'MQ==', '2020-09-29 16:58:27', 'wangluo@suninfo.com', '王洛', '2020-09-25 10:26:25'),
	('wangting', 'MQ==', '2020-09-29 16:58:27', 'wangting@suninfo.com', '王婷', '2020-09-25 10:26:25'),
	('liudeyue', 'MQ==', '2020-10-10 10:37:34', 'liudy@suninfo.com', '刘德月', '2020-09-25 10:26:25'),
	('liwenhui', 'MQ==', '2020-09-29 16:58:27', 'liwh@suninfo.com', '李文慧', '2020-09-25 10:26:25'),
	('liyangyang', 'MQ==', '2020-09-29 16:58:27', 'liyangyang@suninfo.com', '李杨杨', '2020-09-25 10:26:25');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
