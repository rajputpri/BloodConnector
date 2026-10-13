"""
BloodConnect — Ultimate PPT Generator v3
Run: python generate_ppt.py
Output: BloodConnect-PPT.pptx (28 slides, professional-grade)

Requirements:
  pip install python-pptx Pillow
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION
import os

try:
    from PIL import Image
    PIL = True
except ImportError:
    PIL = False
    print("⚠️  Pillow not installed — images won't auto-scale perfectly.")
    print("   Install: pip install Pillow")

# ==================== COLOR PALETTE ====================
RED         = RGBColor(0xDC, 0x26, 0x26)
RED_BRIGHT  = RGBColor(0xEF, 0x44, 0x44)
RED_DARK    = RGBColor(0x99, 0x1B, 0x1B)
RED_DEEP    = RGBColor(0x45, 0x0A, 0x0A)
RED_NIGHT   = RGBColor(0x14, 0x08, 0x08)
RED_SOFT    = RGBColor(0xFE, 0xF2, 0xF2)
GOLD        = RGBColor(0xD4, 0xA2, 0x4C)
GOLD_BRIGHT = RGBColor(0xE5, 0xB8, 0x65)
GOLD_SOFT   = RGBColor(0xF5, 0xE6, 0xC5)
CREAM       = RGBColor(0xFA, 0xF7, 0xF2)
CREAM_2     = RGBColor(0xF5, 0xEF, 0xE6)
WHITE       = RGBColor(0xFF, 0xFF, 0xFF)
INK         = RGBColor(0x1A, 0x14, 0x14)
INK_2       = RGBColor(0x3D, 0x2E, 0x2E)
MUTED       = RGBColor(0x7A, 0x6D, 0x6D)
LINE        = RGBColor(0xEA, 0xE3, 0xD8)

GREEN       = RGBColor(0x16, 0xA3, 0x4A)
GREEN_SOFT  = RGBColor(0xEC, 0xFD, 0xF5)
BLUE        = RGBColor(0x25, 0x63, 0xEB)
BLUE_SOFT   = RGBColor(0xEF, 0xF6, 0xFF)
PURPLE      = RGBColor(0x7C, 0x3A, 0xED)
ORANGE      = RGBColor(0xEA, 0x58, 0x0C)
CYAN        = RGBColor(0x08, 0x91, 0xB2)

# ==================== PRESENTATION ====================
prs = Presentation()
prs.slide_width  = Inches(13.333)
prs.slide_height = Inches(7.5)
SW, SH = prs.slide_width, prs.slide_height
BLANK = prs.slide_layouts[6]

# ==================== SCREENSHOTS ====================
IMG = {
    "homepage":       "docs/screenshots/public/01-homepage.png",
    "donor_list":     "docs/screenshots/public/02-donor-list.png",
    "search":         "docs/screenshots/public/03-search.png",
    "requests":       "docs/screenshots/public/04-requests.png",
    "about":          "docs/screenshots/public/05-about.png",
    "contact":        "docs/screenshots/public/06-contact.png",
    "register":       "docs/screenshots/auth/01-register.png",
    "login":          "docs/screenshots/auth/02-login.png",
    "login_error":    "docs/screenshots/auth/03-login-error.png",
    "access_denied":  "docs/screenshots/auth/04-access-denied.png",
    "create_form":    "docs/screenshots/donor-workflow/01-create-form.png",
    "dashboard":      "docs/screenshots/donor-workflow/02-dashboard.png",
    "offer_pledge":   "docs/screenshots/donor-workflow/03-offer-pledge.png",
    "offer_accepted": "docs/screenshots/donor-workflow/04-offer-accepted.png",
    "toast":          "docs/screenshots/donor-workflow/05-toast.png",
    "admin_dash":     "docs/screenshots/admin/01-admin-dashboard.png",
    "admin_donors":   "docs/screenshots/admin/02-donors-list.png",
    "admin_users":    "docs/screenshots/admin/03-user-list.png",
    "admin_msgs":     "docs/screenshots/admin/04-messages.png",
    "swagger":        "docs/screenshots/admin/05-swagger.png",
    "pm_get":         "docs/screenshots/api-deployment/01-postman-get-donors.png",
    "pm_single":      "docs/screenshots/api-deployment/02-postman-single-donor.png",
    "pm_search":      "docs/screenshots/api-deployment/03-postman-search.png",
    "pm_401":         "docs/screenshots/api-deployment/08-postman-401-unauthorized.png",
    "pm_201":         "docs/screenshots/api-deployment/07-postman-201-created.png",
}

# ==================== HELPERS ====================

def bg(slide, color):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = color

def rect(slide, left, top, w, h, fill=None, line=None, lw=0, rounded=False):
    shp = MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE
    s = slide.shapes.add_shape(shp, left, top, w, h)
    if fill:
        s.fill.solid()
        s.fill.fore_color.rgb = fill
    else:
        s.fill.background()
    if line and lw > 0:
        s.line.color.rgb = line
        s.line.width = Pt(lw)
    else:
        s.line.fill.background()
    s.shadow.inherit = False
    return s

def circle(slide, left, top, w, h, fill, line=None, lw=0):
    c = slide.shapes.add_shape(MSO_SHAPE.OVAL, left, top, w, h)
    c.fill.solid()
    c.fill.fore_color.rgb = fill
    if line and lw > 0:
        c.line.color.rgb = line
        c.line.width = Pt(lw)
    else:
        c.line.fill.background()
    c.shadow.inherit = False
    return c

def text(slide, txt, left, top, w, h, size=16, color=INK, bold=False,
         italic=False, align=PP_ALIGN.LEFT, font="Inter",
         anchor=MSO_ANCHOR.TOP, spacing=1.05):
    tb = slide.shapes.add_textbox(left, top, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = 0; tf.margin_right = 0
    tf.margin_top = 0; tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.alignment = align
    p.line_spacing = spacing
    r = p.add_run()
    r.text = txt
    r.font.size = Pt(size)
    r.font.color.rgb = color
    r.font.bold = bold
    r.font.italic = italic
    r.font.name = font
    return tb

def bullets(slide, lines, left, top, w, h, size=14, color=INK_2,
            line_spacing=1.5, bullet_char="—", gap=0):
    tb = slide.shapes.add_textbox(left, top, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = 0; tf.margin_right = 0
    tf.margin_top = 0; tf.margin_bottom = 0
    for i, item in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.line_spacing = line_spacing
        if gap:
            p.space_after = Pt(gap)
        pref = p.add_run()
        pref.text = f"{bullet_char}  "
        pref.font.size = Pt(size)
        pref.font.color.rgb = RED
        pref.font.bold = True
        pref.font.name = "Inter"
        r = p.add_run()
        r.text = item
        r.font.size = Pt(size)
        r.font.color.rgb = color
        r.font.name = "Inter"
    return tb

def pill(slide, txt, left, top, w, h, bgc=RED, fgc=WHITE, size=10):
    p = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, w, h)
    p.fill.solid()
    p.fill.fore_color.rgb = bgc
    p.line.fill.background()
    p.shadow.inherit = False
    tf = p.text_frame
    tf.margin_left = Inches(0.1); tf.margin_right = Inches(0.1)
    tf.margin_top = 0; tf.margin_bottom = 0
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    par = tf.paragraphs[0]
    par.alignment = PP_ALIGN.CENTER
    r = par.add_run()
    r.text = txt
    r.font.size = Pt(size)
    r.font.color.rgb = fgc
    r.font.bold = True
    r.font.name = "Inter"
    return p

def pageno(slide, n):
    text(slide, f"{n:02d}", SW - Inches(0.9), SH - Inches(0.45),
         Inches(0.6), Inches(0.3), size=10, color=MUTED, bold=True,
         align=PP_ALIGN.RIGHT, font="Consolas")

def footer(slide, color=MUTED):
    text(slide, "BLOODCONNECT", Inches(0.7), SH - Inches(0.45),
         Inches(3), Inches(0.3), size=9, color=color, bold=True,
         font="Consolas")

def ghost(slide, num, left, top, size=280, color=None):
    c = color or RGBColor(0xE5, 0xDD, 0xD5)
    text(slide, num, left, top, Inches(4), Inches(3), size=size,
         color=c, bold=True, font="Inter")

def scaled_dims(path, max_w, max_h):
    """Return (w, h) that fits inside max_w × max_h, preserving aspect."""
    if not PIL or not os.path.exists(path):
        return max_w, max_h
    try:
        with Image.open(path) as im:
            iw, ih = im.size
        ratio = min(max_w / iw, max_h / ih)
        return int(iw * ratio), int(ih * ratio)
    except Exception:
        return max_w, max_h

def image_in_card(slide, path, left, top, box_w, box_h,
                  caption_title="", caption_desc="", accent=RED):
    """Centered image inside a card with title + desc."""
    card_h = box_h + Inches(0.65) if caption_title else box_h
    # card
    rect(slide, left, top, box_w, card_h, WHITE, LINE, 1, rounded=True)
    # top accent
    rect(slide, left, top, box_w, Inches(0.06), accent)

    if os.path.exists(path):
        iw, ih = scaled_dims(path, box_w - Inches(0.16), box_h - Inches(0.16))
        ix = left + (box_w - iw) // 2
        iy = top + Inches(0.12) + (box_h - Inches(0.16) - ih) // 2
        slide.shapes.add_picture(path, ix, iy, width=iw, height=ih)
    else:
        rect(slide, left + Inches(0.1), top + Inches(0.12),
             box_w - Inches(0.2), box_h - Inches(0.16), CREAM_2, LINE, 1, rounded=True)
        text(slide, "[missing]", left, top + box_h / 2 - Inches(0.1),
             box_w, Inches(0.3), size=9, color=MUTED,
             align=PP_ALIGN.CENTER, italic=True)

    if caption_title:
        text(slide, caption_title, left + Inches(0.15),
             top + box_h + Inches(0.05), box_w - Inches(0.3),
             Inches(0.3), size=12, color=INK, bold=True)
    if caption_desc:
        text(slide, caption_desc, left + Inches(0.15),
             top + box_h + Inches(0.32), box_w - Inches(0.3),
             Inches(0.3), size=9, color=MUTED, italic=True)

def section_divider(num, title, subtitle):
    """Reusable section divider — bold red, big number."""
    s = prs.slides.add_slide(BLANK)
    bg(s, RED)
    ghost(s, num, Inches(8), Inches(0.8), size=340,
          color=RGBColor(0x7F, 0x1D, 0x1D))

    text(s, f"SECTION {num}", Inches(0.8), Inches(0.8), Inches(4), Inches(0.4),
         size=13, color=RGBColor(0xFF, 0xCC, 0xCC), bold=True, font="Consolas")

    # Big title
    text(s, title, Inches(0.8), Inches(2.5), Inches(11), Inches(1.5),
         size=80, color=WHITE, bold=True)

    rect(s, Inches(0.85), Inches(4.35), Inches(2.5), Inches(0.12), GOLD)

    text(s, subtitle, Inches(0.8), Inches(4.9), Inches(11), Inches(0.6),
         size=22, color=RGBColor(0xFF, 0xE5, 0xE5), italic=True)
    return s

# ============================================================
# SLIDE 01 — HERO TITLE
# ============================================================
s = prs.slides.add_slide(BLANK)
bg(s, RED_NIGHT)

# Decorations
circle(s, Inches(10.8), Inches(-1.2), Inches(4.5), Inches(4.5), RED_DEEP)
circle(s, Inches(-1.8), Inches(5.3), Inches(3.5), Inches(3.5), RED_DARK)

# Blood drop
circle(s, Inches(9.9), Inches(2.3), Inches(2.9), Inches(2.9), RED)
circle(s, Inches(10.5), Inches(2.7), Inches(0.85), Inches(0.85), RED_BRIGHT)

# Tag
rect(s, Inches(0.8), Inches(0.8), Inches(0.16), Inches(0.16), GOLD)
text(s, "EMERGENCY BLOOD NETWORK", Inches(1.1), Inches(0.72),
     Inches(4), Inches(0.3), size=11, color=GOLD, bold=True, font="Consolas")

# Big title
text(s, "Blood", Inches(0.8), Inches(1.7), Inches(8.5), Inches(1.6),
     size=125, color=WHITE, bold=True, spacing=0.85)
text(s, "Connect", Inches(0.8), Inches(3.15), Inches(8.5), Inches(1.6),
     size=125, color=GOLD, bold=True, spacing=0.85)

# Accent line
rect(s, Inches(0.85), Inches(4.85), Inches(1.4), Inches(0.1), RED)

# Subtitle
text(s, "Real-Time Blood Donation Network",
     Inches(0.8), Inches(5.15), Inches(9), Inches(0.55),
     size=26, color=WHITE, italic=True)

# Sub-sub
text(s, "Compatibility-aware matching  ·  Pledge-based workflow  ·  Live notifications",
     Inches(0.8), Inches(5.75), Inches(11), Inches(0.4),
     size=13, color=RGBColor(0xCC, 0xBB, 0xBB))

# Bottom meta
text(s, "BCA SEMESTER 7   ·   DSC-M-CBA 471P   ·   GUJARAT UNIVERSITY",
     Inches(0.8), Inches(6.5), Inches(11), Inches(0.4),
     size=11, color=GOLD, bold=True, font="Consolas")

text(s, "Prince Rajput", Inches(0.8), Inches(6.9), Inches(6), Inches(0.4),
     size=16, color=WHITE, bold=True)

text(s, "2026", SW - Inches(1.6), Inches(6.9), Inches(0.8), Inches(0.4),
     size=16, color=GOLD, bold=True, font="Consolas", align=PP_ALIGN.RIGHT)

# ============================================================
# SLIDE 02 — AGENDA
# ============================================================
s = prs.slides.add_slide(BLANK)
bg(s, CREAM)
rect(s, Inches(0), Inches(0), Inches(0.18), SH, RED)

pill(s, "AGENDA", Inches(0.75), Inches(0.6), Inches(1.5), Inches(0.38),
     RED, WHITE, 11)

text(s, "What we'll cover.", Inches(0.75), Inches(1.2),
     Inches(11), Inches(0.8), size=44, color=INK, bold=True)

text(s, "From problem to production — a complete walkthrough.",
     Inches(0.75), Inches(2.15), Inches(11), Inches(0.5),
     size=16, color=MUTED, italic=True)

toc = [
    ("01", "The Problem",          "India's blood shortage crisis",       RED),
    ("02", "Our Solution",         "How BloodConnect fixes it",            GOLD),
    ("03", "Tech Stack",           "Modern .NET stack + SignalR",          BLUE),
    ("04", "Signature Features",   "Real-time · Compatibility · Workflow", GREEN),
    ("05", "Live Screenshots",     "Real evidence from production",        PURPLE),
    ("06", "Live Demo",            "It's live. Right now.",                ORANGE),
]

col_w = Inches(5.9)
row_h = Inches(1.2)
gx = Inches(0.75)
gy = Inches(3.05)

for i, (num, title, desc, c) in enumerate(toc):
    col = i % 2; row = i // 2
    x = gx + col * (col_w + Inches(0.2))
    y = gy + row * (row_h + Inches(0.18))
    rect(s, x, y, col_w, row_h, WHITE, LINE, 1, rounded=True)
    rect(s, x, y, Inches(0.08), row_h, c)
    text(s, num, x + Inches(0.3), y + Inches(0.22), Inches(0.9),
         Inches(0.8), size=34, color=c, bold=True, font="Consolas")
    text(s, title, x + Inches(1.25), y + Inches(0.22),
         col_w - Inches(1.4), Inches(0.4), size=18, color=INK, bold=True)
    text(s, desc, x + Inches(1.25), y + Inches(0.65),
         col_w - Inches(1.4), Inches(0.4), size=12, color=MUTED)

pageno(s, 2); footer(s)

# ============================================================
# SLIDE 03 — SECTION 01: PROBLEM
# ============================================================
section_divider("01", "The Problem",
                "India faces a critical blood shortage — traditional methods are failing.")

# ============================================================
# SLIDE 04 — PROBLEM DETAILS + CHART
# ============================================================
s = prs.slides.add_slide(BLANK)
bg(s, CREAM)

pill(s, "THE PROBLEM", Inches(0.75), Inches(0.6), Inches(1.9), Inches(0.38),
     RED, WHITE, 11)
text(s, "Blood shortage is real.", Inches(0.75), Inches(1.2),
     Inches(7), Inches(0.8), size=38, color=INK, bold=True)
text(s, "Every minute counts in an emergency.",
     Inches(0.75), Inches(2.0), Inches(7), Inches(0.5),
     size=16, color=MUTED, italic=True)

y = Inches(2.9)
stats = [
    ("14.6M", "blood units needed yearly in India",       RED),
    ("1.5M",  "unit shortage every single year",           RED_DARK),
    ("63%",   "of transfusions face critical delays",      ORANGE),
    ("72h",   "average donor search time",                 RED_BRIGHT),
]
for val, lbl, c in stats:
    rect(s, Inches(0.75), y, Inches(0.06), Inches(0.5), c)
    text(s, val, Inches(0.95), y - Inches(0.05), Inches(2), Inches(0.6),
         size=32, color=c, bold=True)
    text(s, lbl, Inches(3.0), y + Inches(0.08), Inches(4.5), Inches(0.4),
         size=13, color=INK_2)
    y += Inches(0.85)

# Chart
card = rect(s, Inches(7.9), Inches(2.6), Inches(4.8), Inches(4.2),
            WHITE, LINE, 1, rounded=True)
rect(s, Inches(7.9), Inches(2.6), Inches(4.8), Inches(0.08), RED)
text(s, "BLOOD DEMAND vs SUPPLY", Inches(8.15), Inches(2.85),
     Inches(4), Inches(0.3), size=11, color=RED, bold=True, font="Consolas")

cd = CategoryChartData()
cd.categories = ['2021', '2022', '2023', '2024', '2025']
cd.add_series('Demand', (13.2, 13.8, 14.1, 14.4, 14.6))
cd.add_series('Supply', (11.6, 12.0, 12.6, 13.0, 13.1))

gf = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED,
                        Inches(8.15), Inches(3.3),
                        Inches(4.3), Inches(3.2), cd)
ch = gf.chart
ch.has_legend = True
ch.legend.position = XL_LEGEND_POSITION.BOTTOM
ch.legend.include_in_layout = False
ch.legend.font.size = Pt(10)
ch.legend.font.name = "Inter"
pl = ch.plots[0]
pl.gap_width = 60
pl.series[0].format.fill.solid()
pl.series[0].format.fill.fore_color.rgb = RED
pl.series[1].format.fill.solid()
pl.series[1].format.fill.fore_color.rgb = GOLD

pageno(s, 4); footer(s)

# ============================================================
# SLIDE 05 — SECTION 02: SOLUTION
# ============================================================
section_divider("02", "Our Solution",
                "A verified, real-time, pledge-based network that actually works.")

# ============================================================
# SLIDE 06 — SOLUTION OVERVIEW (3 ROLE CARDS)
# ============================================================
s = prs.slides.add_slide(BLANK)
bg(s, CREAM)

pill(s, "OUR SOLUTION", Inches(0.75), Inches(0.6), Inches(2.2), Inches(0.38),
     RED, WHITE, 11)
text(s, "BloodConnect — the fix.", Inches(0.75), Inches(1.2),
     Inches(11), Inches(0.8), size=38, color=INK, bold=True)
text(s, "One platform. Three roles. Zero friction.",
     Inches(0.75), Inches(2.0), Inches(11), Inches(0.5),
     size=16, color=MUTED, italic=True)

roles = [
    ("USER",   "Post requests",  "Location + urgency aware",
     "Real-time status tracking",              RED),
    ("DONOR",  "Pledge to help", "Verified profile + age check",
     "Track every donation",                   GOLD),
    ("ADMIN",  "Manage users",   "Ban / Promote / Delete",
     "Full system visibility",                 INK),
]
cw = Inches(3.9); ch = Inches(3.6); cy = Inches(3.1)
for i, (role, l1, l2, l3, ac) in enumerate(roles):
    x = Inches(0.75) + i * (cw + Inches(0.2))
    rect(s, x, cy, cw, ch, WHITE, LINE, 1, rounded=True)
    rect(s, x, cy, cw, Inches(0.12), ac)
    pill(s, role, x + Inches(0.35), cy + Inches(0.4), Inches(1.1), Inches(0.35),
         ac, WHITE, 11)
    text(s, l1, x + Inches(0.35), cy + Inches(1.1), cw - Inches(0.7),
         Inches(0.45), size=20, color=INK, bold=True)
    bullets(s, [l2, l3], x + Inches(0.35), cy + Inches(1.85),
            cw - Inches(0.7), Inches(1.4), size=13, color=MUTED,
            bullet_char="·", line_spacing=1.6)

pageno(s, 6); footer(s)

# ============================================================
# SLIDE 07 — SECTION 03: TECH STACK
# ============================================================
section_divider("03", "Tech Stack",
                "Modern .NET stack with real-time SignalR and cloud deployment.")

# ============================================================
# SLIDE 08 — TECH GRID
# ============================================================
s = prs.slides.add_slide(BLANK)
bg(s, RED_NIGHT)

text(s, "TECH STACK", Inches(0.75), Inches(0.6), Inches(4), Inches(0.4),
     size=12, color=GOLD, bold=True, font="Consolas")
text(s, "Built with a modern stack.", Inches(0.75), Inches(1.2),
     Inches(11), Inches(0.9), size=42, color=WHITE, bold=True)
rect(s, Inches(0.8), Inches(2.25), Inches(2), Inches(0.1), RED)

tech = [
    ("ASP.NET Core", "MVC · .NET 10",      "Runtime",     RED),
    ("Entity Framework", "Code-First",     "ORM",         PURPLE),
    ("SQL Server", "Express + Cloud",      "Database",    BLUE),
    ("SignalR", "WebSocket Push",          "Real-Time",   GREEN),
    ("Identity", "Cookie Auth · 3 Roles",  "Security",    GOLD),
    ("Razor Pages", ".cshtml Views",       "UI Layer",    ORANGE),
    ("Swagger", "OpenAPI 3.0",             "API Docs",    CYAN),
    ("MonsterASP", "HTTPS · Let's Encrypt", "Hosting",    RED_BRIGHT),
]
cw = Inches(2.9); ch = Inches(1.95)
gx = Inches(0.75); gy = Inches(3.05)
for i, (name, sub, tag, c) in enumerate(tech):
    col = i % 4; row = i // 4
    x = gx + col * (cw + Inches(0.15))
    y = gy + row * (ch + Inches(0.2))
    rect(s, x, y, cw, ch, RED_DEEP, None, 0, rounded=True)
    # Accent dot
    circle(s, x + Inches(0.2), y + Inches(0.22), Inches(0.16), Inches(0.16), c)
    # Tag
    text(s, tag.upper(), x + Inches(0.5), y + Inches(0.2),
         cw - Inches(0.6), Inches(0.3), size=9, color=GOLD,
         bold=True, font="Consolas")
    # Name
    text(s, name, x + Inches(0.2), y + Inches(0.7), cw - Inches(0.4),
         Inches(0.5), size=17, color=WHITE, bold=True)
    # Sub
    text(s, sub, x + Inches(0.2), y + Inches(1.25), cw - Inches(0.4),
         Inches(0.4), size=11, color=RGBColor(0xAA, 0x99, 0x99))

pageno(s, 8); footer(s, RGBColor(0x77, 0x55, 0x55))

# ============================================================
# SLIDE 09 — ARCHITECTURE
# ============================================================
s = prs.slides.add_slide(BLANK)
bg(s, CREAM)

pill(s, "ARCHITECTURE", Inches(0.75), Inches(0.6), Inches(2.4), Inches(0.38),
     RED, WHITE, 11)
text(s, "Model · View · Controller", Inches(0.75), Inches(1.2),
     Inches(11), Inches(0.8), size=38, color=INK, bold=True)
text(s, "Clean separation — orchestrators, entities, and renderers.",
     Inches(0.75), Inches(2.0), Inches(11), Inches(0.5),
     size=15, color=MUTED, italic=True)

# 3 big boxes
box_w = Inches(3.55); box_h = Inches(2.3); by = Inches(2.85)
flow = [
    ("MODEL",      "Donor · BloodRequest\nDonationOffer · AppUser\nContactMessage",
     "Data Structures", RED),
    ("VIEW",       "Razor .cshtml\nBootstrap 5 + Custom CSS\nSVG Icons + Animations",
     "Presentation", GOLD),
    ("CONTROLLER", "Auth · CRUD · API\nSignalR Push · Notifications\nBusiness Logic",
     "Orchestration", INK),
]
for i, (title, desc, tag, c) in enumerate(flow):
    x = Inches(0.75) + i * (box_w + Inches(0.65))
    rect(s, x, by, box_w, box_h, WHITE, c, 2, rounded=True)
    rect(s, x, by, box_w, Inches(0.1), c)
    text(s, tag.upper(), x + Inches(0.3), by + Inches(0.3),
         box_w - Inches(0.6), Inches(0.3), size=10, color=c,
         bold=True, font="Consolas")
    text(s, title, x + Inches(0.3), by + Inches(0.65),
         box_w - Inches(0.6), Inches(0.5), size=22, color=c, bold=True)
    text(s, desc, x + Inches(0.3), by + Inches(1.3),
         box_w - Inches(0.6), Inches(0.9), size=12, color=INK_2, spacing=1.4)
    if i < 2:
        text(s, "→", x + box_w + Inches(0.08), by + Inches(0.9),
             Inches(0.5), Inches(0.6), size=32, color=c, bold=True,
             align=PP_ALIGN.CENTER)

# DB strip
rect(s, Inches(0.75), Inches(5.5), Inches(11.85), Inches(1.5),
     RED_NIGHT, None, 0, rounded=True)
text(s, "DATABASE — 8 TABLES", Inches(1.05), Inches(5.7),
     Inches(4), Inches(0.3), size=10, color=GOLD, bold=True, font="Consolas")
tables = ["Users", "Donors", "BloodRequests", "DonationOffers",
          "ContactMessages", "+3 Identity"]
tx = Inches(1.05)
for t in tables:
    tw = Inches(1.85)
    pill(s, t, tx, Inches(6.2), tw, Inches(0.42), RED_DEEP, WHITE, 11)
    tx += tw + Inches(0.1)

pageno(s, 9); footer(s)

# ============================================================
# SLIDE 10 — DATA MODEL (ER DIAGRAM)
# ============================================================
s = prs.slides.add_slide(BLANK)
bg(s, CREAM)

pill(s, "DATA MODEL", Inches(0.75), Inches(0.6), Inches(2), Inches(0.38),
     RED, WHITE, 11)
text(s, "Entity relationships.", Inches(0.75), Inches(1.2),
     Inches(11), Inches(0.8), size=38, color=INK, bold=True)
text(s, "One user, one donor. Many requests, many offers.",
     Inches(0.75), Inches(2.0), Inches(11), Inches(0.5),
     size=15, color=MUTED, italic=True)

# Entity cards
def entity(x, y, w, h, title, fields, color):
    rect(s, x, y, w, h, WHITE, color, 2, rounded=True)
    rect(s, x, y, w, Inches(0.45), color)
    text(s, title, x + Inches(0.15), y + Inches(0.08),
         w - Inches(0.3), Inches(0.3), size=13, color=WHITE, bold=True)
    bullets(s, fields, x + Inches(0.15), y + Inches(0.55),
            w - Inches(0.3), h - Inches(0.6), size=10, color=INK_2,
            bullet_char="·", line_spacing=1.3)

# Row 1
entity(Inches(0.75), Inches(2.8), Inches(3.6), Inches(2), "AppUser",
       ["Id (PK)", "Email · FullName", "IsBanned · CreatedAt",
        "Roles: SuperAdmin/Admin/User"], RED)

entity(Inches(4.85), Inches(2.8), Inches(3.6), Inches(2), "Donor",
       ["DonorId (PK)", "UserId (FK → AppUser)",
        "Name · Age · BloodGroup", "State · City · RowVersion"], GOLD)

entity(Inches(8.95), Inches(2.8), Inches(3.6), Inches(2), "BloodRequest",
       ["RequestId (PK)", "UserId (FK → AppUser)",
        "BloodGroup · Urgency", "Status · FulfilledByDonorId"], BLUE)

# Row 2
entity(Inches(2.8), Inches(5.1), Inches(3.6), Inches(1.9), "DonationOffer",
       ["Id (PK)", "RequestId (FK)",
        "DonorId (FK)", "Status: Pledged→Accepted→Completed",
        "UNIQUE (RequestId, DonorId)"], GREEN)

entity(Inches(7.1), Inches(5.1), Inches(3.6), Inches(1.9), "ContactMessage",
       ["Id (PK)", "Name · Email", "Subject · Message",
        "IsRead · CreatedAt"], PURPLE)

pageno(s, 10); footer(s)

# ============================================================
# SLIDE 11 — SECTION 04: SIGNATURE FEATURES
# ============================================================
section_divider("04", "Signature Features",
                "Three features that make BloodConnect stand out from the crowd.")

# ============================================================
# SLIDE 12 — REAL-TIME NOTIFICATIONS
# ============================================================
s = prs.slides.add_slide(BLANK)
bg(s, RED_NIGHT)

pill(s, "★ SIGNATURE FEATURE 01", Inches(0.75), Inches(0.6), Inches(3),
     Inches(0.38), GOLD, RED_NIGHT, 11)
text(s, "Real-Time Notifications", Inches(0.75), Inches(1.2),
     Inches(11), Inches(0.85), size=42, color=WHITE, bold=True)
text(s, "WebSocket-powered instant alerts — zero polling, zero refresh.",
     Inches(0.75), Inches(2.15), Inches(11), Inches(0.5),
     size=16, color=RED_BRIGHT, italic=True)

# Flow diagram
flow_items = [
    ("WRITE",       "New request posted",       RED),
    ("PUBLISH",     "SignalR Hub broadcast",    GOLD),
    ("DELIVER",     "WebSocket to client",      BLUE),
    ("REACT",       "Bell + Toast + Sound",     GREEN),
]
fw = Inches(2.7); fh = Inches(1.9); fy = Inches(3.2)
for i, (title, desc, c) in enumerate(flow_items):
    x = Inches(0.75) + i * (fw + Inches(0.35))
    rect(s, x, fy, fw, fh, RED_DEEP, c, 2, rounded=True)
    text(s, f"0{i+1}", x + Inches(0.15), fy + Inches(0.15),
         Inches(1), Inches(0.4), size=14, color=c, bold=True, font="Consolas")
    text(s, title, x + Inches(0.15), fy + Inches(0.6),
         fw - Inches(0.3), Inches(0.4), size=18, color=c, bold=True,
         font="Consolas")
    text(s, desc, x + Inches(0.15), fy + Inches(1.15),
         fw - Inches(0.3), Inches(0.6), size=11,
         color=RGBColor(0xCC, 0xBB, 0xBB), spacing=1.3)
    if i < 3:
        text(s, "→", x + fw + Inches(0.05), fy + Inches(0.7),
             Inches(0.3), Inches(0.5), size=24, color=GOLD, bold=True,
             align=PP_ALIGN.CENTER)

# Benefits grid
benefits = [
    ("⚡ Instant", "Sub-100ms delivery over WebSocket", GREEN),
    ("🔋 Zero Poll", "No periodic AJAX — saves bandwidth", BLUE),
    ("🔄 Auto-Retry", "Exponential backoff reconnect", GOLD),
    ("💾 Cached", "60s IMemoryCache fallback", PURPLE),
]
bw = Inches(2.9); by = Inches(5.5)
for i, (title, desc, c) in enumerate(benefits):
    x = Inches(0.75) + i * (bw + Inches(0.15))
    rect(s, x, by, bw, Inches(1.2), RED_DEEP, None, 0, rounded=True)
    circle(s, x + Inches(0.15), by + Inches(0.18), Inches(0.14), Inches(0.14), c)
    text(s, title, x + Inches(0.4), by + Inches(0.15),
         bw - Inches(0.5), Inches(0.4), size=14, color=WHITE, bold=True)
    text(s, desc, x + Inches(0.15), by + Inches(0.65),
         bw - Inches(0.3), Inches(0.5), size=10,
         color=RGBColor(0xAA, 0x99, 0x99), spacing=1.25)

pageno(s, 12); footer(s, RGBColor(0x77, 0x55, 0x55))

# ============================================================
# SLIDE 13 — BLOOD COMPATIBILITY (FIXED OVERFLOW)
# ============================================================
s = prs.slides.add_slide(BLANK)
bg(s, CREAM)

pill(s, "★ SIGNATURE FEATURE 02", Inches(0.75), Inches(0.6), Inches(3),
     Inches(0.38), GOLD, WHITE, 11)
text(s, "Blood Compatibility", Inches(0.75), Inches(1.2),
     Inches(8), Inches(0.85), size=42, color=INK, bold=True)
text(s, "Medical accuracy built into every search.",
     Inches(0.75), Inches(2.15), Inches(8), Inches(0.5),
     size=16, color=MUTED, italic=True)

# Left — key facts
facts = [
    ("O−",  "Universal donor",       "Can donate to all 8 groups",  RED),
    ("AB+", "Universal receiver",    "Can receive from all 8 groups", GOLD),
    ("A+",  "Most common (India)",   "~30% of population",           RED_DARK),
    ("B+",  "Second most common",    "~24% of population",           INK),
]
fy = Inches(2.95)
for grp, label, detail, c in facts:
    circle(s, Inches(0.9), fy, Inches(0.75), Inches(0.75), c)
    text(s, grp, Inches(0.9), fy + Inches(0.15), Inches(0.75), Inches(0.5),
         size=18, color=WHITE, bold=True, align=PP_ALIGN.CENTER, font="Consolas")
    text(s, label, Inches(1.85), fy + Inches(0.08), Inches(5), Inches(0.4),
         size=17, color=INK, bold=True)
    text(s, detail, Inches(1.85), fy + Inches(0.45), Inches(5), Inches(0.35),
         size=12, color=MUTED)
    fy += Inches(1.0)

# Right — matrix card (FITTED)
card_x = Inches(7.4)
card_y = Inches(2.7)
card_w = Inches(5.3)
card_h = Inches(4.4)
rect(s, card_x, card_y, card_w, card_h, WHITE, LINE, 1, rounded=True)
rect(s, card_x, card_y, card_w, Inches(0.08), RED)

text(s, "RED CELL COMPATIBILITY MATRIX", card_x + Inches(0.3), card_y + Inches(0.25),
     card_w - Inches(0.6), Inches(0.3), size=10, color=RED,
     bold=True, font="Consolas")

# Matrix — careful sizing
groups = ["O−", "O+", "A−", "A+", "B−", "B+", "AB−", "AB+"]
cell = Inches(0.44)  # reduced from 0.52
mx = card_x + Inches(0.85)   # start of grid data
my = card_y + Inches(0.85)   # start of grid data

# Header
for i, g in enumerate(groups):
    text(s, g, mx + i * cell, my - Inches(0.35), cell, Inches(0.35),
         size=9, color=RED, bold=True, align=PP_ALIGN.CENTER, font="Consolas")

# Rows
matrix = [
    [1,0,0,0,0,0,0,0],
    [1,1,0,0,0,0,0,0],
    [1,0,1,0,0,0,0,0],
    [1,1,1,1,0,0,0,0],
    [1,0,0,0,1,0,0,0],
    [1,1,0,0,1,1,0,0],
    [1,0,1,0,1,0,1,0],
    [1,1,1,1,1,1,1,1],
]
for r_idx, row in enumerate(matrix):
    # Row label
    text(s, groups[r_idx], mx - Inches(0.6),
         my + r_idx * cell + Inches(0.05), Inches(0.5), Inches(0.35),
         size=9, color=RED, bold=True, align=PP_ALIGN.RIGHT, font="Consolas")
    for c_idx, val in enumerate(row):
        cx = mx + c_idx * cell
        cy = my + r_idx * cell
        color = RED if val else RGBColor(0xEE, 0xE7, 0xE0)
        circle(s, cx + Inches(0.06), cy + Inches(0.06),
               cell - Inches(0.12), cell - Inches(0.12), color)

# Caption
text(s, "Rows = Donors  ·  Columns = Receivers",
     card_x, my + 8 * cell + Inches(0.15), card_w, Inches(0.3),
     size=10, color=MUTED, align=PP_ALIGN.CENTER, italic=True, font="Consolas")

pageno(s, 13); footer(s)

# ============================================================
# SLIDE 14 — PLEDGE WORKFLOW
# ============================================================
s = prs.slides.add_slide(BLANK)
bg(s, CREAM)

pill(s, "★ SIGNATURE FEATURE 03", Inches(0.75), Inches(0.6), Inches(3),
     Inches(0.38), GOLD, WHITE, 11)
text(s, "Pledge-Based Workflow", Inches(0.75), Inches(1.2),
     Inches(11), Inches(0.85), size=42, color=INK, bold=True)
text(s, "Two-way confirmation prevents fake fulfillments.",
     Inches(0.75), Inches(2.15), Inches(11), Inches(0.5),
     size=16, color=MUTED, italic=True)

steps = [
    ("01", "PLEDGE",   "Donor clicks\n\"I can donate\"",   RED),
    ("02", "ACCEPT",   "Owner reviews\noffers",            GOLD),
    ("03", "COMPLETE", "Donation marked\ncomplete",        RED_DARK),
    ("04", "FULFILL",  "Request → Fulfilled\nLives saved", GREEN),
]

sw = Inches(2.9); sh = Inches(3.4); sy = Inches(3.05)
for i, (num, title, desc, c) in enumerate(steps):
    x = Inches(0.75) + i * (sw + Inches(0.18))
    rect(s, x, sy, sw, sh, WHITE, LINE, 1, rounded=True)
    rect(s, x, sy, sw, Inches(0.1), c)
    text(s, num, x + Inches(0.3), sy + Inches(0.3), Inches(1.5),
         Inches(0.75), size=36, color=c, bold=True, font="Consolas")
    text(s, title, x + Inches(0.3), sy + Inches(1.2),
         sw - Inches(0.6), Inches(0.5), size=18, color=c, bold=True,
         font="Consolas")
    rect(s, x + Inches(0.3), sy + Inches(1.75), Inches(0.5),
         Inches(0.06), c)
    text(s, desc, x + Inches(0.3), sy + Inches(2.0),
         sw - Inches(0.6), Inches(1.2), size=14, color=INK_2, spacing=1.5)
    if i < 3:
        text(s, "→", x + sw + Inches(0.02), sy + Inches(1.4),
             Inches(0.2), Inches(0.5), size=28, color=c, bold=True,
             align=PP_ALIGN.CENTER)

# Status flow bar
rect(s, Inches(0.75), Inches(6.75), Inches(11.85), Inches(0.5),
     RED_SOFT, None, 0, rounded=True)
rect(s, Inches(0.75), Inches(6.75), Inches(0.1), Inches(0.5), RED)
text(s, "STATUS FLOW:   Pledged   →   Accepted   →   Completed   →   Fulfilled",
     Inches(1.0), Inches(6.87), Inches(11.5), Inches(0.3),
     size=11, color=RED_DARK, bold=True, font="Consolas")

pageno(s, 14); footer(s)

# ============================================================
# SLIDE 15 — ROLE HIERARCHY
# ============================================================
s = prs.slides.add_slide(BLANK)
bg(s, CREAM)

pill(s, "AUTHORIZATION", Inches(0.75), Inches(0.6), Inches(2.4), Inches(0.38),
     RED, WHITE, 11)
text(s, "Three-tier role system.", Inches(0.75), Inches(1.2),
     Inches(11), Inches(0.85), size=42, color=INK, bold=True)
text(s, "Enforced on every request — server-side only.",
     Inches(0.75), Inches(2.15), Inches(11), Inches(0.5),
     size=16, color=MUTED, italic=True)

# Role cards (stacked pyramid)
pyramid = [
    ("SuperAdmin", "Immutable · Cannot be banned or demoted", GOLD,
     "Full system control", "Owns the platform"),
    ("Admin", "Can manage users below · Moderate content", RED_DARK,
     "Ban regular users", "Promote to Admin"),
    ("User", "Basic access · Own profile control", INK,
     "Post requests", "Pledge to donate"),
]
for i, (role, desc, c, t1, t2) in enumerate(pyramid):
    w = Inches(8.5) - i * Inches(1.2)
    x = Inches(0.75) + Inches(0.6) * i
    y = Inches(3.05) + i * Inches(1.25)
    rect(s, x, y, w, Inches(1.1), WHITE, c, 2, rounded=True)
    rect(s, x, y, Inches(0.12), Inches(1.1), c)
    text(s, role, x + Inches(0.3), y + Inches(0.15),
         Inches(2.5), Inches(0.5), size=20, color=c, bold=True)
    text(s, desc, x + Inches(0.3), y + Inches(0.6),
         w - Inches(0.5), Inches(0.4), size=12, color=INK_2)
    text(s, t1, x + w - Inches(3.6), y + Inches(0.2),
         Inches(3.4), Inches(0.35), size=12, color=MUTED,
         align=PP_ALIGN.RIGHT)
    text(s, t2, x + w - Inches(3.6), y + Inches(0.58),
         Inches(3.4), Inches(0.35), size=12, color=MUTED,
         align=PP_ALIGN.RIGHT)

pageno(s, 15); footer(s)

# ============================================================
# SLIDE 16 — SECTION 05: LIVE SCREENSHOTS
# ============================================================
section_divider("05", "Live Screenshots",
                "Real evidence from the production deployment.")

# ============================================================
# SLIDE 17 — HOMEPAGE HERO (BIG)
# ============================================================
s = prs.slides.add_slide(BLANK)
bg(s, RED_NIGHT)

pill(s, "PRODUCTION", Inches(0.75), Inches(0.6), Inches(1.9), Inches(0.38),
     GOLD, RED_NIGHT, 11)
text(s, "Homepage — the first impression.", Inches(0.75), Inches(1.15),
     Inches(11), Inches(0.7), size=38, color=WHITE, bold=True)

# Big image centered
box_x = Inches(0.75)
box_y = Inches(2.15)
box_w = Inches(11.85)
box_h = Inches(4.7)
rect(s, box_x, box_y, box_w, box_h, RED_DEEP, GOLD, 2, rounded=True)

if os.path.exists(IMG["homepage"]):
    iw, ih = scaled_dims(IMG["homepage"], box_w - Inches(0.3), box_h - Inches(0.3))
    ix = box_x + (box_w - iw) // 2
    iy = box_y + (box_h - ih) // 2
    s.shapes.add_picture(IMG["homepage"], ix, iy, width=iw, height=ih)

text(s, "Cinematic hero · Live stats · Blood compatibility chart · Search widget",
     Inches(0.75), Inches(6.95), Inches(11.85), Inches(0.3),
     size=13, color=RGBColor(0xCC, 0xBB, 0xBB),
     align=PP_ALIGN.CENTER, italic=True)

pageno(s, 17); footer(s, RGBColor(0x77, 0x55, 0x55))

# ============================================================
# SLIDE 18 — PUBLIC PAGES (3-grid)
# ============================================================
s = prs.slides.add_slide(BLANK)
bg(s, CREAM)

pill(s, "PUBLIC PAGES", Inches(0.75), Inches(0.6), Inches(2.2), Inches(0.38),
     RED, WHITE, 11)
text(s, "Core public experience.", Inches(0.75), Inches(1.2),
     Inches(11), Inches(0.85), size=42, color=INK, bold=True)

grid = [
    (IMG["donor_list"], "Donor List",           "Verified profiles with availability", RED),
    (IMG["search"],     "Compatibility Search", "O−/AB+ medical logic in action",      GOLD),
    (IMG["requests"],   "Blood Requests",       "Filter by group, urgency, state",     BLUE),
]
cw = Inches(3.9); ch = Inches(2.4); gy = Inches(2.6)
for i, (path, title, desc, c) in enumerate(grid):
    x = Inches(0.75) + i * (cw + Inches(0.2))
    image_in_card(s, path, x, gy, cw, ch, title, desc, c)

pageno(s, 18); footer(s)

# ============================================================
# SLIDE 19 — AUTH PAGES (3-grid)
# ============================================================
s = prs.slides.add_slide(BLANK)
bg(s, CREAM)

pill(s, "AUTHENTICATION", Inches(0.75), Inches(0.6), Inches(2.4),
     Inches(0.38), RED, WHITE, 11)
text(s, "Secure by design.", Inches(0.75), Inches(1.2),
     Inches(11), Inches(0.85), size=42, color=INK, bold=True)

grid = [
    (IMG["register"],    "Register",        "ConfirmPassword + AcceptTerms",  RED),
    (IMG["login"],       "Login",           "Cookie session · 7-day sliding", GOLD),
    (IMG["login_error"], "Login Error",     "Invalid credentials handling",   ORANGE),
]
cw = Inches(3.9); ch = Inches(2.4); gy = Inches(2.6)
for i, (path, title, desc, c) in enumerate(grid):
    x = Inches(0.75) + i * (cw + Inches(0.2))
    image_in_card(s, path, x, gy, cw, ch, title, desc, c)

pageno(s, 19); footer(s)

# ============================================================
# SLIDE 20 — USER WORKFLOW (3-grid)
# ============================================================
s = prs.slides.add_slide(BLANK)
bg(s, CREAM)

pill(s, "DONOR WORKFLOW", Inches(0.75), Inches(0.6), Inches(2.6),
     Inches(0.38), RED, WHITE, 11)
text(s, "From registration to donation.", Inches(0.75), Inches(1.2),
     Inches(11), Inches(0.85), size=42, color=INK, bold=True)

grid = [
    (IMG["create_form"], "Donor Registration", "State dropdown + validations", RED),
    (IMG["dashboard"],   "Personal Dashboard", "Profile, requests, offers, stats", GOLD),
    (IMG["offer_pledge"],"Offer Pledge",       "One-click \"I can donate\"", GREEN),
]
cw = Inches(3.9); ch = Inches(2.4); gy = Inches(2.6)
for i, (path, title, desc, c) in enumerate(grid):
    x = Inches(0.75) + i * (cw + Inches(0.2))
    image_in_card(s, path, x, gy, cw, ch, title, desc, c)

pageno(s, 20); footer(s)

# ============================================================
# SLIDE 21 — ADMIN PANEL (3-grid)
# ============================================================
s = prs.slides.add_slide(BLANK)
bg(s, CREAM)

pill(s, "ADMIN PANEL", Inches(0.75), Inches(0.6), Inches(2), Inches(0.38),
     RED, WHITE, 11)
text(s, "Full control center.", Inches(0.75), Inches(1.2),
     Inches(11), Inches(0.85), size=42, color=INK, bold=True)

grid = [
    (IMG["admin_dash"],  "Admin Dashboard",  "Real-time stats + recent activity", RED),
    (IMG["admin_users"], "User Management",  "Ban · Promote · Delete",            GOLD),
    (IMG["admin_msgs"],  "Messages Inbox",   "Contact form submissions",          PURPLE),
]
cw = Inches(3.9); ch = Inches(2.4); gy = Inches(2.6)
for i, (path, title, desc, c) in enumerate(grid):
    x = Inches(0.75) + i * (cw + Inches(0.2))
    image_in_card(s, path, x, gy, cw, ch, title, desc, c)

pageno(s, 21); footer(s)

# ============================================================
# SLIDE 22 — API TESTING (2×2)
# ============================================================
s = prs.slides.add_slide(BLANK)
bg(s, CREAM)

pill(s, "API TESTING", Inches(0.75), Inches(0.6), Inches(2), Inches(0.38),
     RED, WHITE, 11)
text(s, "Real evidence from Postman.", Inches(0.75), Inches(1.2),
     Inches(11), Inches(0.85), size=42, color=INK, bold=True)

grid = [
    (IMG["pm_get"],    "GET /api/donor",            "200 OK · 4 donors",        GREEN),
    (IMG["pm_search"], "GET /api/donor/search",     "Compatibility-aware",      GOLD),
    (IMG["pm_401"],    "POST /api/donor (no auth)", "401 Unauthorized",         RED),
    (IMG["swagger"],   "Swagger UI",                "Interactive API docs",     BLUE),
]
cw = Inches(5.9); ch = Inches(2.1); gy = Inches(2.55)
for i, (path, title, desc, c) in enumerate(grid):
    col = i % 2; row = i // 2
    x = Inches(0.75) + col * (cw + Inches(0.15))
    y = gy + row * (ch + Inches(0.65))
    image_in_card(s, path, x, y, cw, ch, title, desc, c)

pageno(s, 22); footer(s)

# ============================================================
# SLIDE 23 — API ENDPOINTS + SWAGGER
# ============================================================
s = prs.slides.add_slide(BLANK)
bg(s, RED_NIGHT)

pill(s, "REST API", Inches(0.75), Inches(0.6), Inches(1.7), Inches(0.38),
     RED, WHITE, 11)
text(s, "18+ endpoints. Live-testable.", Inches(0.75), Inches(1.2),
     Inches(11), Inches(0.85), size=42, color=WHITE, bold=True)
text(s, "GET · POST · PUT · DELETE — full CRUD + Auth",
     Inches(0.75), Inches(2.15), Inches(11), Inches(0.5),
     size=16, color=RED_BRIGHT, italic=True)

endpoints = [
    ("GET",    "/api/donor",              "List donors",     GREEN),
    ("GET",    "/api/donor/{id}",         "Single donor",    GREEN),
    ("GET",    "/api/donor/search",       "Compat search",   GOLD),
    ("POST",   "/api/donor",              "Create donor",    RED),
    ("PUT",    "/api/donor/{id}",         "Update donor",    ORANGE),
    ("DELETE", "/api/donor/{id}",         "Delete donor",    RED_DARK),
    ("POST",   "/api/auth/login",         "API login",       RED),
    ("GET",    "/api/auth/me",            "Current user",    GREEN),
]

y = Inches(3.05)
for method, path, desc, mc in endpoints:
    pill(s, method, Inches(0.75), y, Inches(0.9), Inches(0.34), mc, WHITE, 9)
    text(s, path, Inches(1.8), y + Inches(0.03), Inches(4.5), Inches(0.3),
         size=13, color=WHITE, bold=True, font="Consolas")
    text(s, desc, Inches(6.3), y + Inches(0.05), Inches(3), Inches(0.3),
         size=12, color=RGBColor(0x99, 0x88, 0x88))
    y += Inches(0.45)

# Right checklist
rect(s, Inches(9.4), Inches(2.9), Inches(3.2), Inches(3.7),
     RED_DEEP, None, 0, rounded=True)
text(s, "WHY IT'S SOLID", Inches(9.65), Inches(3.1), Inches(3), Inches(0.3),
     size=10, color=GOLD, bold=True, font="Consolas")
checks = [
    "Proper HTTP verbs",
    "Status codes 200-404",
    "DTO pattern — privacy",
    "Owner + Admin checks",
    "Swagger live testing",
    "Postman-compatible",
]
cy2 = Inches(3.6)
for c in checks:
    circle(s, Inches(9.65), cy2 + Inches(0.09), Inches(0.12), Inches(0.12), GREEN)
    text(s, c, Inches(9.9), cy2, Inches(2.6), Inches(0.35),
         size=12, color=WHITE)
    cy2 += Inches(0.44)

pageno(s, 23); footer(s, RGBColor(0x77, 0x55, 0x55))

# ============================================================
# SLIDE 24 — SECTION 06: DEMO
# ============================================================
section_divider("06", "Live Demo",
                "Everything you've seen — running right now, in production.")

# ============================================================
# SLIDE 25 — LIVE DEMO DETAILS
# ============================================================
s = prs.slides.add_slide(BLANK)
bg(s, RED)

ghost(s, "★", Inches(9.6), Inches(0.4), size=300, color=RED_DARK)

pill(s, "LIVE DEMO", Inches(0.85), Inches(0.85), Inches(1.9), Inches(0.38),
     GOLD, RED, 11)
text(s, "It's live. Right now.", Inches(0.85), Inches(1.65),
     Inches(11), Inches(0.95), size=58, color=WHITE, bold=True)
rect(s, Inches(0.9), Inches(3.05), Inches(2.2), Inches(0.12), GOLD)

# URL card
rect(s, Inches(0.85), Inches(3.5), Inches(11.65), Inches(1.4),
     RED_DARK, GOLD, 2, rounded=True)
text(s, "LIVE URL", Inches(1.25), Inches(3.7), Inches(4), Inches(0.3),
     size=11, color=GOLD, bold=True, font="Consolas")
text(s, "bloodconnector.runasp.net", Inches(1.25), Inches(4.05),
     Inches(11), Inches(0.7), size=34, color=WHITE, bold=True, font="Consolas")

# Credentials
text(s, "DEMO CREDENTIALS", Inches(0.85), Inches(5.3), Inches(6), Inches(0.35),
     size=11, color=GOLD, bold=True, font="Consolas")
text(s, "admin@bloodconnect.com", Inches(0.85), Inches(5.75),
     Inches(6), Inches(0.45), size=18, color=WHITE, font="Consolas", bold=True)
text(s, "Admin@123", Inches(0.85), Inches(6.25),
     Inches(6), Inches(0.45), size=18, color=WHITE, font="Consolas", bold=True)

# Deploy info
text(s, "DEPLOYED ON", Inches(7.4), Inches(5.3), Inches(5), Inches(0.35),
     size=11, color=GOLD, bold=True, font="Consolas", align=PP_ALIGN.RIGHT)
text(s, "MonsterASP.NET", Inches(7.4), Inches(5.75), Inches(5.1),
     Inches(0.45), size=18, color=WHITE, bold=True, font="Consolas",
     align=PP_ALIGN.RIGHT)
text(s, "HTTPS  ·  Let's Encrypt  ·  Auto-deploy",
     Inches(7.4), Inches(6.25), Inches(5.1),
     Inches(0.4), size=12, color=RGBColor(0xFF, 0xCC, 0xCC),
     align=PP_ALIGN.RIGHT)

# ============================================================
# SLIDE 26 — IMPACT / KPIs
# ============================================================
s = prs.slides.add_slide(BLANK)
bg(s, CREAM)

pill(s, "IMPACT", Inches(0.75), Inches(0.6), Inches(1.6), Inches(0.38),
     RED, WHITE, 11)
text(s, "Real numbers. Real promise.", Inches(0.75), Inches(1.2),
     Inches(11), Inches(0.85), size=42, color=INK, bold=True)

kpis = [
    ("3",    "Lives saved",       "per single donation",     RED),
    ("8",    "Blood groups",      "compatibility aware",     GOLD),
    ("18+",  "API endpoints",     "RESTful + documented",    BLUE),
    ("100%", "Free",              "zero cost, forever",      GREEN),
]
kw = Inches(2.9); kh = Inches(2.9); ky = Inches(2.7)
for i, (val, label, sub, c) in enumerate(kpis):
    x = Inches(0.75) + i * (kw + Inches(0.2))
    rect(s, x, ky, kw, kh, WHITE, LINE, 1, rounded=True)
    rect(s, x, ky, kw, Inches(0.1), c)
    text(s, val, x + Inches(0.3), ky + Inches(0.6), kw - Inches(0.6),
         Inches(1.1), size=58, color=c, bold=True)
    text(s, label, x + Inches(0.3), ky + Inches(1.7), kw - Inches(0.6),
         Inches(0.45), size=17, color=INK, bold=True)
    text(s, sub, x + Inches(0.3), ky + Inches(2.2), kw - Inches(0.6),
         Inches(0.55), size=12, color=MUTED, spacing=1.3)

# Quote
rect(s, Inches(0.75), Inches(6.0), Inches(11.85), Inches(1.0),
     RED_SOFT, None, 0, rounded=True)
rect(s, Inches(0.75), Inches(6.0), Inches(0.12), Inches(1.0), RED)
text(s, '"One donation can save up to three lives. The only thing standing between a patient',
     Inches(1.1), Inches(6.15), Inches(11.3), Inches(0.35),
     size=14, color=INK, italic=True)
text(s, 'and a donor is a network. Help us build it."',
     Inches(1.1), Inches(6.5), Inches(11.3), Inches(0.35),
     size=14, color=INK, italic=True)

pageno(s, 26); footer(s)

# ============================================================
# SLIDE 27 — FUTURE SCOPE
# ============================================================
s = prs.slides.add_slide(BLANK)
bg(s, CREAM)

pill(s, "FUTURE SCOPE", Inches(0.75), Inches(0.6), Inches(2.2), Inches(0.38),
     RED, WHITE, 11)
text(s, "What's next.", Inches(0.75), Inches(1.2),
     Inches(11), Inches(0.85), size=42, color=INK, bold=True)
text(s, "The roadmap from MVP to platform.",
     Inches(0.75), Inches(2.15), Inches(11), Inches(0.5),
     size=16, color=MUTED, italic=True)

items = [
    ("Q1 2027", "Mobile app",        "React Native / Flutter",       RED),
    ("Q2 2027", "Hospital API",      "Direct request integration",   GOLD),
    ("Q3 2027", "Notifications",     "Email (SendGrid) + SMS",       GREEN),
    ("Q4 2027", "Analytics",         "Chart.js admin dashboards",    BLUE),
    ("2028",    "Multi-language",    "Hindi · Gujarati · English",   PURPLE),
    ("2028",    "Map-based search",  "Google Maps donor view",       ORANGE),
]

start_y = Inches(2.85)
line_x = Inches(2.85)
rect(s, line_x, start_y + Inches(0.15), Inches(0.03),
     Inches(4.4), RGBColor(0xDD, 0xD5, 0xCA))

for i, (q, title, desc, c) in enumerate(items):
    y = start_y + i * Inches(0.75)
    circle(s, line_x - Inches(0.09), y + Inches(0.1),
           Inches(0.2), Inches(0.2), c)
    text(s, q, Inches(0.75), y + Inches(0.03), Inches(1.9),
         Inches(0.4), size=14, color=c, bold=True, font="Consolas",
         align=PP_ALIGN.RIGHT)
    text(s, title, Inches(3.3), y, Inches(3), Inches(0.45),
         size=17, color=INK, bold=True)
    text(s, desc, Inches(6.6), y + Inches(0.03), Inches(6), Inches(0.4),
         size=13, color=MUTED)

pageno(s, 27); footer(s)

# ============================================================
# SLIDE 28 — THANK YOU (REDESIGNED)
# ============================================================
s = prs.slides.add_slide(BLANK)
bg(s, RED_NIGHT)

# Decorations
circle(s, Inches(-1.8), Inches(-1.8), Inches(4.5), Inches(4.5), RED_DARK)
circle(s, Inches(11), Inches(5.3), Inches(4.5), Inches(4.5), RED_DEEP)

# Big blood drop
circle(s, Inches(5.95), Inches(0.9), Inches(1.4), Inches(1.4), RED)
circle(s, Inches(6.35), Inches(1.2), Inches(0.35), Inches(0.35), RED_BRIGHT)

# Big "Thank You"
text(s, "Thank You", Inches(0.7), Inches(2.9), Inches(12), Inches(1.4),
     size=105, color=WHITE, bold=True, align=PP_ALIGN.CENTER)

# Gold underline
rect(s, Inches(6.16), Inches(4.4), Inches(1), Inches(0.08), GOLD)

# Tagline
text(s, "Every drop counts.", Inches(0.7), Inches(4.65), Inches(12),
     Inches(0.7), size=30, color=GOLD, italic=True, align=PP_ALIGN.CENTER)

# 3 Info Cards at bottom (BOLD, REDESIGNED)
card_y = Inches(5.65)
card_h = Inches(1.15)
card_w = Inches(3.8)
gap = Inches(0.18)
total_w = card_w * 3 + gap * 2
start_x = (SW - total_w) // 2

info_cards = [
    ("LIVE WEBSITE", "bloodconnector.runasp.net", RED),
    ("SOURCE CODE",  "github.com/rajputpri/BloodConnector", GOLD),
    ("PRESENTED BY", "Prince Rajput  ·  BCA Sem-7", GREEN),
]

for i, (label, value, c) in enumerate(info_cards):
    x = start_x + i * (card_w + gap)
    rect(s, x, card_y, card_w, card_h, RED_DEEP, c, 1.5, rounded=True)
    rect(s, x, card_y, Inches(0.1), card_h, c)

    text(s, label, x + Inches(0.3), card_y + Inches(0.15),
         card_w - Inches(0.5), Inches(0.3), size=10, color=c,
         bold=True, font="Consolas")
    text(s, value, x + Inches(0.3), card_y + Inches(0.5),
         card_w - Inches(0.5), Inches(0.5), size=13, color=WHITE,
         bold=True, font="Inter")

# ==================== SAVE ====================
output = "BloodConnect-PPT.pptx"
prs.save(output)

print()
print("=" * 60)
print(f"  ✅ SUCCESS! PPT created: {output}")
print(f"  📊 Total slides: {len(prs.slides)}")
print("=" * 60)
print()
print("📋 SLIDE BREAKDOWN:")
print("   01. Hero Title")
print("   02. Agenda / TOC")
print("   03. Section: The Problem")
print("   04. Problem Stats + Chart")
print("   05. Section: Our Solution")
print("   06. Solution — 3 Roles")
print("   07. Section: Tech Stack")
print("   08. Tech Grid (8 tiles)")
print("   09. Architecture — MVC Flow")
print("   10. Data Model — ER Diagram")
print("   11. Section: Signature Features")
print("   12. ★ Real-Time Notifications")
print("   13. ★ Blood Compatibility Matrix")
print("   14. ★ Pledge Workflow")
print("   15. Role Hierarchy")
print("   16. Section: Live Screenshots")
print("   17. Homepage Hero (BIG)")
print("   18. Public Pages (3-grid)")
print("   19. Authentication (3-grid)")
print("   20. Donor Workflow (3-grid)")
print("   21. Admin Panel (3-grid)")
print("   22. API Testing (2×2)")
print("   23. API Endpoints + Swagger")
print("   24. Section: Live Demo")
print("   25. Live Demo Details")
print("   26. Impact / KPIs")
print("   27. Future Scope")
print("   28. Thank You (REDESIGNED)")
print()
print("🎬 NEXT STEPS:")
print("   1. Open BloodConnect-PPT.pptx in PowerPoint")
print("   2. Press F5 for slideshow")
print("   3. For morph transitions:")
print("      • Ctrl+A (select all slides)")
print("      • Transitions tab → Morph")
print("      • Duration: 2.00s")
print("      • Apply To All")