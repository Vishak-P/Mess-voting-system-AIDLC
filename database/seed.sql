-- ============================================================
-- Seed Data
-- 1 admin + 20 students + 30 menus + options + votes
--
-- Passwords (bcrypt):
--   admin@mess.com  → admin123
--   *@test.com      → student123
-- ============================================================

USE mess_voting;

-- ============================================================
-- USERS
-- ============================================================
INSERT INTO users (name, email, password, role) VALUES
('Admin User',    'admin@mess.com',    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMqJqhCangelxqnmGLsQ6IQKK2', 'admin'),
('Aarav Sharma',  'aarav@test.com',    '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'student'),
('Priya Patel',   'priya@test.com',    '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'student'),
('Rohan Gupta',   'rohan@test.com',    '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'student'),
('Sneha Reddy',   'sneha@test.com',    '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'student'),
('Arjun Singh',   'arjun@test.com',    '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'student'),
('Kavya Nair',    'kavya@test.com',    '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'student'),
('Vikram Joshi',  'vikram@test.com',   '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'student'),
('Ananya Iyer',   'ananya@test.com',   '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'student'),
('Rahul Verma',   'rahul@test.com',    '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'student'),
('Pooja Mehta',   'pooja@test.com',    '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'student'),
('Kiran Kumar',   'kiran@test.com',    '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'student'),
('Divya Rao',     'divya@test.com',    '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'student'),
('Suresh Pillai', 'suresh@test.com',   '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'student'),
('Meera Bose',    'meera@test.com',    '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'student'),
('Aditya Shah',   'aditya@test.com',   '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'student'),
('Nisha Tiwari',  'nisha@test.com',    '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'student'),
('Sanjay Dubey',  'sanjay@test.com',   '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'student'),
('Ritu Agarwal',  'ritu@test.com',     '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'student'),
('Manish Yadav',  'manish@test.com',   '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'student'),
('Lakshmi Devi',  'lakshmi@test.com',  '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'student');

-- ============================================================
-- MENUS  (date, meal_type, open_time, deadline, is_locked, created_by)
-- Past week (Apr 28 – May 2): locked, deadline passed
-- Current week (May 6 – May 10): open, deadline in future
-- ============================================================
INSERT INTO menus (date, meal_type, open_time, deadline, is_locked, created_by) VALUES
-- Apr 28
('2026-04-28','breakfast','2026-04-28 00:00:00','2026-04-28 07:30:00',1,1),
('2026-04-28','lunch',    '2026-04-28 00:00:00','2026-04-28 11:30:00',1,1),
('2026-04-28','dinner',   '2026-04-28 00:00:00','2026-04-28 18:30:00',1,1),
-- Apr 29
('2026-04-29','breakfast','2026-04-29 00:00:00','2026-04-29 07:30:00',1,1),
('2026-04-29','lunch',    '2026-04-29 00:00:00','2026-04-29 11:30:00',1,1),
('2026-04-29','dinner',   '2026-04-29 00:00:00','2026-04-29 18:30:00',1,1),
-- Apr 30
('2026-04-30','breakfast','2026-04-30 00:00:00','2026-04-30 07:30:00',1,1),
('2026-04-30','lunch',    '2026-04-30 00:00:00','2026-04-30 11:30:00',1,1),
('2026-04-30','dinner',   '2026-04-30 00:00:00','2026-04-30 18:30:00',1,1),
-- May 1
('2026-05-01','breakfast','2026-05-01 00:00:00','2026-05-01 07:30:00',1,1),
('2026-05-01','lunch',    '2026-05-01 00:00:00','2026-05-01 11:30:00',1,1),
('2026-05-01','dinner',   '2026-05-01 00:00:00','2026-05-01 18:30:00',1,1),
-- May 2
('2026-05-02','breakfast','2026-05-02 00:00:00','2026-05-02 07:30:00',1,1),
('2026-05-02','lunch',    '2026-05-02 00:00:00','2026-05-02 11:30:00',1,1),
('2026-05-02','dinner',   '2026-05-02 00:00:00','2026-05-02 18:30:00',1,1),
-- May 6 (current week — open)
('2026-05-06','breakfast','2026-05-06 00:00:00','2026-05-06 23:59:00',0,1),
('2026-05-06','lunch',    '2026-05-06 00:00:00','2026-05-06 23:59:00',0,1),
('2026-05-06','dinner',   '2026-05-06 00:00:00','2026-05-06 23:59:00',0,1),
-- May 7
('2026-05-07','breakfast','2026-05-07 00:00:00','2026-05-07 23:59:00',0,1),
('2026-05-07','lunch',    '2026-05-07 00:00:00','2026-05-07 23:59:00',0,1),
('2026-05-07','dinner',   '2026-05-07 00:00:00','2026-05-07 23:59:00',0,1),
-- May 8
('2026-05-08','breakfast','2026-05-08 00:00:00','2026-05-08 23:59:00',0,1),
('2026-05-08','lunch',    '2026-05-08 00:00:00','2026-05-08 23:59:00',0,1),
('2026-05-08','dinner',   '2026-05-08 00:00:00','2026-05-08 23:59:00',0,1),
-- May 9
('2026-05-09','breakfast','2026-05-09 00:00:00','2026-05-09 23:59:00',0,1),
('2026-05-09','lunch',    '2026-05-09 00:00:00','2026-05-09 23:59:00',0,1),
('2026-05-09','dinner',   '2026-05-09 00:00:00','2026-05-09 23:59:00',0,1),
-- May 10
('2026-05-10','breakfast','2026-05-10 00:00:00','2026-05-10 23:59:00',0,1),
('2026-05-10','lunch',    '2026-05-10 00:00:00','2026-05-10 23:59:00',0,1),
('2026-05-10','dinner',   '2026-05-10 00:00:00','2026-05-10 23:59:00',0,1);

-- ============================================================
-- MENU OPTIONS (5 dishes per menu, menus 1–30)
-- ============================================================
INSERT INTO menu_options (menu_id, dish_name) VALUES
(1,'Idli Sambar'),(1,'Poha'),(1,'Aloo Paratha'),(1,'Upma'),(1,'Bread Omelette'),
(2,'Dal Rice'),(2,'Rajma Chawal'),(2,'Chole Bhature'),(2,'Veg Biryani'),(2,'Paneer Butter Masala'),
(3,'Roti Sabzi'),(3,'Fried Rice'),(3,'Pasta'),(3,'Dal Makhani'),(3,'Pulao'),
(4,'Dosa Chutney'),(4,'Cornflakes'),(4,'Puri Bhaji'),(4,'Sandwich'),(4,'Paratha Curd'),
(5,'Sambar Rice'),(5,'Kadhi Chawal'),(5,'Matar Paneer'),(5,'Veg Pulao'),(5,'Lemon Rice'),
(6,'Chapati Dal'),(6,'Noodles'),(6,'Veg Manchurian'),(6,'Khichdi'),(6,'Pav Bhaji'),
(7,'Idli Vada'),(7,'Poha Jalebi'),(7,'Methi Paratha'),(7,'Oats Porridge'),(7,'Egg Bhurji'),
(8,'Dal Fry Rice'),(8,'Palak Paneer'),(8,'Aloo Gobi'),(8,'Veg Biryani'),(8,'Curd Rice'),
(9,'Roti Paneer'),(9,'Fried Rice'),(9,'Soup Bread'),(9,'Dal Tadka'),(9,'Veg Curry'),
(10,'Masala Dosa'),(10,'Upma'),(10,'Bread Butter'),(10,'Poha'),(10,'Idli Sambar'),
(11,'Rajma Rice'),(11,'Chole Rice'),(11,'Paneer Masala'),(11,'Veg Pulao'),(11,'Dal Rice'),
(12,'Chapati Sabzi'),(12,'Pasta'),(12,'Noodles'),(12,'Khichdi'),(12,'Pav Bhaji'),
(13,'Idli Sambar'),(13,'Aloo Paratha'),(13,'Cornflakes'),(13,'Sandwich'),(13,'Poha'),
(14,'Dal Rice'),(14,'Veg Biryani'),(14,'Palak Paneer'),(14,'Curd Rice'),(14,'Lemon Rice'),
(15,'Roti Dal'),(15,'Fried Rice'),(15,'Veg Manchurian'),(15,'Soup'),(15,'Pulao'),
-- Current week options (menus 16–30)
(16,'Idli Sambar'),(16,'Poha'),(16,'Aloo Paratha'),(16,'Upma'),(16,'Bread Omelette'),
(17,'Dal Rice'),(17,'Rajma Chawal'),(17,'Chole Bhature'),(17,'Veg Biryani'),(17,'Paneer Butter Masala'),
(18,'Roti Sabzi'),(18,'Fried Rice'),(18,'Pasta'),(18,'Dal Makhani'),(18,'Pulao'),
(19,'Dosa Chutney'),(19,'Cornflakes'),(19,'Puri Bhaji'),(19,'Sandwich'),(19,'Paratha Curd'),
(20,'Sambar Rice'),(20,'Kadhi Chawal'),(20,'Matar Paneer'),(20,'Veg Pulao'),(20,'Lemon Rice'),
(21,'Chapati Dal'),(21,'Noodles'),(21,'Veg Manchurian'),(21,'Khichdi'),(21,'Pav Bhaji'),
(22,'Idli Vada'),(22,'Poha Jalebi'),(22,'Methi Paratha'),(22,'Oats Porridge'),(22,'Egg Bhurji'),
(23,'Dal Fry Rice'),(23,'Palak Paneer'),(23,'Aloo Gobi'),(23,'Veg Biryani'),(23,'Curd Rice'),
(24,'Roti Paneer'),(24,'Fried Rice'),(24,'Soup Bread'),(24,'Dal Tadka'),(24,'Veg Curry'),
(25,'Masala Dosa'),(25,'Upma'),(25,'Bread Butter'),(25,'Poha'),(25,'Idli Sambar'),
(26,'Rajma Rice'),(26,'Chole Rice'),(26,'Paneer Masala'),(26,'Veg Pulao'),(26,'Dal Rice'),
(27,'Chapati Sabzi'),(27,'Pasta'),(27,'Noodles'),(27,'Khichdi'),(27,'Pav Bhaji'),
(28,'Idli Sambar'),(28,'Aloo Paratha'),(28,'Cornflakes'),(28,'Sandwich'),(28,'Poha'),
(29,'Dal Rice'),(29,'Veg Biryani'),(29,'Palak Paneer'),(29,'Curd Rice'),(29,'Lemon Rice'),
(30,'Roti Dal'),(30,'Fried Rice'),(30,'Veg Manchurian'),(30,'Soup'),(30,'Pulao');

-- ============================================================
-- VOTES  (past menus 1–15, users 2–21)
-- option_id ranges: menu 1 → 1-5, menu 2 → 6-10, menu 3 → 11-15,
--   menu 4 → 16-20, menu 5 → 21-25, menu 6 → 26-30,
--   menu 7 → 31-35, menu 8 → 36-40, menu 9 → 41-45,
--   menu 10 → 46-50, menu 11 → 51-55, menu 12 → 56-60,
--   menu 13 → 61-65, menu 14 → 66-70, menu 15 → 71-75
-- ============================================================
INSERT INTO votes (user_id, menu_id, option_id, voted_at) VALUES
-- Menu 1 (Apr 28 breakfast) — all 20 students
(2,1,1,'2026-04-28 06:00:00'),(3,1,2,'2026-04-28 06:05:00'),(4,1,3,'2026-04-28 06:10:00'),
(5,1,1,'2026-04-28 06:15:00'),(6,1,4,'2026-04-28 06:20:00'),(7,1,2,'2026-04-28 06:25:00'),
(8,1,1,'2026-04-28 06:30:00'),(9,1,5,'2026-04-28 06:35:00'),(10,1,3,'2026-04-28 06:40:00'),
(11,1,1,'2026-04-28 06:45:00'),(12,1,2,'2026-04-28 06:50:00'),(13,1,4,'2026-04-28 06:55:00'),
(14,1,1,'2026-04-28 07:00:00'),(15,1,3,'2026-04-28 07:05:00'),(16,1,2,'2026-04-28 07:10:00'),
(17,1,1,'2026-04-28 07:15:00'),(18,1,5,'2026-04-28 07:20:00'),(19,1,4,'2026-04-28 07:25:00'),
(20,1,1,'2026-04-28 07:28:00'),(21,1,2,'2026-04-28 07:29:00'),
-- Menu 2 (Apr 28 lunch)
(2,2,6,'2026-04-28 10:00:00'),(3,2,7,'2026-04-28 10:05:00'),(4,2,8,'2026-04-28 10:10:00'),
(5,2,9,'2026-04-28 10:15:00'),(6,2,6,'2026-04-28 10:20:00'),(7,2,10,'2026-04-28 10:25:00'),
(8,2,7,'2026-04-28 10:30:00'),(9,2,6,'2026-04-28 10:35:00'),(10,2,8,'2026-04-28 10:40:00'),
(11,2,9,'2026-04-28 10:45:00'),(12,2,6,'2026-04-28 10:50:00'),(13,2,7,'2026-04-28 10:55:00'),
(14,2,10,'2026-04-28 11:00:00'),(15,2,6,'2026-04-28 11:05:00'),(16,2,8,'2026-04-28 11:10:00'),
(17,2,6,'2026-04-28 11:15:00'),(18,2,9,'2026-04-28 11:20:00'),(19,2,7,'2026-04-28 11:25:00'),
(20,2,6,'2026-04-28 11:28:00'),(21,2,10,'2026-04-28 11:29:00'),
-- Menu 3 (Apr 28 dinner)
(2,3,11,'2026-04-28 17:00:00'),(3,3,12,'2026-04-28 17:05:00'),(4,3,13,'2026-04-28 17:10:00'),
(5,3,11,'2026-04-28 17:15:00'),(6,3,14,'2026-04-28 17:20:00'),(7,3,15,'2026-04-28 17:25:00'),
(8,3,11,'2026-04-28 17:30:00'),(9,3,12,'2026-04-28 17:35:00'),(10,3,13,'2026-04-28 17:40:00'),
(11,3,11,'2026-04-28 17:45:00'),(12,3,14,'2026-04-28 17:50:00'),(13,3,15,'2026-04-28 17:55:00'),
(14,3,11,'2026-04-28 18:00:00'),(15,3,12,'2026-04-28 18:05:00'),(16,3,13,'2026-04-28 18:10:00'),
(17,3,11,'2026-04-28 18:15:00'),(18,3,14,'2026-04-28 18:20:00'),(19,3,15,'2026-04-28 18:25:00'),
(20,3,11,'2026-04-28 18:28:00'),(21,3,12,'2026-04-28 18:29:00'),
-- Menu 4 (Apr 29 breakfast) — partial
(2,4,16,'2026-04-29 06:00:00'),(3,4,17,'2026-04-29 06:10:00'),(4,4,18,'2026-04-29 06:20:00'),
(5,4,16,'2026-04-29 06:30:00'),(6,4,19,'2026-04-29 06:40:00'),(7,4,20,'2026-04-29 06:50:00'),
(8,4,16,'2026-04-29 07:00:00'),(9,4,17,'2026-04-29 07:10:00'),(10,4,18,'2026-04-29 07:20:00'),
(11,4,16,'2026-04-29 07:25:00'),(12,4,19,'2026-04-29 07:28:00'),
-- Menu 5 (Apr 29 lunch)
(2,5,21,'2026-04-29 10:00:00'),(3,5,22,'2026-04-29 10:10:00'),(4,5,23,'2026-04-29 10:20:00'),
(5,5,21,'2026-04-29 10:30:00'),(6,5,24,'2026-04-29 10:40:00'),(7,5,25,'2026-04-29 10:50:00'),
(8,5,21,'2026-04-29 11:00:00'),(9,5,22,'2026-04-29 11:10:00'),(10,5,23,'2026-04-29 11:20:00'),
-- Menu 6 (Apr 29 dinner)
(2,6,26,'2026-04-29 17:00:00'),(3,6,27,'2026-04-29 17:10:00'),(4,6,28,'2026-04-29 17:20:00'),
(5,6,26,'2026-04-29 17:30:00'),(6,6,29,'2026-04-29 17:40:00'),(7,6,30,'2026-04-29 17:50:00'),
-- Menu 7 (Apr 30 breakfast)
(2,7,31,'2026-04-30 06:00:00'),(3,7,32,'2026-04-30 06:10:00'),(4,7,33,'2026-04-30 06:20:00'),
(5,7,31,'2026-04-30 06:30:00'),(6,7,34,'2026-04-30 06:40:00'),(7,7,35,'2026-04-30 06:50:00'),
(8,7,31,'2026-04-30 07:00:00'),(9,7,32,'2026-04-30 07:10:00'),
-- Menu 8 (Apr 30 lunch)
(2,8,36,'2026-04-30 10:00:00'),(3,8,37,'2026-04-30 10:10:00'),(4,8,38,'2026-04-30 10:20:00'),
(5,8,36,'2026-04-30 10:30:00'),(6,8,39,'2026-04-30 10:40:00'),(7,8,40,'2026-04-30 10:50:00'),
-- Menu 9 (Apr 30 dinner)
(2,9,41,'2026-04-30 17:00:00'),(3,9,42,'2026-04-30 17:10:00'),(4,9,43,'2026-04-30 17:20:00'),
(5,9,41,'2026-04-30 17:30:00'),(6,9,44,'2026-04-30 17:40:00'),
-- Menu 10 (May 1 breakfast)
(2,10,46,'2026-05-01 06:00:00'),(3,10,47,'2026-05-01 06:10:00'),(4,10,48,'2026-05-01 06:20:00'),
(5,10,46,'2026-05-01 06:30:00'),(6,10,49,'2026-05-01 06:40:00'),(7,10,50,'2026-05-01 06:50:00'),
-- Menu 11 (May 1 lunch)
(2,11,51,'2026-05-01 10:00:00'),(3,11,52,'2026-05-01 10:10:00'),(4,11,53,'2026-05-01 10:20:00'),
(5,11,51,'2026-05-01 10:30:00'),(6,11,54,'2026-05-01 10:40:00'),(7,11,55,'2026-05-01 10:50:00'),
-- Menu 12 (May 1 dinner)
(2,12,56,'2026-05-01 17:00:00'),(3,12,57,'2026-05-01 17:10:00'),(4,12,58,'2026-05-01 17:20:00'),
(5,12,56,'2026-05-01 17:30:00'),(6,12,59,'2026-05-01 17:40:00'),
-- Menu 13 (May 2 breakfast)
(2,13,61,'2026-05-02 06:00:00'),(3,13,62,'2026-05-02 06:10:00'),(4,13,63,'2026-05-02 06:20:00'),
(5,13,61,'2026-05-02 06:30:00'),(6,13,64,'2026-05-02 06:40:00'),(7,13,65,'2026-05-02 06:50:00'),
-- Menu 14 (May 2 lunch)
(2,14,66,'2026-05-02 10:00:00'),(3,14,67,'2026-05-02 10:10:00'),(4,14,68,'2026-05-02 10:20:00'),
(5,14,66,'2026-05-02 10:30:00'),(6,14,69,'2026-05-02 10:40:00'),(7,14,70,'2026-05-02 10:50:00'),
-- Menu 15 (May 2 dinner)
(2,15,71,'2026-05-02 17:00:00'),(3,15,72,'2026-05-02 17:10:00'),(4,15,73,'2026-05-02 17:20:00'),
(5,15,71,'2026-05-02 17:30:00'),(6,15,74,'2026-05-02 17:40:00');

-- ============================================================
-- SAMPLE FEEDBACK (past menus, a few students)
-- ============================================================
INSERT INTO feedback (user_id, menu_id, rating, comment) VALUES
(2, 1, 5, 'Idli Sambar was excellent today!'),
(3, 1, 4, 'Poha was good but a bit dry'),
(4, 2, 5, 'Veg Biryani was amazing'),
(5, 2, 3, 'Dal Rice was okay, nothing special'),
(6, 3, 4, 'Dal Makhani was very tasty'),
(7, 3, 5, 'Pulao was perfect'),
(2, 4, 4, 'Dosa was crispy and fresh'),
(3, 5, 5, 'Matar Paneer was the best this week'),
(4, 6, 3, 'Noodles were a bit bland'),
(5, 7, 5, 'Methi Paratha was outstanding');
