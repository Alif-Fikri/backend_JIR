-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               8.0.30 - MySQL Community Server - GPL
-- Server OS:                    Win64
-- HeidiSQL Version:             12.1.0.6537
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Dumping database structure for auth_db
CREATE DATABASE IF NOT EXISTS `auth_db` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `auth_db`;

-- Dumping structure for table auth_db.blacklisted_tokens
CREATE TABLE IF NOT EXISTS `blacklisted_tokens` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `token` varchar(512) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  UNIQUE KEY `token` (`token`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table auth_db.blacklisted_tokens: ~0 rows (approximately)

-- Dumping structure for table auth_db.users
CREATE TABLE IF NOT EXISTS `users` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(50) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `hashed_password` varchar(255) DEFAULT NULL,
  `google_id` varchar(255) DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT '1',
  `is_admin` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table auth_db.users: ~2 rows (approximately)
INSERT INTO `users` (`id`, `username`, `email`, `hashed_password`, `google_id`, `is_active`, `is_admin`) VALUES
	(1, 'a', 'a@gmail.com', '$2b$12$mJeAC/Be2u40tAg/BkMUWuIgBUCsBcnh/EMJn/shvFPAjzz12MuS6', NULL, 1, 0),
	(2, 'q', 'q@gmail.com', '$2b$12$zGQrFHeo1pWzPCn1Q6hkN.ktW6My1N5Bb9Uok1Q7mtyMvDAzHzdOG', NULL, 1, 0);


-- Dumping database structure for jakarta_parks
CREATE DATABASE IF NOT EXISTS `jakarta_parks` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `jakarta_parks`;

-- Dumping structure for table jakarta_parks.addresses
CREATE TABLE IF NOT EXISTS `addresses` (
  `id` int NOT NULL AUTO_INCREMENT,
  `park_id` int DEFAULT NULL,
  `street` varchar(255) DEFAULT NULL,
  `subdistrict` varchar(100) DEFAULT NULL,
  `district` varchar(100) DEFAULT NULL,
  `postcode` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `park_id` (`park_id`),
  KEY `ix_addresses_id` (`id`),
  CONSTRAINT `addresses_ibfk_1` FOREIGN KEY (`park_id`) REFERENCES `parks` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table jakarta_parks.addresses: ~0 rows (approximately)

-- Dumping structure for table jakarta_parks.facilities
CREATE TABLE IF NOT EXISTS `facilities` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `ix_facilities_id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table jakarta_parks.facilities: ~0 rows (approximately)

-- Dumping structure for table jakarta_parks.parks
CREATE TABLE IF NOT EXISTS `parks` (
  `id` int NOT NULL AUTO_INCREMENT,
  `osm_id` int DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `latitude` float DEFAULT NULL,
  `longitude` float DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `osm_id` (`osm_id`),
  KEY `ix_parks_id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table jakarta_parks.parks: ~0 rows (approximately)

-- Dumping structure for table jakarta_parks.park_facility
CREATE TABLE IF NOT EXISTS `park_facility` (
  `park_id` int NOT NULL,
  `facility_id` int NOT NULL,
  PRIMARY KEY (`park_id`,`facility_id`),
  KEY `facility_id` (`facility_id`),
  CONSTRAINT `park_facility_ibfk_1` FOREIGN KEY (`park_id`) REFERENCES `parks` (`id`),
  CONSTRAINT `park_facility_ibfk_2` FOREIGN KEY (`facility_id`) REFERENCES `facilities` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table jakarta_parks.park_facility: ~0 rows (approximately)

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
