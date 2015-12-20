CREATE TABLE `fl_event_raw`(  
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `unit` VARCHAR(255) NOT NULL,
  `village` VARCHAR(255),
  `district` VARCHAR(255),
  `rt` VARCHAR(255),
  `rw` VARCHAR(255),
  `depth` INT UNSIGNED NOT NULL,
  `report_time` DATETIME NOT NULL,
  `request_time` DATETIME NOT NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE `fl_event`(  
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `unit` VARCHAR(255) NOT NULL,
  `village` VARCHAR(255),
  `district` VARCHAR(255),
  `rt` VARCHAR(255),
  `rw` VARCHAR(255),
  `depth` INT UNSIGNED NOT NULL,
  `report_time` DATETIME NOT NULL,
  `request_time` DATETIME NOT NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE `auto_calc`(  
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `t0` DATETIME NOT NULL,
  `t1` DATETIME NOT NULL,
  `damage` DECIMAL(17,2),
  `loss` DECIMAL(17,2),
  PRIMARY KEY (`id`)
);

CREATE TABLE `adhoc_calc`(  
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `id_user` INT(11),
  `id_user_group` INT(11),
  `t0` DATETIME NOT NULL,
  `t1` DATETIME NOT NULL,
  `damage` DECIMAL(17,2),
  `loss` DECIMAL(17,2),
  PRIMARY KEY (`id`)
);
