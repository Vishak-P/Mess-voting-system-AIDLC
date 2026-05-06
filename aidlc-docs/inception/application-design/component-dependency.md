# Component Dependencies
## Mess / Canteen Menu Voting System

---

## Dependency Matrix

| Component | Depends On | Communication Pattern |
|---|---|---|
| BC-01 AuthController | BC-08 DatabaseModels, BC-07 AuthMiddleware, SVC-01 AuthService | Direct function call |
| BC-02 MenuController | BC-08 DatabaseModels, BC-07 AuthMiddleware | Direct function call |
| BC-03 AdminController | BC-08 DatabaseModels, BC-07 AuthMiddleware, SVC-03 MenuService | Direct function call |
| BC-04 VotingController | BC-08 DatabaseModels, BC-07 AuthMiddleware, SVC-02 VotingService | Direct function call |
| BC-05 DashboardController | BC-08 DatabaseModels, BC-07 AuthMiddleware | Direct function call (SQL aggregation) |
| BC-06 FeedbackController | BC-08 DatabaseModels, BC-07 AuthMiddleware | Direct function call |
| FC-01 AuthPages | AuthContext (FC) | React Context |
| FC-02 DashboardPage | api.js, AuthContext | HTTP (Axios) |
| FC-03 VotingPage | api.js, AuthContext, FC-07 VoteModal | HTTP (Axios) + React state |
| FC-04 ResultsPage | api.js, AuthContext, FC-09 FeedbackForm | HTTP (Axios) |
| FC-05 AdminPanel | api.js, AuthContext, FC-08 MenuFormModal | HTTP (Axios) |
| FC-06 Navbar | AuthContext | React Context |
| FC-07 VoteModal | FC-10 VoteButton | Props |
| FC-08 MenuFormModal | api.js | HTTP (Axios) |
| FC-09 FeedbackForm | api.js | HTTP (Axios) |

---

## Data Flow Diagram

```
Browser (React SPA)
    |
    | HTTPS (JWT in Authorization header)
    v
Flask API (/api/*)
    |
    |-- AuthMiddleware (JWT validation on every request)
    |
    |-- Controllers (blueprints)
    |       |
    |       |-- Services (business logic)
    |       |
    |       v
    |   SQLAlchemy ORM
    |       |
    v       v
    MySQL 8.0 Database
```

---

## Key Dependency Rules

1. **Frontend never accesses DB directly** — all data flows through the Flask API
2. **All API calls carry JWT** — AuthMiddleware validates on every protected route
3. **Admin routes double-check role** — `admin_required` decorator on every admin endpoint
4. **DB constraints are the last line of defense** — unique constraints on votes and menus back up application-level checks
5. **Services are stateless** — no shared mutable state between requests
