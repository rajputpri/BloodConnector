# 🚀 Deployment Guide — BloodConnect

Step-by-step deployment to **MonsterASP.NET** (free tier).

**Live URL:** https://bloodconnector.runasp.net

---

## 📋 Prerequisites

- GitHub account with repository
- MonsterASP.NET account (free)
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
4. **Runtime:** .NET 10
5. **Datacenter:** EU (fastest for India)
6. **Application:** **"My own application"** (NOT the demo)
7. **Create**

**Your URL:** `http://<name>.runasp.net`

---

## Step 3: Create SQL Database

1. **Databases** → **Create Database**
2. **Type:** SQL Server 2025
3. **Name:** `BloodConnectDb`
4. **Collation:** `SQL_Latin1_General_CP1_CI_AS` (default)
5. **Plan:** Free
6. **Create**

**Note these details:**
- Server: `dbXXXXX.databaseasp.net`
- Database: `dbXXXXX`
- Username: `dbXXXXX`
- Password: `<generated>`

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

Add to `.gitignore`:
```
appsettings.Production.json
```

---

## Step 5: Update Program.cs

Two changes for production compatibility:

**1. Swagger always on:**
```csharp
// Replace the dev-only block with unconditional:
app.UseSwagger();
app.UseSwaggerUI(c =>
{
    c.SwaggerEndpoint("/swagger/v1/swagger.json", "BloodConnect API v1");
    c.RoutePrefix = "swagger";
});
```

**2. HTTPS redirect dev-only:**
```csharp
if (app.Environment.IsDevelopment())
    app.UseHttpsRedirection();
```

---

## Step 6: Push to GitHub

```bash
git add .
git commit -m "chore: production-ready config"
git push origin main
```

---

## Step 7: Enable Git Deployment

1. MonsterASP → **Websites** → **Manage** your site
2. Left sidebar → **Git deploy**
3. **Repository URL:** `https://github.com/YOUR_USER/BloodConnect.git`
4. **Branch:** `main` (click Load)
5. **Deployment Type:** **Build .NET app**
6. **Enable Git deploy**
7. **Build & publish** (2-5 minutes)

---

## Step 8: Upload Production Config

The `appsettings.Production.json` file is NOT in GitHub. Upload manually:

1. Website → Manage → **WebFTP**
2. Login with FTP credentials (from FTP section)
3. Navigate to `/wwwroot`
4. **Upload** `appsettings.Production.json`

---

## Step 9: Restart & Test

1. Website → Manage → **Restart**
2. Wait 30 seconds
3. Open: `https://your-site.runasp.net`

**Expected:** Homepage loads with database data.

---

## Step 10: Enable HTTPS

1. Website → Manage → **HTTPS**
2. **Issue free certificate** (Let's Encrypt)
3. Wait 1-2 minutes
4. Test: `https://your-site.runasp.net` 🔒

---

## 🐛 Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| `500.30` | App failed to start | Check connection string in `appsettings.Production.json` |
| `500.31` | .NET runtime missing | Select correct .NET version in panel |
| `404` on all routes | Wrong deployment folder | Verify publish output is in `/wwwroot` |
| DB connection fails | Wrong credentials | Verify SQL credentials in panel |
| Build fails | Package restore issue | Check `dotnet build` locally first |

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

**Or** — if using WebDeploy — setup auto-deploy via GitHub Actions (advanced).

---

## 📊 Post-Deployment Checklist

- [ ] Homepage loads without errors
- [ ] CSS/JS assets load (no 404 in DevTools)
- [ ] Database connection works (see donors on `/Donor`)
- [ ] Login works (`/Account/Login`)
- [ ] Swagger loads (`/swagger`)
- [ ] API responds (`/api/donor`)
- [ ] HTTPS certificate active (green lock)
- [ ] Admin panel accessible

---

## 🎓 Viva Notes

**Deployment architecture:**

```
GitHub Repo → MonsterASP Build Server → Staging Area → /wwwroot → Live Site
                    ↑
              dotnet publish -c Release
```

**Security:**
- Production connection string kept out of version control
- HTTPS enforced via Let's Encrypt
- Environment-specific config via `appsettings.Production.json`

---

**Last Updated:** October 2026