# 👤 User Manual — BloodConnect

Complete guide for using the BloodConnect platform.

---

## 📖 Table of Contents

- [Getting Started](#-getting-started)
- [Becoming a Donor](#-becoming-a-donor)
- [Finding Donors](#-finding-donors)
- [Posting a Blood Request](#-posting-a-blood-request)
- [Pledging to Donate](#-pledging-to-donate)
- [Real-Time Notifications](#-real-time-notifications)
- [Personal Dashboard](#-personal-dashboard)
- [Features Overview](#-features-overview)
- [FAQ](#-faq)

---

## 🚀 Getting Started

**Live URL:** https://bloodconnector.runasp.net

### 1. Create an Account

1. Click **"Register"** in the top navigation
2. Fill in:
   - Full Name
   - Email
   - Password (min 6 chars, 1 digit)
   - Confirm Password
   - ✓ Accept terms
3. Click **Register**
4. You'll be logged in automatically
5. A **welcome splash** animation will greet you

### 2. Login (Existing Users)

1. Click **"Sign In"**
2. Enter email + password
3. Click **Sign In**

> [!NOTE]
> After 5 failed attempts, your account will be locked for 5 minutes.

---

## 🩸 Becoming a Donor

### Register as Donor

1. After login, click **"Become a Donor"** in the nav
2. Fill the form:
   - **Full Name**
   - **Age** (must be 18-65)
   - **Blood Group** (dropdown — 8 groups)
   - **State** (dropdown — 28 states + 8 UTs)
   - **City** (free text)
   - **Contact Number** (10 digits)
   - **Availability** toggle
3. Click **Register**

Your profile is created. A **success toast** confirms the action. Now you can pledge on requests.

> [!IMPORTANT]
> One donor profile per user account. Edit anytime from your dashboard.

---

## 🔍 Finding Donors

### Search by Blood Group

1. Go to **Donors** page
2. Select blood group from dropdown
3. Optionally filter by state
4. Click **Search**

**Tip:** The system shows **compatible donors**, not just exact matches.

**Example:** Searching for **B+** donors shows: O−, O+, B−, B+ — because these groups are all medically compatible.

### Exact Match Only

Check **"Exact match only"** checkbox to filter strictly — shows only the requested group.

---

## 📋 Posting a Blood Request

1. Go to **Blood Requests** → **Post Request**
2. Fill the form:
   - **Requester Name**
   - **Blood Group Needed**
   - **State + City**
   - **Contact Number**
   - **Urgency Level** (Low / Medium / High / Critical)
3. Click **Create Request**

**What happens next:**

- Your request is **visible to compatible donors**
- **All admins receive a real-time notification** (bell badge + toast + sound)
- A **success toast** confirms creation

---

## 🤝 Pledging to Donate

### As a Donor

1. Browse **Blood Requests**
2. Find a request where your blood group is compatible
3. Click **"I can donate"**
4. Your offer is registered with status **Pledged**

**What happens next:**

- **Request owner receives a real-time notification** 🔔
- Badge appears on their bell icon
- Toast popup with your name and blood group

### As a Request Owner

1. Go to **My Requests** → Click on your request
2. Click **"View Offers"**
3. Review all pledges from donors
4. Click **Accept** on the best one
   - Others auto-rejected
   - Contact info revealed
   - **Donor receives a real-time notification** 🔔

### Completing Donation

Once donation is done:

1. Either party (owner or accepted donor) clicks **Mark Complete**
2. Request status → **Fulfilled**
3. Both parties get confirmation
4. **Donor receives a completion notification**

---

## 🔔 Real-Time Notifications

BloodConnect's **signature feature** — instant alerts without page refresh.

### What You'll See

**1. Bell Icon 🔔**

- Located in the top navigation bar
- Red badge shows count of new notifications
- Animates with a ring effect on new notification

**2. Toast Popup**

- Slides in from top-right
- Shows title + description
- Auto-dismisses after 7 seconds
- Click to navigate to the relevant page

**3. Sound Chime**

- WhatsApp-style two-tone chime
- Plays on every new notification
- Can be toggled on/off (see below)

### What Triggers Notifications

**For Users (Request Owners):**
- ✅ Donor pledges on your request
- ✅ Donor accepts/rejects your offer
- ✅ Donation completed

**For Admins:**
- ✅ New blood request posted
- ✅ New contact message received

**For Donors:**
- ✅ Your offer is accepted
- ✅ Your offer is rejected
- ✅ Donation marked complete

### Sound Toggle

Look for the **🔊 sound icon** in the navbar. Click to toggle sound on/off. Preference is saved in `localStorage` — persists across sessions.

### Notification Dropdown

Click the bell icon to open the dropdown:

- **Recent items** — up to 8 latest notifications
- **Icon-coded** — 🩸 request, ✉ message, 🤝 offer, ✓ status
- **Relative time** — "Just now", "2 hours ago"
- **Click any item** — navigates to the relevant page
- **"All caught up"** — shown when no new notifications

---

## 📊 Personal Dashboard

Click your **name** in the nav → **Dashboard**

You'll see:

- **Profile summary** — name, email, role, join date
- **Donor profile status** — blood group, location, availability
- **4 stat cards** — Requests Posted, Active, Donations Made, Blood Group
- **My Requests** — all requests you posted
- **My Offers** — all pledges you made as a donor
- **My Donations** — all requests you fulfilled

---

## 🎨 Features Overview

| Feature | Where |
|---------|-------|
| Sound toggle | Navbar (🔊 icon) |
| Bell icon (notifications) | Navbar (right side) |
| Search donors | `/Donor` |
| Post request | `/BloodRequest/Create` |
| View all requests | `/BloodRequest` |
| Dashboard | `/Dashboard` |
| Contact support | `/Home/Contact` |
| FAQ | `/Home/Faq` |
| Logout | User dropdown → Sign Out |

---

## ❓ FAQ

**Q: Can I edit my donor profile?**  
A: Yes — only you can edit your own profile. Admins cannot modify personal info.

**Q: Can I have multiple donor profiles?**  
A: No — one profile per user account.

**Q: How is compatibility calculated?**  
A: Based on standard red cell compatibility. O− is universal donor, AB+ is universal receiver.

**Q: Is my contact number public?**  
A: No — hidden in public listings. Revealed only after both parties agree to a match.

**Q: What if I want to cancel a pledge?**  
A: Before acceptance, you can cancel. After acceptance, contact the owner.

**Q: How do I turn off notification sound?**  
A: Click the 🔊 icon in the navbar. Preference is saved automatically.

**Q: Why did I get a notification?**  
A: Someone pledged on your request, accepted your offer, or posted a new request (if you're admin). Check the bell icon for details.

**Q: Notifications not showing?**  
A: Ensure JavaScript is enabled. Check browser console for `✅ SignalR connected`. If not, refresh the page.

**Q: Do I need to keep the page open to receive notifications?**  
A: Yes — SignalR connection is per-browser-tab. Notifications arrive while the page is open.

**Q: Are notifications stored?**  
A: Only the last 8 items per user are shown in the dropdown. Full activity is visible in your dashboard.

**Q: Can I get email notifications?**  
A: Not yet — email/SMS notifications are in the roadmap.

---

## 📞 Support

- **Contact Form:** [/Home/Contact](/Home/Contact)
- **FAQ:** [/Home/Faq](/Home/Faq)
- **GitHub Issues:** [github.com/rajputpri/BloodConnector/issues](https://github.com/rajputpri/BloodConnector/issues)

---

**Last Updated:** October 2026