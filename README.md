# 🩸 BloodConnect

> A blood donation management platform that helps connect donors with people who need blood, built with ASP.NET Core MVC.

BloodConnect is an educational full-stack project. It demonstrates donor and blood-request management, compatibility-aware search, a pledge-based donation workflow, role-based administration, and a responsive web interface.

> [!IMPORTANT]
> BloodConnect is **not a medical, emergency-response, or production blood-bank system**. Do not use it to make medical decisions or coordinate urgent care. See [Disclaimer](#disclaimer).

## Contents

- [Overview](#overview)
- [Features](#features)
- [Technology](#technology)
- [Architecture](#architecture)
- [Getting started](#getting-started)
- [Configuration](#configuration)
- [Authorization](#authorization)
- [Donation workflow](#donation-workflow)
- [Blood compatibility](#blood-compatibility)
- [API](#api)
- [Project layout](#project-layout)
- [Verification checklist](#verification-checklist)
- [Deployment](#deployment)
- [Roadmap](#roadmap)
- [Disclaimer](#disclaimer)
- [License](#license)

## Overview

BloodConnect supports two connected workflows:

1. People can publish blood requests with an urgency level and location.
2. Donors can find compatible requests and pledge to help. The request owner can accept an offer and coordinate with the donor.

The application includes account management, donor profiles, request and offer tracking, an admin area, and a contact-message inbox.

## Features

### Donor and requester experience

- ASP.NET Core Identity registration, login, logout, password validation, and account lockout.
- Donor profiles with blood group, age, location, and contact details; profile changes are owner-scoped.
- Blood requests with Critical, High, Medium, or Low urgency and status tracking. The original project supports guest request submission; review privacy and spam controls before exposing this publicly.
- Donor search by blood group and location, with compatible-group search or exact-match filtering.
- Pledge workflow: donors offer help, request owners accept an offer, and either party can mark the accepted donation complete.
- User dashboard for profile, requests, offers, and fulfilled donations.
- Contact form with persistent messages and an admin inbox with read/unread tracking.

### Interface

- Responsive, mobile-first layout using Bootstrap 5.
- Warm cream, burgundy, and gold visual theme, inline SVG icons, and Inter typography.
- Toast notifications, confirmation modal, and optional browser-local sound effects.
- CSS and JavaScript animations, including card and button effects.

### Engineering

- MVC separation with Razor views, controllers, domain models, and view models.
- Server-side validation and global antiforgery validation for MVC form posts.
- Role hierarchy and ownership checks for administrative and personal data actions.
- Centralized red-cell compatibility lookup logic in `BloodCompatibility`.
- Unique `(RequestId, DonorId)` index to prevent duplicate pledges.
- Optimistic concurrency token on donor records.
- Cached unread-message count with write-triggered invalidation.
- Read-only EF Core queries use `AsNoTracking`; SQL Server transient retry configuration is documented in the application setup.

## Technology

| Area | Technology |
|---|---|
| Runtime | .NET 10 (`net10.0`) |
| Web | ASP.NET Core MVC and Razor Views |
| Data access | Entity Framework Core 10, Code First |
| Database | SQL Server Express or LocalDB for development |
| Authentication | ASP.NET Core Identity cookies |
| Authorization | Role-based policies and controller checks |
| Caching | `IMemoryCache` |
| UI | Bootstrap 5, custom CSS, vanilla JavaScript |
| Icons | Inline SVG |
| Browser audio | Web Audio API |

## Architecture

```text
Browser
  │
  ▼
ASP.NET Core MVC Controllers ─────── JSON API
  │                                  │
  ├── Domain models / view models    │
  ├── Application services           │
  └── Razor views                     │
          │                           │
          └──────── Entity Framework Core ─────── SQL Server
```

### Design notes

- Controllers handle routing, model binding, authorization, and view orchestration.
- `Models/` contains domain entities, validation helpers, and view models.
- `Services/` contains cross-cutting application services such as unread-message caching.
- Views should remain presentation-focused and should not perform database queries.
- Admin and role-management views should use view models instead of binding directly to Identity entities.

## Getting started

### Prerequisites

- .NET 10 SDK
- SQL Server Express or SQL Server LocalDB
- Git
- Optional: Visual Studio or VS Code with the C# Dev Kit

### 1. Clone and restore

```bash
git clone https://github.com/rajputpri/BloodConnector.git BloodConnect
cd BloodConnect
dotnet restore
```

### 2. Configure the development database

Set `ConnectionStrings:DefaultConnection` in `appsettings.Development.json`. For example:

```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Server=(localdb)\\MSSQLLocalDB;Database=BloodConnectDb;Trusted_Connection=True;TrustServerCertificate=True;"
  }
}
```

Use the server name appropriate for your SQL Server installation. Keep real credentials and production connection strings out of source control.

### 3. Install EF tooling if needed, then apply migrations

```bash
dotnet tool install --global dotnet-ef
dotnet ef database update
```

If `dotnet-ef` is already installed, skip the install command. The migration creates the Identity schema and the application's domain tables.

### 4. Run the application

```bash
dotnet run
```

Open the local URL printed by the application. The source README previously listed `http://localhost:5006`; the actual port depends on the project's launch settings.

### 5. Seeded administrator account

The project documentation describes a seeded account:

```text
Email:    admin@bloodconnect.com
Password: Admin@123
```

Treat these as development-only credentials. Confirm the current seeder behavior in `DbSeeder.cs`, change/remove the default password before any shared deployment, and never publish a deployment with a known default credential.

## Configuration

### Environment variables

ASP.NET Core supports environment-variable configuration using double underscores in place of `:`.

| Variable | Purpose |
|---|---|
| `ASPNETCORE_ENVIRONMENT` | Set to `Production` on a production host |
| `ConnectionStrings__DefaultConnection` | Production database connection string |

Provide secrets through the hosting platform's secret manager or environment configuration. Do not commit production credentials.

### Documented identity and cookie settings

| Setting | Documented value |
|---|---|
| Cookie | ASP.NET Core Identity application cookie |
| `HttpOnly` | Enabled |
| `SameSite` | `Lax` |
| Expiration | 7 days, sliding |
| Lockout | 5 failed attempts, 5-minute lockout |
| Password policy | Minimum 6 characters and a digit |

Verify the effective settings in the application configuration before deployment; these values describe the project documentation and are not a substitute for reviewing runtime configuration.

## Authorization

BloodConnect documents a three-level hierarchy: **SuperAdmin > Admin > User**. Authorization must be enforced on the server for every protected action.

| Action | Owner/User | Admin | SuperAdmin |
|---|:---:|:---:|:---:|
| Edit own donor profile | ✅ | ✅ | ✅ |
| Edit another user's donor profile | ❌ | ❌ | ❌ |
| Delete own donor profile or request | ✅ | ✅ | ✅ |
| Delete another user's request | ❌ | ✅ | ✅ |
| Ban or unban a regular user | ❌ | ✅ | ✅ |
| Ban or unban an Admin | ❌ | ❌ | ✅ |
| Ban or unban a SuperAdmin | ❌ | ❌ | ❌ |
| Promote User to Admin | ❌ | ✅ | ✅ |
| Demote Admin to User | ❌ | ❌ | ✅ |
| Delete a SuperAdmin | ❌ | ❌ | ❌ |
| Ban or delete self | ❌ | ❌ | ❌ |

The documented design reserves personal donor-profile edits to the profile owner. Admins may moderate or remove fraudulent entries but should not change a donor's personal information.

## Donation workflow

```text
Pledged ── owner accepts ──▶ Accepted ── marked complete ──▶ Completed
   │                            │
   ├── donor cancels ──▶ Cancelled
   └── owner chooses another ──▶ Rejected
```

- A donor can create at most one offer for a given request; a unique database index enforces this.
- Donors cannot offer on their own request.
- Compatibility is checked server-side when an offer is made.
- Accepting one offer rejects the other offers for that request.
- Contact details are revealed only after an offer is accepted, according to the documented workflow.
- The request owner or accepted donor can mark the donation complete.
- Fulfilled requests cannot accept new offers.

## Blood compatibility

The application documents red blood cell compatibility. A recipient can receive red cells from the following donor groups:

| Recipient | Compatible donor groups |
|---|---|
| O− | O− |
| O+ | O−, O+ |
| A− | O−, A− |
| A+ | O−, O+, A−, A+ |
| B− | O−, B− |
| B+ | O−, O+, B−, B+ |
| AB− | O−, A−, B−, AB− |
| AB+ | All listed groups |

O− red cells are often described as universal donor red cells, and AB+ recipients can receive red cells from all listed ABO/Rh groups. Actual transfusion decisions require blood typing, screening, and clinical procedures; this table is educational only.

## API

Base path: `/api/donor`

The documented API currently exposes compatibility-aware donor search. Authentication and donor CRUD API endpoints are listed as future work.

### `GET /api/donor/search`

| Parameter | Type | Default | Description |
|---|---|---:|---|
| `bloodGroup` | string | — | Blood group, such as `A+`, `O-`, or `AB+` |
| `location` | string | empty | Case-insensitive location substring |
| `exactMatch` | bool | `false` | Return only the requested blood group when true |
| `page` | int | `1` | 1-based page number |
| `pageSize` | int | `20` | Page size; confirm the server-side maximum in code |

Example response:

```json
{
  "searchMode": "Compatible",
  "compatibleGroups": ["O-", "O+", "A-", "A+"],
  "isExactMatch": false,
  "page": 1,
  "pageSize": 20,
  "totalCount": 14,
  "items": [
    {
      "donorId": 3,
      "name": "Ravi Kumar",
      "bloodGroup": "O+",
      "location": "Gujarat",
      "age": 27,
      "isAvailable": true,
      "isExactMatch": false
    }
  ]
}
```

Search results do not include phone numbers. The documented workflow reveals contact details after an offer is accepted.

## Project layout

```text
BloodConnect/
├── Controllers/
│   ├── HomeController.cs
│   ├── DonorController.cs
│   ├── BloodRequestController.cs
│   ├── DonorApiController.cs
│   ├── AccountController.cs
│   ├── AdminController.cs
│   └── DashboardController.cs
├── Models/
│   ├── AppUser.cs
│   ├── Donor.cs
│   ├── BloodRequest.cs
│   ├── DonationOffer.cs
│   ├── ContactMessage.cs
│   ├── BloodCompatibility.cs
│   ├── DomainValues.cs
│   ├── ValidationAttributes.cs
│   ├── ApplicationDbContext.cs
│   ├── DbSeeder.cs
│   └── ViewModels.cs
├── Services/
│   └── MessageCache.cs
├── Migrations/
├── Views/
├── wwwroot/
│   ├── css/
│   └── js/
├── appsettings.json
├── appsettings.Development.json
└── Program.cs
```

## Verification checklist

The original project description says there is no automated test suite yet. Use this checklist for manual verification, or turn the cases into automated tests as the project evolves.

| Area | Scenarios |
|---|---|
| Authentication | Registration consent, login/logout, lockout, weak-password rejection |
| Authorization | Owner-only edit, owner/admin deletion, role hierarchy, self-protection |
| Ban handling | Banned user's next request signs them out; login is denied |
| Donor management | Create, edit, delete, and age validation (18–65) |
| Search | Compatible and exact results, exact-first ordering, location filter |
| Workflow | Offer, accept, reject competing offers, cancel, complete, duplicate prevention, no self-offer |
| Compatibility | All eight groups, including O− donor and AB+ recipient cases |
| Contact inbox | Persistence, read/unread state, deletion, cached count invalidation |
| Error handling | Branded 404/500 responses without stack-trace disclosure |
| Static assets | CSS/JS cache-busting with `asp-append-version` |

Useful manual checks include searching for `A+` and verifying compatible groups appear with exact matches first, and confirming the unread-message count changes after message writes.

## Deployment

The documented deployment target is a Windows ASP.NET Core host with SQL Server. The project mentions MonsterASP.NET, Somee.com, and Azure App Service as possible hosting options; confirm current hosting capabilities, pricing, and .NET 10 support before choosing a provider.

Publish a release build:

```bash
dotnet publish -c Release -o published
```

Set the production environment and connection string through the host's configuration system. Apply migrations using the deployment process chosen for the project. For example, when using the EF CLI from a trusted deployment environment:

```bash
dotnet ef database update --connection "<production-connection-string>"
```

For a production service, review secrets, seeded accounts, HTTPS, database access, backups, logging, privacy/retention rules, and operational ownership before launch.

## Roadmap

### Documented as implemented

- Authentication and three-tier role system
- Donor CRUD and compatibility-aware search
- Blood-request management and filters
- Pledge-based donation workflow
- Admin panel and user dashboard
- Contact-message inbox and cached unread badge
- Responsive UI, animations, and optional sound effects

### Planned

- State-based location dropdown for consistent data
- REST API CRUD and get-by-id endpoints
- Donation eligibility information (such as weight and last donation date), reviewed by qualified medical stakeholders
- Email notifications
- Dashboard statistics and charts
- Deployment documentation and hosting setup
- Project report and presentation

## Disclaimer

BloodConnect is an educational project for demonstrating full-stack ASP.NET Core development. It is not a verified medical product, blood-bank system, or emergency-response service. Its compatibility lookup is a simplified educational reference and does not replace professional blood typing, crossmatching, screening, or clinical judgment.

Do not rely on this application for real medical decisions or time-critical blood coordination without independent clinical, security, privacy, and operational review. Consent, data retention, medical-data handling, and jurisdiction-specific legal obligations are outside this project's stated scope and require qualified review before any real-world deployment.

## License

This project is provided for educational use. Check the repository for a `LICENSE` file. If you intend to publish or redistribute the code, choose and add an explicit license first.

<p align="center">Made with ❤️ in India · <strong>Every drop counts.</strong></p>
