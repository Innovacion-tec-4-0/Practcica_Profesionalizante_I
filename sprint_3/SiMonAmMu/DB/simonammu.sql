CREATE DATABASE  IF NOT EXISTS `simonammu` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `simonammu`;
-- MySQL dump 10.13  Distrib 8.0.38, for Win64 (x86_64)
--
-- Host: localhost    Database: simonammu
-- ------------------------------------------------------
-- Server version	8.0.39

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
-- Table structure for table `actuadores`
--

DROP TABLE IF EXISTS `actuadores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `actuadores` (
  `id` int NOT NULL AUTO_INCREMENT,
  `tipo` varchar(50) DEFAULT NULL,
  `estado` tinyint(1) DEFAULT NULL,
  `fecha_hora` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `actuadores`
--

LOCK TABLES `actuadores` WRITE;
/*!40000 ALTER TABLE `actuadores` DISABLE KEYS */;
/*!40000 ALTER TABLE `actuadores` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ambiente`
--

DROP TABLE IF EXISTS `ambiente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ambiente` (
  `id` int NOT NULL AUTO_INCREMENT,
  `fecha` datetime DEFAULT CURRENT_TIMESTAMP,
  `temperatura` float DEFAULT NULL,
  `humedad` float DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ambiente`
--

LOCK TABLES `ambiente` WRITE;
/*!40000 ALTER TABLE `ambiente` DISABLE KEYS */;
/*!40000 ALTER TABLE `ambiente` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `avisos_humedad`
--

DROP TABLE IF EXISTS `avisos_humedad`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `avisos_humedad` (
  `id` int NOT NULL AUTO_INCREMENT,
  `fecha` datetime DEFAULT CURRENT_TIMESTAMP,
  `mensaje` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `avisos_humedad`
--

LOCK TABLES `avisos_humedad` WRITE;
/*!40000 ALTER TABLE `avisos_humedad` DISABLE KEYS */;
/*!40000 ALTER TABLE `avisos_humedad` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `control_led`
--

DROP TABLE IF EXISTS `control_led`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `control_led` (
  `id` int NOT NULL AUTO_INCREMENT,
  `fecha` datetime DEFAULT CURRENT_TIMESTAMP,
  `estado` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `control_led`
--

LOCK TABLES `control_led` WRITE;
/*!40000 ALTER TABLE `control_led` DISABLE KEYS */;
/*!40000 ALTER TABLE `control_led` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `datos_ambientales`
--

DROP TABLE IF EXISTS `datos_ambientales`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `datos_ambientales` (
  `id` int NOT NULL AUTO_INCREMENT,
  `temperatura_id` int DEFAULT NULL,
  `humedad_id` int DEFAULT NULL,
  `luz_id` int DEFAULT NULL,
  `fecha_hora` datetime DEFAULT CURRENT_TIMESTAMP,
  `lux_id` int DEFAULT NULL,
  `led_id` int DEFAULT NULL,
  `movimiento_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `temperatura_id` (`temperatura_id`),
  KEY `humedad_id` (`humedad_id`),
  KEY `luz_id` (`luz_id`),
  KEY `lux_id` (`lux_id`),
  KEY `led_id` (`led_id`),
  CONSTRAINT `datos_ambientales_ibfk_1` FOREIGN KEY (`temperatura_id`) REFERENCES `temperatura` (`id`),
  CONSTRAINT `datos_ambientales_ibfk_2` FOREIGN KEY (`humedad_id`) REFERENCES `humedad` (`id`),
  CONSTRAINT `datos_ambientales_ibfk_3` FOREIGN KEY (`luz_id`) REFERENCES `luz` (`id`),
  CONSTRAINT `datos_ambientales_ibfk_4` FOREIGN KEY (`lux_id`) REFERENCES `lux` (`id`),
  CONSTRAINT `datos_ambientales_ibfk_5` FOREIGN KEY (`led_id`) REFERENCES `led` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `datos_ambientales`
--

LOCK TABLES `datos_ambientales` WRITE;
/*!40000 ALTER TABLE `datos_ambientales` DISABLE KEYS */;
/*!40000 ALTER TABLE `datos_ambientales` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `eventos_movimiento`
--

DROP TABLE IF EXISTS `eventos_movimiento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `eventos_movimiento` (
  `id` int NOT NULL AUTO_INCREMENT,
  `movimiento_detectado` tinyint(1) DEFAULT NULL,
  `fecha_hora` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `eventos_movimiento`
--

LOCK TABLES `eventos_movimiento` WRITE;
/*!40000 ALTER TABLE `eventos_movimiento` DISABLE KEYS */;
/*!40000 ALTER TABLE `eventos_movimiento` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `humedad`
--

DROP TABLE IF EXISTS `humedad`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `humedad` (
  `id` int NOT NULL AUTO_INCREMENT,
  `valor` float DEFAULT NULL,
  `timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `humedad`
--

LOCK TABLES `humedad` WRITE;
/*!40000 ALTER TABLE `humedad` DISABLE KEYS */;
/*!40000 ALTER TABLE `humedad` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `led`
--

DROP TABLE IF EXISTS `led`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `led` (
  `id` int NOT NULL AUTO_INCREMENT,
  `estado` tinyint(1) DEFAULT NULL,
  `fecha_hora` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `led`
--

LOCK TABLES `led` WRITE;
/*!40000 ALTER TABLE `led` DISABLE KEYS */;
/*!40000 ALTER TABLE `led` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `luminosidad`
--

DROP TABLE IF EXISTS `luminosidad`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `luminosidad` (
  `id` int NOT NULL AUTO_INCREMENT,
  `fecha` datetime DEFAULT CURRENT_TIMESTAMP,
  `nivel` float DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `luminosidad`
--

LOCK TABLES `luminosidad` WRITE;
/*!40000 ALTER TABLE `luminosidad` DISABLE KEYS */;
/*!40000 ALTER TABLE `luminosidad` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lux`
--

DROP TABLE IF EXISTS `lux`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `lux` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nivel` float DEFAULT NULL,
  `fecha_hora` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lux`
--

LOCK TABLES `lux` WRITE;
/*!40000 ALTER TABLE `lux` DISABLE KEYS */;
/*!40000 ALTER TABLE `lux` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `luz`
--

DROP TABLE IF EXISTS `luz`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `luz` (
  `id` int NOT NULL AUTO_INCREMENT,
  `estado` tinyint(1) DEFAULT NULL,
  `nivel` float DEFAULT NULL,
  `fecha_hora` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `luz`
--

LOCK TABLES `luz` WRITE;
/*!40000 ALTER TABLE `luz` DISABLE KEYS */;
/*!40000 ALTER TABLE `luz` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `movimiento`
--

DROP TABLE IF EXISTS `movimiento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `movimiento` (
  `id` int NOT NULL AUTO_INCREMENT,
  `fecha` datetime DEFAULT CURRENT_TIMESTAMP,
  `estado` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `movimiento`
--

LOCK TABLES `movimiento` WRITE;
/*!40000 ALTER TABLE `movimiento` DISABLE KEYS */;
/*!40000 ALTER TABLE `movimiento` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `potenciometro`
--

DROP TABLE IF EXISTS `potenciometro`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `potenciometro` (
  `id` int NOT NULL AUTO_INCREMENT,
  `fecha` datetime DEFAULT CURRENT_TIMESTAMP,
  `valor` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `potenciometro`
--

LOCK TABLES `potenciometro` WRITE;
/*!40000 ALTER TABLE `potenciometro` DISABLE KEYS */;
/*!40000 ALTER TABLE `potenciometro` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sensores`
--

DROP TABLE IF EXISTS `sensores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sensores` (
  `id` int NOT NULL AUTO_INCREMENT,
  `tipo` varchar(50) DEFAULT NULL,
  `valor` float DEFAULT NULL,
  `fecha_hora` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sensores`
--

LOCK TABLES `sensores` WRITE;
/*!40000 ALTER TABLE `sensores` DISABLE KEYS */;
/*!40000 ALTER TABLE `sensores` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `temperatura`
--

DROP TABLE IF EXISTS `temperatura`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `temperatura` (
  `id` int NOT NULL AUTO_INCREMENT,
  `valor` float DEFAULT NULL,
  `timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `temperatura`
--

LOCK TABLES `temperatura` WRITE;
/*!40000 ALTER TABLE `temperatura` DISABLE KEYS */;
/*!40000 ALTER TABLE `temperatura` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ventilacion`
--

DROP TABLE IF EXISTS `ventilacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ventilacion` (
  `id` int NOT NULL AUTO_INCREMENT,
  `fecha` datetime DEFAULT CURRENT_TIMESTAMP,
  `estado` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ventilacion`
--

LOCK TABLES `ventilacion` WRITE;
/*!40000 ALTER TABLE `ventilacion` DISABLE KEYS */;
/*!40000 ALTER TABLE `ventilacion` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-09-23 16:51:27
