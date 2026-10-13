# 🚀 Deployment Guide — BloodConnect

Step-by-step deployment to **MonsterASP.NET** (free tier).

**Live URL:** https://bloodconnector.runasp.net

---

## 📖 Table of Contents

- [Prerequisites](#-prerequisites)
- [Step 1: Create MonsterASP Account](#step-1-create-monsterasp-account)
- [Step 2: Create Website](#step-2-create-website)
- [Step 3: Create SQL Database](#step-3-create-sql-database)
- [Step 4: Prepare Production Config](#step-4-prepare-production-config)
- [Step 5: Update Program.cs](#step-5-update-programcs)
- [Step 6: Push to GitHub](#step-6-push-to-github)
- [Step 7: Enable Git Deployment](#step-7-enable-git-deployment)
- [Step 8: Upload Production Config](#step-8-upload-production-config)
- [Step 9: Restart & Test](#step-9-restart--test)
- [Step 10: Enable HTTPS](#step-10-enable-https)
- [Troubleshooting](#-troubleshooting)
- [Updating Deployed Site](#-updating-deployed-site)
- [Post-Deployment Checklist](#-post-deployment-checklist)

---

## 📋 Prerequisites

- GitHub account with repository
- MonsterASP.NET account (free)
- .NET 10 SDK locally
- ~30 minutes

---

## Step 1: Create MonsterASP Account

1. Go to [monsterasp.net](https://www.monsterasp.net/)
2. Sign up with email
3. Verify email

---

## Step 2: Create Website

1. Login to admin panel
2. **Websites** → **Create Website**
3. **Name:** `bloodconnector` (or your choice)
4. **Runtime:** `.NET 10`
5. **Datacenter:** **EU** (fastest for India — ~128ms latency)
6. **Application:** **"My own application"** (NOT the demo)
7. **Create**

**Your URL:** `http://<name>.runasp.net`

---

## Step 3: Create SQL Database

1. **Databases** → **Create Database**
2. **Type:** SQL Server 2025
3. **Name:** `BloodConnectDb`
4. **Collation:** `SQL_Latin1_General_CP1_CI_AS` (default — do not change)
5. **Plan:** Free
6. **Create**

**Note these details:**

| Field | Example |
|-------|---------|
| Server | `dbXXXXX.databaseasp.net` |
| Database | `dbXXXXX` |
| Username | `dbXXXXX` |
| Password | `<generated>` (one-time display — save now!) |
| Port | 1433 |

> [!IMPORTANT]
> Password is shown **only once**. Save it immediately.

---

## Step 4: Prepare Production Config

Create `appsettings.Production.json` **locally** (do NOT commit):

```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Server=dbXXXXX.databaseasp.net;Database=dbXXXXX;User Id=dbXXXXX;Password=YOUR_PASSWORD;Encrypt=False;MultipleActiveResultSets=True;TrustServerCertificate=True"
  },
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft.AspNetCore": "Warning"
    }
  },
  "AllowedHosts": "*"
}
```

**Add to `.gitignore`:**

```gitignore
appsettings.Production.json
```

**Create this file via PowerShell:**

```powershell
@'
{
  "ConnectionStrings": {
    "DefaultConnection": "Server=dbXXXXX.databaseasp.net;Database=dbXXXXX;User Id=dbXXXXX;Password=YOUR_ACTUAL_PASSWORD;Encrypt=False;MultipleActiveResultSets=True;TrustServerCertificate=True"
  },
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft.AspNetCore": "Warning"
    }
  },
  "AllowedHosts": "*"
}
'@ | Out-File -FilePath appsettings.Production.json -Encoding utf8
```

---

## Step 5: Update Program.cs

Three changes for production compatibility:

### 1. Swagger always on

```csharp
// Replace the dev-only block with unconditional:
app.UseSwagger();
app.UseSwaggerUI(c =>
{
    c.SwaggerEndpoint("/swagger/v1/swagger.json", "BloodConnect API v1");
    c.RoutePrefix = "swagger";
    c.DocumentTitle = "BloodConnect API Docs";
});
```

### 2. HTTPS redirect dev-only

```csharp
if (app.Environment.IsDevelopment())
    app.UseHttpsRedirection();
```

### 3. API status codes preserved

```csharp
app.UseStatusCodePages(async context =>
{
    var request = context.HttpContext.Request;
    var response = context.HttpContext.Response;

    if (request.Path.StartsWithSegments("/api"))
    {
        response.ContentType = "application/json";
        await response.WriteAsync(
            $"{{\"error\":\"HTTP {response.StatusCode}\",\"statusCode\":{response.StatusCode}}}");
        return;
    }

    if (response.StatusCode >= 400)
    {
        var originalPath = request.Path;
        var originalMethod = request.Method;
        request.Path = "/Home/Error";
        request.Method = "GET";
        request.QueryString = new QueryString($"?code={response.StatusCode}");
        await context.Next(context.HttpContext);
        request.Path = originalPath;
        request.Method = originalMethod;
    }
});
```

### 4. SignalR Hub registration

```csharp
// Add in services
builder.Services.AddSignalR();

// Add after UseAuthorization, before MapControllerRoute
app.MapHub<NotificationHub>("/hubs/notifications");
```

---

## Step 6: Push to GitHub

```bash
git add .
git commit -m "chore: production-ready config with SignalR notifications"
git push origin main
```

---

## Step 7: Enable Git Deployment

1. MonsterASP → **Websites** → **Manage** your site
2. Left sidebar → **Git deploy**
3. **Repository URL:** `https://github.com/YOUR_USER/BloodConnector.git`
4. **Branch:** `main` (click Load to verify)
5. **Deployment Type:** **"Build .NET app"**
6. **Enable Git deploy**
7. **Build & publish** (2-5 minutes)

**What happens behind the scenes:**

```text
GitHub repo
    │
    │ git clone
    ▼
Staging area (D:\Deploy\siteXXXXX\source)
    │
    │ dotnet publish -c Release
    ▼
Published output (D:\Deploy\siteXXXXX\publish)
    │
    │ app_offline + copy
    ▼
Live site (/wwwroot)
```

---

## Step 8: Upload Production Config

The `appsettings.Production.json` is NOT in GitHub. Upload manually:

1. Website → Manage → **WebFTP** (or use `https://webftp.monsterasp.net`)
2. Login with FTP credentials (from FTP section in Manage)
3. Navigate to `/wwwroot`
4. **Upload** `appsettings.Production.json`

**Alternative: Protected Files**

In Git deploy page, use **"Protected Files"** section:

```
appsettings.Production.json
App_Data/
uploads/
```

This ensures future deploys never overwrite this file.

---

## Step 9: Restart & Test

1. Website → Manage → **Restart**
2. Wait 30 seconds (app cold-start)
3. Open: `https://your-site.runasp.net`

**Expected:**

- Homepage loads with database data
- Bell icon visible in navbar (after login)
- Real-time notifications work

**Test SignalR:**

1. Chrome tab 1: Login as admin
2. Chrome tab 2: Login as normal user → post request
3. Tab 1: Should receive **toast + sound + bell badge** instantly ⚡

---

## Step 10: Enable HTTPS

1. Website → Manage → **HTTPS** or **SSL certificates**
2. **Issue free certificate** (Let's Encrypt)
3. Wait 1-2 minutes
4. Test: `https://your-site.runasp.net` 🔒

**SignalR will automatically use `wss://`** (WebSocket Secure) — no code change needed.

---

## 🐛 Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| `500.30` | App failed to start | Check connection string in `appsettings.Production.json` |
| `500.31` | .NET runtime missing | Select correct .NET version in panel (10.x) |
| `404` on all routes | Wrong deployment folder | Verify publish output is in `/wwwroot` |
| DB connection fails | Wrong credentials | Verify SQL credentials — remember DB name is `dbXXXXX` not `BloodConnectDb` |
| Build fails | Package restore issue | Check `dotnet build` locally first |
| Swagger 404 in prod | Dev-only guard | Ensure Swagger is not inside `if (IsDevelopment())` |
| SignalR fails to connect | Auth or transport | Check browser console — should show `✅ SignalR connected` |
| Bell icon missing | Not logged in | Bell only shows for authenticated users |
| 401 on API | Missing cookie | Call `/api/auth/login` first |
| 400 instead of 401 | Old `UseStatusCodePagesWithReExecute` | Use custom `UseStatusCodePages` for API |

---

## 🔄 Updating Deployed Site

**When you make code changes:**

```bash
git add .
git commit -m "feat: your change"
git push origin main
```

Then in MonsterASP:

1. **Git deploy** → **Pull latest**
2. **Build & publish**

**Deploy takes 2-5 minutes.**

### Zero-downtime deploy

MonsterASP automatically puts the site into **app_offline mode** during the copy step:

```text
1. Build in staging
2. Create app_offline.htm (users see "maintenance" page)
3. Copy new files to /wwwroot
4. Delete app_offline.htm
5. App restarts
```

**Downtime:** ~5-10 seconds.

### Auto-deploy via GitHub Actions (Advanced)

You can configure GitHub Actions to hit the MonsterASP deploy webhook on every push. Not covered in this guide.

---

## 📊 Post-Deployment Checklist

- [ ] Homepage loads without errors
- [ ] CSS/JS assets load (no 404 in DevTools)
- [ ] Database connection works (see donors on `/Donor`)
- [ ] Login works (`/Account/Login`)
- [ ] Swagger loads (`/swagger`)
- [ ] API responds (`/api/donor`)
- [ ] Auth API works (`/api/auth/login` returns 200)
- [ ] HTTPS certificate active (green lock)
- [ ] Admin panel accessible (`/Admin`)
- [ ] **SignalR connects** (browser console: `✅ SignalR connected`)
- [ ] **Bell icon visible** in navbar (after login)
- [ ] **Real-time notification test** — 2 browser tabs, admin gets instant alert

---

## 🔐 Production Security Checklist

- [ ] `appsettings.Production.json` NOT in Git
- [ ] Default admin password changed
- [ ] HTTPS enabled with valid certificate
- [ ] Database credentials stored securely
- [ ] Backups configured (MonsterASP → Backups)
- [ ] Error pages don't leak stack traces
- [ ] Seeded test data removed (optional)

---

## 🎓 Viva Notes

**Deployment architecture:**

```text
GitHub Repo
    │
    │ git push
    ▼
MonsterASP Build Server
    │
    │ git clone
    │ dotnet publish -c Release
    ▼
Staging Area
    │
    │ app_offline + copy
    ▼
/wwwroot (Live Site)
    │
    │ app restart
    ▼
https://bloodconnector.runasp.net
```

**Security:**

- Production connection string kept out of version control
- HTTPS enforced via Let's Encrypt
- Environment-specific config via `appsettings.Production.json`
- SignalR automatically upgrades to WSS (WebSocket Secure)

**Performance:**

- EF Core `EnableRetryOnFailure` handles transient DB errors
- SignalR uses WebSocket (not long-polling) for lowest latency
- Static assets served with cache-busting via `asp-append-version`

---

**Last Updated:** October 2026