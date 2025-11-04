-- MySQL dump 10.13  Distrib 8.0.43, for Win64 (x86_64)
--
-- Host: 10.29.128.134    Database: Vestuario
-- ------------------------------------------------------
-- Server version	5.5.5-10.4.28-MariaDB

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
-- Table structure for table `Salidas`
--

DROP TABLE IF EXISTS `Salidas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Salidas` (
  `idSalidas` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `Salida` datetime NOT NULL,
  `Folio` bigint(12) NOT NULL,
  `Area` varchar(50) NOT NULL,
  `CODIGO` varchar(50) NOT NULL,
  `Solicitante` varchar(45) NOT NULL,
  `IdUsr` int(11) NOT NULL,
  `AutorizadoPor` varchar(50) DEFAULT NULL,
  `OBS` varchar(255) DEFAULT NULL,
  `Cant` int(11) NOT NULL,
  `Talento` varchar(255) DEFAULT NULL,
  `Muerto` tinyint(4) NOT NULL DEFAULT 0,
  `ActualizadoEn` datetime NOT NULL DEFAULT current_timestamp(),
  `Es1vez` tinyint(4) NOT NULL DEFAULT 0,
  `IdSolicitante` int(11) NOT NULL,
  `UltimoPedido` datetime DEFAULT NULL,
  `IdStatus` int(11) DEFAULT NULL,
  PRIMARY KEY (`idSalidas`)
) ENGINE=InnoDB AUTO_INCREMENT=52 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-08-29 11:25:28
