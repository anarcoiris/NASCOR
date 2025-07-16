-- Asegúrate de usar la BD
USE `ciberseguridad-pIII`;

-- Borra las tablas si existen para evitar duplicados
DROP TABLE IF EXISTS `user_login_data`;
DROP TABLE IF EXISTS `user_account`;
DROP TABLE IF EXISTS `hashing_algorithms`;
DROP TABLE IF EXISTS `email_validation_status`;

CREATE TABLE `email_validation_status` (
  `EmailValidationStatusId` INT NOT NULL,
  `StatusDescription` VARCHAR(20) NOT NULL,
  PRIMARY KEY (`EmailValidationStatusId`)
) ENGINE=InnoDB;

INSERT INTO `email_validation_status` VALUES
  (1, 'Validated'),
  (2, 'Pending'),
  (3, 'Failed');

CREATE TABLE `hashing_algorithms` (
  `HashAlgorithmId` INT NOT NULL,
  `AlgorithmName` VARCHAR(10) NOT NULL,
  PRIMARY KEY (`HashAlgorithmId`)
) ENGINE=InnoDB;

INSERT INTO `hashing_algorithms` VALUES
  (1, 'MD5'),
  (2, 'SHA256'),
  (3, 'BCRYPT');

CREATE TABLE `user_account` (
  `UserId` INT NOT NULL,
  `FirstName` VARCHAR(100) NOT NULL,
  `LastName` VARCHAR(100) NOT NULL,
  `Gender` CHAR(1),
  `DateOfBirth` DATE,
  PRIMARY KEY (`UserId`)
) ENGINE=InnoDB;

INSERT INTO `user_account` VALUES
  (1, 'John', 'Doe', 'M', '1990-05-15'),
  (2, 'Jane', 'Smith', 'F', '1985-10-23'),
  (3, 'Alice', 'Brown', 'F', '1992-08-14');

CREATE TABLE `user_login_data` (
  `UserId` INT NOT NULL,
  `LoginName` VARCHAR(20) NOT NULL,
  `PasswordHash` VARCHAR(250) NOT NULL,
  `PasswordSalt` VARCHAR(100) NOT NULL,
  `HashAlgorithmId` INT,
  `EmailAddress` VARCHAR(100) NOT NULL,
  `ConfirmationToken` VARCHAR(100),
  `TokenGenerationTime` TIMESTAMP NULL,
  `EmailValidationStatusId` INT,
  `PasswordRecoveryToken` VARCHAR(100),
  `RecoveryTokenTime` TIMESTAMP NULL,
  PRIMARY KEY (`UserId`),
  UNIQUE (`LoginName`),
  UNIQUE (`EmailAddress`),
  FOREIGN KEY (`UserId`) REFERENCES `user_account`(`UserId`),
  FOREIGN KEY (`HashAlgorithmId`) REFERENCES `hashing_algorithms`(`HashAlgorithmId`),
  FOREIGN KEY (`EmailValidationStatusId`) REFERENCES `email_validation_status`(`EmailValidationStatusId`)
) ENGINE=InnoDB;

INSERT INTO `user_login_data` VALUES
  (1, 'johndoe', '56cf72d803180e3ce8ef9a1aae0c5ffc', 'salt1', 1, 'john.doe@example.com', 'token123', '2024-11-09 21:22:28', 1, 'recovery123', '2024-11-09 21:22:28'),
  (2, 'janesmith', '42f15052ad017501bb8fbac3e976fb23', 'salt2', 1, 'jane.smith@example.com', 'token456', '2024-11-09 21:22:28', 2, 'recovery456', '2024-11-09 21:22:28'),
  (3, 'alicebrown', '24daa079f496c06a0df4e486d69c56b9', 'salt3', 1, 'alice.brown@example.com', 'token789', '2024-11-09 21:22:28', 3, 'recovery789', '2024-11-09 21:22:28');
