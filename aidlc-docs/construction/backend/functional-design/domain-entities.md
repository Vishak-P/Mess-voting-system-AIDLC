# Domain Entities — Unit 1: Backend
## Mess / Canteen Menu Voting System

---

## Entity: User

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | INT | PK, AUTO_INCREMENT | Unique identifier |
| name | VARCHAR(100) | NOT NULL | Full name |
| email | VARCHAR(150) | NOT NULL, UNIQUE | Login email |
| password | VARCHAR(255) | NOT NULL | bcrypt hash |
| role | ENUM('admin','student') | NOT NULL, DEFAULT 'student' | Access role |
| created_at | DATETIME | NOT NULL, DEFAULT NOW() | Registration timestamp |

**Relationships**: Has many Votes, has many Feedbacks, has many Menus (created_by)

---

## Entity: Menu

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | INT | PK, AUTO_INCREMENT | Unique identifier |
| date | DATE | NOT NULL | The meal date |
| meal_type | ENUM('breakfast','lunch','dinner') | NOT NULL | Meal slot |
| open_time | DATETIME | NOT NULL | When voting opens |
| deadline | DATETIME | NOT NULL | When voting closes |
| is_locked | TINYINT(1) | NOT NULL, DEFAULT 0 | Manual lock flag |
| created_by | INT | FK → users.id | Admin who created it |
| created_at | DATETIME | NOT NULL, DEFAULT NOW() | Creation timestamp |

**Unique Constraint**: `(date, meal_type)` — one menu per date+meal
**Relationships**: Has many MenuOptions, has many Votes, has many Feedbacks

---

## Entity: MenuOption

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | INT | PK, AUTO_INCREMENT | Unique identifier |
| menu_id | INT | FK → menus.id CASCADE DELETE | Parent menu |
| dish_name | VARCHAR(200) | NOT NULL | Name of the dish |

**Relationships**: Has many Votes

---

## Entity: Vote

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | INT | PK, AUTO_INCREMENT | Unique identifier |
| user_id | INT | FK → users.id CASCADE DELETE | Voter |
| menu_id | INT | FK → menus.id CASCADE DELETE | Menu voted on |
| option_id | INT | FK → menu_options.id CASCADE DELETE | Chosen dish |
| voted_at | DATETIME | NOT NULL, DEFAULT NOW() | Vote timestamp |

**Unique Constraint**: `(user_id, menu_id)` — one vote per user per menu

---

## Entity: Feedback

| Field | Type | Constraints | Description |
|---|---|---|---|
| id | INT | PK, AUTO_INCREMENT | Unique identifier |
| user_id | INT | FK → users.id CASCADE DELETE | Student who submitted |
| menu_id | INT | FK → menus.id CASCADE DELETE | Menu being rated |
| rating | TINYINT | NOT NULL, CHECK(1–5) | Star rating |
| comment | TEXT | NULLABLE | Optional text comment |
| created_at | DATETIME | NOT NULL, DEFAULT NOW() | Submission timestamp |

**Unique Constraint**: `(user_id, menu_id)` — one feedback per user per menu
**Business Rule**: Feedback only allowed after `menu.deadline` has passed
