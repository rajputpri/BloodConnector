# 🏗 Architecture — BloodConnect

System design, data model, real-time architecture, and technical decisions.

---

## 📖 Table of Contents

- [Design Goals](#-design-goals)
- [Layers](#-layers)
- [Data Model](#-data-model)
- [Request Lifecycle](#-request-lifecycle)
- [Real-Time Architecture](#-real-time-architecture)
- [Caching Strategy](#-caching-strategy)
- [Performance Optimizations](#-performance-optimizations)
- [Security Layers](#-security-layers)
- [Key Architectural Decisions](#-key-architectural-decisions)

---

## 🎯 Design Goals

1. **Separation of concerns** — Clean MVC boundaries
2. **Security-first** — Auth, authorization, CSRF on every form
3. **Medical accuracy** — Blood compatibility centralized
4. **Auditability** — Every state transition tracked
5. **Performance** — Indexes, caching, pagination
6. **Real-time first** — SignalR push, no polling
7. **Zero DB overhead for non-critical paths** — Cached badges, smart invalidation

---

## 🏛 Layers

### Presentation Layer

- **Razor Views** — Server-rendered HTML
- **Partial Views** — Reusable components (`_Form.cshtml`)
- **Layouts** — `_Layout.cshtml` (navbar, footer, modals, SignalR client)
- **Tag Helpers** — `asp-for`, `asp-action`, `asp-controller`
- **Client-Side JS** — `site.js`, `animations.js`, `notifications.js`
- **Styling** — Custom CSS design system + Bootstrap 5

### Application Layer

- **Controllers** — HTTP orchestration, model binding, authorization
- **Services** — Cross-cutting concerns:
  - `MessageCache` — Cached unread count
  - `NotificationService` — SignalR push + cache orchestration
- **ViewModels** — UI-specific DTOs
- **API DTOs** — REST-specific shapes

### Real-Time Layer

- **SignalR Hub** — `NotificationHub` (WebSocket server)
- **Groups** — `admins`, `user_{userId}`
- **Push Methods** — `PushNewRequestToAdminsAsync`, `PushNewOfferToOwnerAsync`, etc.
- **Client Handler** — `notifications.js` (browser WebSocket)

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

### Relationships

| From | To | Type | On Delete |
|------|-----|------|-----------|
| AppUser → Donor | 1:1 | SetNull |
| AppUser → BloodRequest | 1:N | SetNull |
| BloodRequest → DonationOffer | 1:N | Cascade |
| Donor → DonationOffer | 1:N | Cascade |
| Donor → BloodRequest (FulfilledByDonor) | 1:N | SetNull |

### Indexes

| Table | Columns | Type |
|-------|---------|------|
| Donors | BloodGroup | Regular |
| Donors | State | Regular |
| Donors | Location | Regular |
| Donors | (BloodGroup, IsAvailable) | Compound |
| Donors | UserId | Regular |
| BloodRequests | UserId | Regular |
| BloodRequests | BloodGroupNeeded | Regular |
| BloodRequests | Status | Regular |
| BloodRequests | RequestDate | Regular |
| BloodRequests | (Status, BloodGroupNeeded) | Compound |
| DonationOffers | (RequestId, DonorId) | **Unique** |
| DonationOffers | Status | Regular |
| DonationOffers | DonorId | Regular |
| ContactMessages | IsRead | Regular |
| ContactMessages | CreatedAt | Regular |

---

## 🔄 Request Lifecycle

```text
1. HTTP Request
   ↓
2. Middleware Pipeline
   ├─ Swagger (dev + prod)
   ├─ StatusCodePages (API → JSON, MVC → HTML)
   ├─ HTTPS redirect (dev only)
   ├─ Routing
   ├─ Authentication (cookie check + ban check via OnValidatePrincipal)
   ├─ Authorization (role + ownership)
   ↓
3. Controller Action
   ├─ Model binding
   ├─ Validation
   ├─ Business logic
   ├─ EF Core query
   ├─ Cache invalidation (if write)
   ├─ SignalR push (if write)
   ↓
4. Response
   ├─ View rendering (MVC)
   └─ JSON serialization (API)
```

---

## ⚡ Real-Time Architecture

### SignalR Hub

**Endpoint:** `/hubs/notifications`  
**Authorization:** `[Authorize]` — login required

**Groups:**

| Group | Members | Receives |
|-------|---------|----------|
| `admins` | All Admin + SuperAdmin users | New requests, New messages |
| `user_{userId}` | Individual user | Offer pledge, Offer status change |

**Hub Lifecycle:**

```csharp
OnConnectedAsync:
  1. Add connection to user_{userId} group
  2. If admin → Add connection to "admins" group

OnDisconnectedAsync:
  1. Remove from user_{userId} group
```

### Push Flow

```text
┌────────────────────────────────────────────────────────────┐
│                     WRITE OPERATION                        │
│  (e.g., new blood request posted)                          │
└────────────────────┬───────────────────────────────────────┘
                     │
                     ▼
┌────────────────────────────────────────────────────────────┐
│  Controller Action                                         │
│  1. Save to DB (EF Core)                                   │
│  2. Call NotificationService.PushXAsync()                  │
│  3. Invalidate cache (InMemoryCache.Remove)                │
└────────────────────┬───────────────────────────────────────┘
                     │
                     ▼
┌────────────────────────────────────────────────────────────┐
│  SignalR Hub                                               │
│  IHubContext<NotificationHub>.Clients                      │
│    .Group("admins")                                        │
│    .SendAsync("ReceiveNotification", payload)              │
└────────────────────┬───────────────────────────────────────┘
                     │
                     │ WebSocket push
                     ▼
┌────────────────────────────────────────────────────────────┐
│  Client (notifications.js)                                 │
│  1. Increment bell badge + bounce animation                │
│  2. Ring bell icon (0.6s rotate)                           │
│  3. Prepend notification item to dropdown                  │
│  4. Play WhatsApp-style chime (Web Audio API)              │
│  5. Show toast (slide-in, 7s auto-dismiss)                 │
└────────────────────────────────────────────────────────────┘
```

### Notification Types

| Type | Icon | Trigger | Target Group |
|------|------|---------|--------------|
| `request` | 🩸 | New blood request posted | `admins` |
| `message` | ✉ | New contact message | `admins` |
| `offer` | 🤝 | Donor pledges on request | `user_{ownerId}` |
| `offer-status` | ✓ | Offer accepted/rejected/completed | `user_{donorId}` |

### Payload Structure

```json
{
  "type": "request",
  "title": "New A+ request",
  "message": "Rahul Sharma · Mumbai, Maharashtra",
  "url": "/BloodRequest/Index",
  "timestamp": "2026-10-12T14:23:45.123Z"
}
```

### Client-Side Resilience

- **Auto-reconnect:** `[0, 2000, 5000, 10000, 30000]` ms exponential backoff
- **Retry on fail:** `setTimeout(start, 5000)` if initial connect fails
- **Reconnect handler:** Logs reconnection, continues listening
- **Disconnect handler:** Auto-retry after 5 seconds

---

## 🗃 Caching Strategy

BloodConnect uses a **hybrid caching approach**:

### Layer 1: IMemoryCache (Read Cache)

| Key | Value | Expiry | Invalidated By |
|-----|-------|--------|----------------|
| `BC_AdminNotifications` | AdminNotification | 60s | Any new request/message |
| `BC_UserNotif_{userId}` | UserNotification | 60s | Any offer/status change |
| `BloodConnect_ContactMessages_UnreadCount` | int | 60s | Any message read/delete |

### Layer 2: SignalR (Push)

**On every write:**
1. Invalidate cache key (`_cache.Remove`)
2. Push SignalR notification to relevant group

### Why This Works

| Scenario | Behavior |
|----------|----------|
| **First page load** | Cache miss → DB query → Cache set (60s) |
| **Subsequent loads within 60s** | Cache hit → No DB query |
| **Write operation** | Cache invalidated + SignalR push |
| **Non-admin users** | Zero extra DB queries (bell not shown for them) |
| **Admin with unread count** | Max 1 query per 60 seconds |

### Cache Invalidation Points

```csharp
// AdminController
ToggleRead()      → _notifications.InvalidateAdmin() + _messageCache.Invalidate()
DeleteMessage()   → _notifications.InvalidateAdmin() + _messageCache.Invalidate()

// BloodRequestController
Create()          → PushNewRequestToAdminsAsync() + InvalidateAdmin
Offer()           → PushNewOfferToOwnerAsync() + InvalidateUser(ownerId)
AcceptOffer()     → PushOfferStatusToDonorAsync() + InvalidateUser(ownerId)
RejectOffer()     → PushOfferStatusToDonorAsync()
CompleteDonation()→ PushOfferStatusToDonorAsync()

// HomeController
Contact()         → PushNewMessageToAdminsAsync() + InvalidateAdmin + _messageCache.Invalidate()
```

---

## ⚡ Performance Optimizations

| Technique | Where | Impact |
|-----------|-------|--------|
| `AsNoTracking()` | All read-only queries | 30-40% faster reads |
| Database indexes | Blood group, state, status | Faster filters |
| Compound indexes | `(BloodGroup, IsAvailable)` | Search optimization |
| Unique compound index | `(RequestId, DonorId)` | Prevents duplicates |
| `IMemoryCache` | Unread counts, notifications | Reduces DB hits by 95%+ |
| SignalR push | Real-time updates | Zero polling overhead |
| Pagination | All list APIs | Prevents massive payloads |
| DTO projection | API responses | Smaller payloads |
| `EnableRetryOnFailure` | SQL connection | Handles transient errors |
| Cache invalidation on write | Every mutation | Real-time consistency |

---

## 🔐 Security Layers

```text
Layer 1: Network
  ├─ HTTPS (production)
  └─ HSTS (disabled for free tier)

Layer 2: Application
  ├─ CSRF tokens (global)
  ├─ Cookie auth (HttpOnly, SameSite)
  ├── Custom ban middleware (OnValidatePrincipal)
  └─ API-specific 401/403 (no redirect)

Layer 3: Authorization
  ├─ Role-based [Authorize]
  ├─ Ownership checks in controllers
  └─ SignalR Hub [Authorize]

Layer 4: Real-Time
  ├─ SignalR groups (users can only access own group)
  ├─ Authentication required for hub connection
  └─ Payload validation on client (XSS prevention)

Layer 5: Data
  ├─ EF Core parameterized queries
  ├─ DTO pattern
  └─ Validation attributes
```

---

## 🎓 Key Architectural Decisions

### 1. MVC over Razor Pages

**Why:** Familiar for BCA syllabus, better for complex workflows with multiple entities.

### 2. Cookie Auth over JWT

**Why:** Server-rendered app with forms — cookies simpler, secure by default, HttpOnly protection.

### 3. DTO Pattern for API

**Why:** Prevents entity leakage, controls what's exposed publicly, contact number privacy.

### 4. Blood Compatibility in Code

**Why:** Single source of truth, reusable across web + API, medical accuracy.

### 5. Pledge Workflow (not direct contact)

**Why:** Prevents fake fulfillments, gives owners control, tracks state transitions.

### 6. Soft Ban over Delete

**Why:** Preserves audit trail, allows unban, prevents data loss.

### 7. Hybrid Cache + Push (SignalR)

**Why:** 
- **Cache:** Reduces DB load for reads
- **Push:** Real-time without polling
- **Invalidation:** Consistency guaranteed
- **Result:** Best of both worlds — fast + real-time

### 8. SignalR Groups over Per-Connection Tracking

**Why:** 
- Admins get broadcast in O(1) with single `SendAsync`
- Users get targeted push with `Group($"user_{id}")`
- No need to track individual connection IDs

### 9. Dedicated Auth API (`/api/auth/*`)

**Why:** 
- Postman/curl can't use MVC antiforgery-protected forms
- API clients need JSON-based login
- Cookie still works for both MVC and API

### 10. Sound via Web Audio API (not `<audio>` tag)

**Why:** 
- No HTTP request for a sound file
- Harmonic layering possible (triangle wave +5 cent detune)
- Compressor for consistent loudness
- Works offline

---

## 📐 Scaling Considerations

**Current free-tier limits:**
- 5 GB disk space (MonsterASP)
- 1 GB SQL database
- Single app instance
- No Redis / distributed cache

**Path to scale:**
1. Replace `IMemoryCache` with Redis (distributed cache)
2. Use Azure SignalR Service (scale SignalR independently)
3. Add read replicas for SQL Server
4. Introduce message queue (RabbitMQ / Azure Service Bus) for SignalR push
5. CDN for static assets
6. Split read/write APIs (CQRS pattern)

---

**Last Updated:** October 2026