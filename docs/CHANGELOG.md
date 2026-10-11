# 📅 Changelog

All notable changes to BloodConnect.

Format: [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)

---

## [Phase 4] — October 2026

### Added
- REST API with full CRUD (Donor, BloodRequest)
- Swagger UI documentation
- State dropdown (28 states + 8 UTs) for data consistency
- POST/PUT/DELETE API endpoints with auth
- Contact message caching (IMemoryCache)
- Live deployment on MonsterASP.NET
- HTTPS via Let's Encrypt
- Comprehensive documentation (README, API, DEPLOYMENT, SECURITY, USER_MANUAL)

### Changed
- Swagger always enabled (was dev-only)
- HTTPS redirect scoped to dev
- State column added to Donor + BloodRequest

### Fixed
- EF Core pending model changes warning
- State column nullable for legacy data
- Duplicate migration cleanup

---

## [Phase 3] — September 2026

### Added
- Contact message feature (admin inbox)
- Cached unread badge counter
- SuperAdmin protection rules
- Role management UI

### Changed
- Cookie authentication refinements
- Admin dashboard improvements

---

## [Phase 2] — August 2026

### Added
- Donor CRUD with validation
- Blood request management
- Compatibility-aware search
- Custom `MustBeTrue` validation
- Age validation (18-65)

### Changed
- Domain values centralized
- Form validation improvements

---

## [Phase 1] — July 2026

### Added
- ASP.NET Core MVC project scaffold
- Identity authentication
- Role-based authorization
- Bootstrap 5 UI
- Custom design system
- Homepage with hero section
- About, FAQ, Contact pages

---

**Format Legend:**
- `Added` — new features
- `Changed` — changes to existing features
- `Deprecated` — soon-to-be removed
- `Removed` — removed features
- `Fixed` — bug fixes
- `Security` — vulnerabilities