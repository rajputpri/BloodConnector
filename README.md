<div align="center">

# 🩸 BloodConnect

### Real-Time Blood Donation Network

**A production-grade full-stack platform connecting blood donors with patients in urgent need**

[![.NET](https://img.shields.io/badge/.NET-10.0-512BD4?style=for-the-badge&logo=dotnet&logoColor=white)](https://dotnet.microsoft.com/)
[![ASP.NET Core](https://img.shields.io/badge/ASP.NET_Core-MVC-512BD4?style=for-the-badge&logo=dotnet)](https://learn.microsoft.com/aspnet/core)
[![EF Core](https://img.shields.io/badge/EF_Core-10.0-512BD4?style=for-the-badge)](https://learn.microsoft.com/ef/core)
[![SQL Server](https://img.shields.io/badge/SQL_Server-Express-CC2927?style=for-the-badge&logo=microsoft-sql-server&logoColor=white)](https://www.microsoft.com/sql-server)
[![License](https://img.shields.io/badge/License-Educational-D4A24C?style=for-the-badge)](LICENSE)

[![Live Demo](https://img.shields.io/badge/🌐_Live_Demo-bloodconnector.runasp.net-DC2626?style=for-the-badge)](https://bloodconnector.runasp.net)
[![Swagger](https://img.shields.io/badge/📖_API_Docs-Swagger-85EA2D?style=for-the-badge&logo=swagger)](https://bloodconnector.runasp.net/swagger)
[![GitHub](https://img.shields.io/badge/GitHub-Source-181717?style=for-the-badge&logo=github)](https://github.com/rajputpri/BloodConnector)

**[🌐 Live Demo](https://bloodconnector.runasp.net)** · **[📖 API Docs](https://bloodconnector.runasp.net/swagger)** · **[🐛 Report Bug](https://github.com/rajputpri/BloodConnector/issues)** · **[✨ Request Feature](https://github.com/rajputpri/BloodConnector/issues)**

</div>

---

## 📸 Screenshots

<div align="center">

### 🏠 Homepage
![Homepage](docs/screenshots/public/01-homepage.png)

### 🩸 Blood Compatibility Chart
![Blood Compatibility](docs/screenshots/public/02-compatibility.png)

### 🔍 Donor Search
![Donor Search](docs/screenshots/public/03-donor-search.png)

### 📊 Admin Dashboard
![Admin Dashboard](docs/screenshots/admin/01-dashboard.png)

</div>

---

## 📖 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Tech Stack](#-tech-stack)
- [Architecture](#-architecture)
- [Quick Start](#-quick-start)
- [Configuration](#-configuration)
- [API Documentation](#-api-documentation)
- [Donation Workflow](#-donation-workflow)
- [Blood Compatibility Logic](#-blood-compatibility-logic)
- [Authorization Model](#-authorization-model)
- [Project Structure](#-project-structure)
- [Testing & Verification](#-testing--verification)
- [Deployment](#-deployment)
- [Documentation](#-documentation)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Overview

**BloodConnect** is a **real-time blood donation management platform** that connects verified donors with patients during emergencies. It eliminates the friction of traditional methods (WhatsApp groups, phone calls, social media) by providing a **compatibility-aware, pledge-based matching system**.

### 💡 The Problem

- India requires **14.6 million blood units annually** but faces a **1.5 million unit shortage**
- Traditional donor discovery is **slow, unverified, and unreliable**
- No way to verify if a donor will actually show up
- Wrong blood group matching leads to **wasted critical time**

### ✅ Our Solution

| Feature | Impact |
|---------|--------|
| **Real-time matching** | Find compatible donors in seconds, not hours |
| **Two-way pledge system** | Both parties confirm — no fake fulfillments |
| **Medical accuracy** | Built-in blood compatibility matrix (O− universal donor, AB+ universal receiver) |
| **Privacy-first** | Contact details revealed only after mutual agreement |
| **Zero cost** | Free forever — no premium tiers, no ads, no data selling |

---

## ✨ Key Features

### 👤 For Users
- **Register & authenticate** with ASP.NET Core Identity (secure password hashing, lockout protection)
- **Post blood requests** with urgency level, location, and contact details
- **Search compatible donors** by blood group, state, and availability
- **Track request status** in real-time (Open → Pledged → Accepted → Fulfilled)
- **Manage profile** through a personal dashboard

### 🩸 For Donors
- **Create verified donor profile** with age validation (18-65 years)
- **Pledge to donate** on active requests using a two-way confirmation flow
- **Browse compatible requests** based on medical accuracy
- **Track personal donations** and contribution history
- **Control availability** status anytime

### 🛡️ For Admins
- **Full user management** — ban/unban, promote/demote, delete
- **Role hierarchy** — SuperAdmin > Admin > User with strict enforcement
- **Moderate donors** — remove fraudulent entries
- **Manage blood requests** — delete policy violations
- **Contact message inbox** — read/unread tracking with cached badge count
- **Real-time dashboard** — stats on donors, requests, and fulfilled donations

### ⚙️ Engineering Highlights
- **REST API with Swagger UI** — 15+ documented endpoints
- **DTO pattern** for API responses (contact privacy protection)
- **RowVersion concurrency** on donor records
- **Global CSRF protection** via `AutoValidateAntiforgeryToken`
- **Cookie-based auth** with ban-checking middleware
- **Cached badge counter** using `IMemoryCache` with write-invalidation
- **EF Core migrations** for version-controlled schema
- **Compatibility matrix** centralized in `BloodCompatibility` helper
- **Unique compound index** prevents duplicate pledges

---

## 🛠 Tech Stack

<table>
<tr>
<td align="center" width="20%">

**Backend**
<br/>
![.NET 10](https://img.shields.io/badge/.NET-10-512BD4?logo=dotnet&logoColor=white)

</td>
<td align="center" width="20%">

**Framework**
<br/>
![ASP.NET Core](https://img.shields.io/badge/ASP.NET_Core-MVC-512BD4?logo=dotnet)

</td>
<td align="center" width="20%">

**Database**
<br/>
![SQL Server](https://img.shields.io/badge/SQL_Server-Express-CC2927?logo=microsoft-sql-server)

</td>
<td align="center" width="20%">

**ORM**
<br/>
![EF Core](https://img.shields.io/badge/EF_Core-10-512BD4)

</td>
<td align="center" width="20%">

**API Docs**
<br/>
![Swagger](https://img.shields.io/badge/Swagger-OpenAPI-85EA2D?logo=swagger)

</td>
</tr>
</table>

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| Runtime | .NET | 10.0 | Application runtime |
| Web Framework | ASP.NET Core MVC | 10.0 | HTTP request handling |
| Data Access | Entity Framework Core | 10.0 | ORM with code-first migrations |
| Database | SQL Server Express | 2019+ | Persistent storage |
| Authentication | ASP.NET Core Identity | 10.0 | Cookie-based auth |
| API Documentation | Swashbuckle.AspNetCore | 10.2.3 | Swagger UI + OpenAPI 3.0 |
| Frontend | Razor Views + Bootstrap | 5.x | Server-rendered UI |
| Styling | Custom CSS (Inter font) | — | Warm premium design system |
| Icons | Inline SVG (Lucide-style) | — | Crisp vector icons |
| Caching | IMemoryCache | — | 60-second badge cache |

---

## 🏗 Architecture

### High-Level Flow

```text
┌─────────────────────────────────────────────────────────────┐
│                         BROWSER                             │
│  (Desktop · Tablet · Mobile — Responsive via Bootstrap 5)   │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ HTTP / HTTPS
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                    ASP.NET CORE MVC                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │ Controllers │  │  Services   │  │  REST API           │  │
│  │ (Business   │  │ (Message    │  │ (DonorApi,          │  │
│  │  Logic)     │  │  Cache)     │  │  BloodRequestApi)   │  │
│  └──────┬──────┘  └─────────────┘  └─────────────────────┘  │
│         │                                                    │
│  ┌──────▼──────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │   Models    │  │  ViewModels │  │  Razor Views        │  │
│  │ (Entities)  │  │  (DTOs)     │  │  (UI Layer)         │  │
│  └──────┬──────┘  └─────────────┘  └─────────────────────┘  │
└─────────┼───────────────────────────────────────────────────┘
          │
          │ EF Core (Code-First Migrations)
          ▼
┌─────────────────────────────────────────────────────────────┐
│                     SQL SERVER                              │
│  ┌──────────┐  ┌────────────┐  ┌──────────────────────┐    │
│  │ Identity │  │  Domain    │  │  Relationship        │    │
│  │  Tables  │  │  Tables    │  │  Tables              │    │
│  │  (5)     │  │  (4)       │  │  (Indexed, FK-linked)│    │
│  └──────────┘  └────────────┘  └──────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

### Data Model

```text
AppUser ────┐
            │ owns
            ▼
          Donor ────┬──── DonationOffer ──── BloodRequest
                    │           │                 │
                    │           │                 │
                    └───────────┘                 │
                    (unique RequestId+DonorId)    │
                                                  │
                                                  │ owned by
                                                  ▼
                                                AppUser
```

### Design Principles

- **Separation of Concerns** — Controllers orchestrate, Models hold state, Views render
- **Thin Controllers** — Business logic pushed to domain services where it makes sense
- **No DB in Views** — All data prepared by controller actions
- **DTO Pattern for API** — Never expose entities directly; use `DonorDto`, `BloodRequestDto`
- **Server-Side Validation** — `[Required]`, `[Range]`, `[RegularExpression]`, custom `[MustBeTrue]`
- **Global CSRF** — Every form post validated via `AutoValidateAntiforgeryToken`
- **Role-Based Access** — `[Authorize(Roles = "...")]` + controller-level ownership checks

---

## 🚀 Quick Start

### Prerequisites

- [.NET 10 SDK](https://dotnet.microsoft.com/download)
- [SQL Server Express](https://www.microsoft.com/sql-server/sql-server-downloads) or LocalDB
- [Git](https://git-scm.com/)
- Optional: [VS Code](https://code.visualstudio.com/) with C# Dev Kit

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/rajputpri/BloodConnector.git
cd BloodConnector

# 2. Restore NuGet packages
dotnet restore

# 3. Install EF Core CLI (if not already)
dotnet tool install --global dotnet-ef

# 4. Update connection string in appsettings.Development.json
#    Example: "Server=localhost\\SQLEXPRESS04;Database=BloodConnectDb;Trusted_Connection=True;TrustServerCertificate=True;"

# 5. Apply migrations
dotnet ef database update

# 6. Run the application
dotnet run
```

**Application will be available at:** `http://localhost:5006`

### Default Admin Credentials

```text
Email:    admin@bloodconnect.com
Password: Admin@123
```

> [!WARNING]
> **Change these credentials immediately in production.** These are seeded for development only.

---

## ⚙ Configuration

### Development (`appsettings.Development.json`)

```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Server=localhost\\SQLEXPRESS04;Database=BloodConnectDb;Trusted_Connection=True;TrustServerCertificate=True;MultipleActiveResultSets=true"
  }
}
```

### Production (`appsettings.Production.json`)

```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Server=YOUR_SERVER;Database=YOUR_DB;User Id=YOUR_USER;Password=YOUR_PASSWORD;Encrypt=False;TrustServerCertificate=True;MultipleActiveResultSets=True"
  }
}
```

> [!IMPORTANT]
> `appsettings.Production.json` is **excluded from version control** (see `.gitignore`). Upload it manually to the hosting server or set via environment variables.

### Environment Variables (Alternative)

| Variable | Purpose |
|----------|---------|
| `ASPNETCORE_ENVIRONMENT` | Set to `Production` on hosting server |
| `ConnectionStrings__DefaultConnection` | Production DB connection string |

---

## 📡 API Documentation

**Live Swagger UI:** [https://bloodconnector.runasp.net/swagger](https://bloodconnector.runasp.net/swagger)

### Endpoints Overview

| Method | Endpoint | Auth | Purpose |
|--------|----------|:----:|---------|
| `GET` | `/api/donor` | 🌐 Public | List all donors (paginated) |
| `GET` | `/api/donor/{id}` | 🌐 Public | Get single donor by ID |
| `GET` | `/api/donor/search` | 🌐 Public | Compatibility-aware search |
| `POST` | `/api/donor` | 🔒 Auth | Create new donor profile |
| `PUT` | `/api/donor/{id}` | 🔒 Owner/Admin | Update donor |
| `DELETE` | `/api/donor/{id}` | 🔒 Owner/Admin | Delete donor |
| `GET` | `/api/bloodrequest` | 🌐 Public | List all blood requests |
| `GET` | `/api/bloodrequest/{id}` | 🌐 Public | Get single request |
| `POST` | `/api/bloodrequest` | 🔒 Auth | Create new request |
| `PUT` | `/api/bloodrequest/{id}` | 🔒 Owner/Admin | Update request |
| `DELETE` | `/api/bloodrequest/{id}` | 🔒 Owner/Admin | Delete request |

**Full API reference:** [docs/API.md](docs/API.md)

### Sample Response — `GET /api/donor/search?bloodGroup=B%2B`

```json
{
  "total": 2,
  "page": 1,
  "pageSize": 20,
  "searchMode": "compatible",
  "requestedBloodGroup": "B+",
  "compatibleGroups": ["O-", "O+", "B-", "B+"],
  "results": [
    {
      "donorId": 15,
      "name": "Gaurav",
      "bloodGroup": "B+",
      "state": "Bihar",
      "location": "Bihar",
      "isExactMatch": true
    }
  ]
}
```

---

## 🤝 Donation Workflow

### Pledge-Based Two-Way Confirmation

```text
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│ PLEDGED  │───▶│ ACCEPTED │───▶│COMPLETED │───▶│FULFILLED │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
     │
     ├──▶ CANCELLED  (donor cancels before acceptance)
     └──▶ REJECTED   (owner chooses another donor)
```

### Rules

- ✅ A donor can pledge **once per request** — enforced by unique `(RequestId, DonorId)` index
- ✅ **Cannot pledge on own request**
- ✅ **Blood group must match** — validated server-side
- ✅ Accepting one offer **auto-rejects all other pending offers**
- ✅ **Contact details revealed only after acceptance**
- ✅ Both owner **and** accepted donor can mark donation complete
- ✅ Fulfilled requests **cannot accept new offers**

---

## 🩸 Blood Compatibility Logic

### Red Cell Compatibility Matrix

| Recipient | Can Receive From |
|-----------|-----------------|
| **O−**  | O− |
| **O+**  | O−, O+ |
| **A−**  | O−, A− |
| **A+**  | O−, O+, A−, A+ |
| **B−**  | O−, B− |
| **B+**  | O−, O+, B−, B+ |
| **AB−** | O−, A−, B−, AB− |
| **AB+** | All 8 groups |

### Key Facts

- **🩸 O− is the universal donor** — can donate red cells to all 8 groups
- **🩸 AB+ is the universal receiver** — can receive red cells from all 8 groups
- **A+ and B+** are the most common in India (~30% and ~24%)

This logic is centralized in `BloodCompatibility.cs` and applied consistently across:
- Web-based donor search
- API search endpoint
- Donation offer validation

---

## 🔐 Authorization Model

### Role Hierarchy

```text
┌─────────────────────────────────────────┐
│           SuperAdmin                     │  ← Highest
│         (Immutable, undeletable)        │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│              Admin                       │
│   (Can manage users below, moderate)     │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│              User                        │  ← Lowest
│         (Basic access)                   │
└─────────────────────────────────────────┘
```

### Permission Matrix

| Action | User | Admin | SuperAdmin |
|--------|:----:|:-----:|:----------:|
| Edit own donor profile | ✅ | ✅ | ✅ |
| Edit another's profile | ❌ | ❌ | ❌ |
| Delete own request | ✅ | ✅ | ✅ |
| Delete another's request | ❌ | ✅ | ✅ |
| Ban regular user | ❌ | ✅ | ✅ |
| Ban an Admin | ❌ | ❌ | ✅ |
| Ban a SuperAdmin | ❌ | ❌ | ❌ |
| Promote User → Admin | ❌ | ✅ | ✅ |
| Demote Admin → User | ❌ | ❌ | ✅ |
| Delete SuperAdmin | ❌ | ❌ | ❌ |
| Ban/delete self | ❌ | ❌ | ❌ |

---

## 📁 Project Structure

```text
BloodConnect/
├── 📁 Controllers/           # HTTP request handlers
│   ├── HomeController.cs        # Homepage, About, Contact, Error
│   ├── DonorController.cs       # Donor CRUD + compatibility search
│   ├── BloodRequestController.cs # Request CRUD + offer workflow
│   ├── DonorApiController.cs    # REST API for donors
│   ├── BloodRequestApiController.cs # REST API for requests
│   ├── AccountController.cs     # Register, Login, Logout
│   ├── AdminController.cs       # Admin panel + role management
│   └── DashboardController.cs   # User dashboard
│
├── 📁 Models/                # Domain entities + ViewModels
│   ├── AppUser.cs              # Extended IdentityUser
│   ├── Donor.cs                # Donor entity
│   ├── BloodRequest.cs         # Blood request entity
│   ├── DonationOffer.cs        # Pledge workflow entity
│   ├── ContactMessage.cs       # Contact form submissions
│   ├── BloodCompatibility.cs   # Compatibility logic
│   ├── DomainValues.cs         # Constants (blood groups, states, etc.)
│   ├── ValidationAttributes.cs # Custom validators
│   ├── ApplicationDbContext.cs # EF Core DbContext
│   ├── DbSeeder.cs             # Seed data (roles, admin)
│   ├── ApiDtos.cs              # API data transfer objects
│   └── ViewModels.cs           # View-specific models
│
├── 📁 Services/              # Cross-cutting concerns
│   └── MessageCache.cs         # Cached unread count
│
├── 📁 Migrations/            # EF Core migrations (version-controlled schema)
│
├── 📁 Views/                 # Razor UI templates
│   ├── Shared/                 # Layouts, partials
│   ├── Home/                   # Homepage, About, Contact, FAQ
│   ├── Donor/                  # Donor pages
│   ├── BloodRequest/           # Request pages
│   ├── Account/                # Auth pages
│   ├── Admin/                  # Admin panel
│   └── Dashboard/              # User dashboard
│
├── 📁 wwwroot/               # Static assets
│   ├── css/                    # Custom stylesheets
│   ├── js/                     # Client-side scripts
│   └── lib/                    # Bootstrap, jQuery
│
├── 📁 docs/                  # 📚 Documentation
│   ├── API.md
│   ├── ARCHITECTURE.md
│   ├── DEPLOYMENT.md
│   ├── SECURITY.md
│   ├── USER_MANUAL.md
│   ├── CHANGELOG.md
│   └── screenshots/            # Organized screenshot gallery
│
├── 📄 Program.cs             # Application entry point
├── 📄 appsettings.json
├── 📄 appsettings.Development.json
├── 📄 appsettings.Production.json  (gitignored)
├── 📄 BloodConnect.csproj
└── 📄 README.md
```

---

## ✅ Testing & Verification

### Manual Verification Checklist

| Area | Scenarios |
|------|-----------|
| **Authentication** | Registration, login, logout, lockout (5 attempts), weak password rejection |
| **Authorization** | Owner-only edit, admin delete, role hierarchy, self-protection |
| **Ban System** | Banned user auto-signed out, login denied |
| **Donor CRUD** | Create, edit, delete, age validation (18-65) |
| **Search** | Compatible + exact match, ordering, state filter |
| **Workflow** | Offer, accept, reject competing offers, cancel, complete |
| **Compatibility** | All 8 groups, universal donor/receiver cases |
| **Contact Inbox** | Persistence, read/unread, deletion, cache invalidation |
| **Error Handling** | Branded 404/500 without stack traces |

### API Testing

All API endpoints tested via **Swagger UI** and **Postman**.

📸 **Screenshots:** [docs/screenshots/api/](docs/screenshots/api/)

---

## 🚀 Deployment

**Live Production:** [https://bloodconnector.runasp.net](https://bloodconnector.runasp.net)

### Deployed On

| Component | Service |
|-----------|---------|
| **Hosting** | MonsterASP.NET (Free tier) |
| **Database** | SQL Server 2025 (MonsterASP managed) |
| **HTTPS** | Let's Encrypt SSL |
| **Auto-deploy** | GitHub → Build & Publish |

**Full deployment guide:** [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)

---

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| [README.md](README.md) | Project overview (this file) |
| [docs/API.md](docs/API.md) | Complete API reference |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | System design & data model |
| [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) | Step-by-step deployment |
| [docs/SECURITY.md](docs/SECURITY.md) | Security model & threat analysis |
| [docs/USER_MANUAL.md](docs/USER_MANUAL.md) | User guide |
| [docs/CHANGELOG.md](docs/CHANGELOG.md) | Version history |

---

## 🗺 Roadmap

### ✅ Completed (Phase 1-4)

- [x] ASP.NET Core Identity authentication
- [x] Three-tier role system (SuperAdmin > Admin > User)
- [x] Donor CRUD with age & location validation
- [x] Blood request management with urgency filters
- [x] Compatibility-aware search
- [x] Pledge-based donation workflow
- [x] Admin panel with user management
- [x] Contact message inbox with caching
- [x] State dropdown (data consistency)
- [x] REST API with full CRUD
- [x] Swagger UI documentation
- [x] Live deployment on MonsterASP.NET
- [x] HTTPS with Let's Encrypt

### 🚀 Planned

- [ ] Email notifications (SendGrid)
- [ ] SMS alerts (Twilio)
- [ ] Mobile app (React Native)
- [ ] Hospital integration API
- [ ] Analytics dashboard (Chart.js)
- [ ] Multi-language support (Hindi, Gujarati)
- [ ] Map-based donor view (Google Maps)
- [ ] Two-factor authentication

---

## 🤝 Contributing

This is an **educational project**. Contributions are welcome for:

- 🐛 Bug fixes
- 📝 Documentation improvements
- ✨ Feature suggestions
- 🎨 UI/UX enhancements

**Process:**
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📜 License

This project is provided for **educational use**. See [LICENSE](LICENSE) for details.

---

## 👨‍💻 Author

**Prince Rajput**
BCA Semester 7 · DSC-M-CBA 471P · Gujarat University

[![GitHub](https://img.shields.io/badge/GitHub-rajputpri-181717?style=flat&logo=github)](https://github.com/rajputpri)

---

## ⚠️ Disclaimer

BloodConnect is an **educational project** demonstrating full-stack ASP.NET Core development. It is **not a medical, emergency-response, or production blood-bank system**. The compatibility lookup is a simplified educational reference and does not replace professional blood typing, crossmatching, screening, or clinical judgment.

Do **not** rely on this application for real medical decisions.

---

<div align="center">

**Made with ❤️ in India**

**Every drop counts.** 🩸

⭐ **Star this repo if it helped you!** ⭐

</div>