# Unit of Work — Story Map
## Mess / Canteen Menu Voting System

---

| Story | Title | Unit 1: Backend | Unit 2: Frontend | Unit 3: Database |
|---|---|:---:|:---:|:---:|
| US-01 | Student Registration | ✅ POST /register | ✅ RegisterPage | ✅ users table |
| US-02 | User Login | ✅ POST /login | ✅ LoginPage | ✅ users table |
| US-03 | Logout | ✅ JWT expiry | ✅ Navbar logout | — |
| US-04 | Admin Role Promotion | ✅ PUT /admin/users/:id/role | ✅ AdminPanel users tab | ✅ users.role |
| US-05 | Create Weekly Menu | ✅ POST /admin/create-menu | ✅ MenuFormModal | ✅ menus + menu_options |
| US-06 | Edit Menu | ✅ PUT /admin/menu/:id | ✅ MenuFormModal (edit) | ✅ menus + menu_options |
| US-07 | Delete Menu | ✅ DELETE /admin/menu/:id | ✅ AdminPanel delete | ✅ CASCADE delete |
| US-08 | Lock Voting | ✅ POST /admin/menu/:id/lock | ✅ AdminPanel lock btn | ✅ menus.is_locked |
| US-09 | Copy Last Week's Menu | ✅ POST /admin/copy-last-week | ✅ AdminPanel copy btn | ✅ menus + menu_options |
| US-10 | View Weekly Menu | ✅ GET /menus?week= | ✅ VotingPage | ✅ menus + menu_options |
| US-11 | Cast a Vote | ✅ POST /vote | ✅ VoteModal | ✅ votes (UNIQUE constraint) |
| US-12 | Change Vote | ✅ POST /vote (upsert) | ✅ VoteModal (pre-select) | ✅ votes (delete+insert) |
| US-13 | View Results (After Deadline) | ✅ GET /results/:id | ✅ ResultsPage | ✅ votes + menu_options |
| US-14 | Submit Meal Feedback | ✅ POST /feedback | ✅ FeedbackForm | ✅ feedback table |
| US-15 | View Feedback (Admin) | ✅ GET /feedback/:id | ✅ AdminPanel feedback | ✅ feedback table |
| US-16 | View Summary Stats | ✅ GET /dashboard/stats | ✅ DashboardPage (admin) | ✅ aggregation queries |
| US-17 | View Voting Charts | ✅ GET /dashboard/stats | ✅ Recharts components | ✅ aggregation queries |
| US-18 | View Recent Activity | ✅ GET /dashboard/stats | ✅ Activity table | ✅ JOIN query |
| US-19 | Export Results as CSV | ✅ GET /export/results?start&end | ✅ AdminPanel export | ✅ votes + menus |

**Coverage**: 19/19 stories covered across all 3 units ✅
