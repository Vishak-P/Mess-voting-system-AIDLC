# User Stories
## Mess / Canteen Menu Voting System

Stories follow the INVEST criteria (Independent, Negotiable, Valuable, Estimable, Small, Testable).
Format: **As a [persona], I want to [action], so that [benefit].**

---

## Epic 1: Authentication

### US-01: Student Registration
**As a** student,
**I want to** register with my name, email, and password,
**so that** I can access the voting system.

**Acceptance Criteria:**
- [ ] Registration form requires name, email, and password (min 8 chars)
- [ ] Duplicate email shows a clear error message
- [ ] Successful registration logs me in automatically and redirects to dashboard
- [ ] My role is set to `student` by default

---

### US-02: User Login
**As a** registered user (student or admin),
**I want to** log in with my email and password,
**so that** I can access my role-specific features.

**Acceptance Criteria:**
- [ ] Login form accepts email and password
- [ ] Invalid credentials show a generic error (no hint about which field is wrong)
- [ ] Successful login stores a JWT token and redirects to dashboard
- [ ] Token expires after 8 hours; expired token redirects to login with a message
- [ ] Login endpoint has brute-force protection (rate limiting)

---

### US-03: Logout
**As a** logged-in user,
**I want to** log out,
**so that** my session is ended and my account is secure.

**Acceptance Criteria:**
- [ ] Logout button is visible in the navbar
- [ ] Clicking logout removes the token from client storage
- [ ] After logout, accessing protected pages redirects to login

---

### US-04: Admin Role Promotion
**As an** admin,
**I want to** promote a student to admin role,
**so that** I can delegate management responsibilities.

**Acceptance Criteria:**
- [ ] Admin Panel shows a list of all users with their roles
- [ ] Admin can change a student's role to admin
- [ ] Role change takes effect immediately (next login reflects new role)
- [ ] Students cannot access this feature

---

## Epic 2: Menu Management (Admin)

### US-05: Create Weekly Menu
**As an** admin,
**I want to** create a menu for a specific date and meal type with dish options and a voting window,
**so that** students can vote for their preferred dish.

**Acceptance Criteria:**
- [ ] Form requires: date, meal type (breakfast/lunch/dinner), voting open time, deadline, and 2–10 dish options
- [ ] Duplicate date + meal type combination shows an error
- [ ] Created menu appears immediately in the menu list
- [ ] Students can see the menu once created

---

### US-06: Edit Menu
**As an** admin,
**I want to** edit a menu's deadline, lock status, or dish options,
**so that** I can correct mistakes or adjust the voting window.

**Acceptance Criteria:**
- [ ] Admin can update deadline, lock status, and dish options
- [ ] Editing dish options on a menu with existing votes warns the admin (votes will be deleted)
- [ ] Changes take effect immediately

---

### US-07: Delete Menu
**As an** admin,
**I want to** delete a menu,
**so that** I can remove incorrect or outdated entries.

**Acceptance Criteria:**
- [ ] Delete requires a confirmation prompt
- [ ] Deleting a menu removes all associated options and votes (cascade)
- [ ] Deleted menu no longer appears in any list

---

### US-08: Lock Voting
**As an** admin,
**I want to** manually lock voting for a menu,
**so that** I can close voting early if needed.

**Acceptance Criteria:**
- [ ] Lock button is visible for unlocked menus in the Admin Panel
- [ ] Locked menus show a "Locked" badge
- [ ] Students cannot vote on locked menus
- [ ] System auto-locks menus when their deadline passes

---

### US-09: Copy Last Week's Menu
**As an** admin,
**I want to** copy last week's menu as a template for the new week,
**so that** I don't have to re-enter recurring dishes from scratch.

**Acceptance Criteria:**
- [ ] "Copy Last Week" button in Admin Panel creates new menu entries for the current week
- [ ] Copied menus have the same dish options but new dates and a default deadline
- [ ] Admin can edit the copied menus before publishing
- [ ] Existing menus for the current week are not overwritten

---

## Epic 3: Voting (Student)

### US-10: View Weekly Menu
**As a** student,
**I want to** view the weekly menu grouped by date and meal type,
**so that** I know what options are available to vote on.

**Acceptance Criteria:**
- [ ] Menu page shows menus grouped by date, ordered breakfast → lunch → dinner
- [ ] Each menu card shows: meal type, date, dish options, deadline, and voting status
- [ ] Student can navigate to previous and next weeks
- [ ] Menus with passed deadlines show a "Closed" or "Locked" badge

---

### US-11: Cast a Vote
**As a** student,
**I want to** vote for one dish per meal,
**so that** my food preference is counted.

**Acceptance Criteria:**
- [ ] Voting modal shows all dish options as selectable buttons
- [ ] Only one option can be selected at a time
- [ ] Submitting a vote shows a success toast notification
- [ ] The voted option is highlighted on the menu card after voting
- [ ] Voting is blocked if the menu is locked or deadline has passed
- [ ] Attempting to vote twice on the same menu shows an error

---

### US-12: Change Vote
**As a** student,
**I want to** change my vote before the deadline,
**so that** I can update my preference if I change my mind.

**Acceptance Criteria:**
- [ ] If I have already voted, the voting modal pre-selects my current choice
- [ ] Selecting a different option and submitting replaces my previous vote
- [ ] Vote change is not allowed after the deadline
- [ ] Success toast confirms the vote was updated

---

### US-13: View Results (After Deadline)
**As a** student,
**I want to** see voting results after the deadline has passed,
**so that** I know which dish won.

**Acceptance Criteria:**
- [ ] Results page is accessible from the menu card after the deadline
- [ ] Results show each dish with vote count, percentage, and rank medals (🥇🥈🥉)
- [ ] The leading dish is highlighted
- [ ] My voted option is marked with "← Your vote"
- [ ] Results are NOT visible before the deadline (students see a "Results available after deadline" message)

---

## Epic 4: Feedback

### US-14: Submit Meal Feedback
**As a** student,
**I want to** rate a meal and leave a comment after the voting deadline,
**so that** I can share my experience with the canteen admin.

**Acceptance Criteria:**
- [ ] Feedback form appears on the results page after the deadline
- [ ] Form includes a 1–5 star rating (required) and optional text comment
- [ ] Each student can submit one feedback per menu
- [ ] Submitting feedback shows a success toast
- [ ] Feedback form is hidden before the deadline

---

### US-15: View Feedback (Admin)
**As an** admin,
**I want to** view student feedback for each menu,
**so that** I can understand student satisfaction and improve future menus.

**Acceptance Criteria:**
- [ ] Admin Panel shows a feedback tab or section per menu
- [ ] Feedback list shows: student name, star rating, comment, and submission time
- [ ] Average rating is displayed per menu

---

## Epic 5: Admin Dashboard & Analytics

### US-16: View Summary Stats
**As an** admin,
**I want to** see summary statistics on the dashboard,
**so that** I have a quick overview of system activity.

**Acceptance Criteria:**
- [ ] Dashboard shows: Total Votes, Total Students, Total Menus, Active Menus
- [ ] Stats update on page load (not real-time)

---

### US-17: View Voting Charts
**As an** admin,
**I want to** see charts of voting activity,
**so that** I can identify trends and popular dishes.

**Acceptance Criteria:**
- [ ] Bar chart: votes per day (last 14 days)
- [ ] Pie chart: dish distribution (top 10 dishes by total votes)
- [ ] Line chart: weekly voting trends (last 8 weeks)
- [ ] Horizontal bar chart: meal type breakdown (breakfast/lunch/dinner)
- [ ] All charts use Recharts and are responsive

---

### US-18: View Recent Activity
**As an** admin,
**I want to** see a recent activity feed,
**so that** I can monitor voting in real time.

**Acceptance Criteria:**
- [ ] Table shows last 10 votes with: student name, dish, meal type, date
- [ ] Table is sorted by most recent first

---

## Epic 6: CSV Export

### US-19: Export Results as CSV
**As an** admin,
**I want to** export voting results for a date range as a CSV file,
**so that** I can use the data in planning meetings.

**Acceptance Criteria:**
- [ ] Export button in Admin Panel opens a date range picker
- [ ] CSV includes columns: Date, Meal Type, Dish Name, Votes
- [ ] File downloads automatically with filename `voting_results_[start]_[end].csv`
- [ ] Empty date range exports all results

---

## Story Summary

| Epic | Stories | Persona |
|---|---|---|
| Authentication | US-01 to US-04 | Student, Admin |
| Menu Management | US-05 to US-09 | Admin |
| Voting | US-10 to US-13 | Student |
| Feedback | US-14 to US-15 | Student, Admin |
| Dashboard & Analytics | US-16 to US-18 | Admin |
| CSV Export | US-19 | Admin |
| **Total** | **19 stories** | |
