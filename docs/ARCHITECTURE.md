# 🏗 Architecture — BloodConnect

System design, data model, and architectural decisions.

---

## 🎯 Design Goals

1. **Separation of concerns** — Clean MVC boundaries
2. **Security-first** — Auth, authorization, CSRF on every form
3. **Medical accuracy** — Blood compatibility centralized
4. **Auditability** — Every state transition tracked
5. **Performance** — Indexes, caching, pagination

---

## 🏛 Layers

### Presentation Layer

- **Razor Views** — Server-rendered HTML
- **Partial Views** — Reusable components (`_Form.cshtml`)
- **Layouts** — `_Layout.cshtml` (navbar, footer, modals)
- **Tag Helpers** — `asp-for`, `asp-action`, `asp-controller`

### Application Layer

- **Controllers** — HTTP orchestration, model binding, authorization
- **Services** — Cross-cutting concerns (`MessageCache`)
- **ViewModels** — UI-specific DTOs
- **API DTOs** — REST-specific shapes

### Domain Layer

- **Entities** — `Donor`, `BloodRequest`, `DonationOffer`, `AppUser`, `ContactMessage`
- **Value Objects** — `BloodCompatibility`, `DomainValues`
- **Validation** — DataAnnotations + custom attributes

### Data Layer

- **DbContext** — `ApplicationDbContext`
- **Migrations** — 8 versioned migrations
- **Repositories** — None (EF Core DbSet used directly)
- **Seeding** — `DbSeeder.SeedAsync()`

---

## 🗄 Data Model

```text
┌────────────────────┐
│     AppUser        │  (extends IdentityUser)
│  ─────────────     │
│  Id (PK)           │
│  Email             │
│  FullName          │
│  IsBanned          │
│  CreatedAt         │
└──────────┬─────────┘
           │
           │ 1:1 (optional)
           ▼
┌────────────────────┐       ┌────────────────────┐
│      Donor         │       │   BloodRequest     │
│  ─────────────     │       │  ─────────────     │
│  DonorId (PK)      │       │  RequestId (PK)    │
│  UserId (FK)       │       │  UserId (FK)       │
│  Name              │       │  RequesterName     │
│  Age               │       │  BloodGroupNeeded  │
│  BloodGroup        │       │  State/City        │
│  State/City        │       │  UrgencyLevel      │
│  Location          │       │  Status            │
│  ContactNumber     │       │  FulfilledByDonorId│
│  IsAvailable       │       └──────────┬─────────┘
│  RowVersion        │                  │
└──────────┬─────────┘                  │
           │                            │
           │ N                          │ N
           │                            │
           ▼                            ▼
        ┌─────────────────────────────────┐
        │       DonationOffer             │
        │  ─────────────────────          │
        │  Id (PK)                        │
        │  RequestId (FK)                 │
        │  DonorId (FK)                   │
        │  Status (Pledged/Accepted/...)  │
        │  CreatedAt, RespondedAt,        │
        │  CompletedAt                    │
        │                                 │
        │  UNIQUE(RequestId, DonorId)     │
        └─────────────────────────────────┘

┌────────────────────┐
│  ContactMessage    │
│  ─────────────     │
│  Id (PK)           │
│  Name, Email       │
│  Subject, Message  │
│  IsRead, CreatedAt │
└────────────────────┘
```

---

## 🔄 Request Lifecycle

```text
1. HTTP Request
   ↓
2. Middleware Pipeline
   - HTTPS redirect (prod)
   - Static files
   - Routing
   - Authentication (cookie check + ban check)
   - Authorization (role/ownership)
   ↓
3. Controller Action
   - Model binding
   - Validation
   - Business logic
   - EF Core query
   ↓
4. Response
   - View rendering (MVC)
   - JSON serialization (API)
```

---

## ⚡ Performance Optimizations

| Technique | Where | Impact |
|-----------|-------|--------|
| `AsNoTracking()` | All read-only queries | 30-40% faster reads |
| Database indexes | Blood group, state, status | Faster filters |
| Compound indexes | `(BloodGroup, IsAvailable)` | Search optimization |
| Unique compound index | `(RequestId, DonorId)` | Prevents duplicates |
| `IMemoryCache` | Unread message count | Reduces DB hits |
| Pagination | All list APIs | Prevents massive payloads |
| DTO projection | API responses | Smaller payloads |
| `EnableRetryOnFailure` | SQL connection | Handles transient errors |

---

## 🔐 Security Layers

```text
Layer 1: Network
  ├─ HTTPS (production)
  └─ HSTS (disabled for free tier)

Layer 2: Application
  ├─ CSRF tokens (global)
  ├─ Cookie auth (HttpOnly, SameSite)
  └─ Custom ban middleware

Layer 3: Authorization
  ├─ Role-based [Authorize]
  └─ Ownership checks in controllers

Layer 4: Data
  ├─ EF Core parameterized queries
  ├─ DTO pattern
  └─ Validation attributes
```

---

## 🎓 Key Architectural Decisions

### 1. MVC over Razor Pages

**Why:** Familiar for BCA syllabus, better for complex workflows with multiple entities.

### 2. Cookie Auth over JWT

**Why:** Server-rendered app with forms — cookies simpler, secure by default.

### 3. DTO Pattern for API

**Why:** Prevents entity leakage, controls what's exposed publicly.

### 4. Blood Compatibility in Code

**Why:** Single source of truth, reusable across web + API, medical accuracy.

### 5. Pledge Workflow (not direct contact)

**Why:** Prevents fake fulfillments, gives owners control, tracks state transitions.

### 6. Soft Ban over Delete

**Why:** Preserves audit trail, allows unban, prevents data loss.

---

**Last Updated:** October 2026