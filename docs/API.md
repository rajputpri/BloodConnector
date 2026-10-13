# 📡 API Reference — BloodConnect

Complete REST API documentation for the BloodConnect platform.

**Base URL (Live):** `https://bloodconnector.runasp.net`  
**Base URL (Local):** `http://localhost:5006`  
**Swagger UI:** [/swagger](https://bloodconnector.runasp.net/swagger)

---

## 📖 Table of Contents

- [Authentication Flow](#-authentication-flow)
- [Auth APIs](#-auth-apis)
- [Donor APIs](#-donor-apis)
- [Blood Request APIs](#-blood-request-apis)
- [Status Codes](#-status-codes)
- [Testing with Postman](#-testing-with-postman)
- [Rate Limiting](#-rate-limiting)

---

## 🔐 Authentication Flow

BloodConnect uses **cookie-based authentication** with ASP.NET Core Identity.

### The Flow

```text
┌────────────────────────────────────────────────────────────┐
│  Step 1: Login                                             │
│  POST /api/auth/login                                      │
│  Body: { email, password }                                 │
│  → 200 OK + Set-Cookie: .AspNetCore.Identity.Application   │
└────────────────────┬───────────────────────────────────────┘
                     │
                     ▼
┌────────────────────────────────────────────────────────────┐
│  Step 2: Cookie Automatically Attached                     │
│  Every subsequent request includes the cookie              │
│  → Protected endpoints now work                            │
└────────────────────┬───────────────────────────────────────┘
                     │
                     ▼
┌────────────────────────────────────────────────────────────┐
│  Step 3: Logout                                            │
│  POST /api/auth/logout                                     │
│  → 200 OK + Cookie cleared                                 │
└────────────────────────────────────────────────────────────┘
```

### Public vs Protected Endpoints

| Symbol | Meaning |
|:------:|---------|
| 🌐 | **Public** — no authentication required |
| 🔒 | **Protected** — cookie-based auth required |

### Key Notes

- **Cookie name:** `.AspNetCore.Identity.Application`
- **Expiry:** 7 days sliding
- **Ban check:** Every request validated via `OnValidatePrincipal` — banned users auto-signed out
- **CSRF:** API endpoints exempt via `[IgnoreAntiforgeryToken]`
- **401 response:** Clean JSON `{ "error": "Unauthorized", "statusCode": 401 }` — no redirect

---

## 🔐 Auth APIs

### `POST /api/auth/login` 🌐

Login with email + password. Returns cookie on success.

**Request Body:**

```json
{
  "email": "admin@bloodconnect.com",
  "password": "Admin@123"
}
```

**Responses:**

| Status | Meaning | Body |
|--------|---------|------|
| `200 OK` | Login successful | `{ "message": "Login successful.", "email": "...", "fullName": "..." }` |
| `400 Bad Request` | Validation failed | `{ "error": "Email and password are required." }` |
| `401 Unauthorized` | Invalid credentials | `{ "error": "Invalid credentials." }` |
| `423 Locked` | Account locked (5 failed attempts) | `{ "error": "Account locked. Try again in 5 minutes." }` |

**Cookie Set:** `.AspNetCore.Identity.Application` (7 days sliding, HttpOnly, SameSite=Lax)

**Example:**

```bash
curl -X POST https://bloodconnector.runasp.net/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@bloodconnect.com","password":"Admin@123"}' \
  -c cookies.txt
```

---

### `POST /api/auth/logout` 🔒

Logout current session. Clears the authentication cookie.

**Request Body:** None

**Responses:**

| Status | Meaning |
|--------|---------|
| `200 OK` | Logged out successfully |
| `401 Unauthorized` | Not logged in |

**Example:**

```bash
curl -X POST https://bloodconnector.runasp.net/api/auth/logout \
  -b cookies.txt
```

---

### `GET /api/auth/me` 🔒

Get current authenticated user's information and roles.

**Response:** `200 OK`

```json
{
  "email": "admin@bloodconnect.com",
  "fullName": "Administrator",
  "roles": ["SuperAdmin", "Admin"],
  "createdAt": "2026-10-03T14:38:28.9532452Z"
}
```

**Example:**

```bash
curl https://bloodconnector.runasp.net/api/auth/me \
  -b cookies.txt
```

---

## 🩸 Donor APIs

### `GET /api/donor` 🌐

List all donors with filters and pagination.

**Query Parameters:**

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `bloodGroup` | string | — | Filter by blood group (e.g., `A+`) |
| `state` | string | — | Filter by Indian state |
| `available` | bool | — | Filter by availability |
| `page` | int | 1 | Page number (1-based) |
| `pageSize` | int | 20 | Results per page (max 100) |

**Example:**

```bash
GET /api/donor?bloodGroup=B%2B&state=Maharashtra&page=1
```

**Response:** `200 OK`

```json
{
  "total": 4,
  "page": 1,
  "pageSize": 20,
  "items": [
    {
      "donorId": 15,
      "name": "Gaurav",
      "bloodGroup": "B+",
      "age": 45,
      "state": "Maharashtra",
      "city": null,
      "location": "Maharashtra",
      "isAvailable": true,
      "contactNumber": null
    }
  ]
}
```

> [!NOTE]
> `contactNumber` is `null` in list responses to protect privacy. It is only revealed in single-donor fetch when authenticated.

---

### `GET /api/donor/{id}` 🌐

Get a single donor by ID.

**Response:** `200 OK`

```json
{
  "donorId": 15,
  "name": "Gaurav",
  "bloodGroup": "B+",
  "age": 45,
  "state": "Maharashtra",
  "location": "Maharashtra",
  "isAvailable": true,
  "contactNumber": "9876543210"
}
```

**Response:** `404 Not Found`

```json
{
  "error": "Donor not found."
}
```

---

### `GET /api/donor/search` 🌐

Blood compatibility-aware search. Returns compatible donors based on medical red-cell compatibility matrix.

**Query Parameters:**

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `bloodGroup` | string | — | Target blood group |
| `exactMatch` | bool | false | If `true`, only exact blood group matches |
| `state` | string | — | Filter by Indian state |
| `location` | string | — | Case-insensitive location substring |
| `page` | int | 1 | Page number |
| `pageSize` | int | 20 | Page size (max 100) |

**Example:**

```bash
GET /api/donor/search?bloodGroup=B%2B&exactMatch=false
```

**Response:** `200 OK`

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
    },
    {
      "donorId": 2,
      "name": "Ravi Kumar",
      "bloodGroup": "O+",
      "state": "Gujarat",
      "location": "Gujarat",
      "isExactMatch": false
    }
  ]
}
```

**Compatibility Matrix (Red Cells):**

| Requested | Compatible Donors |
|-----------|-------------------|
| O− | O− |
| O+ | O−, O+ |
| A− | O−, A− |
| A+ | O−, O+, A−, A+ |
| B− | O−, B− |
| B+ | O−, O+, B−, B+ |
| AB− | O−, A−, B−, AB− |
| AB+ | All 8 groups |

---

### `POST /api/donor` 🔒

Create a new donor profile. **Requires authentication.**

**Rules:**
- One donor profile per user
- Age must be 18-65
- State must be a valid Indian state/UT
- Blood group must match regex `^(A|B|AB|O)[+-]$`

**Request Body:**

```json
{
  "name": "Test Donor",
  "age": 28,
  "bloodGroup": "O+",
  "state": "Gujarat",
  "city": "Surat",
  "contactNumber": "9876543210",
  "isAvailable": true
}
```

**Responses:**

| Status | Meaning | Body |
|--------|---------|------|
| `201 Created` | Donor created | Full donor object |
| `400 Bad Request` | Validation failed | `{ "error": "Invalid Indian state or union territory." }` |
| `401 Unauthorized` | Not logged in | `{ "error": "Unauthorized", "statusCode": 401 }` |
| `409 Conflict` | User already has a donor profile | `{ "error": "You already have a donor profile." }` |

**Location Header:** Points to `/api/donor/{newId}`

---

### `PUT /api/donor/{id}` 🔒

Update donor profile. **Requires ownership or admin role.**

**Request Body:** Same as POST.

**Responses:** `200 OK`, `400`, `401`, `403`, `404`

**Authorization:**

| Role | Can Update |
|------|-----------|
| Owner | ✅ Own profile |
| Admin | ✅ Any profile |
| Other User | ❌ 403 Forbidden |

---

### `DELETE /api/donor/{id}` 🔒

Delete donor profile. **Requires ownership or admin role.**

**Response:** `204 No Content`

**Authorization:**

| Role | Can Delete |
|------|-----------|
| Owner | ✅ Own profile |
| Admin | ✅ Any profile |
| SuperAdmin | ✅ Any profile |
| Other User | ❌ 403 Forbidden |

---

## 📋 Blood Request APIs

Same pattern as Donor APIs.

### Endpoints

| Method | Endpoint | Auth |
|--------|----------|------|
| `GET` | `/api/bloodrequest` | 🌐 Public |
| `GET` | `/api/bloodrequest/{id}` | 🌐 Public |
| `POST` | `/api/bloodrequest` | 🔒 Auth |
| `PUT` | `/api/bloodrequest/{id}` | 🔒 Owner/Admin |
| `DELETE` | `/api/bloodrequest/{id}` | 🔒 Owner/Admin |

### `GET /api/bloodrequest`

**Query Parameters:**

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `bloodGroup` | string | — | Filter by blood group needed |
| `urgency` | string | — | `Low` / `Medium` / `High` / `Critical` |
| `status` | string | — | `Open` / `Fulfilled` |
| `page` | int | 1 | Page number |
| `pageSize` | int | 20 | Page size |

**Response:** `200 OK`

```json
{
  "total": 4,
  "page": 1,
  "pageSize": 20,
  "items": [
    {
      "requestId": 5,
      "requesterName": "Rahul Sharma",
      "bloodGroupNeeded": "A+",
      "state": "Maharashtra",
      "city": "Mumbai",
      "location": "Mumbai, Maharashtra",
      "urgencyLevel": "Critical",
      "status": "Open",
      "requestDate": "2026-10-12T10:23:45Z",
      "contactNumber": null
    }
  ]
}
```

### `POST /api/bloodrequest` 🔒

**Request Body:**

```json
{
  "requesterName": "Rahul Sharma",
  "bloodGroupNeeded": "A+",
  "state": "Maharashtra",
  "city": "Mumbai",
  "contactNumber": "9876543210",
  "urgencyLevel": "Critical"
}
```

**Responses:** `201 Created`, `400`, `401`

> [!TIP]
> Creating a blood request **automatically pushes a real-time SignalR notification** to all admins (bell badge + toast + sound).

---

## 📊 Status Codes

| Code | Meaning | When |
|------|---------|------|
| `200` | OK | Successful GET/PUT |
| `201` | Created | Successful POST |
| `204` | No Content | Successful DELETE |
| `400` | Bad Request | Validation failure |
| `401` | Unauthorized | Missing auth cookie |
| `403` | Forbidden | Not owner/admin |
| `404` | Not Found | Resource missing |
| `409` | Conflict | Duplicate record |
| `423` | Locked | Account locked after failed attempts |
| `500` | Server Error | Unhandled exception (logged) |

---

## 🧪 Testing with Postman

### Import Collection

**Collection:** [`docs/postman/BloodConnect.postman_collection.json`](postman/BloodConnect.postman_collection.json)

### Environment Variables

| Variable | Value |
|----------|-------|
| `baseUrl` | `https://bloodconnector.runasp.net` |

### Testing Sequence

**Step 1: Public APIs (no auth)**
```
GET {{baseUrl}}/api/donor
GET {{baseUrl}}/api/donor/3
GET {{baseUrl}}/api/donor/search?bloodGroup=B%2B
GET {{baseUrl}}/api/bloodrequest
```

**Step 2: Login (get cookie)**
```
POST {{baseUrl}}/api/auth/login
Body: { "email": "admin@bloodconnect.com", "password": "Admin@123" }
→ Cookie auto-saved
```

**Step 3: Authenticated requests**
```
GET {{baseUrl}}/api/auth/me
POST {{baseUrl}}/api/donor  (create)
```

**Step 4: Logout (test 401)**
```
POST {{baseUrl}}/api/auth/logout
POST {{baseUrl}}/api/donor
→ 401 Unauthorized
```

---

## 🚦 Rate Limiting

> [!WARNING]
> **Not implemented yet.** API endpoints currently have no rate limiting. See [SECURITY.md](SECURITY.md#3-rate-limiting) for roadmap.

**Planned:**

- 60 requests/minute per IP
- 5 failed login attempts → 5-minute lockout (already active)
- SignalR connection limit per user

---

## 🎓 Notes

- All responses are JSON with `Content-Type: application/json; charset=utf-8`
- Timezone: UTC (dates in ISO 8601 format)
- Pagination: 1-based (`page=1` is first page)
- Max page size: 100
- All write operations push real-time SignalR notifications to relevant parties
- Cookie handling: use `-c cookies.txt` / `-b cookies.txt` with curl

---

**Last Updated:** October 2026