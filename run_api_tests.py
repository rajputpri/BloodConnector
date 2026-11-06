"""
BloodConnect — Automated API Testing Script
============================================
Chalao: python run_api_tests.py

Yeh script:
1. Login karta hai (cookie save karta hai)
2. Saare API tests chalata hai
3. Har test ka screenshot leta hai (Postman jaisa)
4. docs/screenshots/api-deployment/ me save karta hai
5. Live pe DELETE skip karta hai (safety)

Install:
    pip install requests playwright
    playwright install chromium
"""

import os
import json
import time
from pathlib import Path
from datetime import datetime

import requests
from playwright.sync_api import sync_playwright


# ═══════════════════════════════════════════════════════════
# CONFIG — YAHAN CHANGE KARO
# ═══════════════════════════════════════════════════════════
MODE = "local"   # "live" ya "local"

CONFIGS = {
    "live": {
        "base_url": "https://bloodconnector.runasp.net",
        "admin_email": "admin@bloodconnect.com",
        "admin_pass": "Admin@123",
        "skip_delete": True,   # live pe delete mat karo
    },
    "local": {
        "base_url": "http://localhost:5006",
        "admin_email": "admin@bloodconnect.com",
        "admin_pass": "Admin@123",
        "skip_delete": False,
    },
}

CFG = CONFIGS[MODE]
BASE = CFG["base_url"].rstrip("/")
OUT = Path("docs/screenshots/api-deployment")
OUT.mkdir(parents=True, exist_ok=True)

session = requests.Session()
session.headers.update({"User-Agent": "BloodConnect-Auto-Test"})


# ═══════════════════════════════════════════════════════════
# TEST DEFINITIONS — 20 NAYE TESTS (09-28)
# ═══════════════════════════════════════════════════════════
TESTS = [
    # ---------- GET ----------
    {"num": 9, "name": "GET Non-Existent Donor (404)",
     "method": "GET", "path": "/api/donor/99999", "auth": False},

    {"num": 10, "name": "Search Exact Match Mode",
     "method": "GET", "path": "/api/donor/search?bloodGroup=A%2B&exactMatch=true",
     "auth": False},

    {"num": 11, "name": "Search Invalid Blood Group",
     "method": "GET", "path": "/api/donor/search?bloodGroup=XYZ",
     "auth": False},

    {"num": 12, "name": "Search By State",
     "method": "GET", "path": "/api/donor/search?state=Gujarat",
     "auth": False},

    # ---------- POST ----------
    {"num": 13, "name": "POST Duplicate Donor (409)",
     "method": "POST", "path": "/api/donor", "auth": True,
     "body": {"name": "Duplicate Test", "bloodGroup": "O+", "age": 25,
              "state": "Gujarat", "city": "Surat",
              "contactNumber": "9876500001", "isAvailable": True}},

    {"num": 14, "name": "POST Invalid Blood Group (400)",
     "method": "POST", "path": "/api/donor", "auth": True,
     "body": {"name": "Bad BG", "bloodGroup": "XYZ", "age": 25,
              "state": "Gujarat", "contactNumber": "9876500002"}},

    {"num": 15, "name": "POST Invalid State (400)",
     "method": "POST", "path": "/api/donor", "auth": True,
     "body": {"name": "Bad State", "bloodGroup": "O+", "age": 25,
              "state": "Atlantis", "contactNumber": "9876500003"}},

    {"num": 16, "name": "POST Age Below 18 (400)",
     "method": "POST", "path": "/api/donor", "auth": True,
     "body": {"name": "Too Young", "bloodGroup": "O+", "age": 17,
              "state": "Gujarat", "contactNumber": "9876500004"}},

    {"num": 17, "name": "POST Age Above 65 (400)",
     "method": "POST", "path": "/api/donor", "auth": True,
     "body": {"name": "Too Old", "bloodGroup": "O+", "age": 66,
              "state": "Gujarat", "contactNumber": "9876500005"}},

    {"num": 18, "name": "POST Missing Name (400)",
     "method": "POST", "path": "/api/donor", "auth": True,
     "body": {"bloodGroup": "O+", "age": 25,
              "state": "Gujarat", "contactNumber": "9876500006"}},

    # ---------- PUT ----------
    {"num": 19, "name": "PUT Update Own Donor (200)",
     "method": "PUT", "path": "/api/donor/{own_id}", "auth": True,
     "body": {"name": "Updated Name", "bloodGroup": "O+", "age": 26,
              "state": "Gujarat", "city": "Ahmedabad",
              "contactNumber": "9876543210", "isAvailable": False},
     "resolve_own_id": True},

    {"num": 20, "name": "PUT Other User's Donor (403)",
     "method": "PUT", "path": "/api/donor/1", "auth": True,
     "body": {"name": "IDOR Attempt", "bloodGroup": "O+", "age": 25,
              "state": "Gujarat", "contactNumber": "9999999999"}},

    {"num": 21, "name": "PUT Non-Existent Donor (404)",
     "method": "PUT", "path": "/api/donor/99999", "auth": True,
     "body": {"name": "Ghost", "bloodGroup": "O+", "age": 25,
              "state": "Gujarat", "contactNumber": "9999999999"}},

    {"num": 22, "name": "PUT Invalid Blood Group (400)",
     "method": "PUT", "path": "/api/donor/{own_id}", "auth": True,
     "body": {"name": "Bad Update", "bloodGroup": "XYZ", "age": 25,
              "state": "Gujarat", "contactNumber": "9999999999"},
     "resolve_own_id": True},

    # ---------- DELETE ----------
    {"num": 23, "name": "DELETE Own Donor (204)",
     "method": "DELETE", "path": "/api/donor/{own_id}", "auth": True,
     "resolve_own_id": True, "skip_on_live": True},

    {"num": 24, "name": "DELETE Other's Donor (403)",
     "method": "DELETE", "path": "/api/donor/1", "auth": True,
     "skip_on_live": True},

    {"num": 25, "name": "DELETE Non-Existent (404)",
     "method": "DELETE", "path": "/api/donor/99999", "auth": True,
     "skip_on_live": True},

    # ---------- AUTH ----------
    {"num": 26, "name": "Login With Wrong Password (401)",
     "method": "POST", "path": "/api/auth/login", "auth": False,
     "body": {"email": CFG["admin_email"], "password": "WrongPass@999"},
     "isolated": True},

    {"num": 27, "name": "XSS Attempt in Name Field",
     "method": "POST", "path": "/api/donor", "auth": True,
     "body": {"name": "<script>alert(1)</script>", "bloodGroup": "O+",
              "age": 25, "state": "Gujarat",
              "contactNumber": "9876500010"}},

    {"num": 28, "name": "SQL Injection Attempt",
     "method": "GET", "path": "/api/donor/search?bloodGroup=' OR '1'='1",
     "auth": False},
]


# ═══════════════════════════════════════════════════════════
# LOGIN + COOKIE
# ═══════════════════════════════════════════════════════════
def login():
    print("→ Logging in...")
    try:
        r = session.post(
            f"{BASE}/api/auth/login",
            json={"email": CFG["admin_email"], "password": CFG["admin_pass"]},
            timeout=30,
        )
        if r.status_code == 200:
            print(f"  ✅ Login OK. Cookies: {list(session.cookies.keys())}")
            return True
        print(f"  ❌ Login failed: {r.status_code} {r.text[:200]}")
        return False
    except Exception as e:
        print(f"  ❌ Login error: {e}")
        return False


def get_own_donor_id():
    """Login ke baad, current admin ka donor ID fetch karo."""
    try:
        r = session.get(f"{BASE}/api/donor", timeout=30)
        if r.status_code == 200:
            data = r.json()
            # Apne donor ko dhoondo (jiska contact visible ho ya match kare)
            items = data.get("items", [])
            if items:
                return items[0].get("donorId")
    except Exception:
        pass
    return None


# ═══════════════════════════════════════════════════════════
# REQUEST EXECUTION
# ═══════════════════════════════════════════════════════════
def run_test(test, own_donor_id=None):
    """Ek test run karo, result return karo."""
    url = BASE + test["path"]
    if test.get("resolve_own_id") and own_donor_id:
        url = url.replace("{own_id}", str(own_donor_id))
    elif "{own_id}" in url:
        url = url.replace("{own_id}", "9999")  # fallback

    method = test["method"]
    body = test.get("body")
    headers = {"Content-Type": "application/json"} if body else {}

    # Isolated test = fresh session (no cookies)
    req_session = requests.Session() if test.get("isolated") else session

    start = time.time()
    try:
        r = req_session.request(method, url, json=body, headers=headers,
                                timeout=30)
        elapsed_ms = (time.time() - start) * 1000
    except Exception as e:
        return {
            "num": test["num"], "name": test["name"],
            "method": method, "url": url, "body": body,
            "status": 0, "status_text": "ERROR",
            "response": str(e), "elapsed": 0, "size": 0,
        }

    # Response body format
    try:
        resp_json = r.json()
        resp_body = json.dumps(resp_json, indent=2)
    except Exception:
        resp_body = r.text or "(empty)"

    return {
        "num": test["num"],
        "name": test["name"],
        "method": method,
        "url": url,
        "body": body,
        "status": r.status_code,
        "status_text": r.reason,
        "response": resp_body,
        "elapsed": elapsed_ms,
        "size": len(r.content),
    }


# ═══════════════════════════════════════════════════════════
# HTML GENERATION (Postman jaisa look)
# ═══════════════════════════════════════════════════════════
def build_html(result):
    method = result["method"]
    url = result["url"]
    body = result["body"]
    status = result["status"]
    resp = result["response"]

    method_colors = {"GET": "#61affe", "POST": "#49cc90",
                     "PUT": "#fca130", "DELETE": "#f93e3e"}
    mcolor = method_colors.get(method, "#999")

    if 200 <= status < 300:
        scolor = "#4caf50"
    elif 300 <= status < 400:
        scolor = "#ff9800"
    elif status == 0:
        scolor = "#9e9e9e"
    else:
        scolor = "#f44336"

    body_json = json.dumps(body, indent=2) if body else ""

    html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: -apple-system, 'Segoe UI', sans-serif; background: #f0f2f5; padding: 24px; color: #333; }}
.card {{ max-width: 1200px; margin: 0 auto; background: #fff; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 20px rgba(0,0,0,0.08); }}
.title {{ padding: 18px 24px; background: linear-gradient(135deg, #8B1E3F 0%, #5C0A22 100%); color: #fff; }}
.title .num {{ font-size: 12px; opacity: 0.8; letter-spacing: 1.5px; text-transform: uppercase; }}
.title .name {{ font-size: 20px; font-weight: 600; margin-top: 4px; }}
.urlbar {{ display: flex; gap: 12px; padding: 16px 24px; background: #fafbfc; border-bottom: 1px solid #e8e8e8; align-items: center; }}
.method {{ padding: 10px 20px; background: {mcolor}; color: #fff; border-radius: 6px; font-weight: 700; font-size: 13px; letter-spacing: 0.5px; }}
.url {{ flex: 1; padding: 12px 16px; background: #fff; border: 1px solid #e0e0e0; border-radius: 6px; font-family: 'Consolas', monospace; font-size: 13px; color: #333; }}
.respbar {{ display: flex; gap: 24px; padding: 14px 24px; background: #fafbfc; border-bottom: 1px solid #e8e8e8; align-items: center; }}
.status {{ font-weight: 700; color: {scolor}; font-size: 15px; }}
.meta {{ color: #666; font-size: 13px; }}
.tabs {{ display: flex; padding: 0 24px; background: #fafbfc; border-bottom: 1px solid #e8e8e8; }}
.tab {{ padding: 14px 22px; font-size: 13px; color: #666; border-bottom: 2px solid transparent; font-weight: 500; }}
.tab.active {{ color: #8B1E3F; border-bottom-color: #8B1E3F; }}
.body {{ padding: 20px 24px; background: #fafbfc; }}
.section {{ background: #fff; border: 1px solid #e8e8e8; border-radius: 8px; padding: 16px; margin-bottom: 16px; }}
.section-title {{ font-weight: 600; color: #555; margin-bottom: 10px; font-size: 11.5px; text-transform: uppercase; letter-spacing: 1px; }}
pre {{ background: #f7f7f9; padding: 14px; border-radius: 6px; font-family: 'Consolas', monospace; font-size: 12.5px; line-height: 1.65; overflow-x: auto; color: #2d2d2d; white-space: pre-wrap; }}
</style></head><body>
<div class="card">
  <div class="title">
    <div class="num">Test {result['num']:02d} — API Test Report</div>
    <div class="name">{result['name']}</div>
  </div>
  <div class="urlbar">
    <div class="method">{method}</div>
    <div class="url">{url}</div>
  </div>
  <div class="respbar">
    <span class="status">{status} {result['status_text']}</span>
    <span class="meta">⏱ {result['elapsed']:.0f} ms</span>
    <span class="meta">📦 {result['size']} B</span>
  </div>
  <div class="tabs">
    <div class="tab active">Body</div>
    <div class="tab">Cookies</div>
    <div class="tab">Headers</div>
  </div>
  <div class="body">
    {f'<div class="section"><div class="section-title">Request Body</div><pre>{body_json}</pre></div>' if body else ''}
    <div class="section">
      <div class="section-title">Response Body</div>
      <pre>{resp}</pre>
    </div>
  </div>
</div>
</body></html>"""
    return html


# ═══════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════
def main():
    print(f"\n{'='*60}")
    print(f"  BloodConnect Automated API Testing")
    print(f"  Mode: {MODE.upper()}  |  Base: {BASE}")
    print(f"  Output: {OUT}")
    print(f"{'='*60}\n")

    if not login():
        print("\n❌ Login failed. Exiting.")
        return

    own_donor_id = get_own_donor_id()
    print(f"  Own donor ID: {own_donor_id}\n")

    # Collect results
    all_results = []
    passed = 0
    failed = 0

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1300, "height": 900})

        for test in TESTS:
            # Skip logic
            if test.get("skip_on_live") and MODE == "live":
                print(f"  ⏭  Test {test['num']:02d} skipped (live mode)")
                continue

            print(f"  ▶ Test {test['num']:02d}: {test['name']}")
            result = run_test(test, own_donor_id)

            status = result["status"]
            if 200 <= status < 300:
                print(f"      ✅ {status} {result['status_text']}")
                passed += 1
            else:
                print(f"      ⚠  {status} {result['status_text']}")
                failed += 1

            # Screenshot
            html = build_html(result)
            page.set_content(html)
            page.wait_for_timeout(150)
            fname = f"{test['num']:02d}-postman-{test['method'].lower()}-{status}.png"
            page.screenshot(path=str(OUT / fname), full_page=True)
            print(f"      📸 {fname}")

            all_results.append({**result, "file": fname})

        browser.close()

    # Summary
    print(f"\n{'='*60}")
    print(f"  ✅ Passed: {passed}")
    print(f"  ⚠  Failed: {failed}")
    print(f"  📸 Screenshots: {OUT}")
    print(f"{'='*60}\n")

    # Also save JSON report
    report_file = OUT / "_report.json"
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2)
    print(f"  📄 Report: {report_file}\n")

    print("  Ab GitHub pe push karo:")
    print(f"  git add {OUT}/")
    print(f"  git commit -m 'docs: complete API testing screenshots (automated)'")
    print(f"  git push origin main\n")


if __name__ == "__main__":
    main()