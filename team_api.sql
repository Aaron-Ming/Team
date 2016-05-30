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
  `extra` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`id`,`username`),
  UNIQUE KEY `username` (`username`) USING BTREE,
  KEY `email` (`email`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=46 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'admin','staugur@saintic.com','8879168cbf8a9e11c296530803e93308','陶成伟','/static/upload/15768284.jpg','原谅我一生放荡不羁爱自由','https://www.saintic.com','7h8l4uiKZEopBxjJHGHGduQYLA42Xfbr','Python写的博客应用，采用flask框架。'),(9,'test1','','8879168cbf8a9e11c296530803e93308',NULL,'/static/upload/mmexport1462070594047.jpg',NULL,NULL,NULL,NULL),(10,'test','','098f6bcd4621d373cade4e832627b4f6',NULL,'/static/upload/mmexport1462071607347.jpg',NULL,NULL,NULL,NULL),(11,'tcw','1663116375@qq.com','8879168cbf8a9e11c296530803e93308','Sakura','/static/upload/288CU6HZ7BD4_1.jpg','找到了方向，不再迷茫！','http://www.saintic.com',NULL,NULL),(13,'slx','None','e10adc3949ba59abbe56e057f20f883e',NULL,NULL,NULL,NULL,NULL,NULL),(14,'taochengwei','None','e10adc3949ba59abbe56e057f20f883e',NULL,NULL,NULL,NULL,NULL,NULL),(15,'sic1','staugur@saintic.com','e10adc3949ba59abbe56e057f20f883e',NULL,NULL,NULL,NULL,NULL,NULL),(16,'sic2','staugur@vip.qq.com','c4ca4238a0b923820dcc509a6f75849b',NULL,NULL,NULL,NULL,NULL,NULL),(17,'saintic3','staugur@vip.qq.com','c4ca4238a0b923820dcc509a6f75849b',NULL,NULL,NULL,NULL,NULL,NULL),(18,'saintic4','staugur@vip.qq.com','827ccb0eea8a706c4c34a16891f84e7b',NULL,NULL,NULL,NULL,NULL,NULL),(19,'saintic6','staugur@saintic.com','ebb080afaac3a990ad3f1d0f21742fac',NULL,NULL,NULL,NULL,NULL,NULL),(20,'saintic2','None','e10adc3949ba59abbe56e057f20f883e',NULL,NULL,NULL,NULL,NULL,NULL),(21,'saintic1','staugur@vip.qq','e10adc3949ba59abbe56e057f20f883e',NULL,NULL,NULL,NULL,NULL,NULL),(22,'saintic7','staugur@vip.qq.com','e10adc3949ba59abbe56e057f20f883e',NULL,NULL,NULL,NULL,NULL,NULL),(23,'saintic8','None','e10adc3949ba59abbe56e057f20f883e',NULL,NULL,NULL,NULL,NULL,NULL),(24,'saintic9','staugur@sainitc.net','e10adc3949ba59abbe56e057f20f883e',NULL,NULL,NULL,NULL,NULL,NULL),(25,'saintic10','staugur@sainitc.me','827ccb0eea8a706c4c34a16891f84e7b',NULL,NULL,NULL,NULL,NULL,NULL),(26,'saintic12','staugur@sainitc.me','827ccb0eea8a706c4c34a16891f84e7b',NULL,NULL,NULL,NULL,NULL,NULL),(27,'saintic13','staugur@sainitc.me','827ccb0eea8a706c4c34a16891f84e7b',NULL,NULL,NULL,NULL,NULL,NULL);
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

-- Dump completed on 2016-05-30 17:32:00
