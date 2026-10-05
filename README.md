# 🩸 BloodConnect

> A blood donation management platform connecting donors with patients in real-time. Built with ASP.NET Core MVC as a BCA Sem-7 project.

![.NET](https://img.shields.io/badge/.NET-10.0-512BD4?style=flat-square\&logo=dotnet)
![ASP.NET Core](https://img.shields.io/badge/ASP.NET%20Core-MVC-512BD4?style=flat-square\&logo=dotnet)
![EF Core](https://img.shields.io/badge/EF%20Core-10.0-512BD4?style=flat-square)
![SQL Server](https://img.shields.io/badge/SQL%20Server-Express-CC2927?style=flat-square\&logo=microsoftsqlserver)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-7952B3?style=flat-square\&logo=bootstrap)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## 📌 About

**BloodConnect** is a web application that connects blood donors with patients in need. It goes beyond simple donor listing by using **medical blood compatibility rules**, providing a **pledge-based donation workflow**, and giving administrators complete control over the platform.

Built as a **BCA Semester-7 project** for Gujarat University under:

**DSC-M-CBA 471P — Full Stack Web Development**

---

## ✨ Features

### 🔐 Authentication & Roles

* ASP.NET Core Identity with cookie-based authentication
* 3-tier role hierarchy:

  * **SuperAdmin**
  * **Admin**
  * **User**
* Ban system with automatic sign-out on banned user requests
* Account lockout after 5 failed login attempts
* Persistent authentication cookies with 7-day expiration
* Sliding cookie expiration

### 🩸 Blood Donation

* Donor registration with:

  * Blood group
  * Location
  * Age
* **Blood compatibility-aware donor search**
* Supports exact and compatible blood-group matching
* O⁻ treated as the universal red-blood-cell donor
* AB⁺ treated as the universal red-blood-cell recipient
* Search donors by:

  * Blood group
  * Location
  * Compatibility
* Blood requests with urgency levels:

  * 🔴 Critical
  * 🟠 High
  * 🟡 Medium
  * 🟢 Low
* Guests can post blood requests without logging in

### 🤝 Pledge-Based Donation Workflow

The platform uses a structured donation workflow:

```text
Pledged → Accepted → Completed
             ↓
          Rejected
             ↓
         Cancelled
```

* Donor clicks **"I can donate"** to create a donation pledge
* Request owner can accept one donation offer
* Other pending offers are automatically rejected
* Contact details are revealed after acceptance
* Either party can mark the donation as completed
* Blood request is fulfilled after successful completion
* Complete audit trail with timestamps

### 🛡️ Admin Panel

* Admin dashboard with live statistics
* Manage:

  * Users
  * Donors
  * Blood requests
  * Contact messages
* Promote users to Admin
* Demote Admin users
* Only SuperAdmin can demote Admins
* Ban/unban users
* Protection against:

  * Self-ban
  * Banning SuperAdmin
  * Unauthorized role changes
* Contact message inbox
* Read/unread message tracking

### 👤 User Dashboard

* Profile overview
* Donor profile status
* My blood requests
* My donation offers
* My completed donations
* Centralized user activity dashboard

### 🎨 UI/UX

BloodConnect uses a **warm premium design system** based on:

* Cream
* Burgundy
* Gold

Additional UI features include:

* Inter font
* SVG icons
* Toast notifications
* Custom confirmation modals
* 3D card tilt effects
* Magnetic buttons
* Cursor glow
* Procedural sound effects
* Web Audio API
* Minimal top progress bar
* Fully responsive layout
* Custom CSS animations

> No external sound files are required. Sound effects are generated procedurally using the Web Audio API.

### ⚡ Performance

* `IMemoryCache` for unread message counts
* Maximum one database query per 60 seconds per admin for cached unread counts
* Cache invalidation after write operations
* Indexed database columns for:

  * Blood group
  * Location
  * Status
* `AsNoTracking()` for read-only queries
* `EnableRetryOnFailure()` for transient database errors

---

## 🛠️ Tech Stack

| Layer          | Technology                    |
| -------------- | ----------------------------- |
| Framework      | ASP.NET Core MVC (.NET 10)    |
| Runtime        | .NET 10                       |
| ORM            | Entity Framework Core 10.0.12 |
| Database       | SQL Server Express            |
| Authentication | ASP.NET Core Identity         |
| Frontend       | Razor Views                   |
| UI Framework   | Bootstrap 5                   |
| JavaScript     | Vanilla JavaScript + jQuery   |
| Styling        | Custom CSS3                   |
| Charts         | Chart.js                      |
| Icons          | SVG / Font Awesome            |
| Fonts          | Google Fonts / Inter          |
| Animations     | CSS3 + Vanilla JavaScript     |
| Sound          | Web Audio API                 |
| Caching        | `IMemoryCache`                |

---

## 📁 Project Structure

```text
BloodConnect/
│
├── Controllers/
│   ├── HomeController.cs
│   ├── DonorController.cs
│   ├── BloodRequestController.cs
│   ├── DonorApiController.cs
│   ├── AccountController.cs
│   ├── AdminController.cs
│   └── DashboardController.cs
│
├── Models/
│   ├── AppUser.cs
│   ├── Donor.cs
│   ├── BloodRequest.cs
│   ├── DonationOffer.cs
│   ├── ContactMessage.cs
│   ├── BloodCompatibility.cs
│   ├── ApplicationDbContext.cs
│   ├── DbSeeder.cs
│   └── ViewModels.cs
│
├── Services/
│   └── MessageCache.cs
│
├── Views/
│   ├── Home/
│   ├── Donor/
│   ├── BloodRequest/
│   ├── Account/
│   ├── Admin/
│   └── Dashboard/
│
├── Migrations/
│
├── wwwroot/
│   ├── css/
│   │   ├── site.css
│   │   └── animations.css
│   │
│   └── js/
│       └── animations.js
│
├── Program.cs
├── appsettings.json
└── appsettings.Development.json
```

---

## 🚀 Getting Started

### Prerequisites

Before running BloodConnect, make sure you have:

* [.NET 10 SDK](https://dotnet.microsoft.com/download)
* SQL Server Express or SQL Server LocalDB
* Visual Studio 2022 or Visual Studio Code
* Entity Framework Core CLI tools

---

### 1. Clone the Repository

```bash
git clone https://github.com/rajputpri/BloodConnector.git
cd BloodConnector
```

---

### 2. Configure the Database

Update the connection string in:

```text
appsettings.Development.json
```

Example:

```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Server=localhost\\SQLEXPRESS04;Database=BloodConnectDb;Trusted_Connection=True;TrustServerCertificate=True;"
  }
}
```

> Update the SQL Server instance name according to your local SQL Server installation.

---

### 3. Apply EF Core Migrations

Run:

```bash
dotnet ef database update
```

This will create/update the `BloodConnectDb` database using the existing EF Core migrations.

---

### 4. Run the Application

```bash
dotnet run
```

The application will start on:

```text
http://localhost:5006
```

Open the URL in your browser.

---

## 🔑 Default Admin Credentials

```text
Email:    admin@bloodconnect.com
Password: Admin@123
```

> ⚠️ **Security Warning:** Change the default admin password immediately in any production or publicly deployed environment.

---

## 🔬 Key Design Decisions

### Why Blood Compatibility Search?

Blood type compatibility isn't a simple 1-to-1 relationship.

For example, an **A⁺ patient** can generally receive red blood cells from:

```text
O⁻
O⁺
A⁻
A⁺
```

Therefore, a simple exact-match search would not represent actual blood compatibility rules.

BloodConnect uses a dedicated:

```text
BloodCompatibility.cs
```

class to encode compatibility rules and perform compatibility-aware donor searches.

---

### Why a Pledge-Based Donation Workflow?

A blood request should not be marked as fulfilled simply because someone claims they can donate.

BloodConnect therefore uses a structured workflow:

```text
Donor
  │
  │ "I can donate"
  ▼
Pledged
  │
  │ Request owner accepts
  ▼
Accepted
  │
  │ Donation completed
  ▼
Completed
```

Other possible states include:

```text
Rejected
Cancelled
```

This prevents false fulfillment and provides a clear history of every donation interaction.

---

### Why `IMemoryCache` for Unread Messages?

Only administrators need to see the unread contact-message count.

Instead of executing a database `COUNT(*)` query every time an admin page loads, BloodConnect uses:

```csharp
IMemoryCache
```

The unread count is cached and invalidated whenever relevant message data changes.

This reduces unnecessary database queries while keeping the notification badge accurate.

---

### Why EF Core Migrations?

BloodConnect uses a **Code-First Entity Framework Core** approach.

Benefits include:

* Database schema represented through C# models
* Version-controlled migrations
* Easy database recreation
* Consistent schema between development environments
* Easier collaboration between team members

Database updates can be applied using:

```bash
dotnet ef database update
```

---

## 🌐 API Endpoints

BloodConnect currently provides the following REST API endpoint:

| Method | Endpoint            | Description                                                                                 |
| ------ | ------------------- | ------------------------------------------------------------------------------------------- |
| `GET`  | `/api/donor/search` | Search donors by blood group and location with compatibility-aware filtering and pagination |

### Example

```http
GET /api/donor/search?bloodGroup=A%2B&location=Ahmedabad&page=1&pageSize=10
```

> More REST API endpoints such as `POST`, `PUT`, and `DELETE` are planned for Phase 4.

---

## 🧪 Testing Highlights

BloodConnect includes testing for several important business rules and security boundaries.

### Blood Compatibility

* ✅ O⁻ donor can donate to all supported blood groups
* ✅ AB⁺ can receive from all supported blood groups
* ✅ Exact blood-group matching
* ✅ Compatible blood-group matching

### Role Boundaries

* ✅ Admin cannot ban SuperAdmin
* ✅ Admin cannot modify protected SuperAdmin privileges
* ✅ Users cannot perform admin operations
* ✅ Users cannot self-promote
* ✅ Users cannot self-ban

### Donation Workflow

* ✅ Donor can create a pledge
* ✅ Request owner can accept an offer
* ✅ Only one offer can be accepted
* ✅ Remaining offers are automatically rejected
* ✅ Request cannot be completed without an accepted donation offer
* ✅ Completed donations are tracked

### Cache

* ✅ Unread message count is cached
* ✅ Cache invalidates after relevant writes
* ✅ Badge reflects new message state

### Validation

The application uses multiple validation mechanisms, including:

* ✅ `Required`
* ✅ `StringLength`
* ✅ `Range`
* ✅ `RegularExpression`
* ✅ `EmailAddress`
* ✅ `Compare`
* ✅ Custom validation

---

## 🎓 Academic Context

**Course:** DSC-M-CBA 471P — Full Stack Web Development Project Using ASP.NET Core

**University:** Gujarat University

**Program:** Bachelor of Computer Applications (BCA)

**Semester:** Semester 7

---

## 📚 Syllabus Coverage

| Phase                        | Marks | Status         |
| ---------------------------- | ----: | -------------- |
| Phase 1 — MVC Setup & UI     |    15 | ✅ Complete     |
| Phase 2 — Forms & Validation |    15 | ✅ Complete     |
| Phase 3 — Database & CRUD    |    25 | ✅ Complete     |
| Phase 4 — API & Deployment   |    15 | 🟡 In Progress |
| Report                       |    10 | 🟡 In Progress |
| Presentation                 |    10 | 🟡 In Progress |
| Viva                         |    10 | ✅ Ready        |

**Total:** 100 Marks

---

## 🗺️ Roadmap

### ✅ Completed

* [x] Authentication & role system
* [x] Donor CRUD
* [x] Blood compatibility search
* [x] Blood request CRUD
* [x] Blood request filtering
* [x] Pledge-based donation workflow
* [x] Admin panel
* [x] Role management
* [x] User dashboard
* [x] Contact messages
* [x] Cached unread-message badge
* [x] Premium UI design
* [x] Responsive design
* [x] Animation system
* [x] Web Audio API sound effects

### 🚧 In Progress

* [ ] Location → State dropdown
* [ ] REST API CRUD endpoints
* [ ] API documentation
* [ ] Deployment
* [ ] Final project report
* [ ] PowerPoint presentation

### 🔮 Planned

* [ ] Deploy on [MonsterASP.NET](https://monsterasp.net/)
* [ ] Complete REST API with POST/PUT/DELETE
* [ ] Improve API documentation
* [ ] Add production deployment configuration
* [ ] Add project screenshots
* [ ] Add demo video

---

## 📸 Screenshots

Screenshots will be added soon.

Planned screenshots:

* 🏠 Homepage
* 🩸 Donor search
* 📝 Blood request page
* 🤝 Donation pledge workflow
* 👤 User dashboard
* 🛡️ Admin dashboard
* 📩 Messages inbox
* 📊 Admin statistics

---

## 🤝 Contributing

BloodConnect is currently a **solo academic project**.

Suggestions, bug reports, and feedback are welcome.

If you find an issue, please open a GitHub issue with:

1. A clear description of the problem
2. Steps to reproduce it
3. Expected behavior
4. Actual behavior
5. Screenshots, if applicable

---

## 📄 License

This project is licensed under the **MIT License**.

See the [`LICENSE`](LICENSE) file for details.

---

## 👨‍💻 Author

**Rajput Prince**

BCA — Gujarat University

GitHub: [@rajputpri](https://github.com/rajputpri)

---

## ❤️ Acknowledgement

BloodConnect was developed as an academic project to demonstrate practical implementation of:

* ASP.NET Core MVC
* Entity Framework Core
* SQL Server
* ASP.NET Core Identity
* REST APIs
* Database design
* Authentication & authorization
* Business logic
* Responsive UI development
* Caching and performance optimization

> **BloodConnect — Connecting donors. Saving lives. 🩸❤️**
