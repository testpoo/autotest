-- 导出 autotest 的数据库结构
CREATE DATABASE IF NOT EXISTS `autotest` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `autotest`;

-- 导出  表 autotest.apicases 结构
CREATE TABLE IF NOT EXISTS `apicases` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `type` varchar(255) NOT NULL,
  `product` varchar(255) NOT NULL,
  `model` varchar(255) NOT NULL,
  `steps` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `description` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '',
  `username` varchar(255) NOT NULL,
  `create_date` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=72 DEFAULT CHARSET=utf8;

-- 数据导出被取消选择。

-- 导出  表 autotest.apidates 结构
CREATE TABLE IF NOT EXISTS `apidates` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `case_name` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `path` varchar(255) NOT NULL,
  `method` varchar(255) NOT NULL,
  `request` varchar(255) NOT NULL,
  `checks` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `parameter` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '',
  `description` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '',
  `username` varchar(255) NOT NULL,
  `create_date` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`case_name`,`name`)
) ENGINE=InnoDB AUTO_INCREMENT=77 DEFAULT CHARSET=utf8;

-- 数据导出被取消选择。

-- 导出  表 autotest.apiset 结构
CREATE TABLE IF NOT EXISTS `apiset` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `path` varchar(255) NOT NULL,
  `method` varchar(255) NOT NULL,
  `request` varchar(255) NOT NULL,
  `checks` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `description` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '',
  `username` varchar(255) NOT NULL,
  `create_date` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;

-- 数据导出被取消选择。

-- 导出  表 autotest.apisitues 结构
CREATE TABLE IF NOT EXISTS `apisitues` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `steps` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
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
) ENGINE=InnoDB AUTO_INCREMENT=141 DEFAULT CHARSET=utf8;

-- 数据导出被取消选择。

-- 导出  表 autotest.uicases 结构
CREATE TABLE IF NOT EXISTS `uicases` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `type` varchar(255) NOT NULL,
  `model` varchar(255) NOT NULL,
  `product` varchar(255) NOT NULL,
  `steps` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `description` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '',
  `username` varchar(255) NOT NULL,
  `create_date` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=58 DEFAULT CHARSET=utf8;

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
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8;

-- 数据导出被取消选择。

-- 导出  表 autotest.uisitues 结构
CREATE TABLE IF NOT EXISTS `uisitues` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `steps` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `description` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '',
  `username` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `create_date` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `name` (`name`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;

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
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;

-- 数据导出被取消选择。

-- 正在导出表  autotest.uiset 的数据：~8 rows (大约)
/*!40000 ALTER TABLE `uiset` DISABLE KEYS */;
INSERT INTO `uiset` (`keyword`, `template`, `example`, `description`, `username`, `create_date`) VALUES
	('前往|(\'test_keywordurl\')', 'open', '前往(\'https://www.baidu.com\')', '', 'lvhao', '2020-09-23 15:35:37'),
	('最大化|()', 'maximizeWindow', '最大化()', '', 'lvhao', '2020-09-23 15:35:37'),
	('填写|(\'元素\',\'值\',\'文本\')', 'type', '填写(\'id\',\'kw\',\'selenium\')', '', 'lvhao', '2020-09-23 15:35:37'),
	('点击|(\'元素\',\'值\')', 'click', 'click(\'id\',\'su\')', '', 'lvhao', '2020-09-23 15:35:37'),
	('清除|(\'元素\',\'值\')', 'clear', 'clear(\'id\',\'kw\')', '', 'lvhao', '2020-09-23 15:35:37'),
	('验证标题|(\'文本\')', 'assert_title', 'assert_title(\'selenium\')', '', 'lvhao', '2020-09-23 15:35:37'),
	('隐式等待|(time)', 'implicitlyWwait', 'implicitlyWwait(20)', '', 'lvhao', '2020-09-23 15:35:37'),
	('标题|()', 'getTitle', 'getTitle()', '', 'lvhao', '2020-09-23 15:35:37'),
	('等待|(time)', 'wait', 'wait(5)', '', 'lvhao', '2020-09-23 15:35:37'),
	('验证文本|(\'元素\', \'值\',\'文本\')', 'assert_text', 'assert_text(\'class\',\'nums_text\',\'百度为您找到\')', '', 'lvhao', '2020-09-23 15:35:37'),
	('截图|(\'路径\')', 'getScreenshot', 'getScreenshot(\'D://baidu.png\')', '', 'lvhao', '2020-09-23 15:35:37'),
	('前进|()', 'forward', 'forward()', '', 'lvhao', '2020-09-23 15:35:37'),
	('后退|()', 'back', 'back()', '', 'lvhao', '2020-09-23 15:35:37'),
	('切换frame|(\'元素\',\'值\')', 'switchToFrame', 'switchToFrame(\'id\',\'login_frame\')', '', 'lvhao', '2020-09-23 15:35:37'),
	('切换到最外层frame|()', 'switchToOuterFrame', 'switchToOuterFrame()', '', 'lvhao', '2020-09-23 15:35:37');
/*!40000 ALTER TABLE `uiset` ENABLE KEYS */;

-- 正在导出表  autotest.user 的数据：~4 rows (大约)
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` (`username`, `password`, `last_login`, `email`, `zh_name`, `create_date`) VALUES
	('puyawei', 'MQ==', '2020-09-28 19:41:59', '2', '蒲亚伟', '2020-09-18 17:15:44'),
	('admin', 'MQ==', '2020-09-28 19:41:08', '2', '管理员', '2020-09-18 17:15:44'),
	('lvhao', 'MQ==', '2020-09-23 15:16:45', '2', '吕浩', '2020-09-23 14:50:12'),
	('bailu', 'MQ==', '2020-09-25 10:26:33', 'bailu@suninfo.com', '白露', '2020-09-25 10:26:25');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;