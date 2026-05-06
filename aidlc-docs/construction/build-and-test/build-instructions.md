# Build Instructions
## Mess / Canteen Menu Voting System

---

## Prerequisites

| Requirement | Version | Notes |
|---|---|---|
| Python | 3.9+ | Backend runtime |
| Node.js | 18+ | Frontend build |
| MySQL | 8.0+ | Database |
| pip | Latest | Python package manager |
| npm | 9+ | Node package manager |

---

## 1. Database Setup

```bash
# Create schema
mysql -u root -p < mess-voting-system/database/schema.sql

# Load seed data
mysql -u root -p mess_voting < mess-voting-system/database/seed.sql
```

---

## 2. Backend Setup

```bash
cd mess-voting-system/backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate
# Activate (macOS/Linux)
source venv/bin/activate

# Install pinned dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env: set DB_PASSWORD, SECRET_KEY, JWT_SECRET_KEY

# Initialize database tables (if not using schema.sql)
flask db-init

# Start development server
python app.py
```

**Expected output**: `Running on http://0.0.0.0:5000`

---

## 3. Frontend Setup

```bash
cd mess-voting-system/frontend

# Install pinned dependencies
npm install

# Configure environment
cp .env.example .env
# Edit .env: REACT_APP_API_URL=http://localhost:5000/api

# Start development server
npm start
```

**Expected output**: `Compiled successfully! Local: http://localhost:3000`

---

## 4. Production Build

```bash
# Frontend production build
cd mess-voting-system/frontend
npm run build
# Output: frontend/build/ (deploy to Netlify/Vercel/S3)

# Backend production (Gunicorn)
cd mess-voting-system/backend
pip install gunicorn==21.2.0
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

---

## Troubleshooting

| Error | Cause | Fix |
|---|---|---|
| `ModuleNotFoundError` | venv not activated | Run `source venv/bin/activate` |
| `Access denied for user` | Wrong DB credentials | Check `.env` DB_PASSWORD |
| `CORS error` in browser | CORS_ORIGINS mismatch | Set `CORS_ORIGINS=http://localhost:3000` in `.env` |
| `npm ERR! peer dep` | Node version mismatch | Use Node 18+ |
| `talisman` import error | Package name | Use `from talisman import Talisman` |
