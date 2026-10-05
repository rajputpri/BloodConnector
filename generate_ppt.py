"""
BloodConnect — Premium PPT Generator
Run: python generate_ppt.py
Output: BloodConnect-PPT.pptx (15 slides, magazine-style)
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION

# ==================== COLORS ====================
RED         = RGBColor(0xDC, 0x26, 0x26)
RED_DARK    = RGBColor(0x99, 0x1B, 0x1B)
RED_DEEP    = RGBColor(0x45, 0x0A, 0x0A)
RED_NIGHT   = RGBColor(0x1A, 0x0E, 0x0E)
RED_SOFT    = RGBColor(0xFE, 0xF2, 0xF2)
GOLD        = RGBColor(0xD4, 0xA2, 0x4C)
GOLD_SOFT   = RGBColor(0xF5, 0xE6, 0xC5)
CREAM       = RGBColor(0xFA, 0xF7, 0xF2)
CREAM_2     = RGBColor(0xF5, 0xEF, 0xE6)
WHITE       = RGBColor(0xFF, 0xFF, 0xFF)
INK         = RGBColor(0x1A, 0x14, 0x14)
INK_2       = RGBColor(0x3D, 0x2E, 0x2E)
MUTED       = RGBColor(0x7A, 0x6D, 0x6D)
LINE        = RGBColor(0xEA, 0xE3, 0xD8)

# ==================== PRESENTATION ====================
prs = Presentation()
prs.slide_width  = Inches(13.333)
prs.slide_height = Inches(7.5)
SW, SH = prs.slide_width, prs.slide_height
BLANK = prs.slide_layouts[6]

# ==================== HELPERS ====================

def bg(slide, color):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = color

def rect(slide, left, top, w, h, fill_color=None, line_color=None, line_w=0, rounded=False):
    shape = MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE
    s = slide.shapes.add_shape(shape, left, top, w, h)
    if fill_color:
        s.fill.solid()
        s.fill.fore_color.rgb = fill_color
    else:
        s.fill.background()
    if line_color and line_w > 0:
        s.line.color.rgb = line_color
        s.line.width = Pt(line_w)
    else:
        s.line.fill.background()
    s.shadow.inherit = False
    return s

def circle(slide, left, top, w, h, fill_color, line_color=None, line_w=0):
    c = slide.shapes.add_shape(MSO_SHAPE.OVAL, left, top, w, h)
    c.fill.solid()
    c.fill.fore_color.rgb = fill_color
    if line_color and line_w > 0:
        c.line.color.rgb = line_color
        c.line.width = Pt(line_w)
    else:
        c.line.fill.background()
    c.shadow.inherit = False
    return c

def text(slide, txt, left, top, w, h, size=16, color=INK, bold=False,
         italic=False, align=PP_ALIGN.LEFT, font="Inter", anchor=MSO_ANCHOR.TOP,
         spacing=1.0):
    tb = slide.shapes.add_textbox(left, top, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = 0
    tf.margin_right = 0
    tf.margin_top = 0
    tf.margin_bottom = 0
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
    tf.margin_left = 0
    tf.margin_right = 0
    tf.margin_top = 0
    tf.margin_bottom = 0
    for i, item in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.line_spacing = line_spacing
        if gap: p.space_after = Pt(gap)
        # bullet prefix
        prefix_run = p.add_run()
        prefix_run.text = f"{bullet_char}  "
        prefix_run.font.size = Pt(size)
        prefix_run.font.color.rgb = RED
        prefix_run.font.bold = True
        prefix_run.font.name = "Inter"
        # text run
        r = p.add_run()
        r.text = item
        r.font.size = Pt(size)
        r.font.color.rgb = color
        r.font.name = "Inter"
    return tb

def pill(slide, txt, left, top, w, h, bg_color=RED, text_color=WHITE, size=10):
    p = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, w, h)
    p.fill.solid()
    p.fill.fore_color.rgb = bg_color
    p.line.fill.background()
    p.shadow.inherit = False
    tf = p.text_frame
    tf.margin_left = Inches(0.12)
    tf.margin_right = Inches(0.12)
    tf.margin_top = 0
    tf.margin_bottom = 0
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    par = tf.paragraphs[0]
    par.alignment = PP_ALIGN.CENTER
    r = par.add_run()
    r.text = txt
    r.font.size = Pt(size)
    r.font.color.rgb = text_color
    r.font.bold = True
    r.font.name = "Inter"
    return p

def page_num(slide, num):
    text(slide, f"{num:02d}", SW - Inches(0.9), SH - Inches(0.5),
         Inches(0.6), Inches(0.3), size=10, color=MUTED, bold=True,
         align=PP_ALIGN.RIGHT, font="Consolas")

def footer_brand(slide, color=MUTED):
    text(slide, "BLOODCONNECT", Inches(0.7), SH - Inches(0.5),
         Inches(3), Inches(0.3), size=9, color=color, bold=True,
         font="Consolas")

# Decorative shape — big faded number
def big_ghost_num(slide, num, left, top, size=200, color=None):
    color = color or RGBColor(0xEE, 0xE7, 0xE0)
    text(slide, num, left, top, Inches(4), Inches(3), size=size,
         color=color, bold=True, font="Inter")

# ============================================================
# SLIDE 1 — HERO TITLE
# ============================================================
s = prs.slides.add_slide(BLANK)
bg(s, RED_NIGHT)

# Geometric decorations
circle(s, Inches(10.5), Inches(-1), Inches(4), Inches(4), RED_DEEP)
circle(s, Inches(-1.5), Inches(5.5), Inches(3), Inches(3), RED_DARK)

# Big blood drop shape (approximated with oval)
circle(s, Inches(9.8), Inches(2.2), Inches(2.8), Inches(2.8), RED)
circle(s, Inches(10.4), Inches(2.6), Inches(0.8), Inches(0.8), RGBColor(0xF8, 0x71, 0x71))

# Small accents
rect(s, Inches(0.8), Inches(0.8), Inches(0.15), Inches(0.15), GOLD)
text(s, "EMERGENCY BLOOD NETWORK", Inches(1.05), Inches(0.72),
     Inches(4), Inches(0.3), size=10, color=GOLD, bold=True, font="Consolas")

# Main title
text(s, "Blood", Inches(0.8), Inches(1.8), Inches(8), Inches(1.5),
     size=110, color=WHITE, bold=True, spacing=0.9)
text(s, "Connect", Inches(0.8), Inches(3.1), Inches(8), Inches(1.5),
     size=110, color=GOLD, bold=True, spacing=0.9)

# Accent line
rect(s, Inches(0.85), Inches(4.7), Inches(1.2), Inches(0.08), RED)

# Subtitle
text(s, "Real-time blood donation network", Inches(0.8), Inches(5.0),
     Inches(8), Inches(0.5), size=22, color=WHITE, italic=True)

# Bottom meta
text(s, "BCA SEMESTER 7  ·  DSC-M-CBA 471P  ·  GUJARAT UNIVERSITY",
     Inches(0.8), Inches(6.3), Inches(11), Inches(0.4),
     size=10, color=GOLD, bold=True, font="Consolas")

text(s, "Prince Rajput", Inches(0.8), Inches(6.7), Inches(6), Inches(0.4),
     size=14, color=WHITE, bold=True)

text(s, "2026", SW - Inches(1.6), Inches(6.7), Inches(0.8), Inches(0.4),
     size=14, color=GOLD, bold=True, font="Consolas", align=PP_ALIGN.RIGHT)

# ============================================================
# SLIDE 2 — SECTION DIVIDER: THE PROBLEM
# ============================================================
s = prs.slides.add_slide(BLANK)
bg(s, RED)

# Big ghost number
big_ghost_num(s, "01", Inches(8), Inches(1), size=280, color=RED_DARK)

text(s, "SECTION 01", Inches(0.8), Inches(0.8), Inches(4), Inches(0.4),
     size=12, color=RGBColor(0xFF, 0xCC, 0xCC), bold=True, font="Consolas")

text(s, "The Problem", Inches(0.8), Inches(2.5), Inches(11), Inches(1.5),
     size=72, color=WHITE, bold=True)

rect(s, Inches(0.85), Inches(4.3), Inches(2), Inches(0.1), GOLD)

text(s, "India faces a critical blood shortage — traditional methods are failing.",
     Inches(0.8), Inches(4.8), Inches(11), Inches(0.5),
     size=20, color=RGBColor(0xFF, 0xE5, 0xE5), italic=True)

# ============================================================
# SLIDE 3 — PROBLEM DETAILS + CHART
# ============================================================
s = prs.slides.add_slide(BLANK)
bg(s, CREAM)

pill(s, "THE PROBLEM", Inches(0.7), Inches(0.6), Inches(1.8), Inches(0.35),
     RED, WHITE, 10)

text(s, "Blood shortage is real.", Inches(0.7), Inches(1.2),
     Inches(7), Inches(0.7), size=32, color=INK, bold=True)

text(s, "Every minute counts in an emergency.", Inches(0.7), Inches(1.85),
     Inches(7), Inches(0.5), size=16, color=MUTED, italic=True)

# Left: stats grid
y = Inches(2.7)
stats = [
    ("14.6M", "blood units needed yearly in India"),
    ("1.5M",  "unit shortage every single year"),
    ("63%",   "of transfusions face delays"),
    ("72h",   "average donor search time"),
]
for val, lbl in stats:
    text(s, val, Inches(0.7), y, Inches(2), Inches(0.5),
         size=26, color=RED, bold=True)
    text(s, lbl, Inches(2.8), y + Inches(0.1), Inches(4.5), Inches(0.4),
         size=12, color=INK_2)
    y += Inches(0.75)

# Right: chart card
card = rect(s, Inches(8.0), Inches(2.7), Inches(4.7), Inches(3.9),
            WHITE, LINE, 1, rounded=True)
text(s, "BLOOD DEMAND vs SUPPLY", Inches(8.3), Inches(2.9),
     Inches(4), Inches(0.3), size=10, color=RED, bold=True, font="Consolas")

chart_data = CategoryChartData()
chart_data.categories = ['2021', '2022', '2023', '2024', '2025']
chart_data.add_series('Demand', (13.2, 13.8, 14.1, 14.4, 14.6))
chart_data.add_series('Supply', (11.6, 12.0, 12.6, 13.0, 13.1))

gf = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED,
                        Inches(8.3), Inches(3.3),
                        Inches(4.1), Inches(3.1), chart_data)
chart = gf.chart
chart.has_legend = True
chart.legend.position = XL_LEGEND_POSITION.BOTTOM
chart.legend.include_in_layout = False
chart.legend.font.size = Pt(9)
chart.legend.font.name = "Inter"

plot = chart.plots[0]
plot.gap_width = 60
plot.series[0].format.fill.solid()
plot.series[0].format.fill.fore_color.rgb = RED
plot.series[1].format.fill.solid()
plot.series[1].format.fill.fore_color.rgb = GOLD

page_num(s, 3)
footer_brand(s)

# ============================================================
# SLIDE 4 — SECTION DIVIDER: THE SOLUTION
# ============================================================
s = prs.slides.add_slide(BLANK)
bg(s, RED)

big_ghost_num(s, "02", Inches(8), Inches(1), size=280, color=RED_DARK)

text(s, "SECTION 02", Inches(0.8), Inches(0.8), Inches(4), Inches(0.4),
     size=12, color=RGBColor(0xFF, 0xCC, 0xCC), bold=True, font="Consolas")

text(s, "Our Solution", Inches(0.8), Inches(2.5), Inches(11), Inches(1.5),
     size=72, color=WHITE, bold=True)

rect(s, Inches(0.85), Inches(4.3), Inches(2), Inches(0.1), GOLD)

text(s, "A verified, real-time, pledge-based network that actually works.",
     Inches(0.8), Inches(4.8), Inches(11), Inches(0.5),
     size=20, color=RGBColor(0xFF, 0xE5, 0xE5), italic=True)

# ============================================================
# SLIDE 5 — SOLUTION OVERVIEW
# ============================================================
s = prs.slides.add_slide(BLANK)
bg(s, CREAM)

pill(s, "OUR SOLUTION", Inches(0.7), Inches(0.6), Inches(2), Inches(0.35),
     RED, WHITE, 10)

text(s, "BloodConnect — the fix.", Inches(0.7), Inches(1.2),
     Inches(11), Inches(0.7), size=32, color=INK, bold=True)

text(s, "One platform. Three roles. Zero friction.", Inches(0.7), Inches(1.85),
     Inches(11), Inches(0.5), size=16, color=MUTED, italic=True)

# 3 role cards
roles = [
    ("USER",   "Post requests", "Location + urgency aware", "Real-time status tracking", RED),
    ("DONOR",  "Pledge to help", "Verified profile", "Track donations", GOLD),
    ("ADMIN",  "Manage users",  "Ban / Unban", "Dashboard + analytics", INK),
]

card_w = Inches(3.9)
card_h = Inches(3.4)
y = Inches(2.9)

for i, (role, line1, line2, line3, accent) in enumerate(roles):
    x = Inches(0.7) + i * (card_w + Inches(0.2))
    # Card
    rect(s, x, y, card_w, card_h, WHITE, LINE, 1, rounded=True)
    # Top accent
    rect(s, x, y, card_w, Inches(0.1), accent)
    # Role badge
    pill(s, role, x + Inches(0.3), y + Inches(0.4), Inches(1), Inches(0.3),
         accent, WHITE, 10)
    # Content
    text(s, line1, x + Inches(0.3), y + Inches(1.0), card_w - Inches(0.6),
         Inches(0.4), size=18, color=INK, bold=True)
    bullets(s, [line2, line3], x + Inches(0.3), y + Inches(1.7),
            card_w - Inches(0.6), Inches(1.5), size=13, color=MUTED,
            bullet_char="·", line_spacing=1.5)

page_num(s, 5)
footer_brand(s)

# ============================================================
# SLIDE 6 — TECH STACK
# ============================================================
s = prs.slides.add_slide(BLANK)
bg(s, RED_NIGHT)

text(s, "TECH STACK", Inches(0.7), Inches(0.6), Inches(4), Inches(0.4),
     size=12, color=GOLD, bold=True, font="Consolas")

text(s, "Built with a modern stack.", Inches(0.7), Inches(1.2),
     Inches(11), Inches(0.8), size=38, color=WHITE, bold=True)

rect(s, Inches(0.85), Inches(2.15), Inches(2), Inches(0.08), RED)

# Tech grid — 4 columns x 2 rows
tech = [
    ("ASP.NET", "Core MVC", ".NET 10"),
    ("EF Core", "10.x", "ORM"),
    ("SQL Server", "Express", "Database"),
    ("Identity", "Auth", "3 Roles"),
    ("Razor", "Views", "CSHTML"),
    ("Bootstrap", "5.x", "Responsive"),
    ("Swagger", "OpenAPI", "API Docs"),
    ("MonsterASP", ".NET", "Live Host"),
]

col_w = Inches(2.9)
row_h = Inches(1.9)
gx = Inches(0.7)
gy = Inches(2.9)

for i, (name, version, tag) in enumerate(tech):
    col = i % 4
    row = i // 4
    x = gx + col * (col_w + Inches(0.15))
    y = gy + row * (row_h + Inches(0.2))
    # card
    rect(s, x, y, col_w, row_h, RED_DEEP, None, 0, rounded=True)
    # tag
    pill(s, tag.upper(), x + Inches(0.2), y + Inches(0.2),
         Inches(1.2), Inches(0.28), GOLD, RED_DEEP, 8)
    # name
    text(s, name, x + Inches(0.2), y + Inches(0.75), col_w - Inches(0.4),
         Inches(0.5), size=20, color=WHITE, bold=True)
    # version
    text(s, version, x + Inches(0.2), y + Inches(1.25), col_w - Inches(0.4),
         Inches(0.4), size=13, color=RGBColor(0xF8, 0x71, 0x71), font="Consolas")

page_num(s, 6)
footer_brand(s, RGBColor(0x77, 0x55, 0x55))

# ============================================================
# SLIDE 7 — ARCHITECTURE (MVC + DB)
# ============================================================
s = prs.slides.add_slide(BLANK)
bg(s, CREAM)

pill(s, "ARCHITECTURE", Inches(0.7), Inches(0.6), Inches(2.2), Inches(0.35),
     RED, WHITE, 10)

text(s, "Model · View · Controller", Inches(0.7), Inches(1.2),
     Inches(11), Inches(0.7), size=32, color=INK, bold=True)

# MVC flow — 3 big boxes with arrows
box_w = Inches(3.3)
box_h = Inches(2)
by = Inches(2.6)
flow = [
    ("MODEL",      "Donor · BloodRequest\nDonationOffer · AppUser", RED),
    ("VIEW",       "Razor .cshtml\nBootstrap 5 + Custom CSS", GOLD),
    ("CONTROLLER", "Business logic\nAuth · CRUD · API", INK),
]
for i, (title, desc, color) in enumerate(flow):
    x = Inches(0.7) + i * (box_w + Inches(0.8))
    rect(s, x, by, box_w, box_h, WHITE, color, 2, rounded=True)
    # Top accent bar
    rect(s, x, by, box_w, Inches(0.08), color)
    text(s, title, x + Inches(0.3), by + Inches(0.4), box_w - Inches(0.6),
         Inches(0.5), size=22, color=color, bold=True)
    text(s, desc, x + Inches(0.3), by + Inches(1.1), box_w - Inches(0.6),
         Inches(0.8), size=13, color=INK_2, spacing=1.4)
    # Arrow
    if i < 2:
        text(s, "→", x + box_w + Inches(0.15), by + Inches(0.7),
             Inches(0.5), Inches(0.6), size=32, color=color, bold=True,
             align=PP_ALIGN.CENTER)

# Bottom — DB schema strip
rect(s, Inches(0.7), Inches(5.1), Inches(11.9), Inches(1.6),
     RED_NIGHT, None, 0, rounded=True)
text(s, "DATABASE — 8 TABLES", Inches(1.0), Inches(5.3), Inches(4), Inches(0.3),
     size=10, color=GOLD, bold=True, font="Consolas")

tables = ["Users", "Donors", "BloodRequests", "DonationOffers", "ContactMessages", "+3 Identity"]
tx = Inches(1.0)
for t in tables:
    tw = Inches(1.85)
    pill(s, t, tx, Inches(5.85), tw, Inches(0.4), RED_DEEP, WHITE, 11)
    tx += tw + Inches(0.1)

page_num(s, 7)
footer_brand(s)

# ============================================================
# SLIDE 8 — KEY FEATURES
# ============================================================
s = prs.slides.add_slide(BLANK)
bg(s, CREAM)

pill(s, "FEATURES", Inches(0.7), Inches(0.6), Inches(1.7), Inches(0.35),
     RED, WHITE, 10)

text(s, "What makes it complete.", Inches(0.7), Inches(1.2),
     Inches(11), Inches(0.7), size=32, color=INK, bold=True)

# 2x3 grid of feature tiles
features = [
    ("🔐", "Authentication",   "ASP.NET Identity · 3 roles · Ban system"),
    ("🩸", "Blood Search",     "Compatibility matrix · O− / AB+ logic"),
    ("📋", "Request Flow",     "Post · Filter · Track · Fulfill"),
    ("🤝", "Donation Pledge",  "Two-way confirmation workflow"),
    ("🛡️", "Admin Panel",      "Users · Donors · Requests · Messages"),
    ("📊", "Dashboard",        "Real-time stats · Personal insights"),
]

tile_w = Inches(3.9)
tile_h = Inches(1.9)
gx = Inches(0.7)
gy = Inches(2.4)

for i, (icon, title, desc) in enumerate(features):
    col = i % 3
    row = i // 3
    x = gx + col * (tile_w + Inches(0.2))
    y = gy + row * (tile_h + Inches(0.25))
    rect(s, x, y, tile_w, tile_h, WHITE, LINE, 1, rounded=True)
    # icon circle
    circle(s, x + Inches(0.3), y + Inches(0.4), Inches(0.9), Inches(0.9), RED_SOFT)
    text(s, icon, x + Inches(0.3), y + Inches(0.55), Inches(0.9), Inches(0.6),
         size=24, align=PP_ALIGN.CENTER)
    # title
    text(s, title, x + Inches(1.4), y + Inches(0.45), tile_w - Inches(1.6),
         Inches(0.4), size=17, color=INK, bold=True)
    # desc
    text(s, desc, x + Inches(1.4), y + Inches(0.95), tile_w - Inches(1.6),
         Inches(0.8), size=12, color=MUTED, spacing=1.3)

page_num(s, 8)
footer_brand(s)

# ============================================================
# SLIDE 9 — UNIQUE FEATURE 1 — BLOOD COMPATIBILITY
# ============================================================
s = prs.slides.add_slide(BLANK)
bg(s, RED_NIGHT)

pill(s, "★ UNIQUE FEATURE 01", Inches(0.7), Inches(0.6), Inches(2.6), Inches(0.35),
     GOLD, RED_NIGHT, 10)

text(s, "Blood Compatibility", Inches(0.7), Inches(1.2),
     Inches(8), Inches(0.7), size=38, color=WHITE, bold=True)

text(s, "Medical accuracy built into every search.", Inches(0.7), Inches(2.0),
     Inches(8), Inches(0.5), size=16, color=RGBColor(0xF8, 0x71, 0x71), italic=True)

# Big matrix on right
mx = Inches(7.0)
my = Inches(2.7)
cell = Inches(0.6)
# Header row
groups = ["O−", "O+", "A−", "A+", "B−", "B+", "AB−", "AB+"]
for i, g in enumerate(groups):
    text(s, g, mx + i * cell, my, cell, Inches(0.4),
         size=11, color=GOLD, bold=True, align=PP_ALIGN.CENTER, font="Consolas")

# 8x8 grid
matrix = [
    # O-  O+  A-  A+  B-  B+  AB- AB+   (receivers)
    [1,0,0,0,0,0,0,0],  # O-
    [1,1,0,0,0,0,0,0],  # O+
    [1,0,1,0,0,0,0,0],  # A-
    [1,1,1,1,0,0,0,0],  # A+
    [1,0,0,0,1,0,0,0],  # B-
    [1,1,0,0,1,1,0,0],  # B+
    [1,0,1,0,1,0,1,0],  # AB-
    [1,1,1,1,1,1,1,1],  # AB+
]
for r_idx, row in enumerate(matrix):
    text(s, groups[r_idx], mx - Inches(0.5), my + Inches(0.5) + r_idx * cell,
         Inches(0.45), Inches(0.4), size=11, color=GOLD, bold=True,
         align=PP_ALIGN.RIGHT, font="Consolas")
    for c_idx, val in enumerate(row):
        cx = mx + c_idx * cell
        cy = my + Inches(0.5) + r_idx * cell
        color = RED if val else RGBColor(0x2A, 0x14, 0x14)
        circle(s, cx + Inches(0.08), cy + Inches(0.08),
               cell - Inches(0.16), cell - Inches(0.16), color)

text(s, "Rows = Donors · Columns = Receivers", mx - Inches(0.5), my + Inches(0.5) + 8 * cell + Inches(0.1),
     Inches(5.5), Inches(0.3), size=10, color=RGBColor(0x99, 0x88, 0x88),
     align=PP_ALIGN.CENTER, italic=True, font="Consolas")

# Left side — key facts
facts = [
    ("O−",  "Universal donor",       "Can donate to all 8 groups"),
    ("AB+", "Universal receiver",    "Can receive from all 8 groups"),
    ("A+",  "Most common (India)",   "~30% of population"),
    ("B+",  "Second most common",    "~24% of population"),
]
fy = Inches(3.1)
for grp, label, detail in facts:
    circle(s, Inches(0.9), fy, Inches(0.7), Inches(0.7), RED)
    text(s, grp, Inches(0.9), fy + Inches(0.13), Inches(0.7), Inches(0.5),
         size=16, color=WHITE, bold=True, align=PP_ALIGN.CENTER, font="Consolas")
    text(s, label, Inches(1.8), fy + Inches(0.05), Inches(5), Inches(0.35),
         size=15, color=WHITE, bold=True)
    text(s, detail, Inches(1.8), fy + Inches(0.4), Inches(5), Inches(0.3),
         size=11, color=RGBColor(0xBB, 0xA8, 0xA8))
    fy += Inches(0.95)

page_num(s, 9)
footer_brand(s, RGBColor(0x77, 0x55, 0x55))

# ============================================================
# SLIDE 10 — UNIQUE FEATURE 2 — PLEDGE WORKFLOW
# ============================================================
s = prs.slides.add_slide(BLANK)
bg(s, CREAM)

pill(s, "★ UNIQUE FEATURE 02", Inches(0.7), Inches(0.6), Inches(2.6), Inches(0.35),
     GOLD, WHITE, 10)

text(s, "Pledge-Based Workflow", Inches(0.7), Inches(1.2),
     Inches(11), Inches(0.7), size=32, color=INK, bold=True)

text(s, "Two-way confirmation prevents fake fulfillments.",
     Inches(0.7), Inches(1.9), Inches(11), Inches(0.5),
     size=15, color=MUTED, italic=True)

# 4-step flow
steps = [
    ("01", "PLEDGE",   "Donor clicks\n\"I can donate\"\n→ Offer created", RED),
    ("02", "ACCEPT",   "Owner reviews\noffers\n→ Others auto-reject", GOLD),
    ("03", "COMPLETE", "Donor + Owner\nmark donation\ndone", RED_DARK),
    ("04", "FULFILL",  "Request status\n= Fulfilled\n→ 3 lives saved", INK),
]

step_w = Inches(2.85)
step_h = Inches(3.6)
step_y = Inches(2.9)

for i, (num, title, desc, color) in enumerate(steps):
    x = Inches(0.7) + i * (step_w + Inches(0.25))
    # Card
    rect(s, x, step_y, step_w, step_h, WHITE, LINE, 1, rounded=True)
    # Big number
    text(s, num, x + Inches(0.3), step_y + Inches(0.15), Inches(1.5),
         Inches(0.7), size=32, color=color, bold=True, font="Consolas")
    # Title
    text(s, title, x + Inches(0.3), step_y + Inches(0.9), step_w - Inches(0.6),
         Inches(0.4), size=15, color=color, bold=True)
    # Accent line
    rect(s, x + Inches(0.3), step_y + Inches(1.35), Inches(0.4), Inches(0.06), color)
    # Description
    text(s, desc, x + Inches(0.3), step_y + Inches(1.6), step_w - Inches(0.6),
         Inches(1.8), size=13, color=INK_2, spacing=1.5)
    # Arrow
    if i < 3:
        text(s, "→", x + step_w + Inches(0.02), step_y + Inches(1.5),
             Inches(0.25), Inches(0.5), size=24, color=color, bold=True,
             align=PP_ALIGN.CENTER)

# Status flow bar
rect(s, Inches(0.7), Inches(6.7), Inches(11.9), Inches(0.5), RED_SOFT, None, 0, rounded=True)
text(s, "STATUS FLOW:  Pledged  →  Accepted  →  Completed  →  Fulfilled",
     Inches(0.9), Inches(6.82), Inches(11.5), Inches(0.3),
     size=11, color=RED_DARK, bold=True, font="Consolas")

page_num(s, 10)
footer_brand(s)

# ============================================================
# SLIDE 11 — API + SWAGGER
# ============================================================
s = prs.slides.add_slide(BLANK)
bg(s, RED_NIGHT)

pill(s, "REST API", Inches(0.7), Inches(0.6), Inches(1.6), Inches(0.35),
     RED, WHITE, 10)

text(s, "APIs with Swagger UI.", Inches(0.7), Inches(1.2),
     Inches(11), Inches(0.7), size=38, color=WHITE, bold=True)

text(s, "Live-testable REST endpoints — GET, POST, PUT, DELETE.",
     Inches(0.7), Inches(2.0), Inches(11), Inches(0.5),
     size=15, color=RGBColor(0xF8, 0x71, 0x71), italic=True)

# Left: endpoints list
endpoints = [
    ("GET",    "/api/donor",         "List donors"),
    ("GET",    "/api/donor/{id}",    "Single donor"),
    ("POST",   "/api/donor",         "Create donor"),
    ("PUT",    "/api/donor/{id}",    "Update donor"),
    ("DELETE", "/api/donor/{id}",    "Delete donor"),
    ("GET",    "/api/donor/search",  "Compatibility search"),
    ("GET",    "/api/bloodrequest",  "List requests"),
    ("POST",   "/api/bloodrequest",  "Create request"),
]

y = Inches(2.9)
for method, path, desc in endpoints:
    # Method badge
    mcolor = {"GET": RGBColor(0x22, 0xC5, 0x5E), "POST": RED,
              "PUT": GOLD, "DELETE": RED_DARK}[method]
    pill(s, method, Inches(0.7), y, Inches(0.85), Inches(0.3), mcolor, WHITE, 8)
    # Path
    text(s, path, Inches(1.7), y + Inches(0.02), Inches(4), Inches(0.3),
         size=12, color=WHITE, bold=True, font="Consolas")
    # Desc
    text(s, desc, Inches(5.8), y + Inches(0.04), Inches(3), Inches(0.3),
         size=11, color=RGBColor(0x99, 0x88, 0x88))
    y += Inches(0.42)

# Right: feature checkboxes
card = rect(s, Inches(8.7), Inches(2.9), Inches(3.9), Inches(3.7),
            RED_DEEP, None, 0, rounded=True)

text(s, "WHY IT'S SOLID", Inches(9.0), Inches(3.1), Inches(3.5), Inches(0.3),
     size=10, color=GOLD, bold=True, font="Consolas")

features = [
    "✅  Proper HTTP verbs",
    "✅  Status codes 200/201/404/401",
    "✅  DTO pattern — privacy",
    "✅  Owner + Admin checks",
    "✅  Swagger UI for live testing",
    "✅  Postman-compatible",
]
fy = Inches(3.6)
for f in features:
    text(s, f, Inches(9.0), fy, Inches(3.5), Inches(0.35),
         size=12, color=WHITE)
    fy += Inches(0.42)

page_num(s, 11)
footer_brand(s, RGBColor(0x77, 0x55, 0x55))

# ============================================================
# SLIDE 12 — LIVE DEMO
# ============================================================
s = prs.slides.add_slide(BLANK)
bg(s, RED)

big_ghost_num(s, "★", Inches(9.5), Inches(0.5), size=240, color=RED_DARK)

pill(s, "LIVE DEMO", Inches(0.8), Inches(0.8), Inches(1.8), Inches(0.35),
     GOLD, RED, 10)

text(s, "It's live. Right now.", Inches(0.8), Inches(1.6),
     Inches(11), Inches(0.9), size=54, color=WHITE, bold=True)

rect(s, Inches(0.85), Inches(2.9), Inches(2), Inches(0.1), GOLD)

# URL card
rect(s, Inches(0.8), Inches(3.4), Inches(11.7), Inches(1.3),
     RED_DARK, None, 0, rounded=True)

text(s, "LIVE URL", Inches(1.2), Inches(3.6), Inches(4), Inches(0.3),
     size=10, color=GOLD, bold=True, font="Consolas")
text(s, "bloodconnector.runasp.net", Inches(1.2), Inches(3.9),
     Inches(11), Inches(0.6), size=28, color=WHITE, bold=True, font="Consolas")

# Credentials
text(s, "DEMO CREDENTIALS", Inches(0.8), Inches(5.1), Inches(6), Inches(0.3),
     size=10, color=GOLD, bold=True, font="Consolas")

text(s, "admin@bloodconnect.com", Inches(0.8), Inches(5.5),
     Inches(6), Inches(0.4), size=16, color=WHITE, font="Consolas", bold=True)

text(s, "Admin@123", Inches(0.8), Inches(5.9),
     Inches(6), Inches(0.4), size=16, color=WHITE, font="Consolas", bold=True)

# Deploy info
text(s, "DEPLOYED ON", Inches(7.2), Inches(5.1), Inches(5), Inches(0.3),
     size=10, color=GOLD, bold=True, font="Consolas", align=PP_ALIGN.RIGHT)

text(s, "MonsterASP.NET", Inches(7.2), Inches(5.5), Inches(5.3),
     Inches(0.4), size=16, color=WHITE, bold=True, font="Consolas",
     align=PP_ALIGN.RIGHT)

text(s, "HTTPS · Let's Encrypt · Auto-deploy", Inches(7.2), Inches(5.9),
     Inches(5.3), Inches(0.4), size=12, color=RGBColor(0xFF, 0xCC, 0xCC),
     align=PP_ALIGN.RIGHT)

# ============================================================
# SLIDE 13 — IMPACT / KPI TILES
# ============================================================
s = prs.slides.add_slide(BLANK)
bg(s, CREAM)

pill(s, "IMPACT", Inches(0.7), Inches(0.6), Inches(1.5), Inches(0.35),
     RED, WHITE, 10)

text(s, "Real numbers. Real promise.", Inches(0.7), Inches(1.2),
     Inches(11), Inches(0.7), size=32, color=INK, bold=True)

# 4 KPI tiles
kpis = [
    ("3",    "Lives saved", "per single donation", RED),
    ("8",    "Blood groups", "compatibility aware", GOLD),
    ("5",    "User roles", "SuperAdmin · Admin · User", RED_DARK),
    ("100%", "Free", "zero cost, forever", INK),
]

kpi_w = Inches(2.9)
kpi_h = Inches(2.7)
kx = Inches(0.7)
ky = Inches(2.5)

for i, (val, label, sub, color) in enumerate(kpis):
    x = kx + i * (kpi_w + Inches(0.2))
    rect(s, x, ky, kpi_w, kpi_h, WHITE, LINE, 1, rounded=True)
    # top accent
    rect(s, x, ky, kpi_w, Inches(0.08), color)
    # value
    text(s, val, x + Inches(0.3), ky + Inches(0.5), kpi_w - Inches(0.6),
         Inches(1), size=52, color=color, bold=True)
    # label
    text(s, label, x + Inches(0.3), ky + Inches(1.5), kpi_w - Inches(0.6),
         Inches(0.4), size=15, color=INK, bold=True)
    # sub
    text(s, sub, x + Inches(0.3), ky + Inches(1.95), kpi_w - Inches(0.6),
         Inches(0.5), size=11, color=MUTED, spacing=1.3)

# Bottom quote
rect(s, Inches(0.7), Inches(5.6), Inches(11.9), Inches(1.2),
     RED_SOFT, None, 0, rounded=True)
rect(s, Inches(0.7), Inches(5.6), Inches(0.1), Inches(1.2), RED)
text(s, '"One donation can save up to three lives. The only thing standing',
     Inches(1.1), Inches(5.75), Inches(11.3), Inches(0.35),
     size=14, color=INK, italic=True)
text(s, 'between a patient and a donor is a network. Help us build it."',
     Inches(1.1), Inches(6.1), Inches(11.3), Inches(0.35),
     size=14, color=INK, italic=True)

page_num(s, 13)
footer_brand(s)

# ============================================================
# SLIDE 14 — FUTURE SCOPE
# ============================================================
s = prs.slides.add_slide(BLANK)
bg(s, CREAM)

pill(s, "FUTURE SCOPE", Inches(0.7), Inches(0.6), Inches(2), Inches(0.35),
     RED, WHITE, 10)

text(s, "What's next.", Inches(0.7), Inches(1.2),
     Inches(11), Inches(0.7), size=32, color=INK, bold=True)

text(s, "The roadmap from MVP to platform.", Inches(0.7), Inches(1.85),
     Inches(11), Inches(0.5), size=15, color=MUTED, italic=True)

# Vertical timeline
items = [
    ("Q1 2027", "Mobile app",         "React Native / Flutter"),
    ("Q2 2027", "Hospital API",       "Direct request integration"),
    ("Q3 2027", "Notifications",      "Email (SendGrid) + SMS (Twilio)"),
    ("Q4 2027", "Analytics",          "Chart.js dashboards for admins"),
    ("2028",    "Multi-language",     "Hindi · Gujarati · English"),
    ("2028",    "Map-based search",   "Google Maps donor visualization"),
]

start_y = Inches(2.5)
line_x = Inches(2.7)
# Vertical line
rect(s, line_x, start_y + Inches(0.15), Inches(0.02),
     Inches(4.4), RGBColor(0xDD, 0xD5, 0xCA))

for i, (q, title, desc) in enumerate(items):
    y = start_y + i * Inches(0.75)
    # Dot
    circle(s, line_x - Inches(0.08), y + Inches(0.1),
           Inches(0.18), Inches(0.18), RED)
    # Quarter
    text(s, q, Inches(0.7), y + Inches(0.03), Inches(1.8), Inches(0.35),
         size=13, color=RED, bold=True, font="Consolas", align=PP_ALIGN.RIGHT)
    # Title
    text(s, title, Inches(3.1), y, Inches(3), Inches(0.4),
         size=15, color=INK, bold=True)
    # Desc
    text(s, desc, Inches(6.3), y + Inches(0.02), Inches(6), Inches(0.4),
         size=13, color=MUTED)

page_num(s, 14)
footer_brand(s)

# ============================================================
# SLIDE 15 — THANK YOU
# ============================================================
s = prs.slides.add_slide(BLANK)
bg(s, RED_NIGHT)

circle(s, Inches(-1.5), Inches(-1.5), Inches(4), Inches(4), RED_DARK)
circle(s, Inches(11), Inches(5.5), Inches(4), Inches(4), RED_DEEP)

# Big drop
circle(s, Inches(6), Inches(1.2), Inches(1.4), Inches(1.4), RED)
circle(s, Inches(6.4), Inches(1.5), Inches(0.35), Inches(0.35),
       RGBColor(0xF8, 0x71, 0x71))

text(s, "Thank You", Inches(0.7), Inches(3.0), Inches(12), Inches(1.2),
     size=72, color=WHITE, bold=True, align=PP_ALIGN.CENTER)

rect(s, Inches(6.16), Inches(4.2), Inches(1), Inches(0.06), GOLD)

text(s, "Every drop counts.", Inches(0.7), Inches(4.4), Inches(12),
     Inches(0.6), size=22, color=GOLD, italic=True, align=PP_ALIGN.CENTER)

# Bottom info grid
info_y = Inches(5.5)
text(s, "LIVE", Inches(0.7), info_y, Inches(3.9), Inches(0.3),
     size=9, color=GOLD, bold=True, font="Consolas", align=PP_ALIGN.CENTER)
text(s, "bloodconnector.runasp.net", Inches(0.7), info_y + Inches(0.35),
     Inches(3.9), Inches(0.3), size=11, color=WHITE,
     font="Consolas", align=PP_ALIGN.CENTER)

text(s, "CODE", Inches(4.7), info_y, Inches(3.9), Inches(0.3),
     size=9, color=GOLD, bold=True, font="Consolas", align=PP_ALIGN.CENTER)
text(s, "github.com/rajputpri/BloodConnector", Inches(4.7), info_y + Inches(0.35),
     Inches(3.9), Inches(0.3), size=11, color=WHITE,
     font="Consolas", align=PP_ALIGN.CENTER)

text(s, "BY", Inches(8.7), info_y, Inches(3.9), Inches(0.3),
     size=9, color=GOLD, bold=True, font="Consolas", align=PP_ALIGN.CENTER)
text(s, "Prince Rajput · BCA Sem-7", Inches(8.7), info_y + Inches(0.35),
     Inches(3.9), Inches(0.3), size=11, color=WHITE,
     font="Consolas", align=PP_ALIGN.CENTER)

# ==================== SAVE ====================
output = "BloodConnect-PPT.pptx"
prs.save(output)
print(f"SUCCESS! PPT created: {output}")
print(f"Total slides: {len(prs.slides)}")