# 📅 Changelog

All notable changes to BloodConnect.

Format: [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)  
Versioning: [Semantic Versioning](https://semver.org/)

---

## 📖 Table of Contents

- [Phase 4.5 — Real-Time Notifications](#phase-45--real-time-notifications-october-2026)
- [Phase 4 — API, Deployment](#phase-4--api-deployment-october-2026)
- [Phase 3 — Database & CRUD](#phase-3--database--crud-september-2026)
- [Phase 2 — Forms & Validation](#phase-2--forms--validation-august-2026)
- [Phase 1 — Foundation](#phase-1--foundation-july-2026)

---

## [Phase 4.5] — Real-Time Notifications (October 2026)

**🎯 Focus:** Real-time SignalR notifications with bell icon, toast, and sound.

### Added

#### Real-Time Infrastructure
- **SignalR Hub** (`Hubs/NotificationHub.cs`) — WebSocket server with `[Authorize]`
- **Group-based messaging** — `admins` group for admin alerts, `user_{id}` group for personal
- **Auto-reconnection** — exponential backoff `[0, 2000, 5000, 10000, 30000]` ms
- **NotificationService** — Hybrid cache + SignalR push orchestration
- **Push methods:**
  - `PushNewRequestToAdminsAsync()` — when blood request posted
  - `PushNewMessageToAdminsAsync()` — when contact form submitted
  - `PushNewOfferToOwnerAsync()` — when donor pledges
  - `PushOfferStatusToDonorAsync()` — when offer accepted/rejected/completed

#### Auth API
- **`POST /api/auth/login`** — JSON-based login (returns cookie)
- **`POST /api/auth/logout`** — Logout current session
- **`GET /api/auth/me`** — Current user info + roles
- **`AuthApiController.cs`** — Dedicated controller for API auth

#### UI Components
- **Bell icon** with animated red badge
- **Notification dropdown** — recent 8 items with type-based icons
- **Toast notifications** — slide-in from top-right, auto-dismiss 7s
- **WhatsApp-style sound chime** — Web Audio API (880Hz + 1174Hz)
- **Bell ring animation** — 0.6s shake on new notification
- **Badge bounce animation** — scale pulse on count update
- **Notification item highlight** — fades after 3s

#### Client-Side
- **`wwwroot/js/notifications.js`** — SignalR client + sound + toast
- **`wwwroot/css/notifications.css`** — Toast styling
- **Sound toggle** — persisted in `localStorage`
- **XSS-safe rendering** — `textContent` for all payload text

#### Documentation
- **README** — Real-time architecture section
- **API.md** — 3 new auth endpoints + auth flow diagram
- **ARCHITECTURE.md** — SignalR architecture + caching strategy
- **SECURITY.md** — Real-time security section
- **DEPLOYMENT.md** — SignalR deployment notes
- **USER_MANUAL.md** — Real-time notification guide
- **CHANGELOG.md** — This file

### Changed

- **Program.cs** — Added SignalR service registration + hub mapping
- **BloodRequestController** — Injects NotificationService, pushes on write
- **HomeController** — Pushes on contact form submission
- **AdminController** — Invalidates notification cache on message read/delete
- **LoginPartial** — Now includes bell icon + notification dropdown
- **_Layout.cshtml** — Added SignalR client + notifications.js + notifications.css
- **StatusCodePages** — Custom middleware for API vs MVC error handling

### Fixed

- **400 → 401 for API** — `UseStatusCodePagesWithReExecute` was converting 401 to 400
- **Cache staleness** — Explicit invalidation on every write operation
- **Emoji encoding** — UTF-8 encoding for all markdown files

### Performance

- **Zero polling** — SignalR push replaces periodic AJAX
- **Cache-first reads** — 60s TTL on admin/user notification data
- **Group-based broadcast** — O(1) delivery to admins
- **Reduced DB queries** — 95% reduction for notification badge

### Security

- **SignalR `[Authorize]`** — unauthenticated users cannot connect
- **Group isolation** — users only receive their own notifications
- **Payload sanitization** — no sensitive data in push payloads
- **XSS prevention** — client uses `textContent` for rendering

---

## [Phase 4] — API, Deployment (October 2026)

**🎯 Focus:** REST API, Swagger, live deployment.

### Added

- REST API with full CRUD (Donor, BloodRequest)
- Swagger UI documentation with OpenAPI 3.0
- State dropdown (28 states + 8 UTs) for data consistency
- POST/PUT/DELETE API endpoints with auth
- Contact message caching (`IMemoryCache`)
- Live deployment on MonsterASP.NET
- HTTPS via Let's Encrypt
- Comprehensive documentation (README, API, DEPLOYMENT, SECURITY, USER_MANUAL)
- Postman collection for API testing
- Organized screenshot gallery (30 screenshots)

### Changed

- Swagger always enabled (was dev-only)
- HTTPS redirect scoped to dev
- State column added to Donor + BloodRequest
- DTO pattern for API responses (contact privacy)

### Fixed

- EF Core pending model changes warning
- State column nullable for legacy data
- Duplicate migration cleanup

---

## [Phase 3] — Database & CRUD (September 2026)

**🎯 Focus:** Database, contact messages, role management.

### Added

- Contact message feature (admin inbox)
- Cached unread badge counter (`MessageCache`)
- SuperAdmin protection rules
- Role management UI (promote/demote)
- Admin dashboard with stats
- Ban system with cookie validation

### Changed

- Cookie authentication refinements
- Admin dashboard improvements
- Role hierarchy enforcement

### Fixed

- Migration conflicts (AddBloodRequestOwner duplicate)
- Windows filename conflict (`Users.cshtml` → `UserList.cshtml`)

---

## [Phase 2] — Forms & Validation (August 2026)

**🎯 Focus:** Forms, validation, search.

### Added

- Donor CRUD with validation
- Blood request management
- Compatibility-aware search (`BloodCompatibility` helper)
- Custom `MustBeTrue` validation attribute
- Age validation (18-65)
- Blood group regex validation
- Contact number regex validation

### Changed

- Domain values centralized (`DomainValues.cs`)
- Form validation improvements
- Search ordering (exact match first)

---

## [Phase 1] — Foundation (July 2026)

**🎯 Focus:** Project scaffold, auth, UI.

### Added

- ASP.NET Core MVC project scaffold (.NET 10)
- Identity authentication (Register, Login, Logout)
- Role-based authorization (SuperAdmin, Admin, User)
- Bootstrap 5 UI
- Custom design system (warm cream, burgundy, gold)
- Homepage with hero section
- About, FAQ, Contact pages
- Responsive layout
- Custom CSS (animations.css, site.css)
- Vanilla JS animations (toast, modal, loader, sound)

---

## 📝 Format Legend

| Tag | Meaning |
|-----|---------|
| `Added` | New features |
| `Changed` | Changes to existing features |
| `Deprecated` | Soon-to-be removed features |
| `Removed` | Removed features |
| `Fixed` | Bug fixes |
| `Security` | Security improvements |
| `Performance` | Performance improvements |

---

## 🚀 Upcoming Roadmap

### Phase 5 (Planned)

- [ ] Email notifications (SendGrid)
- [ ] SMS alerts (Twilio)
- [ ] Donation eligibility check (weight, last donation date)
- [ ] Analytics dashboard (Chart.js)
- [ ] Multi-language support (Hindi, Gujarati)

### Phase 6 (Future)

- [ ] Mobile app (React Native)
- [ ] Hospital integration API
- [ ] Map-based donor view (Google Maps)
- [ ] Two-factor authentication
- [ ] Referral program

---

**Last Updated:** October 2026