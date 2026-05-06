# Mess / Canteen Menu Voting System

A production-level full-stack web application for student mess/canteen menu voting.

## Tech Stack
- **Frontend**: React.js + Tailwind CSS + Recharts
- **Backend**: Flask (Python)
- **Database**: MySQL
- **Auth**: JWT-based

## Project Structure
```
mess-voting-system/
├── backend/          # Flask API
├── frontend/         # React app
├── database/         # SQL schema + seed data
└── README.md
```

## Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+
- MySQL 8.0+

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env      # Edit with your DB credentials
flask db-init             # Initialize database
python app.py
```

### Frontend Setup
```bash
cd frontend
npm install
cp .env.example .env      # Edit API URL if needed
npm start
```

### Database Setup
```bash
mysql -u root -p < database/schema.sql
mysql -u root -p mess_voting < database/seed.sql
```

## Default Credentials
- **Admin**: admin@mess.com / admin123
- **Student**: student1@test.com / student123

## API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/register | Register user |
| POST | /api/login | Login |
| GET | /api/menus | Get all menus |
| GET | /api/menu/:id | Get menu by ID |
| POST | /api/admin/create-menu | Create menu (admin) |
| PUT | /api/admin/menu/:id | Update menu (admin) |
| DELETE | /api/admin/menu/:id | Delete menu (admin) |
| POST | /api/vote | Cast vote |
| GET | /api/results/:menu_id | Get results |
| GET | /api/dashboard/stats | Dashboard stats |
| GET | /api/export/results | Export CSV |
