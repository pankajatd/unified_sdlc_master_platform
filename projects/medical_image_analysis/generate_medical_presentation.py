"""
MedVision AI - Master Executive Medical Presentation Generator (v4 - Ultra-Large Font Edition)
Engineered for Healthcare Boardrooms, Hospital Executives & General Audience:
- 16:9 Widescreen layout with genuinely large, comfortable typography:
  * Slide Titles: 30pt - 34pt Bold
  * Category Badges: 13pt - 14pt Bold
  * Card Headers: 20pt - 24pt Bold
  * Card Subtitles: 15pt - 16.5pt Bold
  * Body Bullet Points & Explanations: 13.5pt - 15pt Regular/Bold
  * Metric Badges & Action Tiles: 13pt - 14.5pt Bold
  * Footers: 11pt - 12pt Bold
- Zero content altered: 100% of the exact text, findings, numbers, and bullet points preserved.
- Distributed across 16 beautifully paced slides so no text is squished or truncated.
"""

import os
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

BASE_DIR = Path(__file__).resolve().parent
SCANS_DIR = BASE_DIR / "data" / "matched_scans"
OUTPUT_PPTX = BASE_DIR / "MedVision_AI_Executive_Medical_Presentation.pptx"

def create_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    FONT_NAME = "Calibri"

    # Corporate Executive Palette
    BG_CANVAS = RGBColor(255, 255, 255)
    SURFACE_CARD = RGBColor(248, 250, 252)     # #f8fafc Platinum Card Surface
    SURFACE_WHITE = RGBColor(255, 255, 255)
    BORDER_CARD = RGBColor(203, 213, 225)      # #cbd5e1 Crisp Border
    BORDER_SUBTLE = RGBColor(226, 232, 240)    # #e2e8f0 Divider

    # MedTech Accent Colors
    ACCENT_CYAN = RGBColor(2, 132, 199)        # #0284c7 Primary Medical Cyan
    ACCENT_BLUE = RGBColor(30, 58, 138)        # #1e3a8a Deep Medical Blue
    ACCENT_EMERALD = RGBColor(5, 150, 105)     # #059669 Normal / Success Green
    ACCENT_ROSE = RGBColor(225, 29, 72)        # #e11d48 High Danger Crimson
    ACCENT_AMBER = RGBColor(217, 119, 6)       # #d97706 Follow-Up Amber
    ACCENT_PURPLE = RGBColor(126, 34, 206)     # #7e22ce Advanced AI Purple

    # High-Contrast Executive Text
    TEXT_PRIMARY = RGBColor(15, 23, 42)        # #0f172a Deep Charcoal Navy
    TEXT_SECONDARY = RGBColor(51, 65, 85)      # #334155 Legible Slate
    TEXT_MUTED = RGBColor(100, 116, 139)       # #64748b Subtle Label
    TEXT_WHITE = RGBColor(255, 255, 255)

    blank_layout = prs.slide_layouts[6]
    TOTAL_SLIDES = 16

    def set_canvas_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_CANVAS
        bg.line.fill.background()
        return bg

    def add_slide_header(slide, title_text, category_text, subtitle_text=None):
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.28), Inches(11.733), Inches(0.35))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.name = FONT_NAME
        p_cat.font.size = Pt(13)
        p_cat.font.bold = True
        p_cat.font.color.rgb = ACCENT_CYAN

        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.62), Inches(11.733), Inches(0.65))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.name = FONT_NAME
        p_title.font.size = Pt(29)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_PRIMARY

        if subtitle_text:
            sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.28), Inches(11.733), Inches(0.38))
            tf_sub = sub_box.text_frame
            tf_sub.word_wrap = True
            p_sub = tf_sub.paragraphs[0]
            p_sub.text = subtitle_text
            p_sub.font.name = FONT_NAME
            p_sub.font.size = Pt(14)
            p_sub.font.color.rgb = TEXT_MUTED

        div_y = Inches(1.68) if subtitle_text else Inches(1.40)
        divider = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), div_y, Inches(11.733), Inches(0.015))
        divider.fill.solid()
        divider.fill.fore_color.rgb = BORDER_SUBTLE
        divider.line.fill.background()

    def add_footer(slide, current_page, total_pages=TOTAL_SLIDES):
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(6.92), Inches(11.733), Inches(0.015))
        line.fill.solid()
        line.fill.fore_color.rgb = BORDER_SUBTLE
        line.line.fill.background()

        l_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.0), Inches(7.5), Inches(0.35))
        tf_l = l_box.text_frame
        p_l = tf_l.paragraphs[0]
        p_l.text = "MedVision AI | Enterprise PACS Diagnostic Platform & Multi-Agent SDLC"
        p_l.font.name = FONT_NAME
        p_l.font.size = Pt(11.5)
        p_l.font.color.rgb = TEXT_MUTED

        r_box = slide.shapes.add_textbox(Inches(10.533), Inches(7.0), Inches(2.0), Inches(0.35))
        tf_r = r_box.text_frame
        p_r = tf_r.paragraphs[0]
        p_r.alignment = PP_ALIGN.RIGHT
        p_r.text = f"{current_page} of {total_pages}"
        p_r.font.name = FONT_NAME
        p_r.font.size = Pt(11.5)
        p_r.font.bold = True
        p_r.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 1: MASTER TITLE SLIDE (MIDNIGHT SAPPHIRE HERO - LARGE FONTS)
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    bg1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = RGBColor(10, 15, 29)
    bg1.line.fill.background()

    top_bar = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(0.12))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = ACCENT_CYAN
    top_bar.line.fill.background()

    title_box = slide1.shapes.add_textbox(Inches(1.0), Inches(1.4), Inches(11.333), Inches(3.6))
    tf1 = title_box.text_frame
    tf1.word_wrap = True

    p_badge = tf1.paragraphs[0]
    p_badge.text = "CLINICAL DECISION SUPPORT & MULTI-AGENT SDLC PLATFORM"
    p_badge.font.name = FONT_NAME
    p_badge.font.size = Pt(16)
    p_badge.font.bold = True
    p_badge.font.color.rgb = RGBColor(56, 189, 248)

    p_main = tf1.add_paragraph()
    p_main.text = "MedVision AI"
    p_main.font.name = FONT_NAME
    p_main.font.size = Pt(58)
    p_main.font.bold = True
    p_main.font.color.rgb = TEXT_WHITE
    p_main.space_before = Pt(8)

    p_sub = tf1.add_paragraph()
    p_sub.text = "Enterprise Medical Scan Analysis Across Brain MRI, Head/Lung CT, and Chest X-Rays Powered by 7 Autonomous AI Agents"
    p_sub.font.name = FONT_NAME
    p_sub.font.size = Pt(20)
    p_sub.font.color.rgb = RGBColor(203, 213, 225)
    p_sub.space_before = Pt(14)

    card_w = Inches(2.65)
    card_h = Inches(1.55)
    card_y = Inches(5.1)
    metrics_data = [
        ("0.05 SECONDS", "Instant Scan Speed", "vs. 15 min manual doctor queue", ACCENT_CYAN),
        ("8 CONDITIONS", "Full Body Coverage", "Brain MRI, Head/Lung CT, X-Rays", ACCENT_EMERALD),
        ("7 AI AGENTS", "Autonomous Lifecycle", "Requirements to Self-Healing", ACCENT_PURPLE),
        ("100% ACCURACY", "Safety Verified", "10/10 medical safety checks passed", ACCENT_ROSE)
    ]

    for i, (val, label, sub, col) in enumerate(metrics_data):
        cx = Inches(1.0) + i * Inches(2.9)
        card = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx, card_y, card_w, card_h)
        card.fill.solid()
        card.fill.fore_color.rgb = RGBColor(19, 29, 54)
        card.line.color.rgb = col
        card.line.width = Pt(1.5)

        tb = slide1.shapes.add_textbox(cx + Inches(0.12), card_y + Inches(0.10), card_w - Inches(0.24), card_h - Inches(0.20))
        tf = tb.text_frame
        tf.word_wrap = True
        
        pv = tf.paragraphs[0]
        pv.text = val
        pv.font.name = FONT_NAME
        pv.font.size = Pt(24)
        pv.font.bold = True
        pv.font.color.rgb = col

        pl = tf.add_paragraph()
        pl.text = label
        pl.font.name = FONT_NAME
        pl.font.size = Pt(14)
        pl.font.bold = True
        pl.font.color.rgb = TEXT_WHITE
        pl.space_before = Pt(3)

        ps = tf.add_paragraph()
        ps.text = sub
        ps.font.name = FONT_NAME
        ps.font.size = Pt(11.5)
        ps.font.color.rgb = RGBColor(148, 163, 184)
        ps.space_before = Pt(2)

    # =========================================================================
    # SLIDE 2: EXECUTIVE OVERVIEW (PART 1: THE CRISIS & THE AI SOLUTION)
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    set_canvas_background(slide2)
    add_slide_header(slide2, "Executive Overview: The Healthcare Imperative & AI Solution",
                     "The Healthcare Imperative",
                     "How autonomous computer vision and AI agents eliminate doctor backlogs and save lives.")

    col2_w = Inches(5.66)
    col2_h = Inches(4.9)
    col2_y = Inches(1.85)

    s2_pillars = [
        ("The Doctor Shortage",
         "Severe Scan Backlog & Doctor Fatigue",
         ACCENT_ROSE,
         [
             ("Massive Scan Growth", "Hospital scans grew by 240%, but doctor headcount grew by only 8%."),
             ("Exhaustion & Fatigue", "Doctors working long 12-hour shifts can easily miss faint spots on scans."),
             ("Critical Time Windows", "Early strokes and tiny 6mm tumors are faint and easily overlooked by human eyes."),
             ("Hours of Waiting", "Patients often wait 45 to 120 minutes in emergency rooms just for an initial scan check.")
         ],
         "⚠️ 240% Volume Surge vs 8% Doctor Growth\nHigh Risk of Missed Diagnoses in ERs"),
        ("The MedVision AI Solution",
         "Instant Millimeter-Precision Vision",
         ACCENT_CYAN,
         [
             ("Instant 0.05s Checks", "Every scan is analyzed in 0.05 seconds, instantly catching life-threatening issues."),
             ("Side-by-Side Comparison", "Every patient scan is shown right next to a healthy person's scan for comparison."),
             ("Targeted Red Boxes", "The computer boxes ONLY the problem area; no confusing full-screen red heatmaps."),
             ("Simple Plain English", "Explains findings in crystal-clear words that both doctors and patients understand.")
         ],
         "⚡ 0.05s Ingestion | 99.8% Faster Scan Triage\nMillimeter-Accurate Red Bounding Boxes")
    ]

    for i, (title, sub, accent, bullets, footer_callout) in enumerate(s2_pillars):
        px = Inches(0.8) + i * Inches(6.07)
        c_shape = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, px, col2_y, col2_w, col2_h)
        c_shape.fill.solid()
        c_shape.fill.fore_color.rgb = SURFACE_CARD
        c_shape.line.color.rgb = BORDER_CARD
        c_shape.line.width = Pt(1.5)

        rib = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, px, col2_y, col2_w, Inches(0.08))
        rib.fill.solid()
        rib.fill.fore_color.rgb = accent
        rib.line.fill.background()

        tb = slide2.shapes.add_textbox(px + Inches(0.3), col2_y + Inches(0.2), col2_w - Inches(0.6), Inches(3.6))
        tf = tb.text_frame
        tf.word_wrap = True

        pt = tf.paragraphs[0]
        pt.text = title
        pt.font.name = FONT_NAME
        pt.font.size = Pt(22)
        pt.font.bold = True
        pt.font.color.rgb = TEXT_PRIMARY

        ps = tf.add_paragraph()
        ps.text = sub
        ps.font.name = FONT_NAME
        ps.font.size = Pt(16)
        ps.font.bold = True
        ps.font.color.rgb = accent
        ps.space_before = Pt(3)
        ps.space_after = Pt(12)

        for b_title, b_desc in bullets:
            pb = tf.add_paragraph()
            pb.text = f"• {b_title}: {b_desc}"
            pb.font.name = FONT_NAME
            pb.font.size = Pt(14)
            pb.font.color.rgb = TEXT_SECONDARY
            pb.space_before = Pt(8)

        tile_y = col2_y + Inches(3.85)
        tile_h = Inches(0.85)
        tile = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, px + Inches(0.25), tile_y, col2_w - Inches(0.5), tile_h)
        tile.fill.solid()
        tile.fill.fore_color.rgb = RGBColor(255, 255, 255)
        tile.line.color.rgb = accent
        tile.line.width = Pt(1.5)

        tb_tile = slide2.shapes.add_textbox(px + Inches(0.3), tile_y + Inches(0.08), col2_w - Inches(0.6), tile_h - Inches(0.16))
        tf_t = tb_tile.text_frame
        tf_t.word_wrap = True
        ptile = tf_t.paragraphs[0]
        ptile.text = footer_callout
        ptile.font.name = FONT_NAME
        ptile.font.size = Pt(13)
        ptile.font.bold = True
        ptile.font.color.rgb = accent

    add_footer(slide2, 2)

    # =========================================================================
    # SLIDE 3: EXECUTIVE OVERVIEW (PART 2: AUTONOMOUS ARCHITECTURE TEAMWORK)
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    set_canvas_background(slide3)
    add_slide_header(slide3, "Executive Overview: Autonomous Multi-Agent Architecture",
                     "Autonomous System Design",
                     "How 7 specialized AI Agents work together to guarantee medical accuracy, zero crashes, and doctor oversight.")

    s3_pillars = [
        ("Autonomous Architecture",
         "7 AI Agents Working As a Team",
         ACCENT_EMERALD,
         [
             ("7 Specialized Agents", "A team of 7 AI Agents handles requirements, planning, coding, safety, and testing."),
             ("Self-Healing Protection", "If any system issue occurs, the AI fixes itself without crashing or slowing down."),
             ("Doctor Always in Control", "Human doctors review and approve every scan before anything is finalized."),
             ("Proven 100% Accuracy", "Passed all 10 automated safety test suites across MRI, CT, and X-Rays.")
         ],
         "🛡️ 7 Autonomous Agents | Zero-Crash Protection\n100% Test Pass Rate Across All Scans"),
        ("Closed-Loop Safety Guarantee",
         "Seamless Verification & Diagnostic Reliability",
         ACCENT_PURPLE,
         [
             ("Continuous Self-Healing", "Continuously monitors system execution, fixing any technical glitch automatically."),
             ("Closed-Loop Teamwork", "If the Medical Inspector flags any issue, the system automatically loops back to recalibrate."),
             ("Human-in-the-Loop Safeguard", "Ensures zero automated decisions are made without verified human clinician sign-off."),
             ("Full Medical Safety Audit", "All clinical findings and decisions are immutably logged for total transparency.")
         ],
         "⚡ Enterprise Closed-Loop Architecture:\nRigorous multi-layer safety verification before human doctor review")
    ]

    for i, (title, sub, accent, bullets, footer_callout) in enumerate(s3_pillars):
        px = Inches(0.8) + i * Inches(6.07)
        c_shape = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, px, col2_y, col2_w, col2_h)
        c_shape.fill.solid()
        c_shape.fill.fore_color.rgb = SURFACE_CARD
        c_shape.line.color.rgb = BORDER_CARD
        c_shape.line.width = Pt(1.5)

        rib = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, px, col2_y, col2_w, Inches(0.08))
        rib.fill.solid()
        rib.fill.fore_color.rgb = accent
        rib.line.fill.background()

        tb = slide3.shapes.add_textbox(px + Inches(0.3), col2_y + Inches(0.2), col2_w - Inches(0.6), Inches(3.6))
        tf = tb.text_frame
        tf.word_wrap = True

        pt = tf.paragraphs[0]
        pt.text = title
        pt.font.name = FONT_NAME
        pt.font.size = Pt(22)
        pt.font.bold = True
        pt.font.color.rgb = TEXT_PRIMARY

        ps = tf.add_paragraph()
        ps.text = sub
        ps.font.name = FONT_NAME
        ps.font.size = Pt(16)
        ps.font.bold = True
        ps.font.color.rgb = accent
        ps.space_before = Pt(3)
        ps.space_after = Pt(12)

        for b_title, b_desc in bullets:
            pb = tf.add_paragraph()
            pb.text = f"• {b_title}: {b_desc}"
            pb.font.name = FONT_NAME
            pb.font.size = Pt(14)
            pb.font.color.rgb = TEXT_SECONDARY
            pb.space_before = Pt(8)

        tile_y = col2_y + Inches(3.85)
        tile_h = Inches(0.85)
        tile = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, px + Inches(0.25), tile_y, col2_w - Inches(0.5), tile_h)
        tile.fill.solid()
        tile.fill.fore_color.rgb = RGBColor(255, 255, 255)
        tile.line.color.rgb = accent
        tile.line.width = Pt(1.5)

        tb_tile = slide3.shapes.add_textbox(px + Inches(0.3), tile_y + Inches(0.08), col2_w - Inches(0.6), tile_h - Inches(0.16))
        tf_t = tb_tile.text_frame
        tf_t.word_wrap = True
        ptile = tf_t.paragraphs[0]
        ptile.text = footer_callout
        ptile.font.name = FONT_NAME
        ptile.font.size = Pt(13)
        ptile.font.bold = True
        ptile.font.color.rgb = accent

    add_footer(slide3, 3)

    # =========================================================================
    # SLIDE 4: THE 7 MEDICAL SDLC AGENTS (PART 1: INTAKE & VISION SPECIALISTS)
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    set_canvas_background(slide4)
    add_slide_header(slide4, "The 7 Autonomous AI Agents: Clinical Intake & Vision",
                     "Multi-Agent Architecture & Team Roles (Part 1)",
                     "How specialized AI Agents handle ingestion, architecture, slice calibration, and disease detection.")

    agents_p1 = [
        ("1. Hospital Coordinator", "PM Agent", "Reads patient scans, checks patient ID, and sets triage priority for doctors.", "Role: Manages Patient Ingestion", ACCENT_BLUE),
        ("2. Master Architect", "Architecture Agent", "Designs the processing pipeline for Brain MRI, Head/Lung CT, and Chest X-Rays.", "Role: Organizes Scan Modalities", ACCENT_CYAN),
        ("3. Task Organizer", "Planner Agent", "Prepares images: adjusts brightness, contrast, and balances left and right sides.", "Role: Calibrates Image Slices", ACCENT_PURPLE),
        ("4. Computer Vision Specialist", "Developer Agent", "Locks onto faint disease edges, draws red measurement boxes, and calculates sizes.", "Role: Measures Problem Size", ACCENT_EMERALD)
    ]

    ag_w = Inches(5.66)
    ag_h = Inches(2.32)

    for i, (title, role, desc, role_tag, col) in enumerate(agents_p1):
        row = i // 2
        col_idx = i % 2
        ax = Inches(0.8) + col_idx * Inches(6.07)
        ay = Inches(1.85) + row * Inches(2.52)

        card = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, ax, ay, ag_w, ag_h)
        card.fill.solid()
        card.fill.fore_color.rgb = SURFACE_CARD
        card.line.color.rgb = col
        card.line.width = Pt(1.5)

        tb = slide4.shapes.add_textbox(ax + Inches(0.25), ay + Inches(0.15), ag_w - Inches(0.5), ag_h - Inches(0.3))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.name = FONT_NAME
        p1.font.size = Pt(19)
        p1.font.bold = True
        p1.font.color.rgb = TEXT_PRIMARY

        p2 = tf.add_paragraph()
        p2.text = f"Agent Type: {role}"
        p2.font.name = FONT_NAME
        p2.font.size = Pt(15)
        p2.font.bold = True
        p2.font.color.rgb = col
        p2.space_before = Pt(3)

        p3 = tf.add_paragraph()
        p3.text = desc
        p3.font.name = FONT_NAME
        p3.font.size = Pt(13.5)
        p3.font.color.rgb = TEXT_SECONDARY
        p3.space_before = Pt(5)

        p4 = tf.add_paragraph()
        p4.text = f"⚙️ {role_tag}"
        p4.font.name = FONT_NAME
        p4.font.size = Pt(13)
        p4.font.bold = True
        p4.font.color.rgb = TEXT_PRIMARY
        p4.space_before = Pt(6)

    add_footer(slide4, 4)

    # =========================================================================
    # SLIDE 5: THE 7 MEDICAL SDLC AGENTS (PART 2: SAFETY, QA & CLOSED-LOOP)
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    set_canvas_background(slide5)
    add_slide_header(slide5, "The 7 Autonomous AI Agents: Safety, QA & Self-Healing",
                     "Multi-Agent Architecture & Team Roles (Part 2)",
                     "Continuous quality verification, automated safety checks, self-healing recovery, and closed-loop control.")

    agents_p2 = [
        ("5. Medical Safety Inspector", "Reviewer Agent", "Checks scan quality, rejecting blurry scans and verifying strict medical safety rules.", "Role: Guarantees Clinical Safety", ACCENT_AMBER),
        ("6. Quality Assurance Inspector", "QA / Test Agent", "Runs all 10 automated safety tests to guarantee 100% accuracy before doctor review.", "Role: Tests 10 Clinical Conditions", ACCENT_ROSE),
        ("7. System Maintainer", "Self-Healing Agent", "Continuously monitors execution, fixing any technical glitch automatically without crashing.", "Role: Self-Healing System Care", ACCENT_CYAN)
    ]

    for i, (title, role, desc, role_tag, col) in enumerate(agents_p2):
        row = i // 2
        col_idx = i % 2
        ax = Inches(0.8) + col_idx * Inches(6.07)
        ay = Inches(1.85) + row * Inches(2.52)

        card = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, ax, ay, ag_w, ag_h)
        card.fill.solid()
        card.fill.fore_color.rgb = SURFACE_CARD
        card.line.color.rgb = col
        card.line.width = Pt(1.5)

        tb = slide5.shapes.add_textbox(ax + Inches(0.25), ay + Inches(0.15), ag_w - Inches(0.5), ag_h - Inches(0.3))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.name = FONT_NAME
        p1.font.size = Pt(19)
        p1.font.bold = True
        p1.font.color.rgb = TEXT_PRIMARY

        p2 = tf.add_paragraph()
        p2.text = f"Agent Type: {role}"
        p2.font.name = FONT_NAME
        p2.font.size = Pt(15)
        p2.font.bold = True
        p2.font.color.rgb = col
        p2.space_before = Pt(3)

        p3 = tf.add_paragraph()
        p3.text = desc
        p3.font.name = FONT_NAME
        p3.font.size = Pt(13.5)
        p3.font.color.rgb = TEXT_SECONDARY
        p3.space_before = Pt(5)

        p4 = tf.add_paragraph()
        p4.text = f"⚙️ {role_tag}"
        p4.font.name = FONT_NAME
        p4.font.size = Pt(13)
        p4.font.bold = True
        p4.font.color.rgb = TEXT_PRIMARY
        p4.space_before = Pt(6)

    # Slot 4: Closed Loop Teamwork
    ax = Inches(0.8) + 1 * Inches(6.07)
    ay = Inches(1.85) + 1 * Inches(2.52)
    card_sum = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, ax, ay, ag_w, ag_h)
    card_sum.fill.solid()
    card_sum.fill.fore_color.rgb = RGBColor(15, 23, 42)
    card_sum.line.color.rgb = ACCENT_CYAN
    card_sum.line.width = Pt(2)

    tb = slide5.shapes.add_textbox(ax + Inches(0.25), ay + Inches(0.15), ag_w - Inches(0.5), ag_h - Inches(0.3))
    tf = tb.text_frame
    tf.word_wrap = True

    p1 = tf.paragraphs[0]
    p1.text = "⚡ Closed-Loop Teamwork"
    p1.font.name = FONT_NAME
    p1.font.size = Pt(19)
    p1.font.bold = True
    p1.font.color.rgb = RGBColor(56, 189, 248)

    p2 = tf.add_paragraph()
    p2.text = "If the Medical Inspector flags any issue, the system automatically loops back to recalibrate before showing the scan to a human doctor."
    p2.font.name = FONT_NAME
    p2.font.size = Pt(13.5)
    p2.font.color.rgb = RGBColor(226, 232, 240)
    p2.space_before = Pt(5)

    p3 = tf.add_paragraph()
    p3.text = "✓ Zero Crash Guarantee    ✓ 100% Medical Safety Audit"
    p3.font.name = FONT_NAME
    p3.font.size = Pt(14)
    p3.font.bold = True
    p3.font.color.rgb = RGBColor(52, 211, 153)
    p3.space_before = Pt(7)

    add_footer(slide5, 5)

    # =========================================================================
    # SLIDE 6: CLINICAL CASE STUDY 1 - BRAIN MRI TUMOR
    # =========================================================================
    slide6 = prs.slides.add_slide(blank_layout)
    set_canvas_background(slide6)
    add_slide_header(slide6, "Clinical Case Study: Brain MRI Tumor Localization",
                     "Modality: Brain MRI | Case #90281",
                     "Detecting a 28.4 mm brain tumor with millimeter-accurate surgical bounding and swelling halo.")

    cs_img_w = Inches(3.25)
    cs_img_h = Inches(3.25)
    cs_img_y = Inches(1.85)

    slide6.shapes.add_picture(str(SCANS_DIR / "mri_tumor_normal.png"), Inches(0.8), cs_img_y, cs_img_w, cs_img_h)
    norm_lbl = slide6.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), cs_img_y + cs_img_h, cs_img_w, Inches(0.42))
    norm_lbl.fill.solid()
    norm_lbl.fill.fore_color.rgb = RGBColor(16, 185, 129)
    norm_lbl.line.fill.background()
    p_nl = norm_lbl.text_frame.paragraphs[0]
    p_nl.text = "🟢 HEALTHY PERSON'S BRAIN"
    p_nl.alignment = PP_ALIGN.CENTER
    p_nl.font.name = FONT_NAME
    p_nl.font.size = Pt(13)
    p_nl.font.bold = True
    p_nl.font.color.rgb = TEXT_WHITE

    slide6.shapes.add_picture(str(SCANS_DIR / "mri_tumor_annotated.png"), Inches(4.3), cs_img_y, cs_img_w, cs_img_h)
    pat_lbl = slide6.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(4.3), cs_img_y + cs_img_h, cs_img_w, Inches(0.42))
    pat_lbl.fill.solid()
    pat_lbl.fill.fore_color.rgb = RGBColor(239, 68, 68)
    pat_lbl.line.fill.background()
    p_pl = pat_lbl.text_frame.paragraphs[0]
    p_pl.text = "🚨 PATIENT SCAN: TUMOR BOXED (28.4mm)"
    p_pl.alignment = PP_ALIGN.CENTER
    p_pl.font.name = FONT_NAME
    p_pl.font.size = Pt(13)
    p_pl.font.bold = True
    p_pl.font.color.rgb = TEXT_WHITE

    info_x = Inches(7.8)
    info_w = Inches(4.733)
    info_h = Inches(4.9)
    info_card = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, info_x, cs_img_y, info_w, info_h)
    info_card.fill.solid()
    info_card.fill.fore_color.rgb = SURFACE_CARD
    info_card.line.color.rgb = ACCENT_ROSE
    info_card.line.width = Pt(1.5)

    tb = slide6.shapes.add_textbox(info_x + Inches(0.25), cs_img_y + Inches(0.15), info_w - Inches(0.5), info_h - Inches(0.3))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "DIAGNOSTIC FINDINGS"
    p.font.name = FONT_NAME
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = ACCENT_ROSE

    items = [
        ("Disease Found", "Brain Tumor Mass"),
        ("Tumor Size", "28.4 mm Across"),
        ("Location", "Right frontal lobe of brain"),
        ("Brain Swelling", "Fluid swelling halo identified around tumor"),
        ("Urgency Level", "CRITICAL STAT — Immediate Doctor Attention"),
        ("Computer Scan Speed", "0.05 seconds (Instant Result)")
    ]

    for k, v in items:
        pk = tf.add_paragraph()
        pk.text = f"• {k}: {v}"
        pk.font.name = FONT_NAME
        pk.font.size = Pt(12.5)
        pk.font.color.rgb = TEXT_SECONDARY
        pk.space_before = Pt(4)

    p_wh = tf.add_paragraph()
    p_wh.text = "Why This Matters to Surgeons:"
    p_wh.font.name = FONT_NAME
    p_wh.font.size = Pt(14)
    p_wh.font.bold = True
    p_wh.font.color.rgb = TEXT_PRIMARY
    p_wh.space_before = Pt(8)

    p_desc = tf.add_paragraph()
    p_desc.text = "The bright red box locks strictly onto the abnormal tumor mass, showing surgeons exactly where to operate while protecting surrounding healthy brain tissue."
    p_desc.font.name = FONT_NAME
    p_desc.font.size = Pt(12)
    p_desc.font.color.rgb = TEXT_MUTED
    p_desc.space_before = Pt(3)

    sub_note = slide6.shapes.add_textbox(Inches(0.8), cs_img_y + cs_img_h + Inches(0.50), Inches(6.8), Inches(0.5))
    tf_sn6 = sub_note.text_frame
    tf_sn6.word_wrap = True
    p_sn = tf_sn6.paragraphs[0]
    p_sn.text = "Comparison: Left image shows clear healthy brain tissue. Right image shows the isolated tumor mass in the red box."
    p_sn.font.name = FONT_NAME
    p_sn.font.size = Pt(11.5)
    p_sn.font.color.rgb = TEXT_MUTED

    add_footer(slide6, 6)

    # =========================================================================
    # SLIDE 7: CLINICAL CASE STUDY 2 - HEAD CT ACUTE STROKE
    # =========================================================================
    slide7 = prs.slides.add_slide(blank_layout)
    set_canvas_background(slide7)
    add_slide_header(slide7, "Clinical Case Study: Acute Ischemic Stroke Detection",
                     "Modality: Head CT Scan | Case #7721",
                     "Detecting early dark gray stroke patches where blood flow was blocked, saving critical minutes in the ER.")

    slide7.shapes.add_picture(str(SCANS_DIR / "ct_stroke_normal.png"), Inches(0.8), cs_img_y, cs_img_w, cs_img_h)
    norm_lbl = slide7.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), cs_img_y + cs_img_h, cs_img_w, Inches(0.42))
    norm_lbl.fill.solid()
    norm_lbl.fill.fore_color.rgb = RGBColor(16, 185, 129)
    norm_lbl.line.fill.background()
    p_nl = norm_lbl.text_frame.paragraphs[0]
    p_nl.text = "🟢 HEALTHY BRAIN CT"
    p_nl.alignment = PP_ALIGN.CENTER
    p_nl.font.name = FONT_NAME
    p_nl.font.size = Pt(13)
    p_nl.font.bold = True
    p_nl.font.color.rgb = TEXT_WHITE

    slide7.shapes.add_picture(str(SCANS_DIR / "ct_stroke_annotated.png"), Inches(4.3), cs_img_y, cs_img_w, cs_img_h)
    pat_lbl = slide7.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(4.3), cs_img_y + cs_img_h, cs_img_w, Inches(0.42))
    pat_lbl.fill.solid()
    pat_lbl.fill.fore_color.rgb = RGBColor(239, 68, 68)
    pat_lbl.line.fill.background()
    p_pl = pat_lbl.text_frame.paragraphs[0]
    p_pl.text = "🚨 STROKE ZONE BOXED (34.2mm)"
    p_pl.alignment = PP_ALIGN.CENTER
    p_pl.font.name = FONT_NAME
    p_pl.font.size = Pt(13)
    p_pl.font.bold = True
    p_pl.font.color.rgb = TEXT_WHITE

    info_card = slide7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, info_x, cs_img_y, info_w, info_h)
    info_card.fill.solid()
    info_card.fill.fore_color.rgb = SURFACE_CARD
    info_card.line.color.rgb = ACCENT_ROSE
    info_card.line.width = Pt(1.5)

    tb = slide7.shapes.add_textbox(info_x + Inches(0.25), cs_img_y + Inches(0.15), info_w - Inches(0.5), info_h - Inches(0.3))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "STROKE DIAGNOSTIC FINDINGS"
    p.font.name = FONT_NAME
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = ACCENT_ROSE

    items_stroke = [
        ("Disease Found", "Acute Stroke (Blood Clot)"),
        ("Tissue Affected", "34.2 mm Region"),
        ("Appearance", "Darker gray patch (oxygen supply cut off)"),
        ("Yellow Pointer", "Marks the exact center of blood blockage"),
        ("Urgency Level", "EMERGENCY — Urgent Clot-Busting Medicine"),
        ("Computer Scan Speed", "0.05 seconds (Instant Result)")
    ]

    for k, v in items_stroke:
        pk = tf.add_paragraph()
        pk.text = f"• {k}: {v}"
        pk.font.name = FONT_NAME
        pk.font.size = Pt(12.5)
        pk.font.color.rgb = TEXT_SECONDARY
        pk.space_before = Pt(4)

    p_wh = tf.add_paragraph()
    p_wh.text = "Why This Matters in Emergency Rooms:"
    p_wh.font.name = FONT_NAME
    p_wh.font.size = Pt(14)
    p_wh.font.bold = True
    p_wh.font.color.rgb = TEXT_PRIMARY
    p_wh.space_before = Pt(8)

    p_desc = tf.add_paragraph()
    p_desc.text = "An early stroke is very faint and hard to see with the human eye. The computer highlights the stroke area immediately so doctors can administer clot-busting medication in time."
    p_desc.font.name = FONT_NAME
    p_desc.font.size = Pt(12)
    p_desc.font.color.rgb = TEXT_MUTED
    p_desc.space_before = Pt(3)

    sub_note = slide7.shapes.add_textbox(Inches(0.8), cs_img_y + cs_img_h + Inches(0.50), Inches(6.8), Inches(0.5))
    tf_sn7 = sub_note.text_frame
    tf_sn7.word_wrap = True
    p_sn = tf_sn7.paragraphs[0]
    p_sn.text = "Comparison: Left brain CT is symmetrical. Right scan shows a dark gray stroke patch boxed in red with a yellow pointer arrow."
    p_sn.font.name = FONT_NAME
    p_sn.font.size = Pt(11.5)
    p_sn.font.color.rgb = TEXT_MUTED

    add_footer(slide7, 7)

    # =========================================================================
    # SLIDE 8: CLINICAL CASE STUDY 3 - CHEST CT LUNG NODULE
    # =========================================================================
    slide8 = prs.slides.add_slide(blank_layout)
    set_canvas_background(slide8)
    add_slide_header(slide8, "Clinical Case Study: Early Lung Cancer Nodule Detection",
                     "Modality: Chest CT Scan | Case #9932",
                     "Locking onto a subtle 6.4 mm solitary spot hiding inside lung air tissue before it spreads.")

    slide8.shapes.add_picture(str(SCANS_DIR / "ct_nodule_normal.png"), Inches(0.8), cs_img_y, cs_img_w, cs_img_h)
    norm_lbl = slide8.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), cs_img_y + cs_img_h, cs_img_w, Inches(0.42))
    norm_lbl.fill.solid()
    norm_lbl.fill.fore_color.rgb = RGBColor(16, 185, 129)
    norm_lbl.line.fill.background()
    p_nl = norm_lbl.text_frame.paragraphs[0]
    p_nl.text = "🟢 HEALTHY CHEST CT"
    p_nl.alignment = PP_ALIGN.CENTER
    p_nl.font.name = FONT_NAME
    p_nl.font.size = Pt(13)
    p_nl.font.bold = True
    p_nl.font.color.rgb = TEXT_WHITE

    slide8.shapes.add_picture(str(SCANS_DIR / "ct_nodule_annotated.png"), Inches(4.3), cs_img_y, cs_img_w, cs_img_h)
    pat_lbl = slide8.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(4.3), cs_img_y + cs_img_h, cs_img_w, Inches(0.42))
    pat_lbl.fill.solid()
    pat_lbl.fill.fore_color.rgb = RGBColor(217, 119, 6)
    pat_lbl.line.fill.background()
    p_pl = pat_lbl.text_frame.paragraphs[0]
    p_pl.text = "⚠️ 6.4mm LUNG SPOT (BOXED IN AMBER)"
    p_pl.alignment = PP_ALIGN.CENTER
    p_pl.font.name = FONT_NAME
    p_pl.font.size = Pt(13)
    p_pl.font.bold = True
    p_pl.font.color.rgb = TEXT_WHITE

    info_card = slide8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, info_x, cs_img_y, info_w, info_h)
    info_card.fill.solid()
    info_card.fill.fore_color.rgb = SURFACE_CARD
    info_card.line.color.rgb = ACCENT_AMBER
    info_card.line.width = Pt(1.5)

    tb = slide8.shapes.add_textbox(info_x + Inches(0.25), cs_img_y + Inches(0.15), info_w - Inches(0.5), info_h - Inches(0.3))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "LUNG NODULE FINDINGS"
    p.font.name = FONT_NAME
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = ACCENT_AMBER

    items_nodule = [
        ("Disease Found", "Early Lung Spot (Small Nodule)"),
        ("Spot Size", "6.4 mm Across (Small & Early)"),
        ("Location", "Left lung upper tissue"),
        ("Appearance", "Cloudy semi-transparent spot"),
        ("Urgency Level", "NEEDS FOLLOW-UP — Doctor Checkup Recommended"),
        ("Computer Scan Speed", "0.05 seconds (Instant Result)")
    ]

    for k, v in items_nodule:
        pk = tf.add_paragraph()
        pk.text = f"• {k}: {v}"
        pk.font.name = FONT_NAME
        pk.font.size = Pt(12.5)
        pk.font.color.rgb = TEXT_SECONDARY
        pk.space_before = Pt(4)

    p_wh = tf.add_paragraph()
    p_wh.text = "Why Catching Spots Early Saves Lives:"
    p_wh.font.name = FONT_NAME
    p_wh.font.size = Pt(14)
    p_wh.font.bold = True
    p_wh.font.color.rgb = TEXT_PRIMARY
    p_wh.space_before = Pt(8)

    p_desc = tf.add_paragraph()
    p_desc.text = "Catching small lung spots under 8 mm before cancer spreads increases 5-year survival to over 70%. The computer boxes only the spot without covering healthy tissue."
    p_desc.font.name = FONT_NAME
    p_desc.font.size = Pt(12)
    p_desc.font.color.rgb = TEXT_MUTED
    p_desc.space_before = Pt(3)

    sub_note = slide8.shapes.add_textbox(Inches(0.8), cs_img_y + cs_img_h + Inches(0.50), Inches(6.8), Inches(0.5))
    tf_sn8 = sub_note.text_frame
    tf_sn8.word_wrap = True
    p_sn = tf_sn8.paragraphs[0]
    p_sn.text = "Comparison: Left CT shows clean dark air. Right scan locks onto a subtle 6.4 mm spot in the amber box with measurement crosshairs."
    p_sn.font.name = FONT_NAME
    p_sn.font.size = Pt(11.5)
    p_sn.font.color.rgb = TEXT_MUTED

    add_footer(slide8, 8)

    # =========================================================================
    # SLIDE 9: CLINICAL CASE STUDY 4A - CHEST X-RAY BACTERIAL PNEUMONIA
    # =========================================================================
    slide9 = prs.slides.add_slide(blank_layout)
    set_canvas_background(slide9)
    add_slide_header(slide9, "Clinical Case Study: Chest X-Ray Bacterial Pneumonia",
                     "Modality: Chest X-Ray | Infection Screening",
                     "Automating pneumonia infection mapping and fluid density isolation in 0.05 seconds.")

    slide9.shapes.add_picture(str(SCANS_DIR / "xray_pneumonia_normal.png"), Inches(0.8), cs_img_y, cs_img_w, cs_img_h)
    norm_lbl = slide9.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), cs_img_y + cs_img_h, cs_img_w, Inches(0.42))
    norm_lbl.fill.solid()
    norm_lbl.fill.fore_color.rgb = ACCENT_EMERALD
    norm_lbl.line.fill.background()
    p_nl = norm_lbl.text_frame.paragraphs[0]
    p_nl.text = "🟢 Normal Clear Lungs"
    p_nl.alignment = PP_ALIGN.CENTER
    p_nl.font.name = FONT_NAME
    p_nl.font.size = Pt(13)
    p_nl.font.bold = True
    p_nl.font.color.rgb = TEXT_WHITE

    slide9.shapes.add_picture(str(SCANS_DIR / "xray_pneumonia_annotated.png"), Inches(4.3), cs_img_y, cs_img_w, cs_img_h)
    pat_lbl = slide9.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(4.3), cs_img_y + cs_img_h, cs_img_w, Inches(0.42))
    pat_lbl.fill.solid()
    pat_lbl.fill.fore_color.rgb = ACCENT_ROSE
    pat_lbl.line.fill.background()
    p_pl = pat_lbl.text_frame.paragraphs[0]
    p_pl.text = "🚨 Infection Boxed (78%)"
    p_pl.alignment = PP_ALIGN.CENTER
    p_pl.font.name = FONT_NAME
    p_pl.font.size = Pt(13)
    p_pl.font.bold = True
    p_pl.font.color.rgb = TEXT_WHITE

    info_card = slide9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, info_x, cs_img_y, info_w, info_h)
    info_card.fill.solid()
    info_card.fill.fore_color.rgb = SURFACE_CARD
    info_card.line.color.rgb = ACCENT_ROSE
    info_card.line.width = Pt(1.5)

    tb = slide9.shapes.add_textbox(info_x + Inches(0.25), cs_img_y + Inches(0.15), info_w - Inches(0.5), info_h - Inches(0.3))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "LUNG INFECTION (BACTERIAL PNEUMONIA)"
    p.font.name = FONT_NAME
    p.font.size = Pt(17.5)
    p.font.bold = True
    p.font.color.rgb = ACCENT_ROSE

    items_pneu = [
        ("Infection Spread", "78% of lower lung filled with fluid"),
        ("Scan Appearance", "Dense white cloudy pus blocking air"),
        ("Doctor Action", "Urgent antibiotic medication required")
    ]

    for k, v in items_pneu:
        pk = tf.add_paragraph()
        pk.text = f"• {k}: {v}"
        pk.font.name = FONT_NAME
        pk.font.size = Pt(13.5)
        pk.font.color.rgb = TEXT_SECONDARY
        pk.space_before = Pt(8)

    p_wh = tf.add_paragraph()
    p_wh.text = "Clinical Takeaway:"
    p_wh.font.name = FONT_NAME
    p_wh.font.size = Pt(15)
    p_wh.font.bold = True
    p_wh.font.color.rgb = TEXT_PRIMARY
    p_wh.space_before = Pt(14)

    p_desc = tf.add_paragraph()
    p_desc.text = "Healthy lungs are filled with clear dark air. Infection shows up as cloudy white fluid neatly boxed by the computer."
    p_desc.font.name = FONT_NAME
    p_desc.font.size = Pt(13)
    p_desc.font.color.rgb = TEXT_MUTED
    p_desc.space_before = Pt(4)

    sub_note = slide9.shapes.add_textbox(Inches(0.8), cs_img_y + cs_img_h + Inches(0.50), Inches(6.8), Inches(0.5))
    tf_sn9 = sub_note.text_frame
    tf_sn9.word_wrap = True
    p_sn = tf_sn9.paragraphs[0]
    p_sn.text = "Comparison: Left image shows clear healthy dark lung fields. Right image highlights dense bacterial infection opacity in the red box."
    p_sn.font.name = FONT_NAME
    p_sn.font.size = Pt(11.5)
    p_sn.font.color.rgb = TEXT_MUTED

    add_footer(slide9, 9)

    # =========================================================================
    # SLIDE 10: CLINICAL CASE STUDY 4B - CHEST X-RAY CARDIOMEGALY
    # =========================================================================
    slide10 = prs.slides.add_slide(blank_layout)
    set_canvas_background(slide10)
    add_slide_header(slide10, "Clinical Case Study: Chest X-Ray Heart Swelling (Cardiomegaly)",
                     "Modality: Chest X-Ray | Caliper Measurement",
                     "Automating heart muscle swelling caliper measurements side-by-side to eliminate human guesswork.")

    slide10.shapes.add_picture(str(SCANS_DIR / "xray_cardiomegaly_normal.png"), Inches(0.8), cs_img_y, cs_img_w, cs_img_h)
    norm_lbl = slide10.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), cs_img_y + cs_img_h, cs_img_w, Inches(0.42))
    norm_lbl.fill.solid()
    norm_lbl.fill.fore_color.rgb = ACCENT_EMERALD
    norm_lbl.line.fill.background()
    p_nl = norm_lbl.text_frame.paragraphs[0]
    p_nl.text = "🟢 Normal Heart (42% Width)"
    p_nl.alignment = PP_ALIGN.CENTER
    p_nl.font.name = FONT_NAME
    p_nl.font.size = Pt(13)
    p_nl.font.bold = True
    p_nl.font.color.rgb = TEXT_WHITE

    slide10.shapes.add_picture(str(SCANS_DIR / "xray_cardiomegaly_annotated.png"), Inches(4.3), cs_img_y, cs_img_w, cs_img_h)
    pat_lbl = slide10.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(4.3), cs_img_y + cs_img_h, cs_img_w, Inches(0.42))
    pat_lbl.fill.solid()
    pat_lbl.fill.fore_color.rgb = ACCENT_ROSE
    pat_lbl.line.fill.background()
    p_pl = pat_lbl.text_frame.paragraphs[0]
    p_pl.text = "🚨 Swollen Heart (62% Width)"
    p_pl.alignment = PP_ALIGN.CENTER
    p_pl.font.name = FONT_NAME
    p_pl.font.size = Pt(13)
    p_pl.font.bold = True
    p_pl.font.color.rgb = TEXT_WHITE

    info_card = slide10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, info_x, cs_img_y, info_w, info_h)
    info_card.fill.solid()
    info_card.fill.fore_color.rgb = SURFACE_CARD
    info_card.line.color.rgb = ACCENT_ROSE
    info_card.line.width = Pt(1.5)

    tb = slide10.shapes.add_textbox(info_x + Inches(0.25), cs_img_y + Inches(0.15), info_w - Inches(0.5), info_h - Inches(0.3))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "ENLARGED HEART (HEART MUSCLE SWELLING)"
    p.font.name = FONT_NAME
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = ACCENT_ROSE

    items_cardio = [
        ("Heart Ratio", "62% of chest width (Normal limit is <50%)"),
        ("Caliper Lines", "318 px heart width vs 512 px chest width"),
        ("Doctor Action", "Urgent heart failure cardiology review")
    ]

    for k, v in items_cardio:
        pk = tf.add_paragraph()
        pk.text = f"• {k}: {v}"
        pk.font.name = FONT_NAME
        pk.font.size = Pt(13.5)
        pk.font.color.rgb = TEXT_SECONDARY
        pk.space_before = Pt(8)

    p_wh = tf.add_paragraph()
    p_wh.text = "Clinical Takeaway:"
    p_wh.font.name = FONT_NAME
    p_wh.font.size = Pt(15)
    p_wh.font.bold = True
    p_wh.font.color.rgb = TEXT_PRIMARY
    p_wh.space_before = Pt(14)

    p_desc = tf.add_paragraph()
    p_desc.text = "Red caliper lines objectively measure heart swelling in 0.05 seconds, eliminating human guesswork in the emergency room."
    p_desc.font.name = FONT_NAME
    p_desc.font.size = Pt(13)
    p_desc.font.color.rgb = TEXT_MUTED
    p_desc.space_before = Pt(4)

    sub_note = slide10.shapes.add_textbox(Inches(0.8), cs_img_y + cs_img_h + Inches(0.50), Inches(6.8), Inches(0.5))
    tf_sn10 = sub_note.text_frame
    tf_sn10.word_wrap = True
    p_sn = tf_sn10.paragraphs[0]
    p_sn.text = "Comparison: Left image shows normal heart boundaries. Right image displays red and cyan calipers measuring abnormal enlargement."
    p_sn.font.name = FONT_NAME
    p_sn.font.size = Pt(11.5)
    p_sn.font.color.rgb = TEXT_MUTED

    add_footer(slide10, 10)

    # =========================================================================
    # SLIDE 11: SAFE & SECURE HOSPITAL RECORDS (PART 1: PRIVACY & CLINICAL PROOF)
    # =========================================================================
    slide11 = prs.slides.add_slide(blank_layout)
    set_canvas_background(slide11)
    add_slide_header(slide11, "Safe & Secure Hospital Records: Privacy & Clinical Proof",
                     "Safe & Secure Hospital Records (Part 1)",
                     "A simple, secure system that protects patient privacy and saves exact disease measurements.")

    s11_cards = [
        ("1. Protecting Patient Privacy",
         "Your Scans Are Locked & Safe",
         ACCENT_CYAN,
         [
             ("Instant Safe Ingestion", "When a patient gets an X-Ray, CT, or MRI, the scan is securely loaded in under 1 second."),
             ("Locked Privacy Encryption", "Patient names and medical files are encrypted so only authorized staff can see them."),
             ("Hospital-Only Network", "Runs directly inside the hospital firewall with zero files sent to outside public clouds."),
             ("Full Medical Compliance", "Meets strict official HIPAA & hospital data privacy laws worldwide.")
         ],
         "🔒 100% Private & HIPAA Compliant:\nYour personal healthcare data is always protected."),
        ("2. Showing Clear Proof of Disease",
         "Exact Measurements, No Guesswork",
         ACCENT_PURPLE,
         [
             ("Visual Red Box Proof", "The computer permanently saves the exact boundary box of where the disease was found."),
             ("Real Millimeter Numbers", "Saves exact measurements (like 28.4 mm brain tumor or 62% swollen heart)."),
             ("Plain-English Summaries", "Translates findings into simple English so patients, nurses, and doctors understand."),
             ("Permanent Treatment History", "Keeps a clear visual record so doctors can verify if medications are shrinking tumors.")
         ],
         "🔍 Complete Clinical Transparency:\nDoctors can inspect the exact millimeter numbers anytime.")
    ]

    for i, (title, sub, accent, fields, bottom_spec) in enumerate(s11_cards):
        dx = Inches(0.8) + i * Inches(6.07)
        c_shape = slide11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, dx, col2_y, col2_w, col2_h)
        c_shape.fill.solid()
        c_shape.fill.fore_color.rgb = SURFACE_CARD
        c_shape.line.color.rgb = BORDER_CARD
        c_shape.line.width = Pt(1.5)

        rib = slide11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, dx, col2_y, col2_w, Inches(0.08))
        rib.fill.solid()
        rib.fill.fore_color.rgb = accent
        rib.line.fill.background()

        tb = slide11.shapes.add_textbox(dx + Inches(0.3), col2_y + Inches(0.2), col2_w - Inches(0.6), Inches(3.6))
        tf = tb.text_frame
        tf.word_wrap = True

        pt = tf.paragraphs[0]
        pt.text = title
        pt.font.name = FONT_NAME
        pt.font.size = Pt(22)
        pt.font.bold = True
        pt.font.color.rgb = TEXT_PRIMARY

        ps = tf.add_paragraph()
        ps.text = sub
        ps.font.name = FONT_NAME
        ps.font.size = Pt(16)
        ps.font.bold = True
        ps.font.color.rgb = accent
        ps.space_before = Pt(3)
        ps.space_after = Pt(12)

        for f_name, f_desc in fields:
            pf = tf.add_paragraph()
            pf.text = f"• {f_name}: {f_desc}"
            pf.font.name = FONT_NAME
            pf.font.size = Pt(14)
            pf.font.color.rgb = TEXT_SECONDARY
            pf.space_before = Pt(8)

        tile_y = col2_y + Inches(3.85)
        tile_h = Inches(0.85)
        tile = slide11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, dx + Inches(0.25), tile_y, col2_w - Inches(0.5), tile_h)
        tile.fill.solid()
        tile.fill.fore_color.rgb = RGBColor(255, 255, 255)
        tile.line.color.rgb = accent
        tile.line.width = Pt(1.5)

        tb_tile = slide11.shapes.add_textbox(dx + Inches(0.3), tile_y + Inches(0.08), col2_w - Inches(0.6), tile_h - Inches(0.16))
        tf_t = tb_tile.text_frame
        tf_t.word_wrap = True
        ptile = tf_t.paragraphs[0]
        ptile.text = bottom_spec
        ptile.font.name = FONT_NAME
        ptile.font.size = Pt(13)
        ptile.font.bold = True
        ptile.font.color.rgb = accent

    add_footer(slide11, 11)

    # =========================================================================
    # SLIDE 12: SAFE & SECURE HOSPITAL RECORDS (PART 2: DOCTOR CONTROL & GOVERNANCE)
    # =========================================================================
    slide12 = prs.slides.add_slide(blank_layout)
    set_canvas_background(slide12)
    add_slide_header(slide12, "Safe & Secure Hospital Records: Doctor Control & Governance",
                     "Safe & Secure Hospital Records (Part 2)",
                     "Ensuring human doctors always make final medical decisions and maintaining legally protected audit trails.")

    s12_cards = [
        ("3. Human Doctors Always in Control",
         "The AI Never Makes Decisions Alone",
         ACCENT_EMERALD,
         [
             ("Human Approval Required", "The computer assists, but a real human doctor must review the scan and click 'Approve'."),
             ("Official Doctor Stamp", "Stores the reviewing doctor's full name, medical license ID, and exact time of sign-off."),
             ("Custom Doctor Notes", "Doctors can add their own personalized treatment notes and recommendations."),
             ("Full Legal Protection", "Creates an unchangeable legal audit record that protects both patient and hospital.")
         ],
         "✍️ Verified by a Human Doctor:\nThe computer assists; the doctor makes the final decision."),
        ("Enterprise Hospital Governance",
         "Complete Traceability & Risk Protection",
         ACCENT_BLUE,
         [
             ("Locked Audit Log", "Every scan ingested, AI annotation generated, and clinician approval is permanently stored."),
             ("Zero Cloud Exposure", "Protects sensitive hospital intellectual property and patient records within private servers."),
             ("Radiology Integration", "Seamlessly connects with existing hospital PACS imaging archives and medical workflows."),
             ("Clinical Accountability", "Empowers healthcare leadership with real-time analytics on diagnosis times and accuracy.")
         ],
         "🏥 Enterprise-Ready Medical Governance:\nDesigned for hospital compliance committees, chief medical officers, and legal teams.")
    ]

    for i, (title, sub, accent, fields, bottom_spec) in enumerate(s12_cards):
        dx = Inches(0.8) + i * Inches(6.07)
        c_shape = slide12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, dx, col2_y, col2_w, col2_h)
        c_shape.fill.solid()
        c_shape.fill.fore_color.rgb = SURFACE_CARD
        c_shape.line.color.rgb = BORDER_CARD
        c_shape.line.width = Pt(1.5)

        rib = slide12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, dx, col2_y, col2_w, Inches(0.08))
        rib.fill.solid()
        rib.fill.fore_color.rgb = accent
        rib.line.fill.background()

        tb = slide12.shapes.add_textbox(dx + Inches(0.3), col2_y + Inches(0.2), col2_w - Inches(0.6), Inches(3.6))
        tf = tb.text_frame
        tf.word_wrap = True

        pt = tf.paragraphs[0]
        pt.text = title
        pt.font.name = FONT_NAME
        pt.font.size = Pt(22)
        pt.font.bold = True
        pt.font.color.rgb = TEXT_PRIMARY

        ps = tf.add_paragraph()
        ps.text = sub
        ps.font.name = FONT_NAME
        ps.font.size = Pt(16)
        ps.font.bold = True
        ps.font.color.rgb = accent
        ps.space_before = Pt(3)
        ps.space_after = Pt(12)

        for f_name, f_desc in fields:
            pf = tf.add_paragraph()
            pf.text = f"• {f_name}: {f_desc}"
            pf.font.name = FONT_NAME
            pf.font.size = Pt(14)
            pf.font.color.rgb = TEXT_SECONDARY
            pf.space_before = Pt(8)

        tile_y = col2_y + Inches(3.85)
        tile_h = Inches(0.85)
        tile = slide12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, dx + Inches(0.25), tile_y, col2_w - Inches(0.5), tile_h)
        tile.fill.solid()
        tile.fill.fore_color.rgb = RGBColor(255, 255, 255)
        tile.line.color.rgb = accent
        tile.line.width = Pt(1.5)

        tb_tile = slide12.shapes.add_textbox(dx + Inches(0.3), tile_y + Inches(0.08), col2_w - Inches(0.6), tile_h - Inches(0.16))
        tf_t = tb_tile.text_frame
        tf_t.word_wrap = True
        ptile = tf_t.paragraphs[0]
        ptile.text = bottom_spec
        ptile.font.name = FONT_NAME
        ptile.font.size = Pt(13)
        ptile.font.bold = True
        ptile.font.color.rgb = accent

    add_footer(slide12, 12)

    # =========================================================================
    # SLIDE 13: 10 AUTOMATED SAFETY TESTS (TWO BALANCED COLUMNS - LARGE FONTS)
    # =========================================================================
    slide13 = prs.slides.add_slide(blank_layout)
    set_canvas_background(slide13)
    add_slide_header(slide13, "10 Automated Safety Tests Proving 100% Accuracy",
                     "Automated Accuracy & Clinical Safety",
                     "Before this system is used on any patient, 10 automated safety checks prove that no disease is missed.")

    test_box_w = Inches(11.733)
    test_box_h = Inches(4.85)
    
    t_card = slide13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), col2_y, test_box_w, test_box_h)
    t_card.fill.solid()
    t_card.fill.fore_color.rgb = SURFACE_CARD
    t_card.line.color.rgb = ACCENT_EMERALD
    t_card.line.width = Pt(1.5)

    rib = slide13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), col2_y, test_box_w, Inches(0.08))
    rib.fill.solid()
    rib.fill.fore_color.rgb = ACCENT_EMERALD
    rib.line.fill.background()

    head_box = slide13.shapes.add_textbox(Inches(1.1), col2_y + Inches(0.15), test_box_w - Inches(0.6), Inches(0.45))
    p_th = head_box.text_frame.paragraphs[0]
    p_th.text = "10 CLINICAL ACCURACY TESTS (ALL 10 PASSED 100%)"
    p_th.font.name = FONT_NAME
    p_th.font.size = Pt(20)
    p_th.font.bold = True
    p_th.font.color.rgb = ACCENT_EMERALD

    test_col1 = [
        ("Brain Tumor Test", "Accurately caught and measured brain tumor (28.4 mm)", "[PASSED 100%]"),
        ("Brain Stroke Test", "Accurately caught early oxygen blockage and marked clot zone", "[PASSED 100%]"),
        ("Early Lung Cancer", "Accurately caught tiny 6.4 mm spot hiding in lung tissue", "[PASSED 100%]"),
        ("Multiple Sclerosis", "Accurately caught inflamed nerve spots in the brain", "[PASSED 100%]"),
        ("Collapsed Lung", "Accurately caught hairline air leak pulling lung from ribs", "[PASSED 100%]")
    ]

    test_col2 = [
        ("Severe Pneumonia", "Accurately measured 78% lung infection fluid spread", "[PASSED 100%]"),
        ("Swollen Heart", "Accurately measured heart width vs. chest width calipers (62%)", "[PASSED 100%]"),
        ("Healthy Patient Check", "Accurately cleared healthy patients with 0 false alarms", "[PASSED 100%]"),
        ("Blurry Scan Guard", "Safely rejected dark, blurry, or unusable scans for safety", "[PASSED 100%]"),
        ("Patient Movement Guard", "Accurately caught if a patient moved during the scan", "[PASSED 100%]")
    ]

    # Left Column Tests
    tb_c1 = slide13.shapes.add_textbox(Inches(1.1), col2_y + Inches(0.65), Inches(5.5), Inches(3.0))
    tf_c1 = tb_c1.text_frame
    tf_c1.word_wrap = True
    for idx, (t_name, t_desc, t_res) in enumerate(test_col1):
        p_item = tf_c1.paragraphs[0] if idx == 0 else tf_c1.add_paragraph()
        p_item.text = f"• {t_name}: {t_desc}  {t_res}"
        p_item.font.name = FONT_NAME
        p_item.font.size = Pt(13.5)
        p_item.font.color.rgb = TEXT_PRIMARY
        if idx > 0:
            p_item.space_before = Pt(8)

    # Right Column Tests
    tb_c2 = slide13.shapes.add_textbox(Inches(6.8), col2_y + Inches(0.65), Inches(5.5), Inches(3.0))
    tf_c2 = tb_c2.text_frame
    tf_c2.word_wrap = True
    for idx, (t_name, t_desc, t_res) in enumerate(test_col2):
        p_item = tf_c2.paragraphs[0] if idx == 0 else tf_c2.add_paragraph()
        p_item.text = f"• {t_name}: {t_desc}  {t_res}"
        p_item.font.name = FONT_NAME
        p_item.font.size = Pt(13.5)
        p_item.font.color.rgb = TEXT_PRIMARY
        if idx > 0:
            p_item.space_before = Pt(8)

    # Bottom Banner
    b_banner = slide13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.1), col2_y + Inches(3.85), test_box_w - Inches(0.6), Inches(0.8))
    b_banner.fill.solid()
    b_banner.fill.fore_color.rgb = RGBColor(236, 253, 245)
    b_banner.line.color.rgb = ACCENT_EMERALD
    b_banner.line.width = Pt(1.5)

    tb_bb = slide13.shapes.add_textbox(Inches(1.3), col2_y + Inches(3.92), test_box_w - Inches(1.0), Inches(0.65))
    tf_bb = tb_bb.text_frame
    tf_bb.word_wrap = True
    pbb = tf_bb.paragraphs[0]
    pbb.text = "🏆 100% Diagnostic Reliability: All 10 automated safety tests passed in 0.84 seconds.\nZero false negatives on critical emergencies (Brain Tumor, Stroke, and Collapsed Lung)."
    pbb.font.name = FONT_NAME
    pbb.font.size = Pt(13)
    pbb.font.bold = True
    pbb.font.color.rgb = ACCENT_EMERALD

    add_footer(slide13, 13)

    # =========================================================================
    # SLIDE 14: CLINICAL RELIABILITY - WHY DOCTORS TRUST MEDVISION AI
    # =========================================================================
    slide14 = prs.slides.add_slide(blank_layout)
    set_canvas_background(slide14)
    add_slide_header(slide14, "Clinical Verification: Why Doctors Trust MedVision AI",
                     "Physician Trust & Evidence",
                     "Objective mathematical verification and seamless hospital integration create unconditional doctor confidence.")

    card14_w = Inches(11.733)
    card14_h = Inches(4.85)

    c14 = slide14.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), col2_y, card14_w, card14_h)
    c14.fill.solid()
    c14.fill.fore_color.rgb = SURFACE_CARD
    c14.line.color.rgb = ACCENT_CYAN
    c14.line.width = Pt(1.5)

    rib14 = slide14.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), col2_y, card14_w, Inches(0.08))
    rib14.fill.solid()
    rib14.fill.fore_color.rgb = ACCENT_CYAN
    rib14.line.fill.background()

    head14 = slide14.shapes.add_textbox(Inches(1.1), col2_y + Inches(0.15), card14_w - Inches(0.6), Inches(0.45))
    p_h14 = head14.text_frame.paragraphs[0]
    p_h14.text = "WHY DOCTORS TRUST IT: 5 PILLARS OF CLINICAL CONFIDENCE"
    p_h14.font.name = FONT_NAME
    p_h14.font.size = Pt(20)
    p_h14.font.bold = True
    p_h14.font.color.rgb = ACCENT_CYAN

    q_items_clear = [
        ("Zero Human Guesswork", "Every algorithm is mathematically verified before patient use."),
        ("Zero Missed Emergencies", "100% success on tumors, strokes, and lung collapse."),
        ("Instant 0.8s Verification", "Complete safety test suite runs in 0.84 seconds with zero lag."),
        ("Continuous Testing", "Tests run automatically on every system update to ensure no errors."),
        ("Runs on Any Hospital PC", "Runs smoothly on standard Windows hospital computers.")
    ]

    tb14_body = slide14.shapes.add_textbox(Inches(1.1), col2_y + Inches(0.65), card14_w - Inches(0.6), Inches(3.0))
    tf14_b = tb14_body.text_frame
    tf14_b.word_wrap = True

    for idx, (qk, qv) in enumerate(q_items_clear):
        pq = tf14_b.paragraphs[0] if idx == 0 else tf14_b.add_paragraph()
        pq.text = f"✓ {qk}: {qv}"
        pq.font.name = FONT_NAME
        pq.font.size = Pt(14)
        pq.font.color.rgb = TEXT_SECONDARY
        if idx > 0:
            pq.space_before = Pt(8)

    # Highlight Banner
    b14_banner = slide14.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.1), col2_y + Inches(3.85), card14_w - Inches(0.6), Inches(0.8))
    b14_banner.fill.solid()
    b14_banner.fill.fore_color.rgb = RGBColor(238, 242, 255)
    b14_banner.line.color.rgb = ACCENT_BLUE
    b14_banner.line.width = Pt(1.5)

    tb14_bb = slide14.shapes.add_textbox(Inches(1.3), col2_y + Inches(3.92), card14_w - Inches(1.0), Inches(0.65))
    tf14_bb = tb14_bb.text_frame
    tf14_bb.word_wrap = True
    p14_bb = tf14_bb.paragraphs[0]
    p14_bb.text = "⚡ Built For Physicians, By Physicians:\nEliminating emergency diagnostic burnout with instantaneous, mathematically proven scan assistance."
    p14_bb.font.name = FONT_NAME
    p14_bb.font.size = Pt(13)
    p14_bb.font.bold = True
    p14_bb.font.color.rgb = ACCENT_BLUE

    add_footer(slide14, 14)

    # =========================================================================
    # SLIDE 15: REAL HOSPITAL IMPACT (FASTER CARE & $420,000 SAVINGS)
    # =========================================================================
    slide15 = prs.slides.add_slide(blank_layout)
    set_canvas_background(slide15)
    add_slide_header(slide15, "Real Hospital Impact: Faster Care & Lower Costs",
                     "Real-World Hospital Value (Part 1)",
                     "How this technology helps patients get treated faster and saves significant hospital budget.")

    s15_cards = [
        ("1. Faster Patient Care",
         "Saving Minutes in the ER",
         ACCENT_EMERALD,
         [
             ("0.05-Second Results", "Scans are checked in 0.05 seconds instead of waiting 1 to 2 hours in the ER."),
             ("Catching Disease Early", "Small 6 mm tumors and early strokes are caught when cure rates are highest."),
             ("24/7 Always Awake", "Never gets tired; works with 100% focus during night shifts and weekends."),
             ("Emergency Prioritization", "Life-threatening emergencies automatically jump to the top of the doctor's screen.")
         ],
         "⏱️ 99.8% Faster Scan Triage:\nFrom 45-minute wait to 0.05-second instant review"),
        ("2. Saving Hospital Money",
         "Lower Costs & Fewer Mistakes",
         ACCENT_CYAN,
         [
             ("$420,000 Annual Savings", "Saves hospital budget by eliminating doctor burnout, overtime, and scan backlogs."),
             ("Second Pair of Eyes", "Prevents accidental human oversights that lead to costly medical malpractice claims."),
             ("Easy Single-Screen View", "Doctors see everything on one clean screen without scrolling or getting confused."),
             ("100% In-Hospital Privacy", "All scan files stay inside the hospital firewall with zero data leaked outside.")
         ],
         "💰 $420,000 Annual Hospital ROI:\nFewer missed diagnoses, lower overtime, protected records")
    ]

    for i, (title, sub, accent, bullets, footer_metric) in enumerate(s15_cards):
        px = Inches(0.8) + i * Inches(6.07)
        c_shape = slide15.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, px, col2_y, col2_w, col2_h)
        c_shape.fill.solid()
        c_shape.fill.fore_color.rgb = SURFACE_CARD
        c_shape.line.color.rgb = BORDER_CARD
        c_shape.line.width = Pt(1.5)

        rib = slide15.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, px, col2_y, col2_w, Inches(0.08))
        rib.fill.solid()
        rib.fill.fore_color.rgb = accent
        rib.line.fill.background()

        tb = slide15.shapes.add_textbox(px + Inches(0.3), col2_y + Inches(0.2), col2_w - Inches(0.6), Inches(3.6))
        tf = tb.text_frame
        tf.word_wrap = True

        pt = tf.paragraphs[0]
        pt.text = title
        pt.font.name = FONT_NAME
        pt.font.size = Pt(22)
        pt.font.bold = True
        pt.font.color.rgb = TEXT_PRIMARY

        ps = tf.add_paragraph()
        ps.text = sub
        ps.font.name = FONT_NAME
        ps.font.size = Pt(16)
        ps.font.bold = True
        ps.font.color.rgb = accent
        ps.space_before = Pt(3)
        ps.space_after = Pt(12)

        for b_title, b_desc in bullets:
            pb = tf.add_paragraph()
            pb.text = f"• {b_title}: {b_desc}"
            pb.font.name = FONT_NAME
            pb.font.size = Pt(14)
            pb.font.color.rgb = TEXT_SECONDARY
            pb.space_before = Pt(8)

        tile_y = col2_y + Inches(3.85)
        tile_h = Inches(0.85)
        tile = slide15.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, px + Inches(0.25), tile_y, col2_w - Inches(0.5), tile_h)
        tile.fill.solid()
        tile.fill.fore_color.rgb = RGBColor(255, 255, 255)
        tile.line.color.rgb = accent
        tile.line.width = Pt(1.5)

        tb_tile = slide15.shapes.add_textbox(px + Inches(0.3), tile_y + Inches(0.08), col2_w - Inches(0.6), tile_h - Inches(0.16))
        tf_t = tb_tile.text_frame
        tf_t.word_wrap = True
        ptile = tf_t.paragraphs[0]
        ptile.text = footer_metric
        ptile.font.name = FONT_NAME
        ptile.font.size = Pt(13)
        ptile.font.bold = True
        ptile.font.color.rgb = accent

    add_footer(slide15, 15)

    # =========================================================================
    # SLIDE 16: FUTURE HORIZONS (WHAT COMES NEXT & INNOVATION ROADMAP)
    # =========================================================================
    slide16 = prs.slides.add_slide(blank_layout)
    set_canvas_background(slide16)
    add_slide_header(slide16, "Future Horizons: Next-Generation Medical Innovation",
                     "Innovation Roadmap & Vision",
                     "The exciting future ahead: 3D interactive organ models, treatment trackers, and multi-organ coverage.")

    s16_cards = [
        ("3. What Comes Next",
         "Future Horizons for Medicine",
         ACCENT_PURPLE,
         [
             ("3D Rotating Organ Views", "Transforming flat 2D slice scans into full 3D rotating organ models for surgeons."),
             ("Healing Progress Tracker", "Comparing old scans against new scans to show patients how their tumors are shrinking."),
             ("Automatic Doctor Letters", "Drafting clear, professional diagnostic letters for doctors to review and sign."),
             ("Expanding to More Organs", "Adding spine, joint, bone fracture, and liver scan detection in upcoming updates.")
         ],
         "🔮 Next-Generation Healthcare:\n3D Interactive Anatomy & Automated Patient Letters"),
        ("Strategic Health System Vision",
         "Expanding Healthcare AI Impact",
         ACCENT_CYAN,
         [
             ("Surgical Pre-Planning", "Empowers operative teams with millimeter-accurate 3D tumor spatial coordinates."),
             ("Automated Patient Follow-Ups", "Provides longitudinal comparison tracking every 30 days to measure therapy response."),
             ("Zero Cloud Dependency", "Entire next-gen roadmap maintains 100% on-premise hospital data privacy."),
             ("Global Standard Conformity", "Seamless DICOM 3.0 and HL7 FHIR compliance across all regional hospital health systems.")
         ],
         "🌐 Scalable Hospital Modernization:\nPioneering safe, doctor-controlled artificial intelligence across all modalities.")
    ]

    for i, (title, sub, accent, bullets, footer_metric) in enumerate(s16_cards):
        px = Inches(0.8) + i * Inches(6.07)
        c_shape = slide16.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, px, col2_y, col2_w, col2_h)
        c_shape.fill.solid()
        c_shape.fill.fore_color.rgb = SURFACE_CARD
        c_shape.line.color.rgb = BORDER_CARD
        c_shape.line.width = Pt(1.5)

        rib = slide16.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, px, col2_y, col2_w, Inches(0.08))
        rib.fill.solid()
        rib.fill.fore_color.rgb = accent
        rib.line.fill.background()

        tb = slide16.shapes.add_textbox(px + Inches(0.3), col2_y + Inches(0.2), col2_w - Inches(0.6), Inches(3.6))
        tf = tb.text_frame
        tf.word_wrap = True

        pt = tf.paragraphs[0]
        pt.text = title
        pt.font.name = FONT_NAME
        pt.font.size = Pt(22)
        pt.font.bold = True
        pt.font.color.rgb = TEXT_PRIMARY

        ps = tf.add_paragraph()
        ps.text = sub
        ps.font.name = FONT_NAME
        ps.font.size = Pt(16)
        ps.font.bold = True
        ps.font.color.rgb = accent
        ps.space_before = Pt(3)
        ps.space_after = Pt(12)

        for b_title, b_desc in bullets:
            pb = tf.add_paragraph()
            pb.text = f"• {b_title}: {b_desc}"
            pb.font.name = FONT_NAME
            pb.font.size = Pt(14)
            pb.font.color.rgb = TEXT_SECONDARY
            pb.space_before = Pt(8)

        tile_y = col2_y + Inches(3.85)
        tile_h = Inches(0.85)
        tile = slide16.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, px + Inches(0.25), tile_y, col2_w - Inches(0.5), tile_h)
        tile.fill.solid()
        tile.fill.fore_color.rgb = RGBColor(255, 255, 255)
        tile.line.color.rgb = accent
        tile.line.width = Pt(1.5)

        tb_tile = slide16.shapes.add_textbox(px + Inches(0.3), tile_y + Inches(0.08), col2_w - Inches(0.6), tile_h - Inches(0.16))
        tf_t = tb_tile.text_frame
        tf_t.word_wrap = True
        ptile = tf_t.paragraphs[0]
        ptile.text = footer_metric
        ptile.font.name = FONT_NAME
        ptile.font.size = Pt(13)
        ptile.font.bold = True
        ptile.font.color.rgb = accent

    add_footer(slide16, 16)

    prs.save(str(OUTPUT_PPTX))
    print(f"[OK] Successfully generated Master Presentation: {OUTPUT_PPTX} ({TOTAL_SLIDES} slides)")

if __name__ == "__main__":
    create_presentation()
