# Security Test Instructions
## Mess / Canteen Menu Voting System

---

## SECURITY-05: Input Validation Tests

```bash
# SQL injection attempt (should return 400/401, not 500)
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@mess.com\" OR 1=1 --", "password": "x"}'
# Expected: 401 "Invalid email or password"

# Oversized payload
curl -X POST http://localhost:5000/api/register \
  -H "Content-Type: application/json" \
  -d '{"name": "'$(python -c "print('A'*10000)")'", "email": "x@x.com", "password": "password123"}'
# Expected: 400 (validation error)
```

---

## SECURITY-08: Authorization Tests

```bash
# Student accessing admin endpoint
curl -X GET http://localhost:5000/api/admin/users \
  -H "Authorization: Bearer <student_token>"
# Expected: 403 "Admin access required"

# Unauthenticated access
curl -X GET http://localhost:5000/api/menus
# Expected: 401 "Authentication required"

# Accessing another user's data (IDOR check)
curl -X GET http://localhost:5000/api/results/<menu_id> \
  -H "Authorization: Bearer <student_token>"
# Before deadline: Expected 403
```

---

## SECURITY-09: Error Response Tests

```bash
# Trigger 404 — should not expose stack trace
curl http://localhost:5000/api/nonexistent
# Expected: {"error": "..."} — no stack trace, no framework version

# Trigger 500 — should return generic message
# (Manually break a route and test)
# Expected: {"error": "Internal server error"}
```

---

## SECURITY-12: Brute Force Protection

```bash
# Send 11 login requests in 1 minute
for i in {1..11}; do
  curl -X POST http://localhost:5000/api/login \
    -H "Content-Type: application/json" \
    -d '{"email": "test@test.com", "password": "wrong"}'
done
# Expected: 11th request returns 429 "Too many requests"
```

---

## SECURITY-04: HTTP Headers Check

```bash
curl -I http://localhost:5000/api/health
# Expected headers:
# X-Content-Type-Options: nosniff
# X-Frame-Options: DENY
# Referrer-Policy: strict-origin-when-cross-origin
# Content-Security-Policy: default-src 'self'...
# Strict-Transport-Security: max-age=31536000...
```

---

## SECURITY-10: Dependency Vulnerability Scan

```bash
# Backend
cd mess-voting-system/backend
pip install pip-audit==2.7.3
pip-audit -r requirements.txt
# Expected: 0 known vulnerabilities

# Frontend
cd mess-voting-system/frontend
npm audit --audit-level=high
# Expected: 0 high/critical vulnerabilities
```
