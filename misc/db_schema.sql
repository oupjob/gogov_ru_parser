CREATE TABLE `Department` (
	`id` INT(32) NOT NULL AUTO_INCREMENT DEFAULT 'NULL',
	`full_name` VARCHAR(4096) NOT NULL,
	`region` INT(32) NOT NULL DEFAULT '',
	`region` INT(32) NOT NULL DEFAULT '',
	`county` INT(32) NOT NULL DEFAULT '',
	`distinct` INT(32) NOT NULL DEFAULT '',
	`email` VARCHAR(1024) NOT NULL DEFAULT '',
	`address` VARCHAR(4096) NOT NULL,
	`post_index` VARCHAR(32) NOT NULL,
	`operating_mode` VARCHAR(2048) NOT NULL,
	`website` VARCHAR(128) NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE `County` (
	`id` INT(32) NOT NULL AUTO_INCREMENT,
	`name` VARCHAR(512) NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE `Region` (
	`id` INT(32) NOT NULL AUTO_INCREMENT,
	`name` VARCHAR(512) NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE `Distinct` (
	`id` INT(32) NOT NULL AUTO_INCREMENT,
	`name` VARCHAR(512) NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE `Service` (
	`id` INT(32) NOT NULL AUTO_INCREMENT,
	`department_id` INT(32) NOT NULL,
	`name` VARCHAR(4096) NOT NULL,
	PRIMARY KEY (`id`)
);

ALTER TABLE `Department` ADD CONSTRAINT `Department_fk0` FOREIGN KEY (`region`) REFERENCES ``(``);

ALTER TABLE `Department` ADD CONSTRAINT `Department_fk1` FOREIGN KEY (`region`) REFERENCES `Region`(`id`);

ALTER TABLE `Department` ADD CONSTRAINT `Department_fk2` FOREIGN KEY (`county`) REFERENCES `County`(`id`);

ALTER TABLE `Department` ADD CONSTRAINT `Department_fk3` FOREIGN KEY (`distinct`) REFERENCES `Distinct`(`id`);

ALTER TABLE `Service` ADD CONSTRAINT `Service_fk0` FOREIGN KEY (`department_id`) REFERENCES `Department`(`id`);
