# Component Definitions
## Mess / Canteen Menu Voting System

---

## Backend Components (Flask)

### BC-01: AuthController
**Purpose**: Handles user registration, login, and profile retrieval.
**Responsibilities**:
- Validate registration input (name, email, password)
- Hash passwords with bcrypt before storage
- Issue JWT tokens on successful login/registration
- Return current user profile from JWT identity

### BC-02: MenuController
**Purpose**: Handles menu retrieval for all authenticated users.
**Responsibilities**:
- Return menus filtered by date, meal type, or ISO week
- Return a single menu with its dish options
- Group and sort menus for weekly view

### BC-03: AdminController
**Purpose**: Handles all admin-only menu management operations.
**Responsibilities**:
- Create new menus with dish options and voting window
- Update menu deadline, lock status, and dish options
- Delete menus (cascades to options and votes)
- Manually lock voting for a menu
- Copy last week's menus as templates for the new week
- List all users; promote student to admin
- Enforce admin role on every endpoint

### BC-04: VotingController
**Purpose**: Handles vote casting, vote changes, and per-menu results.
**Responsibilities**:
- Validate voting window is open before accepting a vote
- Enforce one-vote-per-user-per-menu (application + DB constraint)
- Support vote change (delete existing + insert new)
- Return results with vote counts and percentages
- Enforce result visibility rule (students see results only after deadline)

### BC-05: DashboardController
**Purpose**: Provides aggregated analytics data for the admin dashboard.
**Responsibilities**:
- Compute summary stats (total votes, students, menus, active menus)
- Identify most popular dish (all-time)
- Aggregate votes per day (last 14 days)
- Aggregate dish distribution (top 10)
- Aggregate weekly trends (last 8 weeks)
- Aggregate meal type breakdown
- Return recent activity (last 10 votes)
- Export results as CSV with optional date range filter

### BC-06: FeedbackController
**Purpose**: Handles post-meal feedback submission and retrieval.
**Responsibilities**:
- Accept star rating (1–5) and optional text comment
- Enforce one-feedback-per-user-per-menu
- Enforce feedback only after voting deadline
- Return feedback list and average rating per menu (admin)

### BC-07: AuthMiddleware
**Purpose**: Cross-cutting JWT validation and role enforcement.
**Responsibilities**:
- Validate JWT signature, expiration, audience on every protected request
- Provide `admin_required` decorator for admin-only routes
- Return standardized 401/403 error responses

### BC-08: DatabaseModels
**Purpose**: SQLAlchemy ORM models representing the data schema.
**Responsibilities**:
- Define User, Menu, MenuOption, Vote, Feedback models
- Enforce DB-level constraints (unique votes, unique menu per date+meal)
- Provide `to_dict()` serialization methods
- Manage relationships and cascade rules

---

## Frontend Components (React)

### FC-01: AuthPages (LoginPage, RegisterPage)
**Purpose**: User-facing authentication screens.
**Responsibilities**:
- Render login and registration forms with validation
- Call auth API and store JWT token in localStorage
- Redirect to dashboard on success; show toast on error
- Redirect authenticated users away from auth pages

### FC-02: DashboardPage
**Purpose**: Role-aware landing page after login.
**Responsibilities**:
- Admin view: fetch and render analytics stats + charts
- Student view: fetch today's menus + personal vote summary
- Render StatCards, ChartCards, and recent activity table

### FC-03: VotingPage
**Purpose**: Weekly menu browser with voting capability.
**Responsibilities**:
- Fetch menus for the selected week
- Fetch user's existing votes
- Group menus by date, sort by meal type
- Open VoteModal on "Vote Now" click
- Submit vote via API; refresh on success

### FC-04: ResultsPage
**Purpose**: Voting results viewer.
**Responsibilities**:
- List all menus with links to individual results (ResultsList)
- Show per-menu results with bar chart, ranked list, and user's vote (ResultDetail)
- Enforce result visibility (show results only after deadline for students)
- Show FeedbackForm after deadline

### FC-05: AdminPanel
**Purpose**: Admin-only menu management interface.
**Responsibilities**:
- List all menus in a sortable table
- Open MenuFormModal for create/edit
- Trigger delete with confirmation
- Trigger lock voting
- Trigger CSV export with date range picker
- Trigger weekly menu copy

### FC-06: Navbar
**Purpose**: Top navigation bar.
**Responsibilities**:
- Show role-appropriate navigation links
- Display current user name and role
- Provide logout button
- Collapse to hamburger menu on mobile

### FC-07: VoteModal
**Purpose**: Modal dialog for casting or changing a vote.
**Responsibilities**:
- Display dish options as selectable VoteButtons
- Pre-select user's existing vote if changing
- Submit vote to API; show loading state

### FC-08: MenuFormModal
**Purpose**: Admin modal for creating or editing a menu.
**Responsibilities**:
- Form fields: date, meal type, open time, deadline, dish options (dynamic list)
- Validate minimum 2 options, maximum 10
- Submit create or update API call

### FC-09: FeedbackForm
**Purpose**: Post-meal feedback submission form.
**Responsibilities**:
- Star rating selector (1–5)
- Optional text comment textarea
- Submit feedback to API; show success/error toast

### FC-10: Shared UI Components
**Purpose**: Reusable presentational components.
**Responsibilities**:
- `StatCard`: Summary statistic display card
- `ChartCard`: Wrapper card for Recharts charts
- `MenuCard`: Menu display card with voting status
- `VoteButton`: Selectable dish option button
- `Loader` / `Spinner` / `CardLoader`: Loading state indicators
