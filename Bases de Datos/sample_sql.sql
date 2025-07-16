-- --------------------------------------------------------
-- Host:                         localhost
-- Versión del servidor:         9.0.1 - MySQL Community Server - GPL
-- SO del servidor:              Linux
-- HeidiSQL Versión:             11.0.0.5919
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- Volcando estructura de base de datos para ciberseguridad-pIII
CREATE DATABASE IF NOT EXISTS `ciberseguridad-pIII` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `ciberseguridad-pIII`;

-- Volcando estructura para tabla ciberseguridad-pIII.email_validation_status
CREATE TABLE IF NOT EXISTS `email_validation_status` (
  `EmailValidationStatusId` int NOT NULL,
  `StatusDescription` varchar(20) NOT NULL,
  PRIMARY KEY (`EmailValidationStatusId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla ciberseguridad-pIII.email_validation_status: ~3 rows (aproximadamente)
/*!40000 ALTER TABLE `email_validation_status` DISABLE KEYS */;
INSERT INTO `email_validation_status` (`EmailValidationStatusId`, `StatusDescription`) VALUES
	(1, 'Validated'),
	(2, 'Pending'),
	(3, 'Failed');
/*!40000 ALTER TABLE `email_validation_status` ENABLE KEYS */;

-- Volcando estructura para tabla ciberseguridad-pIII.hashing_algorithms
CREATE TABLE IF NOT EXISTS `hashing_algorithms` (
  `HashAlgorithmId` int NOT NULL,
  `AlgorithmName` varchar(10) NOT NULL,
  PRIMARY KEY (`HashAlgorithmId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla ciberseguridad-pIII.hashing_algorithms: ~3 rows (aproximadamente)
/*!40000 ALTER TABLE `hashing_algorithms` DISABLE KEYS */;
INSERT INTO `hashing_algorithms` (`HashAlgorithmId`, `AlgorithmName`) VALUES
	(1, 'MD5'),
	(2, 'SHA256'),
	(3, 'BCRYPT');
/*!40000 ALTER TABLE `hashing_algorithms` ENABLE KEYS */;

-- Volcando estructura para tabla ciberseguridad-pIII.user_account
CREATE TABLE IF NOT EXISTS `user_account` (
  `UserId` int NOT NULL,
  `FirstName` varchar(100) NOT NULL,
  `LastName` varchar(100) NOT NULL,
  `Gender` char(1) DEFAULT NULL,
  `DateOfBirth` date DEFAULT NULL,
  PRIMARY KEY (`UserId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla ciberseguridad-pIII.user_account: ~3 rows (aproximadamente)
/*!40000 ALTER TABLE `user_account` DISABLE KEYS */;
INSERT INTO `user_account` (`UserId`, `FirstName`, `LastName`, `Gender`, `DateOfBirth`) VALUES
	(1, 'John', 'Doe', 'M', '1990-05-15'),
	(2, 'Jane', 'Smith', 'F', '1985-10-23'),
	(3, 'Alice', 'Brown', 'F', '1992-08-14');
/*!40000 ALTER TABLE `user_account` ENABLE KEYS */;

-- Volcando estructura para tabla ciberseguridad-pIII.user_login_data
CREATE TABLE IF NOT EXISTS `user_login_data` (
  `UserId` int NOT NULL,
  `LoginName` varchar(20) NOT NULL,
  `PasswordHash` varchar(250) NOT NULL,
  `PasswordSalt` varchar(100) NOT NULL,
  `HashAlgorithmId` int DEFAULT NULL,
  `EmailAddress` varchar(100) NOT NULL,
  `ConfirmationToken` varchar(100) DEFAULT NULL,
  `TokenGenerationTime` timestamp NULL DEFAULT NULL,
  `EmailValidationStatusId` int DEFAULT NULL,
  `PasswordRecoveryToken` varchar(100) DEFAULT NULL,
  `RecoveryTokenTime` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`UserId`),
  UNIQUE KEY `LoginName` (`LoginName`),
  UNIQUE KEY `EmailAddress` (`EmailAddress`),
  KEY `HashAlgorithmId` (`HashAlgorithmId`),
  KEY `EmailValidationStatusId` (`EmailValidationStatusId`),
  CONSTRAINT `user_login_data_ibfk_1` FOREIGN KEY (`UserId`) REFERENCES `user_account` (`UserId`),
  CONSTRAINT `user_login_data_ibfk_2` FOREIGN KEY (`HashAlgorithmId`) REFERENCES `hashing_algorithms` (`HashAlgorithmId`),
  CONSTRAINT `user_login_data_ibfk_3` FOREIGN KEY (`EmailValidationStatusId`) REFERENCES `email_validation_status` (`EmailValidationStatusId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla ciberseguridad-pIII.user_login_data: ~3 rows (aproximadamente)
/*!40000 ALTER TABLE `user_login_data` DISABLE KEYS */;
INSERT INTO `user_login_data` (`UserId`, `LoginName`, `PasswordHash`, `PasswordSalt`, `HashAlgorithmId`, `EmailAddress`, `ConfirmationToken`, `TokenGenerationTime`, `EmailValidationStatusId`, `PasswordRecoveryToken`, `RecoveryTokenTime`) VALUES
	(1, 'johndoe', '56cf72d803180e3ce8ef9a1aae0c5ffc', 'salt1', 1, 'john.doe@example.com', 'token123', '2024-11-09 21:22:28', 1, 'recovery123', '2024-11-09 21:22:28'),
	(2, 'janesmith', '42f15052ad017501bb8fbac3e976fb23', 'salt2', 1, 'jane.smith@example.com', 'token456', '2024-11-09 21:22:28', 2, 'recovery456', '2024-11-09 21:22:28'),
	(3, 'alicebrown', '24daa079f496c06a0df4e486d69c56b9', 'salt3', 1, 'alice.brown@example.com', 'token789', '2024-11-09 21:22:28', 3, 'recovery789', '2024-11-09 21:22:28');
/*!40000 ALTER TABLE `user_login_data` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
