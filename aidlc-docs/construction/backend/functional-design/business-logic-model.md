# Business Logic Model — Unit 1: Backend
## Mess / Canteen Menu Voting System

---

## Core Workflows

### Workflow 1: User Registration
```
Input: {name, email, password}
1. Validate: name non-empty, email format, password >= 8 chars
2. Check: email not already in users table
3. Hash: bcrypt(password) → hashed_pw
4. Insert: User(name, email, hashed_pw, role='student')
5. Generate: JWT token {id, role}
6. Return: {token, user.to_dict()}
```

### Workflow 2: Login
```
Input: {email, password}
1. Validate: email and password non-empty
2. Lookup: User WHERE email = input.email
3. Verify: bcrypt.check(input.password, user.password)
4. If fail → 401 "Invalid email or password"
5. Generate: JWT token {id, role}
6. Return: {token, user.to_dict()}
```

### Workflow 3: Cast / Change Vote
```
Input: {menu_id, option_id}, JWT identity
1. Validate: menu_id and option_id present
2. Lookup: Menu by menu_id → 404 if not found
3. Check BR-01: voting window open → 403 if closed
4. Validate: MenuOption.menu_id == menu_id → 400 if mismatch
5. Check existing vote: Vote WHERE user_id=me AND menu_id=menu_id
6a. If no existing vote:
    INSERT Vote(user_id, menu_id, option_id)
6b. If existing vote (vote change):
    DELETE existing Vote
    INSERT new Vote(user_id, menu_id, option_id)
    (atomic transaction)
7. Return: {vote.to_dict()}
```

### Workflow 4: Get Results
```
Input: menu_id, JWT identity
1. Lookup: Menu by menu_id → 404 if not found
2. Check BR-04: if student AND deadline not passed → 403
3. Fetch: all MenuOptions for menu_id
4. For each option: count votes
5. Compute: percentage = (vote_count / total) * 100
6. Sort: by vote_count DESC
7. Fetch: user's own vote for this menu
8. Return: {menu, results[], total_votes, user_voted, user_voted_option_id}
```

### Workflow 5: Submit Feedback
```
Input: {menu_id, rating, comment}, JWT identity
1. Validate: rating 1-5, comment max 1000 chars
2. Lookup: Menu by menu_id → 404 if not found
3. Check BR-05a: deadline passed → 403 if not
4. Check BR-05b: no existing feedback → 409 if exists
5. INSERT Feedback(user_id, menu_id, rating, comment)
6. Return: {feedback.to_dict()}
```

### Workflow 6: Dashboard Stats
```
Input: JWT identity (admin only)
1. COUNT votes → total_votes
2. COUNT users WHERE role='student' → total_students
3. COUNT menus → total_menus
4. COUNT menus WHERE is_locked=False AND deadline > now → active_menus
5. JOIN MenuOption+Vote GROUP BY option → most popular dish
6. GROUP votes by date (last 14 days) → votes_per_day[]
7. GROUP votes by dish (top 10) → dish_distribution[]
8. GROUP votes by YEARWEEK (last 8 weeks) → weekly_trends[]
9. GROUP votes by meal_type → meal_breakdown[]
10. JOIN Vote+User+MenuOption+Menu ORDER BY voted_at DESC LIMIT 10 → recent_activity[]
11. Return: all aggregated data
```

### Workflow 7: Export CSV
```
Input: {start_date?, end_date?}, JWT identity (admin only)
1. Build query: Menu JOIN MenuOption LEFT JOIN Vote
2. Apply date filter if start_date/end_date provided
3. GROUP BY menu_id, option_id → vote counts
4. Write CSV rows: [Date, Meal Type, Dish Name, Votes]
5. Return: CSV file as attachment
```

### Workflow 8: Copy Last Week's Menus
```
Input: JWT identity (admin only)
1. Compute: current_week_start (Monday of current week)
2. Compute: last_week_start = current_week_start - 7 days
3. Fetch: all menus WHERE date BETWEEN last_week_start AND last_week_start+6
4. For each source_menu:
   a. target_date = source_menu.date + 7 days
   b. Check: no existing menu for (target_date, source_menu.meal_type)
   c. If exists: add to skipped[]
   d. If not: INSERT new Menu + copy MenuOptions → add to created[]
5. Return: {created[], skipped[]}
```
