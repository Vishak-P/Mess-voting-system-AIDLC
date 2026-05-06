-- ============================================================
-- Mess / Canteen Menu Voting System — Database Schema
-- MySQL 8.0+  |  Character set: utf8mb4
-- ============================================================

CREATE DATABASE IF NOT EXISTS mess_voting
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE mess_voting;

-- ============================================================
-- USERS
-- ============================================================
CREATE TABLE IF NOT EXISTS users (
  id          INT AUTO_INCREMENT PRIMARY KEY,
  name        VARCHAR(100)  NOT NULL,
  email       VARCHAR(150)  NOT NULL UNIQUE,
  password    VARCHAR(255)  NOT NULL,
  role        ENUM('admin','student') NOT NULL DEFAULT 'student',
  created_at  DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_users_email (email),
  INDEX idx_users_role  (role)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================
-- MENUS
-- ============================================================
CREATE TABLE IF NOT EXISTS menus (
  id          INT AUTO_INCREMENT PRIMARY KEY,
  date        DATE          NOT NULL,
  meal_type   ENUM('breakfast','lunch','dinner') NOT NULL,
  open_time   DATETIME      NOT NULL,
  deadline    DATETIME      NOT NULL,
  is_locked   TINYINT(1)    NOT NULL DEFAULT 0,
  created_by  INT           NOT NULL,
  created_at  DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY uq_menu_date_meal (date, meal_type),
  FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE RESTRICT,
  INDEX idx_menus_date      (date),
  INDEX idx_menus_meal_type (meal_type),
  INDEX idx_menus_deadline  (deadline)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================
-- MENU OPTIONS (dishes per menu)
-- ============================================================
CREATE TABLE IF NOT EXISTS menu_options (
  id          INT AUTO_INCREMENT PRIMARY KEY,
  menu_id     INT           NOT NULL,
  dish_name   VARCHAR(200)  NOT NULL,
  FOREIGN KEY (menu_id) REFERENCES menus(id) ON DELETE CASCADE,
  INDEX idx_options_menu_id (menu_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================
-- VOTES
-- ============================================================
CREATE TABLE IF NOT EXISTS votes (
  id          INT AUTO_INCREMENT PRIMARY KEY,
  user_id     INT           NOT NULL,
  menu_id     INT           NOT NULL,
  option_id   INT           NOT NULL,
  voted_at    DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY uq_vote_user_menu (user_id, menu_id),
  FOREIGN KEY (user_id)   REFERENCES users(id)        ON DELETE CASCADE,
  FOREIGN KEY (menu_id)   REFERENCES menus(id)        ON DELETE CASCADE,
  FOREIGN KEY (option_id) REFERENCES menu_options(id) ON DELETE CASCADE,
  INDEX idx_votes_user_id   (user_id),
  INDEX idx_votes_menu_id   (menu_id),
  INDEX idx_votes_option_id (option_id),
  INDEX idx_votes_voted_at  (voted_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================
-- FEEDBACK (post-meal star rating + optional comment)
-- ============================================================
CREATE TABLE IF NOT EXISTS feedback (
  id          INT AUTO_INCREMENT PRIMARY KEY,
  user_id     INT           NOT NULL,
  menu_id     INT           NOT NULL,
  rating      TINYINT       NOT NULL,
  comment     TEXT          NULL,
  created_at  DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY uq_feedback_user_menu (user_id, menu_id),
  CONSTRAINT ck_feedback_rating CHECK (rating >= 1 AND rating <= 5),
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
  FOREIGN KEY (menu_id) REFERENCES menus(id) ON DELETE CASCADE,
  INDEX idx_feedback_menu_id (menu_id),
  INDEX idx_feedback_user_id (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
