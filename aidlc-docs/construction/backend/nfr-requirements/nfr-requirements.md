# NFR Requirements — Unit 1: Backend
## Mess / Canteen Menu Voting System

---

## Performance
| Requirement | Target | Notes |
|---|---|---|
| API response time (p95) | < 500ms | Under 100 concurrent users |
| Dashboard stats endpoint | < 2000ms | Aggregation queries; acceptable |
| DB connection pool | pool_size=10, max_overflow=20 | SQLAlchemy config |
| Connection recycle | 300 seconds | Prevent stale connections |
| Connection pre-ping | Enabled | Detect dead connections |

## Scalability
| Requirement | Target |
|---|---|
| Concurrent users | 500 students |
| Votes per day | ~1500 (500 students × 3 meals) |
| DB rows (votes, 1 year) | ~547,500 — well within MySQL limits |

## Security (SECURITY extension — all rules enforced)
| Rule | Implementation |
|---|---|
| SECURITY-01 | MySQL TLS connection enforced in production; local dev exempt |
| SECURITY-03 | Python `logging` module; structured format; no PII in logs |
| SECURITY-04 | `flask-talisman` or manual middleware sets all required HTTP headers |
| SECURITY-05 | All inputs validated via marshmallow schemas or manual checks; SQLAlchemy ORM (parameterized) |
| SECURITY-06 | N/A — no cloud IAM policies; role checks are application-level |
| SECURITY-07 | N/A — local dev; VPS firewall rules documented in setup guide |
| SECURITY-08 | `jwt_required()` on all protected routes; `admin_required` decorator on admin routes; CORS restricted |
| SECURITY-09 | Generic error messages; no stack traces in production; debug=False in production |
| SECURITY-10 | `requirements.txt` with pinned versions; `pip-audit` recommended |
| SECURITY-11 | Auth logic in `utils/auth_service.py`; rate limiting on `/api/login` |
| SECURITY-12 | bcrypt hashing; JWT expiry 8h; brute-force protection via `flask-limiter` |
| SECURITY-13 | N/A — no external CDN scripts in backend; SQLAlchemy prevents unsafe deserialization |
| SECURITY-14 | Structured logging captures auth failures; log retention policy documented |
| SECURITY-15 | Global error handler in `app.py`; all DB calls in try/except; transactions rolled back on error |

## Reliability
| Requirement | Implementation |
|---|---|
| Vote integrity | DB UNIQUE constraint `(user_id, menu_id)` |
| Menu integrity | DB UNIQUE constraint `(date, meal_type)` |
| Global error handler | Catches all unhandled exceptions; returns `{"error": "Internal server error"}` |
| Transaction safety | Vote change uses atomic delete+insert in single transaction |

## Maintainability
| Requirement | Implementation |
|---|---|
| Blueprint structure | auth, menu, admin, voting, feedback, dashboard |
| Environment config | All secrets in `.env`; never hardcoded |
| Dependency pinning | All packages pinned in `requirements.txt` |
| Code comments | Docstrings on all modules and non-trivial functions |

## Logging
| Requirement | Implementation |
|---|---|
| Format | `%(asctime)s [%(levelname)s] %(name)s: %(message)s` |
| Level | INFO in production, DEBUG in development |
| Sensitive data | Passwords, tokens, PII never logged |
| Auth events | Login success/failure logged with user email (not password) |
