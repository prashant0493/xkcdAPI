/*Create database*/

CREATE DATABASE IF NOT EXISTS xkcdDB;
USE xkcdDB;

/*create tables */

CREATE TABLE `comics`(
    `num` INT(11) NOT NULL,
    `month` VARCHAR(250) COLLATE 'utf8_unicode_ci',
    `link` VARCHAR(250) COLLATE 'utf8_unicode_ci',
    `year` VARCHAR(250) COLLATE 'utf8_unicode_ci',
    `news` VARCHAR(250) COLLATE 'utf8_unicode_ci',
    `safe_title` VARCHAR(250) COLLATE 'utf8_unicode_ci',
    `transcript` VARCHAR(5000) COLLATE 'utf8_unicode_ci',
    `alt` VARCHAR(5000) COLLATE 'utf8_unicode_ci',
    `img` VARCHAR(250) COLLATE 'utf8_unicode_ci',
    `title` VARCHAR(250) COLLATE 'utf8_unicode_ci',
    `day` VARCHAR(250) COLLATE 'utf8_unicode_ci',
    PRIMARY KEY (`num`)
) Engine=InnoDB DEFAULT CHARSET=utf8mb4;
