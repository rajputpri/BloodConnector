# 🔐 Security Model — BloodConnect

Honest documentation of what we protect against, what we don't, and why.

---

## 🛡 What We Protect

### 1. Authentication

| Layer | Implementation |
|-------|----------------|
| Password Storage | ASP.NET Core Identity (PBKDF2, 10,000 iterations, salted) |
| Session | Cookie-based, `HttpOnly`, `SameSite=Lax`, 7-day sliding |
| Lockout | 5 failed attempts → 5-minute lockout |
| Ban Check | Validated on **every request** via `OnValidatePrincipal` |

### 2. Authorization

- Role-based access control (SuperAdmin > Admin > User)
- Ownership checks on all edit/delete actions
- Self-protection rules (can't ban/demote self)
- SuperAdmin immutability (cannot be banned/demoted/deleted)

### 3. CSRF Protection

- Global `AutoValidateAntiforgeryTokenAttribute`
- Every form post validated
- API endpoints explicitly exempted via `[IgnoreAntiforgeryToken]`

### 4. Data Privacy

- **Contact numbers** hidden in public API list views
- Only revealed after mutual offer acceptance
- DTO pattern prevents entity leakage

### 5. Input Validation

- Server-side validation via DataAnnotations
- Custom `MustBeTrueAttribute` for terms acceptance
- State dropdown (dropdown prevents free-text injection)
- SQL injection prevented by EF Core parameterized queries

### 6. Concurrency

- `[Timestamp]` RowVersion on `Donor` entity
- Prevents lost updates in multi-user scenarios

---

## ⚠️ What We Do NOT Protect Against

### 1. HTTPS on Free Tier

**Issue:** Free MonsterASP tier provides HTTP by default (HTTPS available but requires manual activation).

**Mitigation:** Let's Encrypt SSL enabled. Paid tier recommended for production.

### 2. Two-Factor Authentication

**Not implemented.** Users authenticate with password only.

**Roadmap:** TOTP-based 2FA planned.

### 3. Rate Limiting

**Not implemented** on API endpoints. Potential for abuse in production.

**Roadmap:** Consider `AspNetCoreRateLimit` middleware.

### 4. Email Verification

**Not enforced.** Users can register without verifying email ownership.

**Roadmap:** Enable `RequireConfirmedEmail = true` in production.

### 5. Password Complexity

**Weak policy:** Minimum 6 chars + 1 digit. No uppercase/symbol required.

**Trade-off:** User convenience over security. Production apps should enforce stronger policies.

---

## 🎯 Threat Model

### In Scope

| Threat | Mitigation |
|--------|-----------|
| SQL Injection | EF Core parameterized queries |
| CSRF | Global antiforgery validation |
| XSS | Razor auto-escaping, no `Html.Raw` on user input |
| Session Hijacking | HttpOnly + SameSite cookies |
| Unauthorized Access | Role-based `[Authorize]` checks |
| Fake Donors | Pledge-based two-way confirmation |

### Out of Scope

- Denial of Service (DoS)
- Advanced persistent threats (APT)
- Physical server security
- Legal compliance (HIPAA, GDPR-like regulations)
- Medical accuracy validation

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
});
```

### Identity Settings

```csharp
builder.Services.AddIdentity<AppUser, IdentityRole>(options =>
{
    options.Password.RequireDigit = true;
    options.Password.RequiredLength = 6;
    options.Lockout.DefaultLockoutTimeSpan = TimeSpan.FromMinutes(5);
    options.Lockout.MaxFailedAccessAttempts = 5;
})
```

---

## 🚨 Reporting Vulnerabilities

For educational use only. For security issues, contact the repository owner via GitHub.

---

## 🎓 Viva Talking Points

> *"Sir, security ke liye maine ASP.NET Core Identity use ki — passwords PBKDF2 se hashed hain. CSRF protection globally enabled hai via AutoValidateAntiforgeryToken. Ban system cookie validation pe check karta hai har request pe. DTO pattern se sensitive fields (contact number) public API me hide hain. RowVersion se concurrency control hai."*

---

**Last Updated:** October 2026