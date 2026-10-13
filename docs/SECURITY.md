# 🔐 Security Model — BloodConnect

Honest documentation of what we protect against, what we don't, and why.

---

## 📖 Table of Contents

- [What We Protect](#-what-we-protect)
- [Real-Time Security](#-real-time-security)
- [What We Do NOT Protect Against](#-what-we-do-not-protect-against)
- [Threat Model](#-threat-model)
- [Security Configuration Reference](#-security-configuration-reference)
- [Reporting Vulnerabilities](#-reporting-vulnerabilities)

---

## 🛡 What We Protect

### 1. Authentication

| Layer | Implementation |
|-------|----------------|
| Password Storage | ASP.NET Core Identity (PBKDF2, 10,000 iterations, salted) |
| Session | Cookie-based, `HttpOnly`, `SameSite=Lax`, 7-day sliding |
| Lockout | 5 failed attempts → 5-minute lockout |
| Ban Check | Validated on **every request** via `OnValidatePrincipal` |
| API Login | Dedicated `/api/auth/login` endpoint (JSON-based) |

### 2. Authorization

- Role-based access control (SuperAdmin > Admin > User)
- Ownership checks on all edit/delete actions
- Self-protection rules (can't ban/demote self)
- SuperAdmin immutability (cannot be banned/demoted/deleted)
- API-specific authorization — `[Authorize]` with JSON 401 response

### 3. CSRF Protection

- Global `AutoValidateAntiforgeryTokenAttribute`
- Every form post validated
- API endpoints explicitly exempted via `[IgnoreAntiforgeryToken]`

### 4. Data Privacy

- **Contact numbers** hidden in public API list views
- Only revealed after mutual offer acceptance
- DTO pattern prevents entity leakage
- SignalR payloads contain no sensitive data (only IDs + display text)

### 5. Input Validation

- Server-side validation via DataAnnotations
- Custom `MustBeTrueAttribute` for terms acceptance
- State dropdown (dropdown prevents free-text injection)
- Blood group regex validation (`^(A|B|AB|O)[+-]$`)
- Contact number regex (`^[0-9]{10}$`)
- SQL injection prevented by EF Core parameterized queries
- XSS prevention via Razor auto-escaping + `textContent` on client

### 6. Concurrency

- `[Timestamp]` RowVersion on `Donor` entity
- Prevents lost updates in multi-user scenarios
- Unique `(RequestId, DonorId)` index prevents duplicate pledges

### 7. Real-Time Communication

- **SignalR over WebSocket** — TLS encrypted in production
- **Authentication required** — hub has `[Authorize]` attribute
- **Group-based isolation** — users only receive notifications for their own events
- **Automatic reconnection** — exponential backoff, no data loss

---

## 🔔 Real-Time Security

SignalR adds a new attack surface. Here's how we secure it.

### 1. Hub Authentication

```csharp
[Authorize]
public class NotificationHub : Hub
```

- Unauthenticated users **cannot connect** to the hub
- Connection uses the same auth cookie as the rest of the app
- Banned users cannot connect (cookie validation runs before hub access)

### 2. Group Isolation

Users are added to groups based on their identity:

| Group | Who Joins | Data Received |
|-------|-----------|---------------|
| `admins` | Admin + SuperAdmin roles only | Admin alerts (requests, messages) |
| `user_{userId}` | Individual user (by userId) | Personal alerts (offers, status) |

**Security property:** A user can **never** receive notifications from another user's group — the server controls all group membership.

### 3. Payload Sanitization

SignalR payloads contain **only**:
- `type` — notification category (request/message/offer/status)
- `title` — short display text
- `message` — brief description
- `url` — internal link
- `timestamp` — ISO 8601 UTC

**Never included:**
- ❌ User IDs
- ❌ Contact numbers
- ❌ Email addresses
- ❌ Database IDs (except in URLs the user is authorized to see)
- ❌ Raw entity objects

### 4. Client-Side XSS Prevention

All payload text is inserted via `textContent` or through escaped HTML:

```javascript
function escapeHtml(s) {
    const d = document.createElement('div');
    d.textContent = s == null ? '' : String(s);
    return d.innerHTML;
}
```

**Result:** Even if the server sent `<script>alert(1)</script>`, it displays as text — no execution.

### 5. Connection Limits

| Limit | Value | Reason |
|-------|-------|--------|
| Connections per user | Unlimited (dev) | Can have multiple tabs |
| Message size | Default (32 KB) | SignalR default |
| Reconnect attempts | 5 with backoff | Prevents hammering |

> [!NOTE]
> **Production recommendation:** Add per-user connection limits and rate-limit `SendAsync` calls. Not implemented in current version.

### 6. Transport Security

| Environment | Transport |
|-------------|-----------|
| Local development | `ws://localhost:5006` (plain WebSocket) |
| Production (MonsterASP) | `wss://bloodconnector.runasp.net` (TLS) |

**Fallback transports** (in order):
1. WebSockets (preferred — TLS encrypted)
2. Server-Sent Events
3. Long Polling

SignalR picks the best available transport automatically.

---

## ⚠️ What We Do NOT Protect Against

### 1. HTTPS on Free Tier

**Issue:** Free MonsterASP tier provides HTTP by default (HTTPS requires manual activation).

**Mitigation:** Let's Encrypt SSL enabled. Paid tier recommended for production.

### 2. Two-Factor Authentication

**Not implemented.** Users authenticate with password only.

**Roadmap:** TOTP-based 2FA planned.

### 3. Rate Limiting

**Not implemented** on API endpoints. Potential for abuse in production.

**Roadmap:** Consider `AspNetCoreRateLimit` middleware with:
- 60 requests/minute per IP
- 5 failed logins per minute per email
- SignalR connect limit: 5 per minute per user

### 4. Email Verification

**Not enforced.** Users can register without verifying email ownership.

**Roadmap:** Enable `RequireConfirmedEmail = true` in production.

### 5. Password Complexity

**Weak policy:** Minimum 6 chars + 1 digit. No uppercase/symbol required.

**Trade-off:** User convenience over security. Production apps should enforce stronger policies.

### 6. SignalR Abuse

**Not mitigated:**
- Client can open many tabs (each = a new SignalR connection)
- No message size limits beyond default
- No rate limit on incoming messages from client
- No connection throttling per IP

**Roadmap:** Add a `SignalRConnectionLimiter` middleware.

### 7. Server-Side Push Flooding

If a legitimate write operation triggers a push, but a malicious user triggers the write 1000x, all admins receive 1000 notifications.

**Roadmap:** Batch notifications per minute, or add a cooldown per source.

---

## 🎯 Threat Model

### In Scope

| Threat | Mitigation |
|--------|-----------|
| SQL Injection | EF Core parameterized queries |
| CSRF | Global antiforgery validation |
| XSS | Razor auto-escaping, `textContent` on client |
| Session Hijacking | HttpOnly + SameSite cookies |
| Unauthorized Access | Role-based `[Authorize]` checks |
| Fake Donors | Pledge-based two-way confirmation |
| SignalR Eavesdropping | WSS in production, group isolation |
| Notification Spoofing | Server-authoritative push (client cannot forge) |
| Duplicate Pledges | Unique DB index |

### Out of Scope

- Denial of Service (DoS)
- Advanced persistent threats (APT)
- Physical server security
- Legal compliance (HIPAA, GDPR-like regulations)
- Medical accuracy validation
- Network-level attacks (MITM, DNS poisoning)

---

## 📋 Security Configuration Reference

### Cookie Settings (`Program.cs`)

```csharp
builder.Services.ConfigureApplicationCookie(options =>
{
    options.LoginPath = "/Account/Login";
    options.ExpireTimeSpan = TimeSpan.FromDays(7);
    options.SlidingExpiration = true;
    options.Cookie.HttpOnly = true;
    options.Cookie.SameSite = SameSiteMode.Lax;

    // Ban check on every request
    options.Events.OnValidatePrincipal = async context => { /* ... */ };

    // API requests → JSON 401 instead of redirect
    options.Events.OnRedirectToLogin = context =>
    {
        if (context.Request.Path.StartsWithSegments("/api"))
        {
            context.Response.StatusCode = 401;
            context.Response.ContentType = "application/json";
            return context.Response.WriteAsync(
                "{\"error\":\"Unauthorized\",\"statusCode\":401}");
        }
        context.Response.Redirect(context.RedirectUri);
        return Task.CompletedTask;
    };
});
```

### Identity Settings

```csharp
builder.Services.AddIdentity<AppUser, IdentityRole>(options =>
{
    options.Password.RequireDigit = true;
    options.Password.RequiredLength = 6;
    options.Password.RequireNonAlphanumeric = false;
    options.Password.RequireUppercase = false;
    options.User.RequireUniqueEmail = true;
    options.Lockout.DefaultLockoutTimeSpan = TimeSpan.FromMinutes(5);
    options.Lockout.MaxFailedAccessAttempts = 5;
})
```

### SignalR Configuration

```csharp
// Hub
[Authorize]
public class NotificationHub : Hub
{
    public override async Task OnConnectedAsync()
    {
        var userId = Context.UserIdentifier;
        await Groups.AddToGroupAsync(Context.ConnectionId, $"user_{userId}");

        if (Context.User?.IsInRole("Admin") == true ||
            Context.User?.IsInRole("SuperAdmin") == true)
        {
            await Groups.AddToGroupAsync(Context.ConnectionId, "admins");
        }

        await base.OnConnectedAsync();
    }
}

// Program.cs
builder.Services.AddSignalR();
app.MapHub<NotificationHub>("/hubs/notifications");
```

### Client-Side Configuration

```javascript
const connection = new signalR.HubConnectionBuilder()
    .withUrl('/hubs/notifications')
    .withAutomaticReconnect([0, 2000, 5000, 10000, 30000])
    .configureLogging(signalR.LogLevel.Warning)
    .build();
```

---

## 🚨 Reporting Vulnerabilities

BloodConnect is an **educational project**. For security issues:

1. **Do NOT** open a public GitHub issue for sensitive vulnerabilities
2. Contact the repository owner via GitHub directly
3. Provide a clear description + steps to reproduce
4. Allow reasonable time for a fix before public disclosure

---

## 🎓 Viva Talking Points

> *"Sir, security ke liye maine multi-layer approach use ki:*
> - **Authentication:** ASP.NET Core Identity — passwords PBKDF2 se hashed hain
> - **CSRF:** Global `AutoValidateAntiforgeryToken`, API endpoints exempted
> - **Ban System:** Cookie validation har request pe via `OnValidatePrincipal`
> - **Privacy:** DTO pattern se contact number public API me null
> - **Concurrency:** RowVersion se optimistic locking
> - **Real-Time:** SignalR hub `[Authorize]` protected, group-based isolation, payload sanitization, XSS prevention via `textContent`"

**Yeh complete security story hai.** 🔥

---

**Last Updated:** October 2026