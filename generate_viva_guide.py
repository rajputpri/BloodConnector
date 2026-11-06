"""
================================================================================
BLOODCONNECT — MASTER VIVA PREPARATION GUIDE PDF GENERATOR
================================================================================
Student : Rajput Prince Singh (Roll No: 83)
Course  : Full Stack Web Development Project using ASP.NET Core (DSC-M-BCA-471P)
Guide   : Prof. Sejal Shah | Lokmanya College of Computer Applications
================================================================================
Run Command:
    python generate_viva_guide.py
Output File:
    BloodConnect_Viva_Master_Guide_Prince_Roll83.pdf
================================================================================
"""

import os
from xml.sax.saxutils import escape
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

# ─── EYE-CATCHING RICH COLOR PALETTE ──────────────────────────────────────────
BURGUNDY      = colors.HexColor("#7B1E28")   # Primary Header Burgundy
BURGUNDY_DARK = colors.HexColor("#4A0E16")   # Deep Maroon
CRIMSON       = colors.HexColor("#DC2626")   # Vibrant Alert Red
GOLD          = colors.HexColor("#D4A24C")   # Rich Antique Gold
GOLD_LIGHT    = colors.HexColor("#FEF3C7")   # Soft Gold Highlight
CREAM_BG      = colors.HexColor("#FDF8F5")   # Warm Cream Box Fill
NAVY_BLUE     = colors.HexColor("#1E3A8A")   # Deep Concept Blue
BLUE_LIGHT    = colors.HexColor("#EFF6FF")   # Soft Blue Card Fill
GREEN_PASS    = colors.HexColor("#15803D")   # Emerald Green
GREEN_LIGHT   = colors.HexColor("#DCFCE7")   # Soft Green Fill
PURPLE_VIVA   = colors.HexColor("#6B21A8")   # Royal Purple for Examiner Q&A
PURPLE_LIGHT  = colors.HexColor("#F3E8FF")   # Soft Purple Fill
TEXT_DARK     = colors.HexColor("#1F2937")   # Crisp Body Text
TEXT_MUTED    = colors.HexColor("#6B7280")   # Muted Grey
BORDER_WARM   = colors.HexColor("#E5D5CE")   # Soft Border

PAGE_W, PAGE_H = letter


def draw_page_decorations(canvas, doc):
    """Draws a rich top banner bar and bottom footer on every page."""
    canvas.saveState()

    # Top decorative color strip
    canvas.setFillColor(BURGUNDY)
    canvas.rect(0, PAGE_H - 10, PAGE_W, 10, stroke=0, fill=1)
    canvas.setFillColor(GOLD)
    canvas.rect(0, PAGE_H - 13, PAGE_W, 3, stroke=0, fill=1)

    # Running Header
    canvas.setFont("Helvetica-Bold", 8.5)
    canvas.setFillColor(BURGUNDY)
    canvas.drawString(42, PAGE_H - 28, "BLOODCONNECT — MASTER VIVA & CONCEPT GUIDE (ELI3 + TECHNICAL)")
    canvas.setFont("Helvetica", 8.5)
    canvas.setFillColor(TEXT_MUTED)
    canvas.drawRightString(PAGE_W - 42, PAGE_H - 28, "Rajput Prince Singh (Roll No: 83) | DSC-M-BCA-471P")

    canvas.setStrokeColor(BORDER_WARM)
    canvas.setLineWidth(0.7)
    canvas.line(42, PAGE_H - 34, PAGE_W - 42, PAGE_H - 34)

    # Running Footer
    canvas.setStrokeColor(BORDER_WARM)
    canvas.line(42, 38, PAGE_W - 42, 38)
    canvas.setFont("Helvetica", 8.5)
    canvas.setFillColor(TEXT_MUTED)
    canvas.drawString(42, 24, "Guide: Prof. Sejal Shah | Lokmanya College of Computer Applications | Gujarat University")

    canvas.setFont("Helvetica-Bold", 9)
    canvas.setFillColor(CRIMSON)
    canvas.drawRightString(PAGE_W - 42, 24, f"Page {doc.page}")

    canvas.restoreState()


def make_styles():
    base = getSampleStyleSheet()
    styles = {}

    styles["HeroTitle"] = ParagraphStyle(
        "HeroTitle", parent=base["Normal"],
        fontName="Helvetica-Bold", fontSize=20, leading=25,
        textColor=colors.white, alignment=TA_CENTER
    )
    styles["SectionBanner"] = ParagraphStyle(
        "SectionBanner", parent=base["Normal"],
        fontName="Helvetica-Bold", fontSize=13, leading=17,
        textColor=colors.white, alignment=TA_LEFT
    )
    styles["SubHeading"] = ParagraphStyle(
        "SubHeading", parent=base["Normal"],
        fontName="Helvetica-Bold", fontSize=11.5, leading=15,
        textColor=BURGUNDY, spaceBefore=8, spaceAfter=4
    )
    styles["CardBody"] = ParagraphStyle(
        "CardBody", parent=base["Normal"],
        fontName="Helvetica", fontSize=9.3, leading=13.5,
        textColor=TEXT_DARK
    )
    styles["TableHeader"] = ParagraphStyle(
        "TableHeader", parent=base["Normal"],
        fontName="Helvetica-Bold", fontSize=9.2, leading=12,
        textColor=colors.white, alignment=TA_CENTER
    )
    styles["TableCell"] = ParagraphStyle(
        "TableCell", parent=base["Normal"],
        fontName="Helvetica", fontSize=8.8, leading=12,
        textColor=TEXT_DARK, alignment=TA_LEFT
    )
    styles["TableCellBold"] = ParagraphStyle(
        "TableCellBold", parent=base["Normal"],
        fontName="Helvetica-Bold", fontSize=8.8, leading=12,
        textColor=BURGUNDY, alignment=TA_LEFT
    )
    return styles


def section_header(num, title, subtitle, bg_color=BURGUNDY):
    """Creates an eye-catching full-width colored section header bar."""
    st = make_styles()
    p = Paragraph(
        f"<font size='10' color='#FDE68A'>SECTION {num}</font><br/>"
        f"<b>{escape(title)}</b><br/>"
        f"<font size='9' color='#F3F4F6'>{escape(subtitle)}</font>",
        st["SectionBanner"]
    )
    t = Table([[p]], colWidths=[528])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg_color),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LINEBEFORE", (0, 0), (0, -1), 5, GOLD),
    ]))
    return t


def callout_card(badge, title, bacha_explanation, viva_english_answer, border_color=BURGUNDY, bg_color=CREAM_BG):
    """
    Creates a dual-layer card:
      1. 3-Saal Ke Bacche Ke Level Ki Samajh (Hinglish Analogy)
      2. Viva Me Examiner Ke Samne Kya Bolna Hai (Ready-to-Speak English)
    """
    st = make_styles()
    content = (
        f"<font color='#B91C1C'><b>[{escape(badge)}] {escape(title)}</b></font><br/>"
        f"<b><font color='#1E3A8A'>Baccha Level Samajh (Hinglish): </font></b>{escape(bacha_explanation)}<br/>"
        f"<b><font color='#15803D'>Viva Me Bolne Ki Line (English): </font></b><i>\"{escape(viva_english_answer)}\"</i>"
    )
    p = Paragraph(content, st["CardBody"])
    t = Table([[p]], colWidths=[528])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg_color),
        ("BOX", (0, 0), (-1, -1), 0.8, BORDER_WARM),
        ("LINEBEFORE", (0, 0), (0, -1), 4.5, border_color),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    return KeepTogether([t, Spacer(1, 6)])


def qa_card(q_num, question, bacha_hint, crisp_answer):
    """Creates a rapid-fire Viva Q&A card."""
    st = make_styles()
    text = (
        f"<b><font color='#7B1E28'>{escape(q_num)}: {escape(question)}</font></b><br/>"
        f"<b><font color='#B45309'>Easy Logic (Hinglish): </font></b>{escape(bacha_hint)}<br/>"
        f"<b><font color='#15803D'>Examiner Answer: </font></b>{escape(crisp_answer)}"
    )
    p = Paragraph(text, st["CardBody"])
    t = Table([[p]], colWidths=[528])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.white),
        ("BOX", (0, 0), (-1, -1), 0.7, BORDER_WARM),
        ("LINEBEFORE", (0, 0), (0, -1), 4, PURPLE_VIVA),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    return KeepTogether([t, Spacer(1, 5)])


def build_viva_pdf():
    out_file = "BloodConnect_Viva_Master_Guide_Prince_Roll83.pdf"
    doc = SimpleDocTemplate(
        out_file,
        pagesize=letter,
        leftMargin=42,
        rightMargin=42,
        topMargin=44,
        bottomMargin=46,
    )
    st = make_styles()
    story = []

    # ══════════════════════════════════════════════════════════════════════════
    # HERO BANNER (PAGE 1 TOP)
    # ══════════════════════════════════════════════════════════════════════════
    hero_p = Paragraph(
        "<font size='10' color='#FDE68A'>GUJARAT UNIVERSITY • BCA SEM 7 • COURSE: DSC-M-BCA-471P</font><br/>"
        "<font size='20' color='#FFFFFF'><b>BloodConnect — Ultimate Viva &amp; Concept Guide</b></font><br/>"
        "<font size='10.5' color='#FEF3C7'>Baccha-Level Hinglish Analogies + Ready-to-Speak Examiner Answers</font><br/>"
        "<font size='9.5' color='#FFFFFF'>Student: <b>Rajput Prince Singh (Roll No: 83)</b>  |  Guide: <b>Prof. Sejal Shah</b>  |  Live: <b>bloodconnector.runasp.net</b></font>",
        st["HeroTitle"]
    )
    hero_table = Table([[hero_p]], colWidths=[528])
    hero_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), BURGUNDY_DARK),
        ("BOX", (0, 0), (-1, -1), 2, GOLD),
        ("TOPPADDING", (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ("LEFTPADDING", (0, 0), (-1, -1), 14),
        ("RIGHTPADDING", (0, 0), (-1, -1), 14),
    ]))
    story.append(hero_table)
    story.append(Spacer(1, 10))

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 1: PROJECT KYA HAI & MOTIVE KYA HAI (WITH EXAMPLE)
    # ══════════════════════════════════════════════════════════════════════════
    story.append(section_header(
        "1",
        "Mera Project Kya Hai & Iska Motive Kya Hai? (With Real Example)",
        "Sabse pehla sawal jo Examiner puchega: 'Tell me about your project BloodConnect and why you built it.'"
    ))
    story.append(Spacer(1, 8))

    story.append(callout_card(
        "CORE IDEA",
        "BloodConnect Kya Hai? (3-Saal Ke Bacche Ki Bhasha Me)",
        "Socho raat ke 2 baje Ahmedabad ke Civil Hospital me ek patient 'Rajesh' ko turant B+ khoon (blood) chahiye. Abhi log kya karte hain? WhatsApp status lagate hain ya 50 dosto ko phone ghumate hain. Isme 3-4 ghante nikal jaate hain, aadhe phone switch off aate hain, ya galat blood group wale milte hain. BloodConnect ek 'Smart Emergency Matchmaker' website hai! Jaise Uber/Ola sabse paas wale cab driver ko turant dhoondh deta hai, waise hi BloodConnect 2 second ke andar sahi blood group wale verified donors ko dhoondh deta hai aur unke screen par ghanti (live notification + sound) baja deta hai!",
        "BloodConnect is a real-time, full-stack blood donation management platform built on ASP.NET Core 10 MVC and Entity Framework Core 10. Its primary motive is to eliminate life-threatening delays during medical emergencies by replacing slow WhatsApp forwards with instant, medically accurate blood compatibility matching, a two-way pledge workflow, and SignalR live notifications.",
        border_color=CRIMSON, bg_color=CREAM_BG
    ))

    story.append(callout_card(
        "REAL-LIFE EXAMPLE",
        "Examiner Ko Samjhane Ke Liye Step-by-Step Story Example",
        "1. Patient Rajesh ke bhai ne bina login kiye (Guest Mode me) BloodConnect par 'B+ Critical Request' daali. "
        "2. Jaise hi request submit hui, SignalR WebSocket ke zariye Admin ke screen par 'Ting-Tong' (880Hz-1174Hz chime) baji. "
        "3. Donor 'Pawan' (jiska blood O- ya B+ hai) ne request dekhi aur 'I Can Donate' button dabaya -> Status ban gaya PLEDGED. "
        "4. Rajesh ke bhai ne Pawan ka offer ACCEPT kiya -> Baki saare pending offers apne aap REJECT ho gaye aur Pawan ka mobile number screen par dikh gaya! "
        "5. Blood dene ke baad dono ne COMPLETED mark kiya -> Request ban gayi FULFILLED!",
        "For example, if a trauma patient needs A+ blood urgently, a family member can post a request as a Guest without wasting time registering. Our BloodCompatibility engine automatically matches A+, A-, O+, and O- donors. When a donor pledges and the owner accepts, all competing offers are auto-rejected in a single database transaction, and the donor's phone number is securely revealed.",
        border_color=BURGUNDY, bg_color=BLUE_LIGHT
    ))

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 2: USP — MERA PROJECT DUSRI WEBSITES SE ALAG KAISE HAI?
    # ══════════════════════════════════════════════════════════════════════════
    story.append(section_header(
        "2",
        "Mera Project Dusri Blood Websites Se Alag Kaise Hai? (5 Killer USPs)",
        "Why BloodConnect is superior to traditional blood directory websites (Friends2Support, static portals, etc.)",
        bg_color=NAVY_BLUE
    ))
    story.append(Spacer(1, 8))

    usp_data = [
        [
            Paragraph("<b>Feature / Problem</b>", st["TableHeader"]),
            Paragraph("<b>Purani / Dusri Blood Websites</b>", st["TableHeader"]),
            Paragraph("<b>Mera BloodConnect (Unique USP)</b>", st["TableHeader"]),
        ],
        [
            Paragraph("<b>1. Donor Contact Privacy</b>", st["TableCellBold"]),
            Paragraph("Phone number khule-aam public search me dikhta hai. Spammers number chura lete hain aur donors pareshan hote hain.", st["TableCell"]),
            Paragraph("<b>Privacy-First Masking:</b> Search me phone number chhupa rehta hai. Sirf tab dikhta hai jab Request Owner donor ka pledge <b>Accept</b> karta hai!", st["TableCell"]),
        ],
        [
            Paragraph("<b>2. Donation Tracking</b>", st["TableCellBold"]),
            Paragraph("Sirf phonebook ki tarah naam-number dikhati hain. Pata hi nahi chalta ki donor aaya ya nahi.", st["TableCell"]),
            Paragraph("<b>Two-Way Pledge State Machine:</b> Proper lifecycle (<i>Pledged -> Accepted -> Completed -> Fulfilled</i>) with auto-reject of rival offers.", st["TableCell"]),
        ],
        [
            Paragraph("<b>3. Emergency Login Barrier</b>", st["TableCellBold"]),
            Paragraph("Pehle 10-field ka account banao, OTP dalo, tab jaake request post hogi (Emergency me time waste).", st["TableCell"]),
            Paragraph("<b>Guest-Friendly Emergency Request:</b> Emergency me bina login kiye koi bhi blood request post kar sakta hai (Nullable <i>UserId</i>).", st["TableCell"]),
        ],
        [
            Paragraph("<b>4. Blood Group Matching</b>", st["TableCellBold"]),
            Paragraph("Exact match dhundhti hain (A+ maanga toh sirf A+ dikhayengi, jabki O- aur O+ bhi de sakte hain).", st["TableCell"]),
            Paragraph("<b>O(1) Medical Compatibility Engine:</b> <i>BloodCompatibility.cs</i> A+ maangne par <i>O-, O+, A-, A+</i> charo compatible groups dhoondhta hai!", st["TableCell"]),
        ],
        [
            Paragraph("<b>5. Live Notifications</b>", st["TableCellBold"]),
            Paragraph("Page baar-baar refresh (F5) karna padta hai naye requests ya offers dekhne ke liye.", st["TableCell"]),
            Paragraph("<b>SignalR WebSockets + Web Audio API:</b> Bina page refresh kiye live toast popup, bouncing bell badge aur WhatsApp jaisi chime bajti hai!", st["TableCell"]),
        ],
    ]
    usp_table = Table(usp_data, colWidths=[110, 195, 223])
    usp_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), BURGUNDY),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.6, BORDER_WARM),
        ("BACKGROUND", (0, 1), (-1, 1), colors.white),
        ("BACKGROUND", (0, 2), (-1, 2), CREAM_BG),
        ("BACKGROUND", (0, 3), (-1, 3), colors.white),
        ("BACKGROUND", (0, 4), (-1, 4), CREAM_BG),
        ("BACKGROUND", (0, 5), (-1, 5), colors.white),
        ("PADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(usp_table)
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 3: BACCHA LEVEL CORE CONCEPTS (JSON, REST API, CRUD, HTTP VERBS)
    # ══════════════════════════════════════════════════════════════════════════
    story.append(section_header(
        "3",
        "Core Concepts — 3 Saal Ke Bacche Ke Level Se Samjho!",
        "JSON, REST API, CRUD Operations (GET, POST, PUT, DELETE) & HTTP Status Codes",
        bg_color=BURGUNDY
    ))
    story.append(Spacer(1, 8))

    story.append(callout_card(
        "CONCEPT 1",
        "JSON Kya Hota Hai? (JavaScript Object Notation)",
        "Socho aapka C# server Gujarati bolta hai aur mobile app ya Postman English bolta hai. Dono aapas me baat kaise karenge? JSON ek 'Transparent Tiffin Box' hai jiske har dabbe par sticker laga hota hai (Key-Value Pair, jaise {\"name\": \"Pawan\", \"bloodGroup\": \"O-\"}). Ye itna halka aur simple text format hai ki duniya ki har programming language isko padh sakti hai!",
        "JSON (JavaScript Object Notation) is a lightweight, text-based data-interchange format using key-value pairs. In BloodConnect, our REST API serializes C# DTOs (like DonorDto) into JSON so any client—whether a browser, Postman, or mobile app—can consume our data.",
        border_color=GOLD, bg_color=CREAM_BG
    ))

    story.append(callout_card(
        "CONCEPT 2",
        "REST API Kya Hoti Hai? (Representational State Transfer)",
        "Socho aap ek Restaurant me baithe ho. Aap (Browser/Postman) seedha Kitchen (SQL Server Database) me ghus kar khana nahi bana sakte! Beech me ek 'Waiter' hota hai jo aapka order kitchen tak le jata hai aur khana wapas lata hai. Wo Waiter hi REST API hai! Hamare project me DonorApiController (/api/donor) aur AuthApiController (/api/auth) wo Waiter hain.",
        "A REST API is an architectural style that allows different software applications to communicate over HTTP using standard stateless methods (GET, POST, PUT, DELETE) and JSON payloads. In BloodConnect, it allows external apps to search and manage donors without needing the Razor HTML views.",
        border_color=NAVY_BLUE, bg_color=BLUE_LIGHT
    ))

    story.append(Paragraph("<b>CRUD Operations &amp; HTTP Methods (Khilone / Toy Box Ki Kahani Se Samjho):</b>", st["SubHeading"]))

    crud_data = [
        [
            Paragraph("<b>CRUD Letter</b>", st["TableHeader"]),
            Paragraph("<b>HTTP Verb</b>", st["TableHeader"]),
            Paragraph("<b>Baccha Analogy (Toy Box)</b>", st["TableHeader"]),
            Paragraph("<b>Mera BloodConnect Endpoint &amp; Status Code</b>", st["TableHeader"]),
        ],
        [
            Paragraph("<b>C = Create</b>", st["TableCellBold"]),
            Paragraph("<b>POST</b>", st["TableCellBold"]),
            Paragraph("Toy box ke andar ek <b>naya khilona daalna</b>. Server naya record banata hai.", st["TableCell"]),
            Paragraph("<b>POST /api/donor</b> -> Naya donor banata hai. Success par <b>201 Created</b> deta hai (Duplicate ho toh <b>409 Conflict</b>).", st["TableCell"]),
        ],
        [
            Paragraph("<b>R = Read</b>", st["TableCellBold"]),
            Paragraph("<b>GET</b>", st["TableCellBold"]),
            Paragraph("Toy box khol kar <b>khilone dekhna</b> (bina kuch badle). Sabse safe operation!", st["TableCell"]),
            Paragraph("<b>GET /api/donor</b> ya <b>GET /api/donor/search?bloodGroup=A+</b> -> Data lata hai. Status: <b>200 OK</b> (Na mile toh <b>404 Not Found</b>).", st["TableCell"]),
        ],
        [
            Paragraph("<b>U = Update</b>", st["TableCellBold"]),
            Paragraph("<b>PUT</b>", st["TableCellBold"]),
            Paragraph("Pehle se rakhe khilone ka <b>rang ya battery badalna</b> (Existing data edit karna).", st["TableCell"]),
            Paragraph("<b>PUT /api/donor/{id}</b> -> Sirf Owner ya Admin donor update kar sakta hai. Status: <b>200 OK</b>.", st["TableCell"]),
        ],
        [
            Paragraph("<b>D = Delete</b>", st["TableCellBold"]),
            Paragraph("<b>DELETE</b>", st["TableCellBold"]),
            Paragraph("Toy box me se khilona <b>bahar fek dena / mita dena</b>.", st["TableCell"]),
            Paragraph("<b>DELETE /api/donor/{id}</b> -> Record delete karta hai. Status: <b>204 No Content</b> (Dusra user kare toh <b>403 Forbidden</b>).", st["TableCell"]),
        ],
    ]
    crud_table = Table(crud_data, colWidths=[72, 65, 175, 216])
    crud_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), CRIMSON),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.6, BORDER_WARM),
        ("BACKGROUND", (0, 1), (-1, 1), colors.white),
        ("BACKGROUND", (0, 2), (-1, 2), CREAM_BG),
        ("BACKGROUND", (0, 3), (-1, 3), colors.white),
        ("BACKGROUND", (0, 4), (-1, 4), CREAM_BG),
        ("PADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(crud_table)
    story.append(Spacer(1, 8))

    status_p = Paragraph(
        "<b>8 HTTP Status Codes Jo Viva Me Puchenge (1-Second Memory Trick):</b><br/>"
        "• <b>200 OK:</b> Sab badhiya hai (GET/PUT pass)  |  "
        "• <b>201 Created:</b> Naya record ban gaya (POST pass)  |  "
        "• <b>204 No Content:</b> Delete ho gaya, wapas bhejne ko kuch nahi<br/>"
        "• <b>400 Bad Request:</b> Form me galti hai (Age 17 daali ya State 'Wakanda' daala)  |  "
        "• <b>401 Unauthorized:</b> 'Tum kaun ho?' (Bina login kiye API maari)<br/>"
        "• <b>403 Forbidden:</b> 'Main janta hu tum kaun ho, par ye tumhara data nahi hai!' (IDOR Test 24)  |  "
        "• <b>404 Not Found:</b> ID 999999 exist nahi karti  |  "
        "• <b>409 Conflict:</b> Ek user 2 donor profile nahi bana sakta!",
        st["CardBody"]
    )
    st_box = Table([[status_p]], colWidths=[528])
    st_box.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), GOLD_LIGHT),
        ("BOX", (0, 0), (-1, -1), 1, GOLD),
        ("PADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(st_box)
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 4: API TESTING, POSTMAN VS SWAGGER & COOKIE AUTH VS JWT
    # ══════════════════════════════════════════════════════════════════════════
    story.append(section_header(
        "4",
        "API Testing, Postman vs Swagger & Cookie vs JWT (Most Important!)",
        "Examiner pakka puchega: 'Tumhare dost ne JWT use kiya, tumne kya use kiya? Aur Postman kyu use kiya?'",
        bg_color=PURPLE_VIVA
    ))
    story.append(Spacer(1, 8))

    story.append(callout_card(
        "API TESTING",
        "API Testing Kya Hoti Hai?",
        "Website ke sundar buttons aur forms ke peeche jo C# engine (API) laga hai, usko bina browser/UI ke seedha test karna! Jaise car ki body lagane se pehle engine ko workshop me chala kar check karte hain ki brake aur accelerator sahi kaam kar rahe hain ya nahi. Maine kul 28 API tests kiye hain (Happy path, 400 validation, 401 unauth, 403 IDOR, 409 duplicate, XSS aur SQL Injection).",
        "API testing is the process of directly testing backend HTTP endpoints by sending JSON requests and verifying status codes, response payloads, validation rules, and security boundaries independently of the frontend UI.",
        border_color=PURPLE_VIVA, bg_color=PURPLE_LIGHT
    ))

    story.append(Paragraph("<b>Postman vs Swagger UI — Kya Farak Hai Aur Maine Postman Se Testing Kyu Ki?</b>", st["SubHeading"]))

    ps_data = [
        [
            Paragraph("<b>Point of Comparison</b>", st["TableHeader"]),
            Paragraph("<b>Swagger UI (/swagger)</b>", st["TableHeader"]),
            Paragraph("<b>Postman Desktop (Maine 28 Tests Isme Kiye)</b>", st["TableHeader"]),
        ],
        [
            Paragraph("<b>1. Asli Kaam Kya Hai?</b>", st["TableCellBold"]),
            Paragraph("Ye API ka <b>Live Menu Card (Documentation)</b> hai jo code se auto-generate hota hai.", st["TableCell"]),
            Paragraph("Ye ek <b>Complete API Testing Laboratory</b> hai jisme hum test suites aur automation banate hain.", st["TableCell"]),
        ],
        [
            Paragraph("<b>2. Cookie &amp; Session Handling</b>", st["TableCellBold"]),
            Paragraph("Browser ke current session se chipka rehta hai; 2 alag users (User A vs User B) ko test karna mushkil hai.", st["TableCell"]),
            Paragraph("<b>Built-in Cookie Jar:</b> Postman `.AspNetCore.Identity.Application` cookie ko control karne deta hai (IDOR Test 24 ke liye best!).", st["TableCell"]),
        ],
        [
            Paragraph("<b>3. Saved Test Collection</b>", st["TableCellBold"]),
            Paragraph("Page band karte hi saare test inputs gayab ho jaate hain.", st["TableCell"]),
            Paragraph("Maine apne saare <b>28 API Tests</b> save kiye hain (<i>BloodConnect.postman_collection.json</i>) jo 1 click me dubara run ho sakte hain.", st["TableCell"]),
        ],
    ]
    ps_table = Table(ps_data, colWidths=[115, 195, 218])
    ps_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY_BLUE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.6, BORDER_WARM),
        ("BACKGROUND", (0, 1), (-1, 1), colors.white),
        ("BACKGROUND", (0, 2), (-1, 2), BLUE_LIGHT),
        ("BACKGROUND", (0, 3), (-1, 3), colors.white),
        ("PADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(ps_table)
    story.append(Spacer(1, 8))

    story.append(callout_card(
        "VIVA TRAP QUESTION",
        "Tumne JWT Use Kyu Nahi Kiya? Cookie Authentication Kyu Use Kiya?",
        "Socho Water Park me 2 tarah ke pass milte hain: "
        "1. JWT (Paper Ticket): Ek baar de diya toh jab tak time khatam nahi hota, gatekeeper usko rok nahi sakta (Stateless). "
        "2. Cookie Auth (Haath Ka Wristband - Jo Maine Use Kiya): Browser har ride (request) par apne aap wristband dikhata hai, HttpOnly=true hone se koi chor (JavaScript XSS) isko chura nahi sakta, aur sabse badi baat — agar koi fake blood request daale aur Admin usko BAN kare, toh mera 'OnValidatePrincipal' gatekeeper AGLI SECOND uska wristband kaat kar usko bahar fek deta hai! SignalR WebSockets ke saath bhi Cookie Auth makkhan ki tarah kaam karta hai.",
        "While JWT is stateless and cannot be easily revoked before expiration without a custom blacklist, BloodConnect requires instant moderation for medical safety. I used ASP.NET Core Identity Cookie Authentication with HttpOnly=true, SameSite=Lax, and a custom OnValidatePrincipal event. Even for REST API calls (/api/auth/login), Postman receives the encrypted Identity cookie, and if an Admin bans a malicious user, their session is invalidated immediately on the very next request.",
        border_color=GREEN_PASS, bg_color=GREEN_LIGHT
    ))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 5: TOP 10 TECHNICAL VIVA QUESTIONS (FROM YOUR REPORT & CODE)
    # ══════════════════════════════════════════════════════════════════════════
    story.append(section_header(
        "5",
        "Top 10 Project & Report Viva Questions (With Baccha Logic)",
        "Prof. Sejal Shah ya External Examiner aapki report dekh kar jo 10 sabse main sawal puchenge",
        bg_color=BURGUNDY
    ))
    story.append(Spacer(1, 8))

    qas = [
        (
            "Q1", "How does your Blood Compatibility logic work in code?",
            "Humne database me table banane ke bajaye C# ka 'switch expression' (BloodCompatibility.cs) banaya hai. Jaise O- sabko khoon de sakta hai (Universal Donor) aur AB+ sabse le sakta hai (Universal Receiver). Ye 0 second — yaani O(1) time me jawab deta hai.",
            "It is implemented as a static C# switch expression in BloodCompatibility.cs that maps any recipient blood group to a read-only list of compatible donor groups in O(1) constant time, following real RBC transfusion rules."
        ),
        (
            "Q2", "What is IDOR and how did you prevent it in BloodConnect?",
            "IDOR (Insecure Direct Object Reference) ka matlab hai URL me '/Donor/Edit/5' ki jagah '/Donor/Edit/6' likh kar kisi dusre ka data chhedna. Maine har Edit/Delete par server-side check lagaya hai: 'Kya ye record isi logged-in user ka hai?' Agar nahi, toh Test 24 ki tarah 403 Forbidden aata hai!",
            "IDOR occurs when a user manipulates an ID in the URL or API to access another user's resource. I prevented it by enforcing server-side ownership checks (if donor.UserId != currentUserId && !User.IsInRole('Admin') return Forbid()) on every update and delete action."
        ),
        (
            "Q3", "What is Optimistic Concurrency (RowVersion) in your Donor model?",
            "Socho 2 Admin ek hi time par ek donor ka data edit karke Save dabayein. Pehle wale ka save gayab na ho, isliye Donor table me 'RowVersion' naam ka ek secret stamp ([Timestamp] byte[]) hota hai. Agar beech me data badal gaya, toh EF Core 'DbUpdateConcurrencyException' dekar rok deta hai.",
            "I added a [Timestamp] byte[] RowVersion property on the Donor entity. SQL Server automatically updates this binary token on every edit. If two users modify the same record concurrently, EF Core detects the RowVersion mismatch and throws a DbUpdateConcurrencyException, preventing lost updates."
        ),
        (
            "Q4", "Why did you use IMemoryCache with a 60-second TTL only for unread messages?",
            "Admin navbar me 'Unread Messages' ka badge har page load par dikhta hai. Har baar database ko puchna paani ki tanki baar-baar check karne jaisa hai. Isliye 60 second ke liye count ko RAM (IMemoryCache) me rakh liya, aur jab naya message aaye toh cache clear kar diya!",
            "Unread message counts are read on every page navigation but written rarely. Caching the count in IMemoryCache for 60 seconds reduces repetitive SQL queries by over 90%, and we explicitly invalidate the cache whenever a message is created or read."
        ),
        (
            "Q5", "How did you prevent SQL Injection (Test 28) and XSS (Test 27)?",
            "SQL Injection: Humne kahi bhi string jod kar raw SQL nahi likhi; EF Core LINQ apne aap input ko 'Parameter' bana deta hai (Test 28 me 'Gujarat OR 1=1' ko sirf ek naam samjha). XSS: Razor Engine har output ko encode kar deta hai, toh <script> tag execute hone ke bajaye plain text ban kar dikhta hai.",
            "SQL Injection is prevented because EF Core uses parameterized LINQ queries exclusively, treating malicious inputs as literal values. XSS is prevented because the Razor View Engine automatically HTML-encodes all rendered output."
        ),
    ]

    for q_num, q, hint, ans in qas:
        story.append(qa_card(q_num, q, hint, ans))

    story.append(PageBreak())

    qas_part2 = [
        (
            "Q6", "Explain your Role Hierarchy (SuperAdmin > Admin > User).",
            "3-manzil ki building hai: Sabse upar SuperAdmin (Boss - jisko koi ban ya delete nahi kar sakta, warna pura system lock ho jayega). Beech me Admin (jo normal users ko ban kar sakta hai par dusre Admin ko nahi). Neeche User (jo donor ya patient banta hai). Aur koi khud ko ban nahi kar sakta!",
            "BloodConnect enforces a strict 3-tier hierarchy: SuperAdmin is immutable and cannot be banned, demoted, or deleted. Admins can moderate regular Users and requests but cannot ban fellow Admins. Self-protection rules also prevent any admin from banning themselves."
        ),
        (
            "Q7", "How do your Real-Time Notifications & Sound Chime work?",
            "Humne SignalR WebSocket pipe lagaya hai (/hubs/notifications). Jab naya request ya pledge hota hai, server turant pipe se JSON bhejta hai. Aur sound ke liye koi MP3 file nahi daali — Browser ke Web Audio API se 880Hz aur 1174Hz ki do musical waves jod kar WhatsApp jaisi घंटी bajayi hai!",
            "We use ASP.NET Core SignalR over WebSockets with role-based groups ('admins' and 'user_{id}'). On any state change, NotificationService pushes a payload to the target group, and the client plays a procedural two-tone harmonic chime (880Hz and 1174Hz) synthesized via the browser's Web Audio API."
        ),
        (
            "Q8", "Why is there a Unique Compound Index on (RequestId, DonorId) in DonationOffer?",
            "Taaki ek hi donor ek hi blood request par 10 baar 'I Can Donate' daba kar spam na kar sake! Database level par hi lock laga diya hai ki 1 Request + 1 Donor = Sirf 1 Offer.",
            "In ApplicationDbContext, I configured a unique compound index on (RequestId, DonorId) in the DonationOffers table. This guarantees at the database level that a donor can pledge only once per blood request."
        ),
        (
            "Q9", "What is the difference between Code-First and Database-First in EF Core?",
            "Code-First (Jo maine use kiya): Pehle C# me classes (Donor.cs, BloodRequest.cs) likho, aur 'dotnet ef migrations add' chala kar SQL Server tables apne aap banwao. Database-First: Pehle SQL me table banao phir C# code generate karo.",
            "I used the EF Core Code-First approach where domain models and relationships are defined in C# classes and Fluent API, and database schema changes are version-controlled using EF Core Migrations."
        ),
        (
            "Q10", "How did you deploy BloodConnect to production?",
            "Code ko Release mode me publish kiya aur MonsterASP.NET ke Windows Shared Hosting par daala. Database SQL Server 2025 par host kiya, appsettings.Production.json me connection string lagayi, aur Let's Encrypt se free HTTPS SSL lock lagaya.",
            "The application is deployed on MonsterASP.NET Windows shared hosting with a managed SQL Server database and automatic Let's Encrypt HTTPS SSL at https://bloodconnector.runasp.net."
        ),
    ]

    for q_num, q, hint, ans in qas_part2:
        story.append(qa_card(q_num, q, hint, ans))

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 6: ADVANTAGES, LIMITATIONS & FUTURE SCOPE
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Spacer(1, 4))
    story.append(section_header(
        "6",
        "Advantages, Limitations & Future Scope (Honest Viva Answers)",
        "Examiner jab puche: 'Tell me the advantages and limitations/drawbacks of your system'",
        bg_color=NAVY_BLUE
    ))
    story.append(Spacer(1, 8))

    adv_lim_data = [
        [
            Paragraph("<b>Advantages (Mere Project Ke Fayde)</b>", st["TableHeader"]),
            Paragraph("<b>Limitations (Abhi Kya Kami Hai — Be Honest!)</b>", st["TableHeader"]),
            Paragraph("<b>Future Scope (Aage Kya Jorenge)</b>", st["TableHeader"]),
        ],
        [
            Paragraph(
                "• <b>Instant Matching:</b> O(1) compatibility logic se seconds me sahi donor milta hai.<br/><br/>"
                "• <b>100% Privacy Safe:</b> Pledge accept hone tak donor ka phone number chhupa rehta hai.<br/><br/>"
                "• <b>Zero Emergency Friction:</b> Guest user bina login ke request daal sakta hai.<br/><br/>"
                "• <b>Live WebSockets:</b> Bina page refresh kiye bell badge aur sound chime bajti hai.<br/><br/>"
                "• <b>Enterprise Security:</b> CSRF, XSS, SQLi, IDOR aur RowVersion concurrency se protected hai.",
                st["TableCell"]
            ),
            Paragraph(
                "• <b>1. No Lab Report Verification Yet:</b> Abhi donor apna blood group khud select karta hai (Pathology lab PDF verification abhi nahi hai).<br/><br/>"
                "• <b>2. State/City Text Filter vs Live GPS:</b> Abhi State aur City se filter hota hai, exact 5km Google Map GPS radius nahi hai.<br/><br/>"
                "• <b>3. Internet Dependency:</b> SignalR notifications ke liye donor ka internet on hona chahiye (Offline SMS abhi nahi jata).<br/><br/>"
                "• <b>4. Shared Hosting Cold Start:</b> Free tier MonsterASP hosting par 20 min idle rehne par pehla load 3-4 sec leta hai.",
                st["TableCell"]
            ),
            Paragraph(
                "• <b>1. Twilio SMS &amp; WhatsApp API:</b> Critical request aate hi offline donors ko direct SMS jayega.<br/><br/>"
                "• <b>2. Google Maps Geolocation:</b> Hospital se 5 km ke daayre (radius) me donors ko map par dikhana.<br/><br/>"
                "• <b>3. Medical Cooldown Tracker:</b> Ek baar blood dene ke baad donor ko 90 days (3 mahine) ke liye auto-unavailable karna.<br/><br/>"
                "• <b>4. Mobile App (.NET MAUI):</b> Android/iOS app with background push notifications.",
                st["TableCell"]
            ),
        ]
    ]
    adv_table = Table(adv_lim_data, colWidths=[176, 176, 176])
    adv_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), GREEN_PASS),
        ("BACKGROUND", (1, 0), (1, 0), CRIMSON),
        ("BACKGROUND", (2, 0), (2, 0), PURPLE_VIVA),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.7, BORDER_WARM),
        ("BACKGROUND", (0, 1), (0, 1), GREEN_LIGHT),
        ("BACKGROUND", (1, 1), (1, 1), CREAM_BG),
        ("BACKGROUND", (2, 1), (2, 1), PURPLE_LIGHT),
        ("PADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(adv_table)
    story.append(Spacer(1, 10))

    final_p = Paragraph(
        "<b>VIVA GOLDEN TIP FOR PRINCE (ROLL NO: 83):</b><br/>"
        "Jab Examiner puche <i>'Show me something unique in your project'</i>, toh turant 2 browser tabs kholna — "
        "Ek me Admin login rakhna aur dusre me Guest Request daalna. Jaise hi <b>SignalR ki घंटी (Chime + Toast)</b> "
        "bina page refresh kiye bajegi aur aap <b>BloodCompatibility.cs</b> + <b>28 Postman Tests</b> dikhaoge, "
        "full marks (100/100) pakke hain! All the best bhai!",
        st["CardBody"]
    )
    final_box = Table([[final_p]], colWidths=[528])
    final_box.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), GOLD_LIGHT),
        ("BOX", (0, 0), (-1, -1), 1.5, BURGUNDY),
        ("PADDING", (0, 0), (-1, -1), 10),
    ]))
    story.append(final_box)

    doc.build(story, onFirstPage=draw_page_decorations, onLaterPages=draw_page_decorations)
    print("======================================================================")
    print(f"SUCCESS! Viva Master Guide PDF Generated: {out_file}")
    print("======================================================================")


if __name__ == "__main__":
    build_viva_pdf()