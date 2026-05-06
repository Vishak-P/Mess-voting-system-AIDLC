# Requirements Document
## Mess / Canteen Menu Voting System

---

## Intent Analysis Summary

| Field | Value |
|---|---|
| **User Request** | Build a production-level full-stack web application for mess/canteen menu voting |
| **Request Type** | New Project (Greenfield) |
| **Scope Estimate** | Multiple Components — React frontend, Flask backend, MySQL database |
| **Complexity Estimate** | Moderate — standard CRUD + voting logic + analytics dashboard |

---

## Functional Requirements

### FR-01: Authentication & User Management
- **FR-01.1** Users can self-register with name, email, and password (minimum 8 characters)
- **FR-01.2** Users log in with email and password; receive a JWT access token valid for 8 hours
- **FR-01.3** Two roles exist: `admin` and `student` (default on registration: `student`)
- **FR-01.4** Admin can promote any student to admin role from the Admin Panel
- **FR-01.5** All protected routes require a valid JWT token; expired/invalid tokens redirect to login
- **FR-01.6** Logout invalidates the client-side token (client deletes token from storage)

### FR-02: Menu Management (Admin)
- **FR-02.1** Admin can create a menu entry for a specific date + meal type (breakfast / lunch / dinner)
- **FR-02.2** Each menu has an admin-defined voting open time and close (deadline) time
- **FR-02.3** Each menu has 2–10 dish options
- **FR-02.4** Admin can edit a menu's deadline, lock status, and dish options
- **FR-02.5** Admin can delete a menu (cascades to options and votes)
- **FR-02.6** Admin can manually lock voting for any menu at any time
- **FR-02.7** System auto-locks menus when their deadline passes
- **FR-02.8** System can auto-copy last week's menu as a template for the new week (weekly reset)
- **FR-02.9** Only one menu entry is allowed per date + meal type combination

### FR-03: Voting (Student)
- **FR-03.1** Students can view the weekly menu grouped by date and meal type
- **FR-03.2** Students can vote for exactly one dish per menu (one vote per user per menu)
- **FR-03.3** Voting is only allowed when the menu's voting window is open (after open time, before deadline, not locked)
- **FR-03.4** Students can change their vote any time before the voting deadline
- **FR-03.5** Duplicate votes are prevented at both application and database constraint level
- **FR-03.6** Students can navigate between weeks to view past and future menus

### FR-04: Results
- **FR-04.1** Voting results (vote counts and percentages per dish) are visible to students only after the voting deadline has passed
- **FR-04.2** Results show a ranked list of dishes with vote counts, percentages, and medal indicators (🥇🥈🥉)
- **FR-04.3** The leading dish is highlighted prominently
- **FR-04.4** Students can see which option they personally voted for
- **FR-04.5** Admin can view results at any time (before or after deadline)

### FR-05: Meal Feedback
- **FR-05.1** After a meal's voting deadline has passed, students can submit feedback consisting of a star rating (1–5) and an optional text comment
- **FR-05.2** Each student can submit one feedback entry per menu
- **FR-05.3** Admin can view all feedback in the Admin Panel

### FR-06: Admin Dashboard & Analytics
- **FR-06.1** Admin dashboard displays summary stats: total votes, total students, total menus, active menus
- **FR-06.2** Dashboard shows the most popular dish (all-time)
- **FR-06.3** Dashboard shows a bar chart of votes per day (last 14 days)
- **FR-06.4** Dashboard shows a pie chart of dish distribution (top 10 dishes by votes)
- **FR-06.5** Dashboard shows a line chart of weekly voting trends (last 8 weeks)
- **FR-06.6** Dashboard shows a horizontal bar chart of meal type breakdown (breakfast / lunch / dinner)
- **FR-06.7** Dashboard shows a recent activity table (last 10 votes)
- **FR-06.8** All charts use Recharts library

### FR-07: CSV Export
- **FR-07.1** Admin can export voting results filtered by a date range (start date + end date)
- **FR-07.2** CSV columns: Date, Meal Type, Dish Name, Votes
- **FR-07.3** Export is triggered via a button in the Admin Panel; file downloads automatically

### FR-08: Notifications
- **FR-08.1** In-app toast notifications are shown for all key actions (vote cast, login success, errors, etc.)
- **FR-08.2** No email or SMS notifications required

---

## Non-Functional Requirements

### NFR-01: Performance
- **NFR-01.1** API response time under normal load (≤100 concurrent users) must be < 500ms for all endpoints
- **NFR-01.2** Dashboard stats endpoint may take up to 2 seconds (aggregation query)
- **NFR-01.3** Frontend initial load time < 3 seconds on a standard broadband connection

### NFR-02: Scalability
- **NFR-02.1** System must support up to 500 concurrent students (college campus scale)
- **NFR-02.2** Database connection pooling must be configured (pool_recycle, pool_pre_ping)

### NFR-03: Security
- **NFR-03.1** Passwords hashed with bcrypt (adaptive algorithm)
- **NFR-03.2** JWT tokens signed with a secret key stored in environment variables (never hardcoded)
- **NFR-03.3** All admin endpoints enforce server-side role checks
- **NFR-03.4** CORS restricted to explicitly allowed origins (configured via environment variable)
- **NFR-03.5** All database queries use SQLAlchemy ORM (parameterized — no raw SQL concatenation)
- **NFR-03.6** Input validation on all API endpoints (type, length, format)
- **NFR-03.7** HTTP security headers set on all responses (CSP, HSTS, X-Content-Type-Options, X-Frame-Options, Referrer-Policy)
- **NFR-03.8** Rate limiting on login endpoint to prevent brute-force attacks
- **NFR-03.9** Structured application logging (no PII or tokens in logs)
- **NFR-03.10** Generic error messages returned to clients (no stack traces)

### NFR-04: Reliability
- **NFR-04.1** Database unique constraints enforce vote integrity at the DB level (not just application level)
- **NFR-04.2** Global error handler catches all unhandled exceptions and returns safe responses
- **NFR-04.3** Database connection pool configured with pre-ping to handle stale connections

### NFR-05: Usability
- **NFR-05.1** Responsive UI supporting mobile (320px+) and desktop (1280px+)
- **NFR-05.2** Card-based layout with clean spacing and modern design (Tailwind CSS)
- **NFR-05.3** Loading states shown during all async operations
- **NFR-05.4** Toast notifications for all user-facing actions

### NFR-06: Maintainability
- **NFR-06.1** Backend structured as Flask blueprints (auth, menu, admin, voting, dashboard)
- **NFR-06.2** Frontend structured as pages + components + context + utils
- **NFR-06.3** Environment variables used for all configuration (`.env` files, never hardcoded)
- **NFR-06.4** Code comments on all non-trivial functions and modules

### NFR-07: Data
- **NFR-07.1** Voting history retained indefinitely (no automatic purge)
- **NFR-07.2** MySQL 8.0 on local machine for development
- **NFR-07.3** Database schema uses utf8mb4 character set

### NFR-08: Deployment
- **NFR-08.1** Backend deployable to a single VPS/server (Flask + Gunicorn)
- **NFR-08.2** Frontend deployable to separate static hosting (Netlify / Vercel)
- **NFR-08.3** Docker Compose file provided for local development convenience
- **NFR-08.4** All dependencies pinned to exact versions (requirements.txt, package.json)

---

## Extension Configuration

| Extension | Status |
|---|---|
| Security Baseline | **ENABLED** — all 15 SECURITY rules enforced as blocking constraints |
| Property-Based Testing | **DISABLED** — simple CRUD application, PBT not required |

---

## Constraints & Assumptions

- Admin accounts are created by promoting existing student accounts (no separate admin registration flow)
- Vote change is implemented as delete-old-vote + insert-new-vote (not an update)
- Weekly menu copy is a manual admin action triggered from the Admin Panel (not a cron job)
- Feedback feature is additive — it does not affect voting results
- The system is single-canteen (one menu per date+meal, not multi-canteen)
- All times are stored and processed in UTC; frontend displays in local time

---

## Out of Scope

- Multi-canteen / multi-campus support
- Email or SMS notifications
- Mobile native app (web responsive only)
- Payment or ordering functionality
- Nutritional information per dish
