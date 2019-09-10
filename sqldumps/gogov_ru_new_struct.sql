-- phpMyAdmin SQL Dump
-- version 4.6.6deb4
-- https://www.phpmyadmin.net/
--
-- Хост: localhost:3306
-- Время создания: Сен 07 2019 г., 13:51
-- Версия сервера: 10.1.38-MariaDB-0+deb9u1
-- Версия PHP: 7.0.33-0+deb9u3

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `gogov_ru`
--

-- --------------------------------------------------------

--
-- Структура таблицы `county`
--

CREATE TABLE `county` (
  `id` int(11) NOT NULL,
  `name` text CHARACTER SET utf8
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Структура таблицы `district`
--

CREATE TABLE `district` (
  `id` int(11) NOT NULL,
  `name` text CHARACTER SET utf8
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Структура таблицы `MFC_department`
--

CREATE TABLE `MFC_department` (
  `id` int(11) NOT NULL,
  `fullname` text CHARACTER SET utf8,
  `shortname` text CHARACTER SET utf8,
  `ceo` text CHARACTER SET utf8,
  `direction` text CHARACTER SET utf8,
  `address` text CHARACTER SET utf8,
  `address_additional` text CHARACTER SET utf8,
  `post_index` text CHARACTER SET utf8,
  `operating_mode` text CHARACTER SET utf8,
  `email` text CHARACTER SET utf8,
  `phone` text CHARACTER SET utf8,
  `website` text CHARACTER SET utf8,
  `coverage` text CHARACTER SET utf8,
  `source_url` text CHARACTER SET utf8,
  `county_id` int(11) DEFAULT NULL,
  `region_id` int(11) DEFAULT NULL,
  `district_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Структура таблицы `MFC_department2service`
--

CREATE TABLE `MFC_department2service` (
  `department_id` int(11) DEFAULT NULL,
  `service_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Структура таблицы `region`
--

CREATE TABLE `region` (
  `id` int(11) NOT NULL,
  `name` text CHARACTER SET utf8
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Структура таблицы `service`
--

CREATE TABLE `service` (
  `id` int(11) NOT NULL,
  `destination_url` text CHARACTER SET utf8,
  `name` text CHARACTER SET utf8,
  `parent_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `county`
--
ALTER TABLE `county`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name_idx` (`name`(32));

--
-- Индексы таблицы `district`
--
ALTER TABLE `district`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name_idx` (`name`(32));

--
-- Индексы таблицы `MFC_department`
--
ALTER TABLE `MFC_department`
  ADD PRIMARY KEY (`id`),
  ADD KEY `county_id` (`county_id`),
  ADD KEY `region_id` (`region_id`),
  ADD KEY `district_id` (`district_id`);

--
-- Индексы таблицы `MFC_department2service`
--
ALTER TABLE `MFC_department2service`
  ADD KEY `department_id` (`department_id`),
  ADD KEY `service_id` (`service_id`);

--
-- Индексы таблицы `region`
--
ALTER TABLE `region`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name_idx` (`name`(32));

--
-- Индексы таблицы `service`
--
ALTER TABLE `service`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name_idx` (`name`(32)),
  ADD KEY `parent_id` (`parent_id`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `county`
--
ALTER TABLE `county`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT для таблицы `district`
--
ALTER TABLE `district`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT для таблицы `MFC_department`
--
ALTER TABLE `MFC_department`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT для таблицы `region`
--
ALTER TABLE `region`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT для таблицы `service`
--
ALTER TABLE `service`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- Ограничения внешнего ключа сохраненных таблиц
--

--
-- Ограничения внешнего ключа таблицы `MFC_department`
--
ALTER TABLE `MFC_department`
  ADD CONSTRAINT `MFC_department_ibfk_1` FOREIGN KEY (`county_id`) REFERENCES `county` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `MFC_department_ibfk_2` FOREIGN KEY (`region_id`) REFERENCES `region` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `MFC_department_ibfk_3` FOREIGN KEY (`district_id`) REFERENCES `district` (`id`) ON DELETE SET NULL;

--
-- Ограничения внешнего ключа таблицы `MFC_department2service`
--
ALTER TABLE `MFC_department2service`
  ADD CONSTRAINT `MFC_department2service_ibfk_1` FOREIGN KEY (`department_id`) REFERENCES `MFC_department` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `MFC_department2service_ibfk_2` FOREIGN KEY (`service_id`) REFERENCES `service` (`id`) ON DELETE CASCADE;

--
-- Ограничения внешнего ключа таблицы `service`
--
ALTER TABLE `service`
  ADD CONSTRAINT `service_ibfk_1` FOREIGN KEY (`parent_id`) REFERENCES `service` (`id`) ON DELETE CASCADE;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
