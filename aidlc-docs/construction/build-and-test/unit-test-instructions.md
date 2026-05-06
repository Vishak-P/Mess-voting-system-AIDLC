# Unit Test Instructions
## Mess / Canteen Menu Voting System

---

## Backend Unit Tests (pytest)

### Setup
```bash
cd mess-voting-system/backend
pip install pytest==8.2.2 pytest-flask==1.3.0 pytest-cov==5.0.0
```

### Run Tests
```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```

### Key Test Cases to Implement

#### Auth Tests (`tests/test_auth.py`)
- `test_register_success` — valid input creates user, returns token
- `test_register_duplicate_email` — returns 409
- `test_register_short_password` — returns 400
- `test_login_success` — valid credentials return token
- `test_login_invalid_password` — returns 401 (generic message)
- `test_login_unknown_email` — returns 401 (same generic message)

#### Voting Tests (`tests/test_voting.py`)
- `test_cast_vote_success` — valid vote returns 201
- `test_cast_vote_closed_window` — returns 403
- `test_cast_vote_duplicate` — returns 409
- `test_change_vote_success` — second vote replaces first
- `test_results_student_before_deadline` — returns 403
- `test_results_student_after_deadline` — returns 200 with results
- `test_results_admin_before_deadline` — returns 200 (admin bypass)

#### Admin Tests (`tests/test_admin.py`)
- `test_create_menu_success` — admin creates menu
- `test_create_menu_student_forbidden` — student gets 403
- `test_create_menu_duplicate` — returns 409
- `test_delete_menu_cascades` — votes deleted with menu
- `test_copy_last_week` — creates menus for current week
- `test_promote_user` — changes role successfully

#### Feedback Tests (`tests/test_feedback.py`)
- `test_submit_feedback_after_deadline` — returns 201
- `test_submit_feedback_before_deadline` — returns 403
- `test_submit_feedback_duplicate` — returns 409

### Expected Coverage Target: ≥ 80%

---

## Frontend Unit Tests (React Testing Library)

### Setup
```bash
cd mess-voting-system/frontend
# react-scripts includes jest + @testing-library/react
```

### Run Tests
```bash
npm test -- --watchAll=false --coverage
```

### Key Test Cases to Implement

#### Component Tests
- `LoginPage` — renders form, shows error on invalid submit
- `RegisterPage` — validates password match
- `VoteModal` — renders options, submit disabled until selection
- `FeedbackForm` — star rating interaction, submit calls API
- `StatCard` — renders title and value
- `MenuCard` — shows "Voted" badge when userVotedOptionId set

#### Context Tests
- `AuthContext` — login stores token, logout clears storage
