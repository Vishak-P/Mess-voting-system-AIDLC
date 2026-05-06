# Component Methods
## Mess / Canteen Menu Voting System

---

## BC-01: AuthController

| Method | Signature | Description |
|---|---|---|
| `register` | `POST /api/register` → `{token, user}` | Validate input, hash password, create user, return JWT |
| `login` | `POST /api/login` → `{token, user}` | Verify credentials, return JWT |
| `profile` | `GET /api/profile` → `{user}` | Return current user from JWT identity |

---

## BC-02: MenuController

| Method | Signature | Description |
|---|---|---|
| `get_menus` | `GET /api/menus?date&meal_type&week` → `{menus[], count}` | Return filtered menus with options |
| `get_menu` | `GET /api/menu/<id>` → `{menu}` | Return single menu with options |

---

## BC-03: AdminController

| Method | Signature | Description |
|---|---|---|
| `create_menu` | `POST /api/admin/create-menu` → `{menu}` | Create menu with options and voting window |
| `update_menu` | `PUT /api/admin/menu/<id>` → `{menu}` | Update deadline, lock, or options |
| `delete_menu` | `DELETE /api/admin/menu/<id>` → `{message}` | Delete menu + cascade |
| `lock_menu` | `POST /api/admin/menu/<id>/lock` → `{menu}` | Manually lock voting |
| `copy_last_week` | `POST /api/admin/copy-last-week` → `{created[], skipped[]}` | Copy last week's menus to current week |
| `list_users` | `GET /api/admin/users` → `{users[], count}` | List all users |
| `promote_user` | `PUT /api/admin/users/<id>/role` → `{user}` | Change user role |

---

## BC-04: VotingController

| Method | Signature | Description |
|---|---|---|
| `cast_vote` | `POST /api/vote` → `{vote}` | Cast or change vote; enforce voting window and uniqueness |
| `get_results` | `GET /api/results/<menu_id>` → `{menu, results[], total_votes, user_voted}` | Return results; enforce visibility rule |
| `my_votes` | `GET /api/my-votes` → `{votes[], count}` | Return all votes by current user |

---

## BC-05: DashboardController

| Method | Signature | Description |
|---|---|---|
| `dashboard_stats` | `GET /api/dashboard/stats` → `{summary, most_popular_dish, votes_per_day[], dish_distribution[], weekly_trends[], meal_breakdown[], recent_activity[]}` | All analytics data |
| `export_results` | `GET /api/export/results?start_date&end_date` → CSV | Export results as CSV with optional date range |

---

## BC-06: FeedbackController

| Method | Signature | Description |
|---|---|---|
| `submit_feedback` | `POST /api/feedback` → `{feedback}` | Submit star rating + comment; enforce post-deadline and one-per-user |
| `get_feedback` | `GET /api/feedback/<menu_id>` → `{feedback[], avg_rating}` | Return feedback for a menu (admin: all; student: own) |

---

## BC-07: AuthMiddleware

| Method | Signature | Description |
|---|---|---|
| `admin_required` | Decorator → 403 if not admin | Enforce admin role on decorated routes |
| JWT handlers | `expired_token_loader`, `invalid_token_loader`, `unauthorized_loader` | Return standardized 401 responses |

---

## BC-08: DatabaseModels

| Model | Key Methods |
|---|---|
| `User` | `to_dict()` → `{id, name, email, role, created_at}` |
| `Menu` | `to_dict(include_options)`, `is_voting_open()` → bool |
| `MenuOption` | `to_dict()` → `{id, menu_id, dish_name, vote_count}` |
| `Vote` | `to_dict()` → `{id, user_id, menu_id, option_id, voted_at}` |
| `Feedback` | `to_dict()` → `{id, user_id, menu_id, rating, comment, created_at}` |

---

## Frontend Method Signatures (Key Hooks & Functions)

| Component | Method | Description |
|---|---|---|
| `AuthContext` | `login(email, password)` → `{success, user?, error?}` | Call login API, store token |
| `AuthContext` | `register(name, email, password)` → `{success, user?, error?}` | Call register API, store token |
| `AuthContext` | `logout()` → void | Clear token and user from storage |
| `VotingPage` | `handleVoteSubmit(menuId, optionId)` → void | POST /vote, refresh menus |
| `AdminPanel` | `handleDelete(id)` → void | DELETE /admin/menu/:id with confirmation |
| `AdminPanel` | `handleLock(id)` → void | POST /admin/menu/:id/lock |
| `AdminPanel` | `handleExport(startDate, endDate)` → void | GET /export/results, trigger download |
| `AdminPanel` | `handleCopyLastWeek()` → void | POST /admin/copy-last-week |
| `ResultsPage` | `fetchResults(menuId)` → void | GET /results/:id, enforce visibility |
