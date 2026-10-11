# 📡 API Reference — BloodConnect

Complete REST API documentation for the BloodConnect platform.

**Base URL (Live):** `https://bloodconnector.runasp.net`  
**Base URL (Local):** `http://localhost:5006`  
**Swagger UI:** [/swagger](https://bloodconnector.runasp.net/swagger)

---

## 🔐 Authentication

- **Public endpoints** (`GET`) — no authentication required
- **Protected endpoints** (`POST`, `PUT`, `DELETE`) — cookie-based auth required
- Login via `/Account/Login` before calling protected endpoints
- Banned users automatically signed out on next request

---

## 📋 Endpoints

### Donor APIs

#### `GET /api/donor`

List all donors with filters and pagination.

**Query Parameters:**

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `bloodGroup` | string | — | Filter by blood group (e.g., `A+`) |
| `state` | string | — | Filter by Indian state |
| `available` | bool | — | Filter by availability |
| `page` | int | 1 | Page number |
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

#### `GET /api/donor/{id}`

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

---

#### `GET /api/donor/search`

Blood compatibility-aware search.

**Query Parameters:**

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `bloodGroup` | string | — | Target blood group |
| `exactMatch` | bool | false | Exact match only (vs compatible) |
| `state` | string | — | Filter by state |
| `page` | int | 1 | Page number |
| `pageSize` | int | 20 | Page size |

**Example:**
```bash
GET /api/donor/search?bloodGroup=B%2B&exactMatch=false
```

**Response:** `200 OK`
```json
{
  "total": 2,
  "searchMode": "compatible",
  "requestedBloodGroup": "B+",
  "compatibleGroups": ["O-", "O+", "B-", "B+"],
  "results": [...]
}
```

---

#### `POST /api/donor` 🔒

Create a new donor profile. **Requires authentication.**

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

| Status | Meaning |
|--------|---------|
| `201 Created` | Donor created |
| `400 Bad Request` | Validation failed |
| `401 Unauthorized` | Not logged in |
| `409 Conflict` | User already has a donor profile |

---

#### `PUT /api/donor/{id}` 🔒

Update donor profile. **Requires ownership or admin role.**

**Request Body:** Same as POST.

**Responses:** `200 OK`, `400`, `401`, `403`, `404`

---

#### `DELETE /api/donor/{id}` 🔒

Delete donor profile. **Requires ownership or admin role.**

**Response:** `204 No Content`

---

### Blood Request APIs

Same pattern as Donor APIs:

| Method | Endpoint | Auth |
|--------|----------|------|
| `GET` | `/api/bloodrequest` | Public |
| `GET` | `/api/bloodrequest/{id}` | Public |
| `POST` | `/api/bloodrequest` | 🔒 Auth |
| `PUT` | `/api/bloodrequest/{id}` | 🔒 Owner/Admin |
| `DELETE` | `/api/bloodrequest/{id}` | 🔒 Owner/Admin |

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

---

## 🧪 Testing with Postman

Import our Postman collection for one-click testing:

**Collection:** [`docs/postman/BloodConnect.postman_collection.json`](postman/BloodConnect.postman_collection.json)

**Environment Variables:**
- `baseUrl` = `https://bloodconnector.runasp.net`

---

## 🎓 Notes

- All responses are JSON
- Content-Type: `application/json; charset=utf-8`
- Timezone: UTC (dates in ISO 8601)
- Pagination: 1-based
- Max page size: 100

---

**Last Updated:** October 2026