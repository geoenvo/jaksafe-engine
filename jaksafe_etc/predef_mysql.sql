DROP TABLE IF EXISTS `adhoc_predef_calc` ;

CREATE TABLE `adhoc_predef_calc` (
  `id_event` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_user` int(11) DEFAULT NULL,
  `id_user_group` int(11) DEFAULT NULL,
  `event_name` varchar(100),
  `damage` decimal(17,2) DEFAULT NULL,
  `loss` decimal(17,2) DEFAULT NULL,
  PRIMARY KEY (`id_event`)
)