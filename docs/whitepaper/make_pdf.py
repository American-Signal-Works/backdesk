"""Build the Ambient whitepaper PDF."""
from __future__ import annotations
import os
from datetime import date

from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, NextPageTemplate, PageBreak,
    Paragraph, Spacer, Image, Table, TableStyle, KeepTogether,
    HRFlowable, FrameBreak,
)

HERE = os.path.dirname(__file__)
FIG = os.path.join(HERE, "figures")
OUT = os.path.join(HERE, "Ambient-Whitepaper.pdf")

# Brand --------------------------------------------------------------
INK      = HexColor("#0F172A")
SUBINK   = HexColor("#475569")
MUTED    = HexColor("#64748B")
HAIRLINE = HexColor("#E2E8F0")
PANEL    = HexColor("#F8FAFC")
INDIGO   = HexColor("#4F46E5")
INDIGO_L = HexColor("#EEF2FF")
EMERALD  = HexColor("#059669")
EMERALD_L= HexColor("#ECFDF5")
AMBER    = HexColor("#D97706")

# Page geometry ------------------------------------------------------
PAGE_W, PAGE_H = LETTER
MARGIN_L = 0.85 * inch
MARGIN_R = 0.85 * inch
MARGIN_T = 0.95 * inch
MARGIN_B = 0.95 * inch

# Try to register a nicer system font; fall back to Helvetica
BODY_FONT = "Helvetica"
BODY_BOLD = "Helvetica-Bold"
MONO_FONT = "Courier"

def try_register():
    global BODY_FONT, BODY_BOLD
    for reg, bold, name_r, name_b in [
        ("/System/Library/Fonts/Supplemental/Arial.ttf",
         "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
         "Body", "BodyBold"),
        ("/Library/Fonts/Inter-Regular.ttf",
         "/Library/Fonts/Inter-SemiBold.ttf",
         "Body", "BodyBold"),
    ]:
        if os.path.exists(reg) and os.path.exists(bold):
            try:
                pdfmetrics.registerFont(TTFont(name_r, reg))
                pdfmetrics.registerFont(TTFont(name_b, bold))
                BODY_FONT = name_r
                BODY_BOLD = name_b
                return
            except Exception:
                pass

try_register()

# Styles -------------------------------------------------------------
ss = getSampleStyleSheet()

def style(name, **kwargs):
    base = dict(name=name, fontName=BODY_FONT, fontSize=10.5, leading=15,
                textColor=INK, alignment=TA_LEFT, spaceBefore=0, spaceAfter=0)
    base.update(kwargs)
    return ParagraphStyle(**base)

S_TITLE      = style("Title",      fontName=BODY_BOLD, fontSize=34, leading=38, textColor=INK, spaceAfter=4)
S_SUBTITLE   = style("Subtitle",   fontName=BODY_FONT, fontSize=14, leading=18, textColor=SUBINK, spaceAfter=22)
S_COVER_META = style("CoverMeta",  fontName=BODY_FONT, fontSize=9.5, leading=14, textColor=MUTED)

S_H1         = style("H1", fontName=BODY_BOLD, fontSize=18, leading=23, textColor=INK,
                     spaceBefore=18, spaceAfter=8)
S_H2         = style("H2", fontName=BODY_BOLD, fontSize=13, leading=18, textColor=INK,
                     spaceBefore=14, spaceAfter=6)
S_EYEBROW    = style("Eyebrow", fontName=BODY_BOLD, fontSize=8.5, leading=10,
                     textColor=INDIGO, spaceBefore=0, spaceAfter=3)
S_BODY       = style("Body",  alignment=TA_JUSTIFY, spaceAfter=8)
S_BODYLEAD   = style("BodyLead", fontSize=12, leading=18, textColor=INK, spaceAfter=10)
S_BULLET     = style("Bullet", leftIndent=14, bulletIndent=2, spaceAfter=4)
S_CAPTION    = style("Caption", fontSize=8.5, leading=12, textColor=MUTED,
                     alignment=TA_CENTER, spaceBefore=4, spaceAfter=14)
S_CODE       = style("Code", fontName=MONO_FONT, fontSize=8.5, leading=12, textColor=INK,
                     leftIndent=10, rightIndent=10, spaceBefore=4, spaceAfter=10,
                     backColor=PANEL, borderColor=HAIRLINE, borderWidth=0.5,
                     borderPadding=8)
S_QUOTE      = style("Quote", fontSize=11.5, leading=18, textColor=SUBINK,
                     leftIndent=14, spaceBefore=4, spaceAfter=10,
                     borderColor=INDIGO, borderWidth=0, borderPadding=0)
S_TOC        = style("TOC", fontSize=10.5, leading=18, textColor=INK)
S_FOOTER     = style("Footer", fontSize=8.0, leading=10, textColor=MUTED, alignment=TA_CENTER)

# Page decorations ---------------------------------------------------
def draw_cover(canv, doc):
    canv.saveState()
    # left accent rule
    canv.setFillColor(INDIGO)
    canv.rect(0, 0, 0.18 * inch, PAGE_H, fill=1, stroke=0)
    # wordmark dot
    canv.setFillColor(INDIGO)
    canv.circle(MARGIN_L + 6, PAGE_H - 0.75 * inch, 6, fill=1, stroke=0)
    canv.setFont(BODY_BOLD, 11)
    canv.setFillColor(INK)
    canv.drawString(MARGIN_L + 18, PAGE_H - 0.78 * inch, "Ambient")
    # footer
    canv.setFont(BODY_FONT, 8)
    canv.setFillColor(MUTED)
    canv.drawString(MARGIN_L, 0.5 * inch,
                    f"© {date.today().year} Ambient · Confidential — for review only")
    canv.restoreState()

def draw_body(canv, doc):
    canv.saveState()
    # subtle header rule
    canv.setStrokeColor(HAIRLINE)
    canv.setLineWidth(0.5)
    canv.line(MARGIN_L, PAGE_H - 0.7 * inch, PAGE_W - MARGIN_R, PAGE_H - 0.7 * inch)
    # wordmark
    canv.setFillColor(INDIGO); canv.circle(MARGIN_L + 4, PAGE_H - 0.5 * inch, 3.5, fill=1, stroke=0)
    canv.setFont(BODY_BOLD, 8.5); canv.setFillColor(INK)
    canv.drawString(MARGIN_L + 11, PAGE_H - 0.52 * inch, "Ambient  ·  Whitepaper")
    canv.setFont(BODY_FONT, 8.5); canv.setFillColor(MUTED)
    canv.drawRightString(PAGE_W - MARGIN_R, PAGE_H - 0.52 * inch, "Confidential — for review only")
    # footer page number
    canv.setFont(BODY_FONT, 8); canv.setFillColor(MUTED)
    canv.drawCentredString(PAGE_W / 2, 0.55 * inch, f"{doc.page}")
    canv.restoreState()

# Document setup -----------------------------------------------------
doc = BaseDocTemplate(
    OUT, pagesize=LETTER,
    leftMargin=MARGIN_L, rightMargin=MARGIN_R,
    topMargin=MARGIN_T, bottomMargin=MARGIN_B,
    title="Ambient — Whitepaper",
    author="Ambient",
    subject="Product and technical summary",
)

cover_frame = Frame(MARGIN_L, MARGIN_B, PAGE_W - MARGIN_L - MARGIN_R,
                    PAGE_H - MARGIN_T - MARGIN_B, id="cover", showBoundary=0,
                    leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
body_frame = Frame(MARGIN_L, MARGIN_B, PAGE_W - MARGIN_L - MARGIN_R,
                   PAGE_H - MARGIN_T - MARGIN_B, id="body", showBoundary=0,
                   leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
doc.addPageTemplates([
    PageTemplate(id="cover", frames=[cover_frame], onPage=draw_cover),
    PageTemplate(id="body",  frames=[body_frame],  onPage=draw_body),
])

# Helpers ------------------------------------------------------------
def H1(text, story):
    story.append(Paragraph(text, S_H1))
    story.append(HRFlowable(width="100%", thickness=0.5, color=HAIRLINE,
                            spaceBefore=2, spaceAfter=10))

def H2(text, story):
    story.append(Paragraph(text, S_H2))

def P(text, story, lead=False):
    story.append(Paragraph(text, S_BODYLEAD if lead else S_BODY))

def bullets(items, story):
    for it in items:
        story.append(Paragraph(f"• {it}", S_BULLET))
    story.append(Spacer(1, 6))

def fig(name, caption, story, width=6.4 * inch):
    path = os.path.join(FIG, name)
    img = Image(path)
    iw, ih = img.imageWidth, img.imageHeight
    scale = width / iw
    img._restrictSize(width, ih * scale)
    img.drawWidth = width
    img.drawHeight = ih * scale
    img.hAlign = "CENTER"
    story.append(Spacer(1, 4))
    story.append(img)
    story.append(Paragraph(caption, S_CAPTION))

def callout(text, story, color=INDIGO_L, border=INDIGO):
    t = Table([[Paragraph(text, style("CalloutBody",
                                       fontSize=10.5, leading=15, textColor=INK))]],
              colWidths=[PAGE_W - MARGIN_L - MARGIN_R - 0.04 * inch])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), color),
        ("BOX", (0, 0), (-1, -1), 0.6, border),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    story.append(t)
    story.append(Spacer(1, 10))

def kv_table(rows, story, col_widths=(1.7 * inch, 4.5 * inch)):
    # rows: list[(key, value)]
    data = [[Paragraph(k, style("KV_K", fontName=BODY_BOLD, fontSize=10, leading=14)),
             Paragraph(v, style("KV_V", fontName=BODY_FONT, fontSize=10, leading=14))]
            for k, v in rows]
    t = Table(data, colWidths=col_widths, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("LINEBELOW", (0, 0), (-1, -2), 0.4, HAIRLINE),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    story.append(t)
    story.append(Spacer(1, 10))

def matrix(header, rows, story, col_widths=None):
    data = [[Paragraph(h, style("MH", fontName=BODY_BOLD, fontSize=9.5,
                                leading=12, textColor=colors.white))
             for h in header]]
    for r in rows:
        data.append([Paragraph(c, style("MC", fontSize=9.5, leading=12))
                     for c in r])
    cw = col_widths or [(PAGE_W - MARGIN_L - MARGIN_R) / len(header)] * len(header)
    t = Table(data, colWidths=cw, hAlign="LEFT", repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), INK),
        ("TEXTCOLOR",  (0, 0), (-1, 0), colors.white),
        ("LINEBELOW",  (0, 0), (-1, -1), 0.4, HAIRLINE),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, PANEL]),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    story.append(t)
    story.append(Spacer(1, 10))


story = []

# COVER ----------------------------------------------------------------
story.append(Spacer(1, 1.4 * inch))
story.append(Paragraph("Eyebrow".upper(), style("CoverEyebrow", fontName=BODY_BOLD,
                                                fontSize=9, leading=11, textColor=INDIGO,
                                                spaceAfter=14)))
# replace with real eyebrow
story[-1] = Paragraph("WHITEPAPER  ·  v1", style("CoverEyebrow", fontName=BODY_BOLD,
                                                  fontSize=9.5, leading=11, textColor=INDIGO,
                                                  spaceAfter=18))
story.append(Paragraph("Ambient", S_TITLE))
story.append(Paragraph("The workspace for your data.", S_SUBTITLE))

cover_lead = (
    "Ambient is a workspace where pages, blocks, and typed collections "
    "compose into living documents — populated by pluggable connections that "
    "import data from the systems you already use. v1 ships an opinionated "
    "trading journal on top of a generic platform that scales to any "
    "structured-data vertical without rewrites."
)
story.append(Paragraph(cover_lead, style("CoverLead", fontSize=12.5,
                                          leading=20, textColor=INK,
                                          spaceAfter=28)))

cover_meta = [
    ["Document",  "Product & technical summary"],
    ["Audience",  "Prospective investors and team members"],
    ["Status",    "Confidential — for review only"],
    ["Date",      date.today().strftime("%B %Y")],
    ["Version",   "v1"],
]
t = Table(cover_meta, colWidths=[1.2 * inch, 4.5 * inch])
t.setStyle(TableStyle([
    ("FONTNAME", (0, 0), (0, -1), BODY_BOLD),
    ("FONTNAME", (1, 0), (1, -1), BODY_FONT),
    ("FONTSIZE", (0, 0), (-1, -1), 9.5),
    ("TEXTCOLOR", (0, 0), (0, -1), SUBINK),
    ("TEXTCOLOR", (1, 0), (1, -1), INK),
    ("LEFTPADDING", (0, 0), (-1, -1), 0),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ("TOPPADDING", (0, 0), (-1, -1), 0),
]))
story.append(t)

story.append(NextPageTemplate("body"))
story.append(PageBreak())

# CONTENTS ------------------------------------------------------------
H1("Contents", story)
toc = [
    ("1.", "Executive summary"),
    ("2.", "The problem"),
    ("3.", "Ambient in one paragraph"),
    ("4.", "Product overview"),
    ("5.", "System architecture"),
    ("6.", "Data model"),
    ("7.", "The platform seam"),
    ("8.", "The first vertical — Trading"),
    ("9.", "Security & multi-tenancy"),
    ("10.", "Performance"),
    ("11.", "Technology stack"),
    ("12.", "Roadmap"),
    ("13.", "Why now"),
    ("A.", "Appendix — design decisions"),
    ("B.", "Glossary"),
]
toc_data = [[Paragraph(n, S_TOC), Paragraph(t_, S_TOC)] for n, t_ in toc]
toc_tbl = Table(toc_data, colWidths=[0.5 * inch, 5.5 * inch])
toc_tbl.setStyle(TableStyle([
    ("LEFTPADDING", (0, 0), (-1, -1), 0),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ("TOPPADDING", (0, 0), (-1, -1), 4),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
]))
story.append(toc_tbl)
story.append(PageBreak())

# 1. Executive summary ------------------------------------------------
H1("1. Executive summary", story)
P(
    "Ambient is a multi-tenant SaaS workspace for structured data. It "
    "combines three primitives — <b>pages</b>, <b>blocks</b>, and "
    "<b>collections</b> — with a fourth concept, <b>connections</b>, that "
    "import data from external systems and feed the same collections users "
    "create by hand. Together they let a user assemble a document, a "
    "dashboard, and a database in the same workspace.",
    story, lead=True,
)
P(
    "Our v1 product ships an opinionated <b>trading journal</b> as the first "
    "vertical: it ingests Interactive Brokers Activity Statement CSVs, "
    "aggregates raw fills into round-trip trades, and surfaces them through "
    "pre-built dashboards. Every part of this experience is built on generic "
    "platform primitives — the only trading-specific code is a CSV parser, "
    "an aggregation pipeline, and three template files. Adding a new "
    "vertical is a matter of adding a Connection and a Template, not "
    "rebuilding the platform.",
    story,
)
P(
    "The product is built on Next.js 15, Supabase (Auth + Postgres + "
    "Storage), and the Plate.js block editor. Security is enforced by "
    "Postgres Row-Level Security, not by application code. Server "
    "Components and Server Actions are the only ways to read and write "
    "user data — there are no REST APIs to misuse.",
    story,
)
callout(
    "<b>Why Ambient matters:</b> Notion is a generic workspace with no data "
    "model. Airtable is a database with a weak editor. Vertical SaaS tools "
    "are siloed by industry. Ambient is the first workspace that treats "
    "<b>importable, typed data</b> as a first-class primitive — turning a "
    "single product into a platform for any vertical that lives in spreadsheets today.",
    story,
)

# 2. The problem ------------------------------------------------------
H1("2. The problem", story)
P(
    "Knowledge workers live inside two unrelated tools. The first is a "
    "<b>document editor</b> — Notion, Confluence, Google Docs — where they "
    "write, think, and share. The second is a <b>spreadsheet or database</b> "
    "— Excel, Airtable, a vertical SaaS — where their structured data lives. "
    "Connecting the two is manual, brittle, and constantly out of date.",
    story,
)
P(
    "The result is everyday friction: KPIs in slide decks that no one "
    "remembers to refresh, dashboards bolted onto data warehouses that take "
    "an engineer to change, journals and review documents that quietly fall "
    "out of sync with the underlying numbers.",
    story,
)
H2("Existing tools each miss one half", story)
matrix(
    ["Tool", "Strength", "What it lacks"],
    [
        ["Notion / Confluence",
         "Beautiful block editor; calm document UX",
         "No real data model; no importers; no typed aggregations"],
        ["Airtable / Coda",
         "Rich typed databases; formula columns",
         "Editor is an afterthought; pricing scales poorly per workspace"],
        ["Vertical SaaS (e.g., TraderSync, Edgewonk)",
         "Domain templates, importers, KPIs out of the box",
         "Locked to one vertical; you cannot bring your own data shape"],
        ["BI tools (Looker, Metabase)",
         "Powerful analytics on warehouses",
         "Not a workspace; not editable by the person doing the work"],
    ],
    story,
    col_widths=[1.5 * inch, 2.0 * inch, 3.0 * inch],
)
P(
    "Each tool optimizes for one half of the problem. The user pays for "
    "all of them and stitches the gap by hand.",
    story,
)

# 3. Ambient in one paragraph -----------------------------------------
H1("3. Ambient in one paragraph", story)
story.append(Paragraph(
    "<b>Ambient is a workspace where you can write a document, define a "
    "typed collection, and import data from external systems — all on the "
    "same canvas, secured by Row-Level Security, and built so that adding "
    "a new vertical is additive, not invasive.</b>",
    style("OneLiner", fontSize=13.5, leading=20, textColor=INK,
          leftIndent=14, rightIndent=14, spaceBefore=4, spaceAfter=14,
          backColor=INDIGO_L, borderColor=INDIGO, borderWidth=0.6,
          borderPadding=14)))

# 4. Product overview -------------------------------------------------
H1("4. Product overview", story)
P("Ambient is organized around four primitives. Each one is generic; "
  "trading-specific behavior is layered on top.", story)

H2("Pages", story)
P("A page is the top-level object in the sidebar. It has one of two types:", story)
bullets([
    "<b>Dashboard</b> — a Plate.js block document containing text, images, and data-aware blocks (Card, Chart, Table, Row).",
    "<b>Collection</b> — a typed list view backed by a schema (text, number, currency, date, datetime, select, multi-select, checkbox).",
], story)

H2("Blocks", story)
P("Blocks live inside dashboard pages. The four data-aware blocks all read from a collection, "
  "referenced by ID:", story)
bullets([
    "<b>Card</b> — one metric (count, sum, average, percentage) over a filtered collection.",
    "<b>Chart</b> — line, bar, or area chart of grouped aggregations.",
    "<b>Table</b> — a slice of a collection's list view, with sort, filter, and visible-field configuration.",
    "<b>Row</b> — a single collection row rendered inline, with all of its fields.",
], story)
P("No block type is trading-specific. The Trade detail UI is the generic <i>Row</i> block "
  "pointed at a row in the system-managed <i>Trades</i> collection.", story)

H2("Collections", story)
P("Collections are universal. Users can create them by hand or have them produced by a "
  "connection. The data lives in a generic JSONB row store with a typed schema. The same "
  "primitive backs a user's homemade 'Books I'm reading' list and the IBKR connection's "
  "system-managed <i>Trades</i> table.", story)

H2("Connections", story)
P("A connection is a pluggable importer. It declares the file types it parses, the "
  "collections it produces, optional per-connection settings, and an optional "
  "<b>post-process pipeline</b> that runs after import (e.g., aggregating raw fills into "
  "round-trip trades). v1 ships one connection — Interactive Brokers Activity Statement. "
  "Adding more is purely additive.", story)

P("These four primitives compose to form every product surface in v1:", story)
bullets([
    "A blank workspace with a Cmd+K palette to create pages.",
    "Apply a <b>template</b> (saved page recipe) to instantiate a pre-built dashboard.",
    "Import data from a <b>connection</b> to populate system collections.",
    "Mix system data with your own collections, your own fields, your own notes.",
], story)

story.append(PageBreak())

# 5. System architecture ----------------------------------------------
H1("5. System architecture", story)
P("Ambient is a server-rendered Next.js application backed by Supabase. The architecture "
  "is deliberately boring — Server Components do reads, Server Actions do writes, and "
  "Postgres Row-Level Security is the security boundary.", story)
fig("01_system_architecture.png",
    "Figure 1.  Three-tier architecture. Server Components own reads; Server Actions own writes; "
    "RLS is enforced inside Postgres on every owned table.", story)

H2("Key architectural choices", story)
kv_table([
    ("Server Components for reads",
     "Data fetching colocated with rendering; no client-side state library; React's RSC cache "
     "deduplicates fetches across nested blocks."),
    ("Server Actions for writes",
     "Type-safe, RPC-style writes. No REST API surface to misuse or to keep in sync with the client."),
    ("RLS as the boundary",
     "Every owned table has a policy: <font face='Courier'>owner_type = 'user' AND owner_id = auth.uid()</font>. "
     "Forgetting a WHERE clause cannot leak data."),
    ("Soft delete by default",
     "Pages and collections have <font face='Courier'>deleted_at</font>; standard queries filter it out. "
     "Trash & Restore is a v2 UI feature with no migration needed."),
    ("One region, single database",
     "Same-region Vercel + Supabase. Multi-region is an enterprise-tier concern; we are explicit about "
     "the latency trade-off."),
], story)

# 6. Data model -------------------------------------------------------
H1("6. Data model", story)
P("Ambient stores all structured user data in a small, generic schema. The same tables back "
  "user-created collections, system collections produced by connections, and any future "
  "view types (kanban, calendar, gallery) that we ship.", story)
fig("03_data_model.png",
    "Figure 2.  Core schema. All owned tables carry <font face='Courier'>owner_id</font> + "
    "<font face='Courier'>owner_type</font>; v1 uses <font face='Courier'>'user'</font>, v2 will "
    "extend the same policy to workspaces with zero migrations.",
    story)

H2("Forward-compatible ownership", story)
P("Every content table uses an <i>owner_id + owner_type</i> pair instead of a bare "
  "<i>user_id</i>. v1 always sets <i>owner_type = 'user'</i>. When Ambient ships teams in "
  "v2, the same column accepts <i>owner_type = 'workspace'</i> and the RLS policy extends "
  "with an <i>OR</i> clause — no column rename, no migration of existing rows.", story)

H2("Typed fields", story)
matrix(
    ["Field type", "Stored shape", "Notes"],
    [
        ["text", "string", "—"],
        ["number", "number", "Configurable precision and 'decimal'/'percent' format."],
        ["currency", "{ amount, currency_code }",
         "Multi-currency-aware. Aggregations group by code in v1; FX in v2."],
        ["date", "ISO date", "—"],
        ["datetime", "ISO timestamp (UTC)",
         "Always stored in UTC; rendered in the user's profile timezone."],
        ["select / multi_select", "string / string[]",
         "Option list with name, value, and color stored per field."],
        ["checkbox", "boolean", "—"],
    ],
    story,
    col_widths=[1.3 * inch, 1.9 * inch, 3.3 * inch],
)

P("All row data is stored as a single JSONB column keyed by field id. Expression indexes "
  "are added per-collection on hot fields when needed. At v1 volumes (thousands of rows "
  "per user) we have measured sub-50ms aggregations against this layout — no materialized "
  "views are required to hit our latency targets.", story)

# 7. Platform seam ----------------------------------------------------
H1("7. The platform seam", story)
P("The single most important architectural decision in Ambient is the boundary between "
  "blocks and data. Every data-aware block — Card, Chart, Table, Row — talks to a typed "
  "<i>Collection</i> interface, never to a specific table or domain concept:", story)

story.append(Paragraph(
    "interface Collection {<br/>"
    "&nbsp;&nbsp;list(opts):  Promise&lt;Row[]&gt;<br/>"
    "&nbsp;&nbsp;count(opts): Promise&lt;number&gt;<br/>"
    "&nbsp;&nbsp;aggregate(opts): Promise&lt;AggregateResult&gt;<br/>"
    "&nbsp;&nbsp;getRow(rowId): Promise&lt;Row | null&gt;<br/>"
    "}",
    S_CODE))

fig("04_platform_seam.png",
    "Figure 3.  Blocks bind to the Collection interface, not to underlying tables. "
    "New backing sources (computed collections, federated sources) are additive.",
    story)

callout(
    "<b>Implication for investors:</b> the marginal cost of a new vertical is a "
    "Connection (parser + pipeline) and a Template (page recipe). Everything "
    "the user sees — pages, blocks, the editor, the list view, security, "
    "settings — is shared platform code.",
    story,
)

# 8. First vertical: trading -----------------------------------------
H1("8. The first vertical — Trading", story)
P("v1 ships an opinionated trading journal — the first user-facing surface of the "
  "platform. We picked trading deliberately:", story)
bullets([
    "<b>High-signal data.</b> Every fill has a timestamp, price, and quantity. There is no "
    "ambiguity, so the aggregation pipeline can be tested deterministically.",
    "<b>Painful status quo.</b> Existing trading journals are siloed and ugly; users "
    "routinely export CSVs and rebuild dashboards in Excel.",
    "<b>Repeat usage.</b> Active traders review performance daily, weekly, and monthly "
    "— a workflow that benefits from a workspace, not a one-off report.",
], story)

H2("Connection: IBKR Activity Statement", story)
P("The connection parses Interactive Brokers' multi-section Activity Statement CSV. It is "
  "section-aware, timezone-aware (configurable per connection; default America/New_York), "
  "and idempotent — re-importing the same file adds zero new rows. Non-stock asset "
  "categories are silently skipped and recorded in an audit table.", story)

H2("Pipeline: Fills → Trades", story)
P("After fills are upserted, an aggregator walks fills per symbol in chronological order "
  "and groups them into <i>round-trip trades</i> (flat-to-flat). The algorithm handles "
  "scaling in, partial closes, exact closes, and direction flips — a single fill that "
  "crosses zero is split into a closing portion and an opening portion for the new "
  "direction. Per-trade P&amp;L is computed using weighted-average entry and exit prices.", story)
fig("05_ibkr_pipeline.png",
    "Figure 4.  The IBKR pipeline. CSV → parsed Fills → round-trip Trades — each step is a "
    "pure function, fully unit-tested, and idempotent.",
    story)

H2("Templates: pre-built dashboards", story)
P("Three trading templates ship with v1 — Performance Dashboard, Daily Journal, and "
  "Weekly Review. Each is stored as a JSON file in the repo and applied via "
  "<b>+ New page → Apply template</b>. Templates compose the same generic blocks that any "
  "user can drop into any page.", story)

# 9. Security --------------------------------------------------------
H1("9. Security & multi-tenancy", story)
P("Ambient is multi-tenant from day one. We treat data isolation as a security boundary, "
  "not a feature.", story)
fig("07_security.png",
    "Figure 5.  Every read and write is filtered by Postgres RLS on the user's session "
    "identity. Cross-tenant reads are blocked at the database, not by application code.",
    story)

H2("Three Supabase clients", story)
matrix(
    ["Client", "Where", "Permissions"],
    [
        ["Browser client", "Client Components", "RLS-bound to <font face='Courier'>auth.uid()</font>"],
        ["Server client", "Server Components, Server Actions", "RLS-bound to the user's session"],
        ["Admin client", "Service-role-only Server Actions (account deletion, seed reset)",
         "Bypasses RLS; gated by folder convention + lint rule"],
    ],
    story,
    col_widths=[1.2 * inch, 2.9 * inch, 2.4 * inch],
)

H2("Storage", story)
P("Two private Supabase Storage buckets — <i>attachments</i> and <i>avatars</i> — both with "
  "RLS policies that limit reads and writes to paths prefixed by the user's id.", story)

H2("Auth", story)
P("Email/password and Google OAuth via Supabase Auth. Email-change requires confirmation; "
  "delete-account triggers an admin Server Action that cascades through foreign keys. 2FA "
  "is supported by Supabase and ships in v2.", story)

# 10. Performance ----------------------------------------------------
H1("10. Performance", story)
kv_table([
    ("Latency", "Same-region Vercel + Supabase deployments. Server Components stream first paint."),
    ("Connections", "All server-side connections use the Supabase pooler URL — no per-request "
                    "connection storms under serverless load."),
    ("Bundle size", "Per-route code splitting. The Plate.js editor and Recharts are "
                    "dynamic-imported and never reach the marketing or auth bundles."),
    ("Re-renders", "Plate's onChange is debounced 500ms before persisting; the React RSC cache "
                    "deduplicates identical fetches across blocks on the same page."),
    ("Save safety", "Optimistic concurrency on page documents; pending debounced saves are "
                     "force-flushed on navigate and beforeunload."),
    ("Quality gate", "Lighthouse CI runs on every PR — Performance score below 90 on the dashboard "
                     "route fails the build."),
], story)

# 11. Tech stack -----------------------------------------------------
H1("11. Technology stack", story)
matrix(
    ["Layer", "Choice", "Why"],
    [
        ["Framework",   "Next.js 15 (App Router)",
         "Server Components fit the latency bar; mature SaaS ecosystem."],
        ["UI library",  "shadcn/ui + Tailwind",
         "Owned, copy-paste primitives; accessible by default; theme-able."],
        ["Editor",      "Plate.js (Slate-based)",
         "First-class shadcn integration; granular plugins for our data-aware blocks."],
        ["Charts",      "Recharts via shadcn Chart wrapper",
         "Lazy-loaded only where used."],
        ["Backend",     "Supabase (Auth + Postgres + Storage)",
         "One provider; RLS-aware; predictable cost curve."],
        ["State",       "None (server-owned)",
         "Server Components + URL state; no client store library to maintain."],
        ["Testing",     "Vitest + Playwright + axe-core",
         "Unit, integration (RLS), and end-to-end coverage on every PR."],
        ["Observability", "Sentry, Vercel Analytics, Supabase logs, Lighthouse CI",
         "Minimal but complete — enough to debug a customer incident."],
    ],
    story,
    col_widths=[1.2 * inch, 2.1 * inch, 3.2 * inch],
)

# 12. Roadmap --------------------------------------------------------
H1("12. Roadmap", story)
P("Ambient's roadmap is organized around <b>verticals</b>, not features. Every release "
  "either deepens an existing vertical or adds a new one — the platform itself grows by "
  "necessity, not by speculation.", story)
fig("06_verticals.png",
    "Figure 6.  Trading is the first vertical; future verticals plug in at the Connection + "
    "Template layer without changing the platform core.",
    story)

matrix(
    ["Phase", "Focus", "Highlights"],
    [
        ["v1  (now)",    "Trading vertical, core platform",
         "IBKR connection, Fills → Trades, 3 templates, Cmd+K, settings, RLS."],
        ["v1.5", "Trading depth, polish",
         "Additional IBKR sections (cash, fees, dividends), more templates, mobile read."],
        ["v2",   "Teams, billing, marketing",
         "<font face='Courier'>owner_type='workspace'</font>, Stripe, public landing + docs."],
        ["v2.5", "Second vertical (TBD)",
         "Sales pipeline or content calendar — chosen from inbound signal."],
        ["v3+",  "Platform features",
         "Computed collections, inter-collection relations, view types (kanban, calendar)."],
    ],
    story,
    col_widths=[0.9 * inch, 1.8 * inch, 3.8 * inch],
)

# 13. Why now --------------------------------------------------------
H1("13. Why now", story)
P("Three shifts have made Ambient possible — and necessary — at the same time:", story)
bullets([
    "<b>Server-rendered React is finally fast.</b> Next.js Server Components close the gap "
    "with classic server-rendered apps while keeping the React component model. The "
    "Notion-class editor experience no longer requires a Notion-class engineering team.",
    "<b>RLS-first databases are production-ready.</b> Supabase has matured Row-Level "
    "Security from a power-user feature to a reliable security boundary. Multi-tenancy "
    "is now a default, not a milestone.",
    "<b>Block editors are commoditized.</b> Plate.js and similar libraries make it "
    "possible to ship a serious block editor as a single dependency. The differentiator "
    "is no longer the editor itself — it is what the editor reads from.",
], story)
callout(
    "Ambient bets that the next workspace is not a better Notion or a prettier Airtable, "
    "but a workspace where <b>importable, typed data</b> is the primitive — and where every "
    "new vertical is a Connection, not a fork.",
    story, color=EMERALD_L, border=EMERALD,
)

# Appendix A ---------------------------------------------------------
story.append(PageBreak())
H1("Appendix A — Design decisions", story)
matrix(
    ["Decision", "Choice", "Rationale"],
    [
        ["Storage shape for rows", "JSONB keyed by field id",
         "One primitive for user collections and system collections; expression indexes per-field as needed."],
        ["Ownership column", "<font face='Courier'>owner_id</font> + <font face='Courier'>owner_type</font>",
         "Forward-compatible to v2 teams without a column rename."],
        ["P&amp;L math", "Weighted average",
         "Correct for performance review. FIFO matters for taxes; out of v1 scope; isolated for swap."],
        ["Round-trip rule", "Flat → flat per symbol",
         "Matches the user's mental model; flip handling makes it deterministic on every CSV."],
        ["Editor", "Plate.js",
         "Slate-based, granular plugins, shadcn integration; we own the data-aware blocks layer."],
        ["Realtime / collab", "Deferred to v2",
         "Single-user editing covers v1 use cases; CRDT layer is invasive enough to be its own milestone."],
        ["Background queue",   "Deferred — synchronous Server Actions in v1",
         "v1 imports are bounded (≤10k fills); queue is a v2 concern when we add larger feeds."],
        ["Materialized views", "None in v1",
         "Direct queries with indexes hit our latency bar; add only if metrics demand it."],
    ],
    story,
    col_widths=[1.4 * inch, 1.9 * inch, 3.1 * inch],
)

# Appendix B ---------------------------------------------------------
H1("Appendix B — Glossary", story)
kv_table([
    ("Page",       "A top-level sidebar item — either a Dashboard or a Collection."),
    ("Dashboard",  "A page containing a Plate.js block document."),
    ("Collection", "A typed table (schema + rows) shown via a list view."),
    ("Block",      "An element in a Plate document. Data-aware blocks: Card, Chart, Table, Row."),
    ("View",       "A saved configuration (sort, filters, visible fields) for a collection."),
    ("Connection", "A pluggable importer that produces collections from external data."),
    ("Template",   "A saved page recipe applied via + New page → Apply template."),
    ("Pipeline",   "A named transform run after a connection imports — e.g., Fills → Trades."),
    ("Round-trip", "One trade, defined as flat → position → flat on a single symbol."),
    ("System collection",
     "Created and managed by a connection; users can add adjacent fields but cannot rename or delete the system fields."),
], story)

# Footer page ---------------------------------------------------------
story.append(Spacer(1, 24))
story.append(HRFlowable(width="100%", thickness=0.5, color=HAIRLINE,
                        spaceBefore=2, spaceAfter=14))
story.append(Paragraph(
    "Ambient — confidential.  This document is shared for the recipient's review and "
    "should not be redistributed without permission. Forward questions to the founding "
    "team.",
    style("Closing", fontSize=9, leading=14, textColor=MUTED, alignment=TA_LEFT)
))

doc.build(story)
print("Wrote", OUT)
