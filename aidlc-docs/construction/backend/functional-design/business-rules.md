# Business Rules — Unit 1: Backend
## Mess / Canteen Menu Voting System

---

## BR-01: Voting Window
A student may cast or change a vote on a menu **only if ALL** of the following are true:
1. `menu.is_locked == False`
2. `datetime.utcnow() >= menu.open_time`
3. `datetime.utcnow() < menu.deadline`

If any condition fails → HTTP 403 "Voting is closed for this menu"

---

## BR-02: Vote Uniqueness
Each `(user_id, menu_id)` pair may have at most one Vote row.
- Enforced at application layer (check before insert)
- Enforced at database layer (UNIQUE constraint)
- On duplicate → HTTP 409 "You have already voted for this meal"

---

## BR-03: Vote Change
A student may change their vote by:
1. Deleting the existing Vote row for `(user_id, menu_id)`
2. Inserting a new Vote row with the new `option_id`
This is an atomic operation within a single DB transaction.
Vote change is only allowed while BR-01 conditions are met.

---

## BR-04: Result Visibility
- **Admin**: Can view results at any time (before or after deadline)
- **Student**: Can view results **only after** `datetime.utcnow() >= menu.deadline`
  - Before deadline → HTTP 403 "Results are not available until voting closes"

---

## BR-05: Feedback Eligibility
A student may submit feedback for a menu **only if**:
1. `datetime.utcnow() >= menu.deadline` (voting has closed)
2. No existing Feedback row for `(user_id, menu_id)`

If condition 1 fails → HTTP 403 "Feedback is only available after the voting deadline"
If condition 2 fails → HTTP 409 "You have already submitted feedback for this meal"

---

## BR-06: Menu Uniqueness
Only one Menu may exist per `(date, meal_type)` combination.
- Enforced at application layer (check before insert)
- Enforced at database layer (UNIQUE constraint)
- On duplicate → HTTP 409 "Menu for this date and meal already exists"

---

## BR-07: Admin Role Enforcement
All admin endpoints verify `identity["role"] == "admin"` server-side.
Client-side hiding is not sufficient — every admin route uses the `admin_required` decorator.
Non-admin access → HTTP 403 "Admin access required"

---

## BR-08: Auto-Lock
Menus whose `deadline < datetime.utcnow()` and `is_locked == False` are auto-locked.
This runs:
- On every call to `menu.is_voting_open()` (lazy check)
- Via the scheduler utility (periodic batch lock)

---

## BR-09: Weekly Menu Copy
When copying last week's menus:
1. Compute `last_week_start = current_week_start - 7 days`
2. Fetch all menus where `date BETWEEN last_week_start AND last_week_start + 6`
3. For each source menu, create a new menu with:
   - `date = source.date + 7 days`
   - Same `meal_type` and dish options
   - `open_time` and `deadline` set to default times (admin can edit after)
   - `is_locked = False`
4. Skip if a menu already exists for the target `(date, meal_type)`
5. Return `{created: [...], skipped: [...]}`

---

## BR-10: Input Validation Rules

| Field | Rule |
|---|---|
| email | Valid email format (regex), max 150 chars |
| password | Min 8 characters |
| name | Non-empty, max 100 chars |
| dish_name | Non-empty, max 200 chars |
| options count | Min 2, max 10 per menu |
| rating | Integer 1–5 inclusive |
| comment | Max 1000 chars |
| date | Valid ISO date (YYYY-MM-DD) |
| deadline / open_time | Valid ISO 8601 datetime; deadline must be after open_time |
