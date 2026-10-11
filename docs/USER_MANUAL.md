# 👤 User Manual — BloodConnect

Complete guide for using the BloodConnect platform.

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

### 2. Login (Existing Users)

1. Click **"Sign In"**
2. Enter email + password
3. Click **Sign In**

---

## 🩸 Becoming a Donor

### Register as Donor

1. After login, click **"Become a Donor"** in the nav
2. Fill the form:
   - **Full Name**
   - **Age** (must be 18-65)
   - **Blood Group** (dropdown)
   - **State** (dropdown — 28 states + 8 UTs)
   - **City** (free text)
   - **Contact Number** (10 digits)
   - **Availability** toggle
3. Click **Register**

Your profile is created. Now you can pledge on requests.

---

## 🔍 Finding Donors

### Search by Blood Group

1. Go to **Donors** page
2. Select blood group from dropdown
3. Optionally filter by state
4. Click **Search**

**Tip:** The system shows **compatible donors**, not just exact matches.
- Searching for **B+** shows: O−, O+, B−, B+
- This is medical accuracy.

### Exact Match Only

Check **"Exact match only"** checkbox to filter strictly.

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

Your request is now visible to compatible donors.

---

## 🤝 Pledging to Donate

### As a Donor

1. Browse **Blood Requests**
2. Find a request where your blood group is compatible
3. Click **"I can donate"**
4. Your offer is registered with status **Pledged**

### As a Request Owner

1. Go to **My Requests** → Click on your request
2. Click **"View Offers"**
3. Review all pledges from donors
4. Click **Accept** on the best one
   - Others auto-rejected
   - Contact info revealed

### Completing Donation

Once donation is done:
1. Either party (owner or accepted donor) clicks **Mark Complete**
2. Request status → **Fulfilled**
3. Both parties get confirmation

---

## 📊 Personal Dashboard

Click your **name** in the nav → **Dashboard**

You'll see:
- Profile summary
- Donor profile status
- My Requests (posted)
- My Offers (pledged)
- My Donations (fulfilled)
- Real-time stats

---

## 🔔 Notification Badge

Admins see a **red badge** on "Messages" link showing **unread contact messages** count.

---

## 🎨 Features Overview

| Feature | Where |
|---------|-------|
| Sound toggle | Navbar (🔊 icon) |
| Search donors | `/Donor` |
| Post request | `/BloodRequest/Create` |
| View all requests | `/BloodRequest` |
| Dashboard | `/Dashboard` |
| Contact support | `/Home/Contact` |
| FAQ | `/Home/Faq` |

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

---

## 📞 Support

- **Contact Form:** [/Home/Contact](/Home/Contact)
- **GitHub Issues:** [github.com/rajputpri/BloodConnector/issues](https://github.com/rajputpri/BloodConnector/issues)

---

**Last Updated:** October 2026