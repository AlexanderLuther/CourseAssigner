--
-- Current Database: `COURSE_ASSIGNER`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `COURSE_ASSIGNER` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */;

USE `COURSE_ASSIGNER`;

--
-- Table structure for table `CAREER`
--

DROP TABLE IF EXISTS `CAREER`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `CAREER` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `description` text DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `CAREER`
--

LOCK TABLES `CAREER` WRITE;
/*!40000 ALTER TABLE `CAREER` DISABLE KEYS */;
INSERT INTO `CAREER` VALUES
(1,'Industrial'),
(2,'Mecanica'),
(3,'Civil'),
(4,'Mecanica Industrial'),
(5,'Sistemas');
/*!40000 ALTER TABLE `CAREER` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `CLASSROOM`
--

DROP TABLE IF EXISTS `CLASSROOM`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `CLASSROOM` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `description` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `CLASSROOM`
--

LOCK TABLES `CLASSROOM` WRITE;
/*!40000 ALTER TABLE `CLASSROOM` DISABLE KEYS */;
/*!40000 ALTER TABLE `CLASSROOM` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `COURSE`
--

DROP TABLE IF EXISTS `COURSE`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `COURSE` (
  `code` varchar(10) NOT NULL,
  `name` text NOT NULL,
  `id_career` int(11) NOT NULL,
  `id_semester` int(11) NOT NULL,
  `id_section` int(11) NOT NULL,
  `id_course_type` int(11) NOT NULL,
  PRIMARY KEY (`code`),
  KEY `COURSE_CAREER_id_fk` (`id_career`),
  KEY `COURSE_COURSE_TYPE_id_fk` (`id_course_type`),
  KEY `COURSE_SECTION_id_fk` (`id_section`),
  KEY `COURSE_SEMESTER_id_fk` (`id_semester`),
  CONSTRAINT `COURSE_CAREER_id_fk` FOREIGN KEY (`id_career`) REFERENCES `CAREER` (`id`),
  CONSTRAINT `COURSE_COURSE_TYPE_id_fk` FOREIGN KEY (`id_course_type`) REFERENCES `COURSE_TYPE` (`id`),
  CONSTRAINT `COURSE_SECTION_id_fk` FOREIGN KEY (`id_section`) REFERENCES `SECTION` (`id`),
  CONSTRAINT `COURSE_SEMESTER_id_fk` FOREIGN KEY (`id_semester`) REFERENCES `SEMESTER` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `COURSE`
--

LOCK TABLES `COURSE` WRITE;
/*!40000 ALTER TABLE `COURSE` DISABLE KEYS */;
/*!40000 ALTER TABLE `COURSE` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `COURSE_TYPE`
--

DROP TABLE IF EXISTS `COURSE_TYPE`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `COURSE_TYPE` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `description` text DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `COURSE_TYPE`
--

LOCK TABLES `COURSE_TYPE` WRITE;
/*!40000 ALTER TABLE `COURSE_TYPE` DISABLE KEYS */;
INSERT INTO `COURSE_TYPE` VALUES
(1,'Optativo'),
(2,'Obligatorio');
/*!40000 ALTER TABLE `COURSE_TYPE` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `PERIOD`
--

DROP TABLE IF EXISTS `PERIOD`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `PERIOD` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `start_time` time DEFAULT NULL,
  `end_time` time DEFAULT NULL,
  `description` text DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `PERIOD`
--

LOCK TABLES `PERIOD` WRITE;
/*!40000 ALTER TABLE `PERIOD` DISABLE KEYS */;
INSERT INTO `PERIOD` VALUES
(1,'13:40:00','14:30:00','Periodo 1'),
(2,'14:30:00','15:20:00','Periodo 2'),
(3,'15:20:00','16:10:00','Periodo 3'),
(4,'16:10:00','17:00:00','Periodo 4'),
(5,'17:00:00','17:50:00','Periodo 5'),
(6,'17:50:00','18:40:00','Periodo 6'),
(7,'18:40:00','19:30:00','Periodo 7'),
(8,'19:30:00','20:20:00','Periodo 8'),
(9,'20:20:00','21:10:00','Periodo 9');
/*!40000 ALTER TABLE `PERIOD` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `SECTION`
--

DROP TABLE IF EXISTS `SECTION`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `SECTION` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `description` text DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `SECTION`
--

LOCK TABLES `SECTION` WRITE;
/*!40000 ALTER TABLE `SECTION` DISABLE KEYS */;
INSERT INTO `SECTION` VALUES
(1,'A'),
(2,'B'),
(3,'C'),
(4,'D'),
(5,'E'),
(6,'F'),
(7,'G'),
(8,'H'),
(9,'I'),
(10,'J'),
(11,'K'),
(12,'L');
/*!40000 ALTER TABLE `SECTION` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `SEMESTER`
--

DROP TABLE IF EXISTS `SEMESTER`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `SEMESTER` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `description` text DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `SEMESTER`
--

LOCK TABLES `SEMESTER` WRITE;
/*!40000 ALTER TABLE `SEMESTER` DISABLE KEYS */;
INSERT INTO `SEMESTER` VALUES
(1,'1er Semestre'),
(2,'2do Semestre'),
(3,'3er Semestre'),
(4,'4to Semestre'),
(5,'5to Semestre'),
(6,'6to Semestre'),
(7,'7mo Semestre'),
(8,'8vo Semestre'),
(9,'9no Semestre'),
(10,'10mo Semestre');
/*!40000 ALTER TABLE `SEMESTER` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `TEACHER`
--

DROP TABLE IF EXISTS `TEACHER`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `TEACHER` (
  `id` varchar(10) NOT NULL,
  `name` text NOT NULL,
  `entry_time` time NOT NULL,
  `departure_time` time NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `TEACHER`
--

LOCK TABLES `TEACHER` WRITE;
/*!40000 ALTER TABLE `TEACHER` DISABLE KEYS */;
/*!40000 ALTER TABLE `TEACHER` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `TIME`
--

DROP TABLE IF EXISTS `TIME`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `TIME` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `time` time NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `TIME`
--

LOCK TABLES `TIME` WRITE;
/*!40000 ALTER TABLE `TIME` DISABLE KEYS */;
INSERT INTO `TIME` VALUES
(1,'13:40:00'),
(2,'14:30:00'),
(3,'15:20:00'),
(4,'16:10:00'),
(5,'17:00:00'),
(6,'17:50:00'),
(7,'18:40:00'),
(8,'19:30:00'),
(9,'20:20:00'),
(10,'21:10:00');
/*!40000 ALTER TABLE `TIME` ENABLE KEYS */;
UNLOCK TABLES;
