"""
BloodConnect — Auto Screenshot Script
Run: python take_screenshots.py
"""

from playwright.sync_api import sync_playwright
import os
import time

BASE_URL = "https://bloodconnector.runasp.net"
ROOT = r"C:\Prince\BloodConnect\docs\screenshots"

# Folders create karo
folders = ["public", "auth", "donor-workflow", "admin"]
for f in folders:
    os.makedirs(os.path.join(ROOT, f), exist_ok=True)

# Public pages (no login needed)
public_pages = [
    ("/", "01-homepage.png"),
    ("/Donor", "02-donor-list.png"),
    ("/Donor/Search?bloodGroup=B%2B", "03-search.png"),
    ("/BloodRequest", "04-requests.png"),
    ("/Home/About", "05-about.png"),
    ("/Home/Contact", "06-contact.png"),
    ("/Home/Faq", "07-faq.png"),
    ("/xyzabc", "08-404.png"),
]

# Auth pages (no login)
auth_pages = [
    ("/Account/Register", "01-register.png"),
    ("/Account/Login", "02-login.png"),
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()

    print("=" * 50)
    print("BloodConnect — Auto Screenshots")
    print("=" * 50)

    # Public pages
    print("\n📁 PUBLIC pages (8 screenshots)...")
    for url, filename in public_pages:
        full_url = BASE_URL + url
        save_path = os.path.join(ROOT, "public", filename)
        try:
            page.goto(full_url, timeout=30000)
            page.wait_for_load_state("networkidle", timeout=15000)
            time.sleep(2)  # animations settle
            page.screenshot(path=save_path, full_page=False)
            print(f"  ✅ {filename}")
        except Exception as e:
            print(f"  ❌ {filename} — {e}")

    # Auth pages
    print("\n📁 AUTH pages (2 screenshots)...")
    for url, filename in auth_pages:
        full_url = BASE_URL + url
        save_path = os.path.join(ROOT, "auth", filename)
        try:
            page.goto(full_url, timeout=30000)
            page.wait_for_load_state("networkidle", timeout=15000)
            time.sleep(2)
            page.screenshot(path=save_path, full_page=False)
            print(f"  ✅ {filename}")
        except Exception as e:
            print(f"  ❌ {filename} — {e}")

    # Login as admin
    print("\n🔐 Logging in as admin...")
    try:
        page.goto(BASE_URL + "/Account/Login", timeout=30000)
        page.fill('input[name="Email"]', "admin@bloodconnect.com")
        page.fill('input[name="Password"]', "Admin@123")
        page.click('button[type="submit"]')
        page.wait_for_load_state("networkidle", timeout=15000)
        time.sleep(2)
        print("  ✅ Login successful")
    except Exception as e:
        print(f"  ❌ Login failed — {e}")

    # Admin pages (login required)
    admin_pages = [
        ("/Admin", "01-admin-dashboard.png"),
        ("/Admin/Donors", "02-donors-list.png"),
        ("/Admin/UserList", "03-user-list.png"),
        ("/Admin/Messages", "04-messages.png"),
        ("/swagger", "05-swagger.png"),
    ]

    print("\n📁 ADMIN pages (5 screenshots)...")
    for url, filename in admin_pages:
        full_url = BASE_URL + url
        save_path = os.path.join(ROOT, "admin", filename)
        try:
            page.goto(full_url, timeout=30000)
            page.wait_for_load_state("networkidle", timeout=15000)
            time.sleep(2)
            page.screenshot(path=save_path, full_page=False)
            print(f"  ✅ {filename}")
        except Exception as e:
            print(f"  ❌ {filename} — {e}")

    # Donor workflow pages
    donor_pages = [
        ("/Donor/Create", "01-create-form.png"),
        ("/Dashboard", "02-dashboard.png"),
        ("/BloodRequest", "03-offer-pledge.png"),
    ]

    print("\n📁 DONOR WORKFLOW (3 screenshots)...")
    for url, filename in donor_pages:
        full_url = BASE_URL + url
        save_path = os.path.join(ROOT, "donor-workflow", filename)
        try:
            page.goto(full_url, timeout=30000)
            page.wait_for_load_state("networkidle", timeout=15000)
            time.sleep(2)
            page.screenshot(path=save_path, full_page=False)
            print(f"  ✅ {filename}")
        except Exception as e:
            print(f"  ❌ {filename} — {e}")

    browser.close()

print("\n" + "=" * 50)
print("✅ DONE! Screenshots saved to: docs/screenshots/")
print("=" * 50)