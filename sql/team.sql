-- MySQL dump 10.13  Distrib 5.1.73, for redhat-linux-gnu (x86_64)
--
-- Host: localhost    Database: team
-- ------------------------------------------------------
-- Server version	5.1.73

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `team`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `team` /*!40100 DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci */;

USE `team`;

--
-- Table structure for table `blog`
--

DROP TABLE IF EXISTS `blog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `blog` (
  `id` int(4) NOT NULL AUTO_INCREMENT COMMENT 'BlogId',
  `title` varchar(30) NOT NULL COMMENT '文章标题',
  `content` varchar(2000) NOT NULL COMMENT '文章',
  `create_time` varchar(20) DEFAULT NULL COMMENT '文章创建时间',
  `update_time` varchar(20) DEFAULT NULL COMMENT '文章更新时间',
  `tag` varchar(20) DEFAULT '技术' COMMENT '文章标签',
  `catalog` varchar(10) DEFAULT '未分类' COMMENT '文章分类目录',
  `sources` varchar(10) DEFAULT '原创',
  PRIMARY KEY (`id`),
  KEY `id` (`id`,`create_time`,`tag`,`catalog`,`sources`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=50 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `blog`
--

LOCK TABLES `blog` WRITE;
/*!40000 ALTER TABLE `blog` DISABLE KEYS */;
INSERT INTO `blog` VALUES (47,'测试1','技术博客测试文章',NULL,NULL,'技术','未分类','原创'),(48,'测试2','生活与娱乐',NULL,NULL,'生活','未分类','原创'),(49,'测试3','爱情与情爱',NULL,NULL,'生活','未分类','原创');
/*!40000 ALTER TABLE `blog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(25) NOT NULL,
  `email` varchar(50) DEFAULT NULL,
  `password` varchar(32) NOT NULL,
  `cname` varchar(25) DEFAULT NULL,
  `avatar` varchar(300) DEFAULT NULL,
  `motto` varchar(200) DEFAULT NULL,
  `url` varchar(50) DEFAULT NULL,
  `token` varchar(32) DEFAULT NULL,
  `time` varchar(15) DEFAULT NULL,
  `extra` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`id`,`username`),
  UNIQUE KEY `username` (`username`) USING BTREE,
  KEY `email` (`email`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=66 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'admin','staugur@saintic.com','8879168cbf8a9e11c296530803e93308','陶成伟','/static/upload/15768284.jpg','原谅我一生放荡不羁爱自由','https://www.saintic.com','7h8l4uiKZEopBxjJHGHGduQYLA42Xfbr',NULL,'Python写的博客应用，采用flask框架。'),(62,'test_case10','None','e10adc3949ba59abbe56e057f20f883e',NULL,NULL,NULL,NULL,'xrK6HNUvRnqD2wfMHCTIb0ucg+YcjF//',NULL,NULL),(63,'test_123','None','8879168cbf8a9e11c296530803e93308',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(64,'aaron','None','449a36b6689d841d7d27f31b4b7cc73a','测试别名',NULL,NULL,NULL,'c8FEDOTJ8+CjIsev2wOWorCUQcAjTmyC',NULL,NULL),(65,'Mr.tao','None','8879168cbf8a9e11c296530803e93308',NULL,NULL,NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-07-17 18:27:50
