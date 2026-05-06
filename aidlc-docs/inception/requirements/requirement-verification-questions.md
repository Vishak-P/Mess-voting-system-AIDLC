# Requirements Verification Questions
## Mess / Canteen Menu Voting System

**Instructions**: Please answer each question by filling in the `[Answer]:` tag with the letter of your choice (A, B, C, D, or X for custom). For X answers, describe your response after the tag.

---

## Section 1: Functional Requirements

### Q1: User Registration & Role Assignment
How should admin accounts be created?

A) Only via direct database insertion (no self-registration for admins)
B) First registered user automatically becomes admin
C) A special admin registration code/invite link is required
D) Admin can promote any student to admin from the admin panel
X) Other (please describe after [Answer]: tag below)

[Answer]: 

---

### Q2: Voting Window
When exactly can students vote for a meal?

A) Any time before the deadline set by admin (no time restriction)
B) Only on the same day as the meal (e.g., breakfast voting only on that morning)
C) Up to 24 hours before the meal
D) Admin sets both open and close times per menu
X) Other (please describe after [Answer]: tag below)

[Answer]: 

---

### Q3: Vote Change Policy
Can a student change their vote after submitting?

A) No — votes are final once submitted
B) Yes — students can change their vote any time before the deadline
C) Yes — but only within 15 minutes of casting the original vote
X) Other (please describe after [Answer]: tag below)

[Answer]: 

---

### Q4: Results Visibility
When can students see voting results?

A) Immediately after voting (real-time results visible to all)
B) Only after the voting deadline has passed
C) Only after the student has voted (see results after your own vote)
D) Results are only visible to admins; students never see them
X) Other (please describe after [Answer]: tag below)

[Answer]: 

---

### Q5: Weekly Menu Reset
How should the weekly menu reset work?

A) Admin manually creates each week's menu (no auto-reset)
B) System auto-copies last week's menu as a template for the new week
C) System auto-generates a new week's menu from a predefined dish pool
D) Admin sets a recurring template that auto-publishes each week
X) Other (please describe after [Answer]: tag below)

[Answer]: 

---

### Q6: Meal Feedback
Should students be able to leave feedback/ratings after a meal?

A) Yes — free-text feedback after voting deadline passes
B) Yes — star rating (1–5) only
C) Yes — both star rating and optional text comment
D) No — voting only, no post-meal feedback needed
X) Other (please describe after [Answer]: tag below)

[Answer]: 

---

### Q7: Notification System
What level of notification support is required?

A) None — no notifications needed
B) In-app toast/banner notifications only (no email/SMS)
C) Email notifications (voting open, deadline reminder)
D) SMS via Twilio (mock/placeholder acceptable for now)
E) Both email and SMS
X) Other (please describe after [Answer]: tag below)

[Answer]: 

---

## Section 2: Non-Functional Requirements

### Q8: Expected User Scale
How many concurrent users should the system support?

A) Small — up to 100 students (single hostel/canteen)
B) Medium — 100–500 students (college campus)
C) Large — 500–2000 students (university)
D) Enterprise — 2000+ students (multi-campus)
X) Other (please describe after [Answer]: tag below)

[Answer]: 

---

### Q9: Deployment Target
Where will this application be deployed?

A) Local development only (no production deployment needed)
B) Single server / VPS (e.g., AWS EC2, DigitalOcean Droplet)
C) Containerized (Docker + Docker Compose)
D) Cloud-managed services (AWS RDS, Elastic Beanstalk, etc.)
E) Kubernetes / container orchestration
X) Other (please describe after [Answer]: tag below)

[Answer]: 

---

### Q10: Authentication Token Expiry
How long should JWT access tokens remain valid?

A) 1 hour (high security, frequent re-login)
B) 8 hours (standard workday session)
C) 24 hours (daily login)
D) 7 days (weekly, remember-me style)
X) Other (please describe after [Answer]: tag below)

[Answer]: 

---

### Q11: Data Retention
How long should voting history and results be retained?

A) Indefinitely (never delete old data)
B) 1 academic year (then archive/delete)
C) 1 semester
D) Admin can manually purge old data
X) Other (please describe after [Answer]: tag below)

[Answer]: 

---

## Section 3: Technical Context

### Q12: MySQL Version & Hosting
What MySQL setup will be used?

A) MySQL 8.0 on local machine (development only)
B) MySQL 8.0 on a dedicated server
C) AWS RDS MySQL
D) PlanetScale or other managed MySQL
X) Other (please describe after [Answer]: tag below)

[Answer]: 

---

### Q13: Frontend Hosting
Where will the React frontend be served from?

A) Same server as Flask backend (Flask serves static build)
B) Separate static hosting (Netlify, Vercel, S3+CloudFront)
C) Nginx reverse proxy in front of both
D) Development only — no production hosting needed yet
X) Other (please describe after [Answer]: tag below)

[Answer]: 

---

### Q14: CSV Export Scope
What should the CSV export include?

A) All voting results (all menus, all options, vote counts)
B) Results for a specific date range (admin selects range)
C) Results for a specific week
D) Per-menu export (one CSV per menu)
X) Other (please describe after [Answer]: tag below)

[Answer]: 

---

## Section 4: Extensions

### Q15: Security Extension
Should security extension rules be enforced for this project?

A) Yes — enforce all SECURITY rules as blocking constraints (recommended for production-grade applications)
B) No — skip all SECURITY rules (suitable for PoCs, prototypes, and experimental projects)
X) Other (please describe after [Answer]: tag below)

[Answer]: 

---

### Q16: Property-Based Testing Extension
Should property-based testing (PBT) rules be enforced for this project?

A) Yes — enforce all PBT rules as blocking constraints
B) Partial — enforce PBT rules only for pure functions and serialization round-trips
C) No — skip all PBT rules (suitable for simple CRUD applications)
X) Other (please describe after [Answer]: tag below)

[Answer]: 

---

*Please fill in all [Answer]: tags above, then reply to proceed to Requirements Document generation.*
