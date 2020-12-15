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
  `exec_result` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '',
  `description` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '',
  `username` varchar(255) NOT NULL,
  `create_date` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=111 DEFAULT CHARSET=utf8;



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
) ENGINE=InnoDB AUTO_INCREMENT=182 DEFAULT CHARSET=utf8;



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
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;



-- 导出  表 autotest.apisitues 结构
CREATE TABLE IF NOT EXISTS `apisitues` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `exec_mode` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `steps` varchar(2550) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '',
  `description` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '',
  `username` varchar(255) NOT NULL,
  `create_date` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;



-- 导出  表 autotest.auth 结构
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
) ENGINE=InnoDB AUTO_INCREMENT=50 DEFAULT CHARSET=utf8;



-- 导出  表 autotest.report 结构
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
) ENGINE=InnoDB AUTO_INCREMENT=3396 DEFAULT CHARSET=utf8;



-- 导出  表 autotest.uicases 结构
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
) ENGINE=InnoDB AUTO_INCREMENT=1788 DEFAULT CHARSET=utf8;



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
) ENGINE=InnoDB AUTO_INCREMENT=84 DEFAULT CHARSET=utf8;



-- 导出  表 autotest.uisitues 结构
CREATE TABLE IF NOT EXISTS `uisitues` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `exec_mode` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `steps` varchar(12500) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '0',
  `description` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '',
  `username` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `create_date` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `name` (`name`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=90 DEFAULT CHARSET=utf8;



-- 导出  表 autotest.user 结构
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



-- 导出  表 autotest.versions 结构
CREATE TABLE IF NOT EXISTS `versions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `version` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `username` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `create_date` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `version` (`version`)
) ENGINE=InnoDB AUTO_INCREMENT=158 DEFAULT CHARSET=utf8;

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