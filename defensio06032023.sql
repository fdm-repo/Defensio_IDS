-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Mar 06, 2023 at 03:08 PM
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
-- Table structure for table `arachni_report`
--

CREATE TABLE `arachni_report` (
  `id_arac_report` int(11) NOT NULL,
  `id_job` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `email_leak_result`
--

CREATE TABLE `email_leak_result` (
  `Id_leak_result` int(11) NOT NULL,
  `email` varchar(200) DEFAULT NULL,
  `Id_leak_HBP` varchar(1000) DEFAULT NULL,
  `source` varchar(1000) DEFAULT NULL,
  `title` varchar(500) DEFAULT NULL,
  `date` varchar(200) DEFAULT NULL,
  `emailcount` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `email_leak_target`
--

CREATE TABLE `email_leak_target` (
  `Id_leak_target` int(11) NOT NULL,
  `email` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

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
(1, 'HomeAdry', 'wmEgi9sSxLIl', 'Istrana', '2023-03-05 23:35:12', '2023-03-05 23:35:15', '2023-03-05 23:49:53', '2023-03-05 23:35:22', '133', 'ERR_C2_OFF', 'ERR_C2_OFF', 'ERR_C2_OFF', 'ERR_C2_OFF', 'ERR_C2_OFF', 'on'),
(2, 'fidem_soc', 'DIdXmNmU6Fbl', 'verona', '2023-01-04 16:37:11', '2023-01-04 16:37:05', NULL, NULL, '145', 'rKjxlhHZPDwT', 'DIdXmNmU6Fbl', 'DIdXmNmU6Fbl', NULL, NULL, 'off'),
(3, 'fixAdry', '0LU7vMeBFOEG', 'Istrana', '2023-02-07 14:41:37', '2023-02-07 14:41:37', '2023-02-07 14:41:17', '2023-02-07 14:41:17', '144', 'ERR_C2_OFF', 'ERR_C2_OFF', 'ERR_C2_OFF', NULL, 'ERR_C2_OFF', 'off'),
(34, 'VM_Istrana', 'aJLaKVZ2DM2W', 'Istrana', '2022-12-22 14:16:44', '2022-12-22 14:16:49', NULL, NULL, '33', '0YK8Q9CWLZfF', 'OS66Mpc3716A', 'OS66Mpc3716A', NULL, NULL, 'off');

-- --------------------------------------------------------

--
-- Table structure for table `host`
--

CREATE TABLE `host` (
  `id` int(11) NOT NULL,
  `id_job` int(11) NOT NULL,
  `start_job` datetime NOT NULL,
  `ip` varchar(20) DEFAULT NULL,
  `hostname` varchar(255) DEFAULT NULL,
  `os_name` varchar(200) DEFAULT NULL,
  `os_accuracy` varchar(4) DEFAULT NULL,
  `type` varchar(200) DEFAULT NULL,
  `vendor` varchar(200) DEFAULT NULL,
  `osfamily` varchar(200) DEFAULT NULL,
  `osgen` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `job`
--

CREATE TABLE `job` (
  `id_job` int(11) NOT NULL,
  `id_asset` int(11) NOT NULL,
  `nome` varchar(50) NOT NULL,
  `ip` varchar(50) NOT NULL,
  `netmask` varchar(20) NOT NULL,
  `single_port` varchar(6) DEFAULT NULL,
  `low_port` varchar(6) DEFAULT NULL,
  `high_port` varchar(6) DEFAULT NULL,
  `public_ip` varchar(2) DEFAULT 'no',
  `abilitato` varchar(5) NOT NULL DEFAULT 'off',
  `net_discovery` varchar(5) NOT NULL DEFAULT 'off',
  `arachni` varchar(5) NOT NULL DEFAULT 'off',
  `enumforlinux` varchar(3) NOT NULL DEFAULT 'off',
  `openvas` varchar(3) NOT NULL DEFAULT 'off',
  `eseguito_openvas` varchar(3) NOT NULL DEFAULT 'off',
  `eseguito_arachni` varchar(3) DEFAULT 'off',
  `eseguito_enum4linux` varchar(3) DEFAULT 'off',
  `utente` varchar(50) DEFAULT NULL,
  `exclude_ip` varchar(2000) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `openvas_ref`
--

CREATE TABLE `openvas_ref` (
  `id_ref_DB` int(11) NOT NULL,
  `id_result` varchar(50) DEFAULT NULL,
  `ref` varchar(1000) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `openvas_report`
--

CREATE TABLE `openvas_report` (
  `id_report_DB` int(11) NOT NULL,
  `id_job` varchar(10) DEFAULT NULL,
  `id_report` varchar(50) DEFAULT NULL,
  `id_task` varchar(50) DEFAULT NULL,
  `scan_start` varchar(20) DEFAULT NULL,
  `scan_end` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `openvas_result`
--

CREATE TABLE `openvas_result` (
  `id_result_DB` int(11) NOT NULL,
  `id_report` varchar(50) DEFAULT NULL,
  `id_result` varchar(50) DEFAULT NULL,
  `name_vul` varchar(200) DEFAULT NULL,
  `host` varchar(50) DEFAULT NULL,
  `port` varchar(50) DEFAULT NULL,
  `nvt` varchar(100) DEFAULT NULL,
  `threat` varchar(50) DEFAULT NULL,
  `severity` varchar(50) DEFAULT NULL,
  `description` longtext DEFAULT NULL,
  `type_verification` varchar(200) DEFAULT NULL,
  `family` varchar(300) DEFAULT NULL,
  `t_summary` varchar(1000) DEFAULT NULL,
  `t_insight` varchar(2000) DEFAULT NULL,
  `t_affected` varchar(2000) DEFAULT NULL,
  `t_impact` varchar(2000) DEFAULT NULL,
  `t_solution` varchar(2000) DEFAULT NULL,
  `t_vuldetect` varchar(2000) DEFAULT NULL,
  `t_solution_type` varchar(2000) DEFAULT NULL,
  `solution` varchar(2000) DEFAULT NULL,
  `solution_type` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Triggers `openvas_result`
--
DELIMITER $$
CREATE TRIGGER `statistic Log` AFTER INSERT ON `openvas_result` FOR EACH ROW UPDATE statistic_job SET statistic_job.Log = (SELECT COUNT(openvas_result.threat) FROM openvas_result WHERE openvas_result.threat ='Log') WHERE statistic_job.id_statistic ='1'
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `openvas_scan`
--

CREATE TABLE `openvas_scan` (
  `id_job` varchar(11) NOT NULL,
  `id_task` varchar(40) NOT NULL,
  `status` varchar(20) NOT NULL,
  `progression` varchar(3) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `Port`
--

CREATE TABLE `Port` (
  `id_port` int(11) NOT NULL,
  `id_job` int(11) NOT NULL,
  `ip` varchar(20) NOT NULL,
  `port_n` varchar(6) NOT NULL,
  `name` varchar(25) NOT NULL,
  `state` varchar(20) NOT NULL,
  `reason` varchar(20) NOT NULL,
  `product` varchar(50) NOT NULL,
  `version` varchar(50) NOT NULL,
  `info` varchar(250) NOT NULL,
  `start_job` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `scheduling`
--

CREATE TABLE `scheduling` (
  `id_sched` int(11) NOT NULL,
  `id_job` int(11) DEFAULT NULL,
  `en_weekday` varchar(3) NOT NULL DEFAULT 'off',
  `en_monthday` varchar(3) NOT NULL DEFAULT 'off',
  `en_day` varchar(3) NOT NULL DEFAULT 'off',
  `weekday` varchar(20) DEFAULT 'undefined',
  `monthday` varchar(20) DEFAULT 'undefined',
  `orario` varchar(10) DEFAULT 'undefined',
  `utente` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `smb_bruteforce`
--

CREATE TABLE `smb_bruteforce` (
  `id_bruteforce` int(11) NOT NULL,
  `id_job` varchar(20) NOT NULL,
  `ip_host` varchar(20) DEFAULT NULL,
  `user` varchar(100) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL,
  `start_scan` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `smb_enum`
--

CREATE TABLE `smb_enum` (
  `id_smb_enum` datetime NOT NULL,
  `job` varchar(50) NOT NULL,
  `host` varchar(20) DEFAULT NULL,
  `user` varchar(50) DEFAULT NULL,
  `ldap` varchar(50) DEFAULT NULL,
  `samba` varchar(50) DEFAULT NULL,
  `dominio` varchar(50) DEFAULT NULL,
  `netbios_computer_name` varchar(50) DEFAULT NULL,
  `netbios_domain_name` varchar(50) DEFAULT NULL,
  `dns_domain` varchar(50) DEFAULT NULL,
  `fqdn` varchar(50) DEFAULT NULL,
  `derived_membership` varchar(50) DEFAULT NULL,
  `derived_domain` varchar(50) DEFAULT NULL,
  `sessions_possible` varchar(5) DEFAULT NULL,
  `sessions_null` varchar(5) DEFAULT NULL,
  `sessions_password` varchar(50) DEFAULT NULL,
  `sessions_kerberos` varchar(50) DEFAULT NULL,
  `sessions_nthash` varchar(50) DEFAULT NULL,
  `sessions_random_user` varchar(50) DEFAULT NULL,
  `rpc_domain` varchar(50) DEFAULT NULL,
  `rpc_domain_sid` varchar(50) DEFAULT NULL,
  `rpc_membership` varchar(50) DEFAULT NULL,
  `os` varchar(100) DEFAULT NULL,
  `os_version` varchar(100) DEFAULT NULL,
  `os_release` varchar(100) DEFAULT NULL,
  `os_build` varchar(100) DEFAULT NULL,
  `native_os` varchar(100) DEFAULT NULL,
  `native_lan_manager` varchar(100) DEFAULT NULL,
  `platform_id` varchar(100) DEFAULT NULL,
  `server_type` varchar(100) DEFAULT NULL,
  `server_type_sring` varchar(100) DEFAULT NULL,
  `domain_group` varchar(250) DEFAULT NULL,
  `policy_password_history_length` varchar(50) DEFAULT NULL,
  `policy_minimum_password_length` varchar(50) DEFAULT NULL,
  `policy_maximum_password_age` varchar(50) DEFAULT NULL,
  `policy_lockout_observation_window` varchar(50) DEFAULT NULL,
  `policy_lockout_duration` varchar(50) DEFAULT NULL,
  `policy_lockout_threshold` varchar(50) DEFAULT NULL,
  `policy_force_logoff_time` varchar(50) DEFAULT NULL,
  `printers` varchar(50) DEFAULT NULL,
  `start_scan` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `smb_errors`
--

CREATE TABLE `smb_errors` (
  `id_smb_error` int(11) NOT NULL,
  `job` varchar(50) NOT NULL,
  `host` varchar(50) NOT NULL,
  `id_smb_enum` datetime NOT NULL,
  `services` varchar(200) DEFAULT NULL,
  `sessions` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `smb_password_rules`
--

CREATE TABLE `smb_password_rules` (
  `id_smb_password_rules` int(11) NOT NULL,
  `job` varchar(50) NOT NULL,
  `host` varchar(50) NOT NULL,
  `id_smb_enum` datetime NOT NULL,
  `domain_pass_complex` varchar(200) DEFAULT NULL,
  `domain_pass_no_anon_change` varchar(200) DEFAULT NULL,
  `domain_pass_no_clear_change` varchar(200) DEFAULT NULL,
  `domain_pass_lockhout_admins` varchar(200) DEFAULT NULL,
  `domain_pass_store_cleartext` varchar(200) DEFAULT NULL,
  `domain_password_refuse_change` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `smb_share`
--

CREATE TABLE `smb_share` (
  `id_smb_share` int(11) NOT NULL,
  `job` varchar(50) NOT NULL,
  `host` varchar(50) NOT NULL,
  `id_smb_enum` datetime NOT NULL,
  `nome_condivisione` varchar(256) DEFAULT NULL,
  `type` varchar(50) DEFAULT NULL,
  `comment` varchar(200) DEFAULT NULL,
  `mapping` varchar(50) DEFAULT NULL,
  `listing` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `smb_sharing_bruteforce`
--

CREATE TABLE `smb_sharing_bruteforce` (
  `id_share_bruteforce` int(11) NOT NULL,
  `id_job` varchar(20) NOT NULL,
  `ip_host` varchar(20) NOT NULL,
  `username` varchar(100) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL,
  `nome_condivisione` varchar(256) DEFAULT NULL,
  `diritti` varchar(100) DEFAULT NULL,
  `file_dir` varchar(5) DEFAULT NULL,
  `percorso` varchar(257) DEFAULT NULL,
  `dimensione_file` varchar(20) DEFAULT NULL,
  `start_scan` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `smb_user`
--

CREATE TABLE `smb_user` (
  `id_smb_user` int(11) NOT NULL,
  `job` varchar(50) NOT NULL,
  `host` varchar(50) NOT NULL,
  `id_smb_enum` datetime NOT NULL,
  `username` varchar(50) DEFAULT NULL,
  `name` varchar(50) DEFAULT NULL,
  `acb` varchar(50) DEFAULT NULL,
  `description` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `statistic_job`
--

CREATE TABLE `statistic_job` (
  `id_statistic` int(11) NOT NULL,
  `id_job` int(11) DEFAULT NULL,
  `Log` int(11) DEFAULT NULL,
  `Medium` int(11) DEFAULT NULL,
  `High` int(11) DEFAULT NULL,
  `N_host` int(11) DEFAULT NULL,
  `N_service` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

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
-- Table structure for table `test_statistic_job`
--

CREATE TABLE `test_statistic_job` (
  `Id_test` int(11) NOT NULL,
  `Level` varchar(11) NOT NULL,
  `Value` int(11) NOT NULL
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

-- --------------------------------------------------------

--
-- Table structure for table `user_pass`
--

CREATE TABLE `user_pass` (
  `id_user_pass` int(11) NOT NULL,
  `username` varchar(200) DEFAULT NULL,
  `password` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `web_scanner_ref`
--

CREATE TABLE `web_scanner_ref` (
  `id_ref` int(11) NOT NULL,
  `digest` varchar(50) NOT NULL,
  `title` varchar(50) DEFAULT NULL,
  `url` varchar(300) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `web_scanner_report`
--

CREATE TABLE `web_scanner_report` (
  `id_report_web` int(11) NOT NULL,
  `id_job` int(10) NOT NULL,
  `ip` varchar(20) DEFAULT NULL,
  `port` varchar(20) DEFAULT NULL,
  `start_scan` varchar(50) DEFAULT NULL,
  `finish_scan` varchar(50) DEFAULT NULL,
  `id_report_seed` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `web_scanner_result`
--

CREATE TABLE `web_scanner_result` (
  `id_result` int(11) NOT NULL,
  `seed` varchar(50) NOT NULL,
  `name` varchar(200) DEFAULT NULL,
  `description` varchar(5000) DEFAULT NULL,
  `remedy_guidance` varchar(2000) DEFAULT NULL,
  `severity` varchar(50) DEFAULT NULL,
  `cwe` varchar(10) DEFAULT NULL,
  `digest` varchar(20) DEFAULT NULL,
  `vector_class` varchar(200) DEFAULT NULL,
  `vector_type` varchar(200) DEFAULT NULL,
  `vector_url` varchar(200) DEFAULT NULL,
  `vector_action` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `whois_result`
--

CREATE TABLE `whois_result` (
  `id_result_whois` int(11) NOT NULL,
  `id_job` varchar(10) NOT NULL,
  `ip_domain` varchar(200) NOT NULL,
  `result` varchar(16000) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `arachni_report`
--
ALTER TABLE `arachni_report`
  ADD PRIMARY KEY (`id_arac_report`);

--
-- Indexes for table `email_leak_result`
--
ALTER TABLE `email_leak_result`
  ADD PRIMARY KEY (`Id_leak_result`);

--
-- Indexes for table `email_leak_target`
--
ALTER TABLE `email_leak_target`
  ADD PRIMARY KEY (`Id_leak_target`);

--
-- Indexes for table `engines`
--
ALTER TABLE `engines`
  ADD PRIMARY KEY (`id_engines_DB`);

--
-- Indexes for table `host`
--
ALTER TABLE `host`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `job`
--
ALTER TABLE `job`
  ADD PRIMARY KEY (`id_job`);

--
-- Indexes for table `openvas_ref`
--
ALTER TABLE `openvas_ref`
  ADD PRIMARY KEY (`id_ref_DB`);

--
-- Indexes for table `openvas_report`
--
ALTER TABLE `openvas_report`
  ADD PRIMARY KEY (`id_report_DB`);

--
-- Indexes for table `openvas_result`
--
ALTER TABLE `openvas_result`
  ADD PRIMARY KEY (`id_result_DB`);

--
-- Indexes for table `openvas_scan`
--
ALTER TABLE `openvas_scan`
  ADD PRIMARY KEY (`id_task`),
  ADD UNIQUE KEY `id_task` (`id_task`);

--
-- Indexes for table `Port`
--
ALTER TABLE `Port`
  ADD PRIMARY KEY (`id_port`);

--
-- Indexes for table `scheduling`
--
ALTER TABLE `scheduling`
  ADD PRIMARY KEY (`id_sched`);

--
-- Indexes for table `smb_bruteforce`
--
ALTER TABLE `smb_bruteforce`
  ADD PRIMARY KEY (`id_bruteforce`);

--
-- Indexes for table `smb_enum`
--
ALTER TABLE `smb_enum`
  ADD PRIMARY KEY (`id_smb_enum`);

--
-- Indexes for table `smb_errors`
--
ALTER TABLE `smb_errors`
  ADD PRIMARY KEY (`id_smb_error`);

--
-- Indexes for table `smb_password_rules`
--
ALTER TABLE `smb_password_rules`
  ADD PRIMARY KEY (`id_smb_password_rules`);

--
-- Indexes for table `smb_share`
--
ALTER TABLE `smb_share`
  ADD PRIMARY KEY (`id_smb_share`);

--
-- Indexes for table `smb_sharing_bruteforce`
--
ALTER TABLE `smb_sharing_bruteforce`
  ADD PRIMARY KEY (`id_share_bruteforce`);

--
-- Indexes for table `smb_user`
--
ALTER TABLE `smb_user`
  ADD PRIMARY KEY (`id_smb_user`);

--
-- Indexes for table `statistic_job`
--
ALTER TABLE `statistic_job`
  ADD PRIMARY KEY (`id_statistic`);

--
-- Indexes for table `suricata_alert`
--
ALTER TABLE `suricata_alert`
  ADD PRIMARY KEY (`id_result_alert`),
  ADD UNIQUE KEY `timestamp` (`timestamp`);

--
-- Indexes for table `test_statistic_job`
--
ALTER TABLE `test_statistic_job`
  ADD PRIMARY KEY (`Id_test`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `user_pass`
--
ALTER TABLE `user_pass`
  ADD PRIMARY KEY (`id_user_pass`);

--
-- Indexes for table `web_scanner_ref`
--
ALTER TABLE `web_scanner_ref`
  ADD PRIMARY KEY (`id_ref`);

--
-- Indexes for table `web_scanner_report`
--
ALTER TABLE `web_scanner_report`
  ADD PRIMARY KEY (`id_report_web`);

--
-- Indexes for table `web_scanner_result`
--
ALTER TABLE `web_scanner_result`
  ADD PRIMARY KEY (`id_result`);

--
-- Indexes for table `whois_result`
--
ALTER TABLE `whois_result`
  ADD PRIMARY KEY (`id_result_whois`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `arachni_report`
--
ALTER TABLE `arachni_report`
  MODIFY `id_arac_report` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `email_leak_result`
--
ALTER TABLE `email_leak_result`
  MODIFY `Id_leak_result` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `email_leak_target`
--
ALTER TABLE `email_leak_target`
  MODIFY `Id_leak_target` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `engines`
--
ALTER TABLE `engines`
  MODIFY `id_engines_DB` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=35;

--
-- AUTO_INCREMENT for table `host`
--
ALTER TABLE `host`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `job`
--
ALTER TABLE `job`
  MODIFY `id_job` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `openvas_ref`
--
ALTER TABLE `openvas_ref`
  MODIFY `id_ref_DB` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `openvas_report`
--
ALTER TABLE `openvas_report`
  MODIFY `id_report_DB` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `openvas_result`
--
ALTER TABLE `openvas_result`
  MODIFY `id_result_DB` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `Port`
--
ALTER TABLE `Port`
  MODIFY `id_port` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `scheduling`
--
ALTER TABLE `scheduling`
  MODIFY `id_sched` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `smb_bruteforce`
--
ALTER TABLE `smb_bruteforce`
  MODIFY `id_bruteforce` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `smb_errors`
--
ALTER TABLE `smb_errors`
  MODIFY `id_smb_error` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `smb_password_rules`
--
ALTER TABLE `smb_password_rules`
  MODIFY `id_smb_password_rules` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `smb_share`
--
ALTER TABLE `smb_share`
  MODIFY `id_smb_share` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `smb_sharing_bruteforce`
--
ALTER TABLE `smb_sharing_bruteforce`
  MODIFY `id_share_bruteforce` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `smb_user`
--
ALTER TABLE `smb_user`
  MODIFY `id_smb_user` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `statistic_job`
--
ALTER TABLE `statistic_job`
  MODIFY `id_statistic` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `suricata_alert`
--
ALTER TABLE `suricata_alert`
  MODIFY `id_result_alert` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `test_statistic_job`
--
ALTER TABLE `test_statistic_job`
  MODIFY `Id_test` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `user_pass`
--
ALTER TABLE `user_pass`
  MODIFY `id_user_pass` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `web_scanner_ref`
--
ALTER TABLE `web_scanner_ref`
  MODIFY `id_ref` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `web_scanner_report`
--
ALTER TABLE `web_scanner_report`
  MODIFY `id_report_web` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `web_scanner_result`
--
ALTER TABLE `web_scanner_result`
  MODIFY `id_result` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `whois_result`
--
ALTER TABLE `whois_result`
  MODIFY `id_result_whois` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
