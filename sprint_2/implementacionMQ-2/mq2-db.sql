CREATE DATABASE  IF NOT EXISTS `iot` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `iot`;
-- MySQL dump 10.13  Distrib 8.0.32, for Win64 (x86_64)
--
-- Host: localhost    Database: iot
-- ------------------------------------------------------
-- Server version	8.0.32

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `sensores`
--

DROP TABLE IF EXISTS `sensores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sensores` (
  `id` int NOT NULL AUTO_INCREMENT,
  `sensor` int NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `descripcion` varchar(50) DEFAULT NULL,
  `fecha` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=83 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sensores`
--

LOCK TABLES `sensores` WRITE;
/*!40000 ALTER TABLE `sensores` DISABLE KEYS */;
INSERT INTO `sensores` VALUES (33,1,'humedad','Humedad: 41.00 Temperatura: 21.00','2024-09-14 11:46:12'),(34,1,'humedad','Humedad: 41.00 Temperatura: 21.00','2024-09-14 11:46:16'),(35,1,'humedad','Humedad: 41.00 Temperatura: 21.00','2024-09-14 11:46:20'),(36,1,'humedad','Humedad: 41.00 Temperatura: 21.00','2024-09-14 11:46:24'),(37,1,'humedad','Humedad: 41.00 Temperatura: 21.00','2024-09-14 11:46:29'),(38,1,'humedad','Humedad: 41.00 Temperatura: 21.00','2024-09-14 11:46:32'),(39,1,'humedad','Humedad: 40.00 Temperatura: 21.00','2024-09-14 11:46:36'),(40,1,'humedad','Humedad: 40.00 Temperatura: 21.00','2024-09-14 11:46:40'),(41,1,'humedad','Humedad: 40.00 Temperatura: 21.00','2024-09-14 11:46:44'),(42,1,'humedad','Humedad: 40.00 Temperatura: 21.00','2024-09-14 11:46:49'),(43,1,'humedad','Humedad: 40.00 Temperatura: 21.00','2024-09-14 11:46:52'),(44,1,'humedad','Humedad: 41.00 Temperatura: 20.90','2024-09-14 11:46:57'),(45,1,'humedad','Humedad: 41.00 Temperatura: 20.70','2024-09-14 11:47:00'),(46,1,'humedad','Humedad: 41.00 Temperatura: 20.60','2024-09-14 11:47:08'),(47,1,'humedad','Humedad: 41.00 Temperatura: 20.60','2024-09-14 11:47:09'),(48,1,'humedad','-31.20','2024-09-24 18:19:39'),(49,1,'humedad','-31.20','2024-09-24 18:19:41'),(50,1,'humedad','-31.20','2024-09-24 18:19:43'),(51,1,'humedad','-31.20','2024-09-24 18:19:45'),(52,1,'humedad','-31.20','2024-09-24 18:19:47'),(53,1,'humedad','-31.20','2024-09-24 18:19:49'),(54,1,'humedad','-31.20','2024-09-24 18:19:51'),(55,1,'humedad','-31.20','2024-09-24 18:19:54'),(56,1,'humedad','-31.20','2024-09-24 18:19:56'),(57,1,'humedad','-31.20','2024-09-24 18:19:58'),(58,1,'humedad','-31.20','2024-09-24 18:20:00'),(59,1,'humedad','-31.20','2024-09-24 18:20:02'),(60,1,'humedad','-31.20','2024-09-24 18:20:04'),(61,1,'humedad','-31.20','2024-09-24 18:20:06'),(62,1,'humedad','-31.20','2024-09-24 18:20:08'),(63,1,'humedad','-31.20','2024-09-24 18:20:10'),(64,1,'humedad','-31.20','2024-09-24 18:20:12'),(65,1,'humedad','-31.20','2024-09-24 18:20:14'),(66,1,'humedad','-31.20','2024-09-24 18:20:16'),(67,1,'humedad','-31.20','2024-09-24 18:20:19'),(68,1,'humedad','-31.20','2024-09-24 18:20:21'),(69,1,'humedad','-31.20','2024-09-24 18:20:23'),(70,1,'humedad','-31.20','2024-09-24 18:20:25'),(71,1,'humedad','-31.20','2024-09-24 18:20:27'),(72,1,'humedad','-31.20','2024-09-24 18:20:29'),(73,1,'humedad','-31.20','2024-09-24 18:20:31'),(74,1,'humedad','-31.20','2024-09-24 18:20:33'),(75,1,'humedad','38511.57','2024-09-24 18:20:46'),(76,1,'humedad','38511.57','2024-09-24 18:20:48'),(77,1,'humedad','38511.57','2024-09-24 18:20:50'),(78,1,'humedad','38511.57','2024-09-24 18:20:52'),(79,1,'humedad','38511.57','2024-09-24 18:20:54'),(80,1,'humedad','38511.57','2024-09-24 18:20:56'),(81,1,'humedad','38511.57','2024-09-24 18:20:58'),(82,1,'humedad','38511.57','2024-09-24 18:21:01');
/*!40000 ALTER TABLE `sensores` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-09-25 16:03:45
