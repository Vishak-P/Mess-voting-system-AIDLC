# Units of Work
## Mess / Canteen Menu Voting System

---

## Unit 1: Backend — Flask REST API

**Description**: The Flask Python backend providing all REST API endpoints, JWT authentication, business logic, and database access.

**Tech Stack**: Python 3.9+, Flask 3.x, Flask-JWT-Extended, Flask-SQLAlchemy, Flask-Bcrypt, Flask-CORS, PyMySQL

**Responsibilities**:
- All API endpoints (auth, menu, admin, voting, dashboard, feedback, export)
- JWT token issuance and validation
- Password hashing (bcrypt)
- Business rule enforcement (voting window, result visibility, vote uniqueness)
- Database ORM models and migrations
- Structured logging and error handling
- Rate limiting on login endpoint
- HTTP security headers middleware
- CSV export generation

**Directory Structure**:
```
backend/
├── app.py                  # Application factory + entry point
├── requirements.txt        # Pinned dependencies
├── .env.example
├── config/
│   ├── __init__.py
│   └── settings.py         # Environment-based config
├── models/
│   ├── __init__.py
│   ├── base.py             # SQLAlchemy instance
│   ├── user.py
│   ├── menu.py
│   ├── menu_option.py
│   ├── vote.py
│   └── feedback.py         # NEW: feedback model
├── routes/
│   ├── __init__.py
│   ├── auth.py
│   ├── menu.py
│   ├── admin.py
│   ├── voting.py
│   ├── feedback.py         # NEW: feedback routes
│   └── dashboard.py
└── utils/
    ├── __init__.py
    ├── auth_service.py     # NEW: extracted auth helpers
    ├── voting_service.py   # NEW: voting business rules
    ├── menu_service.py     # NEW: menu copy + auto-lock
    ├── notifications.py
    └── scheduler.py
```

**Stories Covered**: US-01, US-02, US-03, US-04, US-05, US-06, US-07, US-08, US-09, US-11, US-12, US-13, US-14, US-15, US-16, US-17, US-18, US-19

---

## Unit 2: Frontend — React SPA

**Description**: The React single-page application providing the student and admin user interfaces.

**Tech Stack**: React 18, React Router v6, Tailwind CSS, Recharts, Axios, react-hot-toast, react-icons, date-fns

**Responsibilities**:
- All pages (Login, Register, Dashboard, Voting, Results, Admin Panel)
- JWT storage and attachment to API requests
- Role-based route guards
- Responsive UI (mobile + desktop)
- Charts (bar, pie, line, horizontal bar) via Recharts
- Toast notifications
- Loading states
- Vote modal, menu form modal, feedback form

**Directory Structure**:
```
frontend/
├── package.json            # Pinned dependencies
├── tailwind.config.js
├── postcss.config.js
├── .env.example
├── public/
│   └── index.html
└── src/
    ├── index.js
    ├── index.css
    ├── App.js              # Router + route guards
    ├── context/
    │   └── AuthContext.js
    ├── utils/
    │   ├── api.js          # Axios instance + interceptors
    │   └── helpers.js
    ├── components/
    │   ├── Navbar.jsx
    │   ├── MenuCard.jsx
    │   ├── VoteButton.jsx
    │   ├── VoteModal.jsx
    │   ├── MenuFormModal.jsx
    │   ├── FeedbackForm.jsx  # NEW
    │   ├── ChartCard.jsx
    │   ├── StatCard.jsx
    │   └── Loader.jsx
    └── pages/
        ├── LoginPage.jsx
        ├── RegisterPage.jsx
        ├── DashboardPage.jsx
        ├── VotingPage.jsx
        ├── ResultsPage.jsx
        └── AdminPanel.jsx
```

**Stories Covered**: US-01, US-02, US-03, US-04, US-05, US-06, US-07, US-08, US-09, US-10, US-11, US-12, US-13, US-14, US-15, US-16, US-17, US-18, US-19

---

## Unit 3: Database — MySQL Schema + Seed Data

**Description**: The MySQL database schema, constraints, indexes, and seed data.

**Tech Stack**: MySQL 8.0, utf8mb4

**Responsibilities**:
- Table definitions: users, menus, menu_options, votes, feedback
- Unique constraints (vote uniqueness, menu uniqueness per date+meal)
- Foreign key relationships with cascade rules
- Indexes for query performance
- Seed data: 1 admin + 20 students + 30 menus + options + votes

**Directory Structure**:
```
database/
├── schema.sql              # CREATE TABLE statements
└── seed.sql                # INSERT statements for test data
```

**Stories Covered**: All stories (data foundation)

---

## Unit Summary

| Unit | Tech | Stories | Dependencies |
|---|---|---|---|
| 1: Backend | Python/Flask | 18/19 | Unit 3 (MySQL) |
| 2: Frontend | React/Tailwind | 19/19 | Unit 1 (API) |
| 3: Database | MySQL | All | None |

**Development Order**: Unit 3 → Unit 1 → Unit 2 (database first, then API, then UI)
