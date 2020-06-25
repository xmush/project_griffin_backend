-- MySQL dump 10.13  Distrib 5.7.29, for Linux (x86_64)
--
-- Host: localhost    Database: project_griffin
-- ------------------------------------------------------
-- Server version	5.7.29-0ubuntu0.18.04.1

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
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_type`
--

DROP TABLE IF EXISTS `product_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `product_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `icon` text,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_type`
--

LOCK TABLES `product_type` WRITE;
/*!40000 ALTER TABLE `product_type` DISABLE KEYS */;
INSERT INTO `product_type` VALUES (1,'VIDEOTRON','https://firebasestorage.googleapis.com/v0/b/testapp-22a56.appspot.com/o/images%2Fcategory_icon%2Fvideotron.jpg?alt=media&token=1aa16065-6e95-4d45-a854-475c03bee705','2020-06-15 19:59:54','2020-06-15 20:00:14');
/*!40000 ALTER TABLE `product_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `publisher`
--

DROP TABLE IF EXISTS `publisher`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `publisher` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `publisher_name` varchar(100) NOT NULL,
  `address` text,
  `publisher_pict` text,
  `company_sertificate` text NOT NULL,
  `npwp_number` varchar(100) DEFAULT NULL,
  `npwp_pict` text,
  `bank_account_name` varchar(100) DEFAULT NULL,
  `bank_account_number` varchar(100) DEFAULT NULL,
  `bank_account_detail` text,
  `is_authorized` tinyint(1) NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `publisher_name` (`publisher_name`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `publisher_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `publisher`
--

LOCK TABLES `publisher` WRITE;
/*!40000 ALTER TABLE `publisher` DISABLE KEYS */;
INSERT INTO `publisher` VALUES (4,'Derby\'s Ads places','Jalan Tidar no 23 Malang, Jawa Timur','https://firebasestorage.googleapis.com/v0/b/testapp-22a56.appspot.com/o/images%2Fuser_publisher_pict%2FScreenshot%20from%202020-06-09%2019-16-54.png?alt=media&token=a8f7126f-398e-4ab3-8fc7-ef3e15bec90d','https://firebasestorage.googleapis.com/v0/b/testapp-22a56.appspot.com/o/images%2Fuser_company_sertificate%2Fvideotron.jpg?alt=media&token=b51b735a-8bc6-4b07-9fc6-8d4a329285d4','192012918297526244','https://firebasestorage.googleapis.com/v0/b/testapp-22a56.appspot.com/o/images%2Fuser_npwp_pict%2Fcoffindance.jpg?alt=media&token=89ed9dcf-c332-4192-838a-542c64db3e21','AFN Ads Spot','012345321','Bank BNI KCP Malang',1,'2020-06-16 17:37:28','2020-06-16 18:39:45',4),(5,'Derby\'s Ads place','Jalan Terusan Surabaya, Malang, Jawa Timur','https://firebasestorage.googleapis.com/v0/b/testapp-22a56.appspot.com/o/images%2Fuser_publisher_pict%2FScreenshot%20from%202020-05-31%2021-01-00.png?alt=media&token=d9ba1240-e2c7-4774-ab31-efa1e25a3774','https://firebasestorage.googleapis.com/v0/b/testapp-22a56.appspot.com/o/images%2Fuser_company_sertificate%2FScreenshot%20from%202020-06-09%2012-32-49.png?alt=media&token=b3a79d66-2afb-4dad-9cc4-b628fa70dca8','192112918297526244','https://firebasestorage.googleapis.com/v0/b/testapp-22a56.appspot.com/o/images%2Fuser_npwp_pict%2FScreenshot%20from%202020-05-12%2022-13-15.png?alt=media&token=3caa60e6-add0-4359-a692-71cad9b29ea1','DPS Spot','0112345321','Bank BRI KCP Surabaya',0,'2020-06-16 18:37:24','2020-06-16 18:38:55',5);
/*!40000 ALTER TABLE `publisher` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `phone` varchar(15) NOT NULL,
  `email` varchar(100) NOT NULL,
  `user_type` varchar(100) NOT NULL,
  `is_publisher` tinyint(1) NOT NULL,
  `address` text,
  `profil_pict` text,
  `KTP_number` varchar(100) DEFAULT NULL,
  `KTP_pict` text,
  `password` varchar(255) DEFAULT NULL,
  `salt` varchar(255) DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `phone` (`phone`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'admin','082326386609','admin@gmail.com','admin',0,'','','','','4ca22bfea8b4fb08216ab1a35e9e371565bf8c3f4870c96168a7ebce034dcfa74be4213eb0555e78effe60969b84ee527f5ebcf73c2c09c91edf723780a2eea3','c51907b5878949d788fde80f031fc88a','2020-06-15 19:56:49',NULL),(2,'Andre Novado','081321324351','andreh@gmail.com','user',0,'','','','','8aed683f083c424bcf55e806ff095e1e359051d5e9cecf95394d10e3a816a7cf08a0232d269da367f92142f9a2cb0d2db6514ae2dbdd0cfae5b24f7b815feff3','356555a58309469fb17ed339caab1101','2020-06-15 19:57:50',NULL),(3,'Bagas Kurniajati','082121324351','bagas@gmail.com','user',0,'','','','','2ec9f89625b75c248282904a66d4e65ace67fdd0e6906a2e4313ecf49054f116b2c5660262cd9a8476e5821521365e5d75bf0f1d1d5e41dfa55131427f5f55e3','490439437b954247a7c60d0aee307cf2','2020-06-15 19:58:08',NULL),(4,'Andre Fajar N','085421324351','afn@gmail.com','user',1,'Tulung Agung, Jawa Timurs','https://firebasestorage.googleapis.com/v0/b/testapp-22a56.appspot.com/o/images%2Fuser_profil_pict%2Fpollackimg.jpeg?alt=media&token=db7b4a41-eca8-4b6f-8bd6-b2d0e06a820c','330112121490009','https://firebasestorage.googleapis.com/v0/b/testapp-22a56.appspot.com/o/images%2Fuser_KTP_pict%2FScreenshot%20from%202020-05-31%2021-01-00.png?alt=media&token=97d53662-e670-4e32-9169-05ecbe9b70c8','23a2bb570bb252757c1e028c7f3f9703ac595ba510ef2cefd1fae923074e572bc1617d68b7892606849229485734c8f4d32e6f6cf62d80944559b0985c5eb9b8','fa90edac7d4245599f8e0c65a0384216','2020-06-16 14:50:08','2020-06-16 18:36:03'),(5,'Derby Prayogo S','083121324351','derby@gmail.com','user',0,'Surabaya, Jawa Timur','https://firebasestorage.googleapis.com/v0/b/testapp-22a56.appspot.com/o/images%2Fuser_profil_pict%2Fvideotron.jpg?alt=media&token=b3b8b9e6-a204-4914-bc1c-e7c0712657f1','3301113121490009','https://firebasestorage.googleapis.com/v0/b/testapp-22a56.appspot.com/o/images%2Fuser_KTP_pict%2Fpollackimg.jpeg?alt=media&token=9c5ff978-3d3c-476f-bf1e-aacb19f638e6','b68a8a3f32f15c9a57c18c8290571b9a168cf0481e187888939ae3027af047cb77f6645724693e3578be6d7b1008a121a2fcc442b1d34a5e70e1afa3339c2746','75da272bcbfd4e50ba0d751b04e6e6bd','2020-06-16 18:33:34','2020-06-16 18:35:47');
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

-- Dump completed on 2020-06-16 18:55:08
