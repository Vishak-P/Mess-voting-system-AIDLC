# Unit of Work Dependencies
## Mess / Canteen Menu Voting System

---

## Dependency Matrix

| Unit | Depends On | Type | Notes |
|---|---|---|---|
| Unit 1: Backend | Unit 3: Database | Runtime | Flask connects to MySQL via SQLAlchemy |
| Unit 2: Frontend | Unit 1: Backend | Runtime | React calls Flask REST API via Axios |
| Unit 3: Database | None | — | Independent; must be set up first |

---

## Build Order

```
Unit 3 (Database)
    └── Unit 1 (Backend)
            └── Unit 2 (Frontend)
```

Unit 3 must be running before Unit 1 can start. Unit 1 must be running before Unit 2 can be fully tested.

---

## Integration Points

| Integration | Protocol | Auth | Notes |
|---|---|---|---|
| Frontend → Backend | HTTP/REST (JSON) | JWT Bearer token | Axios interceptor attaches token |
| Backend → Database | TCP (MySQL protocol) | DB user/password | SQLAlchemy connection pool |

---

## Shared Contracts

### API Contract (Unit 1 ↔ Unit 2)
- Base URL: `http://localhost:5000/api` (dev) / configured via `REACT_APP_API_URL`
- All responses: `Content-Type: application/json`
- Auth: `Authorization: Bearer <token>` header
- Error format: `{"error": "message"}`
- Success format: `{"key": value, ...}`

### Database Contract (Unit 3 ↔ Unit 1)
- Connection string: `mysql+pymysql://user:pass@host:port/mess_voting`
- Character set: utf8mb4
- All tables use InnoDB engine
