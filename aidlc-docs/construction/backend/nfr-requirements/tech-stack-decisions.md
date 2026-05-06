# Tech Stack Decisions — Unit 1: Backend

| Decision | Choice | Rationale |
|---|---|---|
| Web framework | Flask 3.x | Lightweight, blueprint-based, well-suited for REST APIs at this scale |
| ORM | Flask-SQLAlchemy 3.x | Parameterized queries, relationship management, migration support |
| Auth | Flask-JWT-Extended 4.x | JWT issuance, validation, identity injection |
| Password hashing | Flask-Bcrypt (bcrypt) | Adaptive algorithm; SECURITY-12 compliant |
| CORS | Flask-CORS 4.x | Origin restriction; SECURITY-08 compliant |
| Rate limiting | Flask-Limiter | Brute-force protection on login; SECURITY-11/12 compliant |
| Security headers | flask-talisman | CSP, HSTS, X-Frame-Options, etc.; SECURITY-04 compliant |
| DB driver | PyMySQL 1.x | Pure Python MySQL driver; works with SQLAlchemy |
| Migrations | Flask-Migrate (Alembic) | Schema version control |
| Validation | Manual + marshmallow | Input validation; SECURITY-05 compliant |
| CSV generation | Python stdlib `csv` | No extra dependency needed |
| Logging | Python stdlib `logging` | Structured logging; SECURITY-03 compliant |
| WSGI server (prod) | Gunicorn | Production-grade; not included in requirements.txt (separate install) |
