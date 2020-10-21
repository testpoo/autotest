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
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;

-- 数据导出被取消选择。

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
) ENGINE=InnoDB AUTO_INCREMENT=191 DEFAULT CHARSET=utf8;

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
  `steps` varchar(12500) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '0',
  `next_steps` varchar(2550) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '',
  `description` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '',
  `activity` int(11) NOT NULL,
  `username` varchar(255) NOT NULL,
  `create_date` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=97 DEFAULT CHARSET=utf8;

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
) ENGINE=InnoDB AUTO_INCREMENT=59 DEFAULT CHARSET=utf8;

-- 数据导出被取消选择。

-- 导出  表 autotest.uisitues 结构
CREATE TABLE IF NOT EXISTS `uisitues` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `exec_mode` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `steps` varchar(2550) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '',
  `description` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '',
  `username` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `create_date` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `name` (`name`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8;

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
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8;

-- 数据导出被取消选择。

-- 导出  表 autotest.versions 结构
CREATE TABLE IF NOT EXISTS `versions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `version` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `username` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `create_date` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `version` (`version`)
) ENGINE=InnoDB AUTO_INCREMENT=158 DEFAULT CHARSET=utf8;

-- 数据导出被取消选择。
