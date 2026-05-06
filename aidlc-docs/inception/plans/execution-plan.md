# Execution Plan
## Mess / Canteen Menu Voting System

---

## Detailed Analysis Summary

### Change Impact Assessment
| Area | Impact | Description |
|---|---|---|
| User-facing changes | Yes | Full student and admin UI with voting, results, feedback, dashboard |
| Structural changes | Yes | New full-stack system — Flask API + React SPA + MySQL |
| Data model changes | Yes | New schema: users, menus, menu_options, votes, feedback |
| API changes | Yes | New REST API with 15+ endpoints |
| NFR impact | Yes | Security (JWT, bcrypt, CORS, rate limiting), performance (connection pooling), scalability (500 users) |

### Risk Assessment
| Factor | Level |
|---|---|
| **Risk Level** | Medium |
| **Rollback Complexity** | Easy (greenfield — nothing to roll back to) |
| **Testing Complexity** | Moderate (voting uniqueness constraints, role-based access, deadline logic) |

---

## Workflow Visualization

```mermaid
flowchart TD
    Start(["User Request"])

    subgraph INCEPTION["🔵 INCEPTION PHASE"]
        WD["Workspace Detection\nCOMPLETED"]
        RA["Requirements Analysis\nCOMPLETED"]
        US["User Stories\nCOMPLETED"]
        WP["Workflow Planning\nIN PROGRESS"]
        AD["Application Design\nEXECUTE"]
        UG["Units Generation\nEXECUTE"]
        RE["Reverse Engineering\nSKIP - Greenfield"]
    end

    subgraph CONSTRUCTION["🟢 CONSTRUCTION PHASE"]
        FD1["Functional Design\nUnit 1: Backend\nEXECUTE"]
        NFR1["NFR Requirements\nUnit 1: Backend\nEXECUTE"]
        NFRD1["NFR Design\nUnit 1: Backend\nEXECUTE"]
        CG1["Code Generation\nUnit 1: Backend\nEXECUTE"]
        CG2["Code Generation\nUnit 2: Frontend\nEXECUTE"]
        CG3["Code Generation\nUnit 3: Database\nEXECUTE"]
        BT["Build and Test\nEXECUTE"]
    end

    subgraph OPERATIONS["🟡 OPERATIONS PHASE"]
        OPS["Operations\nPLACEHOLDER"]
    end

    Start --> WD
    WD --> RA
    RA --> US
    US --> WP
    WP --> AD
    AD --> UG
    UG --> FD1
    FD1 --> NFR1
    NFR1 --> NFRD1
    NFRD1 --> CG1
    CG1 --> CG2
    CG2 --> CG3
    CG3 --> BT
    BT -.-> OPS
    BT --> End(["Complete"])

    style WD fill:#4CAF50,stroke:#1B5E20,stroke-width:3px,color:#fff
    style RA fill:#4CAF50,stroke:#1B5E20,stroke-width:3px,color:#fff
    style US fill:#4CAF50,stroke:#1B5E20,stroke-width:3px,color:#fff
    style WP fill:#4CAF50,stroke:#1B5E20,stroke-width:3px,color:#fff
    style AD fill:#FFA726,stroke:#E65100,stroke-width:3px,stroke-dasharray:5 5,color:#000
    style UG fill:#FFA726,stroke:#E65100,stroke-width:3px,stroke-dasharray:5 5,color:#000
    style RE fill:#BDBDBD,stroke:#424242,stroke-width:2px,stroke-dasharray:5 5,color:#000
    style FD1 fill:#FFA726,stroke:#E65100,stroke-width:3px,stroke-dasharray:5 5,color:#000
    style NFR1 fill:#FFA726,stroke:#E65100,stroke-width:3px,stroke-dasharray:5 5,color:#000
    style NFRD1 fill:#FFA726,stroke:#E65100,stroke-width:3px,stroke-dasharray:5 5,color:#000
    style CG1 fill:#4CAF50,stroke:#1B5E20,stroke-width:3px,color:#fff
    style CG2 fill:#4CAF50,stroke:#1B5E20,stroke-width:3px,color:#fff
    style CG3 fill:#4CAF50,stroke:#1B5E20,stroke-width:3px,color:#fff
    style BT fill:#4CAF50,stroke:#1B5E20,stroke-width:3px,color:#fff
    style OPS fill:#BDBDBD,stroke:#424242,stroke-width:2px,stroke-dasharray:5 5,color:#000
    style Start fill:#CE93D8,stroke:#6A1B9A,stroke-width:3px,color:#000
    style End fill:#CE93D8,stroke:#6A1B9A,stroke-width:3px,color:#000
    style INCEPTION fill:#BBDEFB,stroke:#1565C0,stroke-width:3px,color:#000
    style CONSTRUCTION fill:#C8E6C9,stroke:#2E7D32,stroke-width:3px,color:#000
    style OPERATIONS fill:#FFF59D,stroke:#F57F17,stroke-width:3px,color:#000
    linkStyle default stroke:#333,stroke-width:2px
```

---

## Phases to Execute

### 🔵 INCEPTION PHASE
- [x] Workspace Detection — COMPLETED
- [x] Reverse Engineering — SKIPPED (Greenfield project)
- [x] Requirements Analysis — COMPLETED
- [x] User Stories — COMPLETED (19 stories, 2 personas)
- [x] Workflow Planning — IN PROGRESS
- [ ] Application Design — **EXECUTE**
  - **Rationale**: New system with multiple components (API, SPA, DB). Component boundaries, service layer, and method signatures need definition before code generation.
- [ ] Units Generation — **EXECUTE**
  - **Rationale**: System decomposes into 3 distinct units (Backend, Frontend, Database) with different tech stacks and independent development paths.

### 🟢 CONSTRUCTION PHASE — Per-Unit Loop

#### Unit 1: Backend (Flask API)
- [ ] Functional Design — **EXECUTE**
  - **Rationale**: New data models (feedback table), complex business logic (vote change, deadline enforcement, weekly copy), and API contracts need detailed design.
- [ ] NFR Requirements — **EXECUTE**
  - **Rationale**: Security extension enabled; performance, rate limiting, logging, and CORS requirements need explicit NFR specification.
- [ ] NFR Design — **EXECUTE**
  - **Rationale**: NFR patterns (bcrypt, JWT, rate limiting, structured logging, security headers) need to be incorporated into the design.
- [ ] Infrastructure Design — SKIP
  - **Rationale**: Deployment target is a single VPS (not cloud-managed). No IaC or cloud resource mapping needed at this stage.
- [ ] Code Generation — **EXECUTE** (ALWAYS)

#### Unit 2: Frontend (React + Tailwind)
- [ ] Functional Design — SKIP
  - **Rationale**: Frontend is a consumer of the backend API. Component structure is straightforward; no complex business logic in the UI layer.
- [ ] NFR Requirements — SKIP
  - **Rationale**: Frontend NFRs (security headers, responsive design) are covered by the backend NFR design and Tailwind CSS.
- [ ] NFR Design — SKIP
  - **Rationale**: Same rationale as NFR Requirements for frontend.
- [ ] Infrastructure Design — SKIP
  - **Rationale**: Static hosting (Netlify/Vercel) — no IaC needed.
- [ ] Code Generation — **EXECUTE** (ALWAYS)

#### Unit 3: Database (MySQL Schema + Seed)
- [ ] Functional Design — SKIP
  - **Rationale**: Schema is fully defined in the Backend Functional Design.
- [ ] NFR Requirements — SKIP
  - **Rationale**: DB NFRs covered in Backend NFR design.
- [ ] NFR Design — SKIP
  - **Rationale**: Same as above.
- [ ] Infrastructure Design — SKIP
  - **Rationale**: Local MySQL for development; no cloud IaC needed.
- [ ] Code Generation — **EXECUTE** (ALWAYS)

### After All Units:
- [ ] Build and Test — **EXECUTE** (ALWAYS)

### 🟡 OPERATIONS PHASE
- [ ] Operations — PLACEHOLDER

---

## Success Criteria
- **Primary Goal**: Fully functional voting system with student and admin roles
- **Key Deliverables**: Flask API, React SPA, MySQL schema, seed data, build instructions
- **Quality Gates**:
  - All 15 SECURITY rules compliant or documented N/A
  - All 19 user stories have corresponding implementation
  - Unique vote constraint enforced at DB level
  - JWT auth working for all protected routes
  - Admin dashboard charts rendering with real data
