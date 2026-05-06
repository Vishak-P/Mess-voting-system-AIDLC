# Integration Test Instructions
## Mess / Canteen Menu Voting System

---

## Setup

```bash
# Start backend (with test DB)
cd mess-voting-system/backend
DB_NAME=mess_voting_test python app.py

# In another terminal, start frontend
cd mess-voting-system/frontend
REACT_APP_API_URL=http://localhost:5000/api npm start
```

---

## Scenario 1: Full Voting Workflow (Student)

**Description**: Student registers → logs in → views menu → votes → sees results after deadline

**Steps**:
1. `POST /api/register` with valid student data → expect 201 + token
2. `GET /api/menus?date=<today>` with token → expect menus list
3. `POST /api/vote` with valid menu_id + option_id → expect 201
4. `POST /api/vote` same menu_id → expect 409 (duplicate)
5. `GET /api/results/<menu_id>` before deadline → expect 403
6. (Manually set menu deadline to past in DB)
7. `GET /api/results/<menu_id>` after deadline → expect 200 with results

---

## Scenario 2: Admin Menu Lifecycle

**Steps**:
1. Login as admin → get token
2. `POST /api/admin/create-menu` → expect 201
3. `GET /api/menus` → menu appears in list
4. `PUT /api/admin/menu/<id>` update deadline → expect 200
5. `POST /api/admin/menu/<id>/lock` → expect 200, is_locked=true
6. Student tries to vote on locked menu → expect 403
7. `DELETE /api/admin/menu/<id>` → expect 200
8. `GET /api/menus` → menu no longer in list

---

## Scenario 3: Vote Change

**Steps**:
1. Student votes for option A → expect 201
2. Student votes for option B (same menu) → expect 201 (vote changed)
3. `GET /api/results/<menu_id>` (admin) → option B has 1 vote, option A has 0

---

## Scenario 4: Feedback After Deadline

**Steps**:
1. Set menu deadline to past
2. `POST /api/feedback` with rating=4, comment="Good" → expect 201
3. `POST /api/feedback` same menu → expect 409
4. `GET /api/feedback/<menu_id>` as admin → expect feedback list with avg_rating

---

## Scenario 5: CSV Export with Date Range

**Steps**:
1. Login as admin
2. `GET /api/export/results?start_date=2026-05-01&end_date=2026-05-07` → expect CSV download
3. Verify CSV has correct columns: Date, Meal Type, Dish Name, Votes
4. `GET /api/export/results` (no params) → expect all results

---

## Cleanup
```bash
mysql -u root -p -e "DROP DATABASE IF EXISTS mess_voting_test;"
```
