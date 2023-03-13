-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Mar 13, 2023 at 09:51 PM
-- Server version: 10.6.7-MariaDB-2ubuntu1.1
-- PHP Version: 8.1.2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `defensio`
--

-- --------------------------------------------------------

--
-- Table structure for table `engines`
--

CREATE TABLE `engines` (
  `id_engines_DB` int(11) NOT NULL,
  `identity` varchar(20) NOT NULL,
  `token` varchar(12) DEFAULT NULL,
  `location` varchar(50) DEFAULT NULL,
  `last_check_ND` datetime DEFAULT NULL,
  `last_check_VA` datetime DEFAULT NULL,
  `last_check_SS` datetime DEFAULT NULL,
  `last_check_WS` datetime DEFAULT NULL,
  `codeword` varchar(20) DEFAULT NULL,
  `active_defensio` varchar(12) DEFAULT NULL,
  `active_webscanner` varchar(12) DEFAULT NULL,
  `active_openvas` varchar(12) DEFAULT NULL,
  `active_suricata` varchar(12) DEFAULT NULL,
  `active_share_scanner` varchar(20) DEFAULT NULL,
  `defensio_ATTIVO` varchar(5) NOT NULL DEFAULT 'off'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `engines`
--

INSERT INTO `engines` (`id_engines_DB`, `identity`, `token`, `location`, `last_check_ND`, `last_check_VA`, `last_check_SS`, `last_check_WS`, `codeword`, `active_defensio`, `active_webscanner`, `active_openvas`, `active_suricata`, `active_share_scanner`, `defensio_ATTIVO`) VALUES
(1, 'HomeAdry', 'wmEgi9sSxLIl', 'Istrana', '2023-03-13 21:51:02', '2023-03-13 21:51:02', '2023-03-13 21:51:03', '2023-03-13 21:51:10', '133', 'Attivo', 'Attivo', 'Attivo', 'Attivo', 'Attivo', 'on'),
(2, 'fidem_soc', 'DIdXmNmU6Fbl', 'verona', '2023-01-04 16:37:11', '2023-01-04 16:37:05', NULL, NULL, '145', 'rKjxlhHZPDwT', 'DIdXmNmU6Fbl', 'DIdXmNmU6Fbl', NULL, NULL, 'off'),
(3, 'fixAdry', '0LU7vMeBFOEG', 'Istrana', '2023-02-07 14:41:37', '2023-02-07 14:41:37', '2023-02-07 14:41:17', '2023-02-07 14:41:17', '144', 'ERR_C2_OFF', 'ERR_C2_OFF', 'ERR_C2_OFF', NULL, 'ERR_C2_OFF', 'off'),
(34, 'VM_Istrana', 'aJLaKVZ2DM2W', 'Istrana', '2022-12-22 14:16:44', '2022-12-22 14:16:49', NULL, NULL, '33', '0YK8Q9CWLZfF', 'OS66Mpc3716A', 'OS66Mpc3716A', NULL, NULL, 'off');

-- --------------------------------------------------------

--
-- Table structure for table `suricata_alert`
--

CREATE TABLE `suricata_alert` (
  `id_result_alert` int(11) NOT NULL,
  `timestamp` varchar(80) DEFAULT NULL,
  `id_asset` varchar(20) NOT NULL,
  `src_ip` varchar(50) DEFAULT NULL,
  `src_port` varchar(10) DEFAULT NULL,
  `dest_ip` varchar(50) DEFAULT NULL,
  `dest_port` varchar(10) DEFAULT NULL,
  `proto` varchar(10) DEFAULT NULL,
  `action` varchar(50) DEFAULT NULL,
  `gid` varchar(10) DEFAULT NULL,
  `signature_id` varchar(50) DEFAULT NULL,
  `rev` varchar(20) DEFAULT NULL,
  `signature` varchar(2000) DEFAULT NULL,
  `category` varchar(1000) DEFAULT NULL,
  `severity` int(3) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(10) NOT NULL,
  `username` varchar(50) NOT NULL,
  `fullname` varchar(75) NOT NULL,
  `password` varchar(50) NOT NULL,
  `email` varchar(75) NOT NULL,
  `active` tinyint(1) NOT NULL,
  `categoria` varchar(50) DEFAULT NULL,
  `avatar` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `username`, `fullname`, `password`, `email`, `active`, `categoria`, `avatar`) VALUES
(2, 'adriano.condro@gmail.com', 'Adriano Condro', '!?p4ssw0rd!?', 'adriano.condro@gmail.com', 1, 'Administrator', NULL),
(3, 'demouser@fidemsrl.it', 'Demo User', '!?d3m0us3r?!', 'demouser@fidemsrl.it', 1, 'User', ''),
(4, 'carmine.buono@fidemsrl.it', 'Carmine Buono', '!?p4ssw0rd!?', 'carmine.buono@fidemsrl.it', 1, 'Administrator', NULL),
(5, 'demis.menon@fidemsrl.it', 'Demis Menon', '!?p4ssw0rd!?', 'demis.menon@fidemsrl.it', 1, 'Administrator', NULL),
(6, 'giovanni.finetto@fidemsrl.it', 'Giovanni Finetto', '!?p4ssw0rd!?', 'giovanni.finetto@fidemsrl.it', 1, 'Administrator', NULL),
(7, 'soc-2@fidemsrl.it', 'Leonardo Tamellini', '!?p4ssw0rd!?', 'soc-2@fidemsrl.it', 1, 'Administrator', NULL),
(8, 'demoadmin@fidemsrl.it', 'Demo Admin', '!?d3mo4dm1n!?', 'demoadmin@fidemsrl.it', 1, 'Administrator', NULL);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `engines`
--
ALTER TABLE `engines`
  ADD PRIMARY KEY (`id_engines_DB`);

--
-- Indexes for table `suricata_alert`
--
ALTER TABLE `suricata_alert`
  ADD PRIMARY KEY (`id_result_alert`),
  ADD UNIQUE KEY `timestamp` (`timestamp`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `engines`
--
ALTER TABLE `engines`
  MODIFY `id_engines_DB` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=35;

--
-- AUTO_INCREMENT for table `suricata_alert`
--
ALTER TABLE `suricata_alert`
  MODIFY `id_result_alert` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
