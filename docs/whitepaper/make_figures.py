"""Generate diagrams for the Ambient whitepaper."""
from __future__ import annotations
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
from matplotlib.lines import Line2D
import os

OUT = os.path.join(os.path.dirname(__file__), "figures")
os.makedirs(OUT, exist_ok=True)

# Palette ----------------------------------------------------------------
INK      = "#0F172A"   # near-black text
SUBINK   = "#475569"   # secondary text
HAIRLINE = "#CBD5E1"   # borders / dividers
SURFACE  = "#FFFFFF"
PANEL    = "#F8FAFC"   # subtle panel fill
PANEL2   = "#F1F5F9"
INDIGO   = "#4F46E5"
INDIGO_2 = "#6366F1"
INDIGO_L = "#EEF2FF"
EMERALD  = "#059669"
EMERALD_L= "#ECFDF5"
AMBER    = "#D97706"
AMBER_L  = "#FEF3C7"
ROSE     = "#E11D48"
ROSE_L   = "#FFE4E6"
ARROW    = "#64748B"

plt.rcParams.update({
    "font.family": ["Helvetica", "Arial", "sans-serif"],
    "font.size": 9,
    "axes.edgecolor": HAIRLINE,
    "savefig.facecolor": "white",
    "savefig.dpi": 220,
    "figure.dpi": 220,
})

def box(ax, x, y, w, h, label, sub=None, fill=SURFACE, edge=HAIRLINE,
        text=INK, subcolor=SUBINK, size=10, sub_size=8.5, weight="bold",
        radius=0.04, lw=1.0):
    patch = FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad=0.01,rounding_size={radius}",
        linewidth=lw, edgecolor=edge, facecolor=fill,
    )
    ax.add_patch(patch)
    if sub:
        ax.text(x + w/2, y + h*0.62, label, ha="center", va="center",
                color=text, fontsize=size, weight=weight)
        ax.text(x + w/2, y + h*0.30, sub, ha="center", va="center",
                color=subcolor, fontsize=sub_size)
    else:
        ax.text(x + w/2, y + h/2, label, ha="center", va="center",
                color=text, fontsize=size, weight=weight)
    return (x, y, w, h)

def arrow(ax, x1, y1, x2, y2, color=ARROW, lw=1.4, style="-|>", connectionstyle=None, label=None):
    arr = FancyArrowPatch(
        (x1, y1), (x2, y2),
        arrowstyle=style, mutation_scale=10,
        color=color, lw=lw,
        connectionstyle=connectionstyle or "arc3,rad=0",
    )
    ax.add_patch(arr)
    if label:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        ax.text(mx, my + 0.05, label, ha="center", va="bottom",
                color=SUBINK, fontsize=8, style="italic")

def setup(ax, w=10, h=6):
    ax.set_xlim(0, w); ax.set_ylim(0, h)
    ax.set_aspect("equal"); ax.axis("off")

def save(fig, name):
    fig.savefig(os.path.join(OUT, name), bbox_inches="tight", pad_inches=0.25,
                facecolor="white")
    plt.close(fig)

# ------------------------------------------------------------------------
# Figure 1: System architecture
# ------------------------------------------------------------------------
def fig_system_architecture():
    fig, ax = plt.subplots(figsize=(9.5, 6.4))
    setup(ax, 10, 7)

    # tier panels (background)
    for (x, y, w, h, label) in [
        (0.4, 5.4, 9.2, 1.3, "Client  ·  Browser"),
        (0.4, 3.2, 9.2, 1.8, "Edge  ·  Vercel (Next.js App Router)"),
        (0.4, 0.4, 9.2, 2.4, "Data plane  ·  Supabase (single region)"),
    ]:
        ax.add_patch(FancyBboxPatch(
            (x, y), w, h, boxstyle="round,pad=0.01,rounding_size=0.08",
            linewidth=0.8, edgecolor=HAIRLINE, facecolor=PANEL))
        ax.text(x + 0.18, y + h - 0.22, label, color=SUBINK,
                fontsize=8.5, weight="bold")

    # Client tier
    box(ax, 0.8, 5.55, 2.4, 0.95, "Sidebar", "Pages • Cmd+K", fill=SURFACE)
    box(ax, 3.5, 5.55, 3.4, 0.95, "Plate.js editor", "Custom data-aware blocks", fill=SURFACE)
    box(ax, 7.2, 5.55, 2.2, 0.95, "List view", "Type-aware cells", fill=SURFACE)

    # Edge tier
    box(ax, 0.8, 3.7, 2.7, 1.05, "Server Components", "All reads", fill=INDIGO_L, edge=INDIGO_2)
    box(ax, 3.8, 3.7, 2.7, 1.05, "Server Actions", "All writes", fill=INDIGO_L, edge=INDIGO_2)
    box(ax, 6.8, 3.7, 2.6, 1.05, "Middleware", "Session refresh\nAuth gate", fill=SURFACE)

    # Data tier
    box(ax, 0.8, 1.8, 2.0, 0.95, "Postgres",  "pages • collections\nrows • views", fill=SURFACE)
    box(ax, 3.0, 1.8, 1.9, 0.95, "Auth",  "Email / OAuth\nSessions", fill=SURFACE)
    box(ax, 5.1, 1.8, 2.0, 0.95, "Storage", "attachments • avatars", fill=SURFACE)
    box(ax, 7.3, 1.8, 2.1, 0.95, "Row-Level Security", "owner_id = auth.uid()", fill=EMERALD_L, edge=EMERALD)

    box(ax, 0.8, 0.6, 8.6, 0.8,
        "Observability:  Sentry (PII-stripped)   •   Vercel Analytics   •   Supabase logs   •   Lighthouse CI ≥ 90",
        fill=PANEL2, size=9, weight="normal")

    # arrows
    arrow(ax, 5, 5.5, 5, 4.85, lw=1.6, label="HTTPS")
    arrow(ax, 5, 3.65, 5, 2.85, lw=1.6, label="Supabase JS (pooler)")

    ax.text(5, 6.85, "System architecture", ha="center", va="bottom",
            color=INK, fontsize=13, weight="bold")

    save(fig, "01_system_architecture.png")


# ------------------------------------------------------------------------
# Figure 2: Conceptual model — Pages, Blocks, Collections, Connections
# ------------------------------------------------------------------------
def fig_conceptual_model():
    fig, ax = plt.subplots(figsize=(9.5, 5.6))
    setup(ax, 10, 6)

    # Pages
    box(ax, 0.4, 3.6, 3.2, 2.0, "Pages",
        "Dashboards  •  Collections\n(typed list views)",
        fill=INDIGO_L, edge=INDIGO_2, size=11)

    # Blocks (inside dashboards)
    box(ax, 4.0, 4.5, 5.6, 1.1, "Blocks",
        "Text  •  Heading  •  Card  •  Chart  •  Table  •  Row",
        fill=SURFACE, size=10)

    # Collection interface seam
    box(ax, 4.0, 2.7, 5.6, 1.3, "Collection interface",
        "list( ) · count( ) · aggregate( ) · getRow( )",
        fill=AMBER_L, edge=AMBER, size=10.5)

    # Underlying collections
    box(ax, 0.4, 0.4, 2.9, 1.7, "User-created\ncollections",
        "Schema + rows\nStored as JSONB",
        fill=SURFACE, size=10)
    box(ax, 3.6, 0.4, 2.9, 1.7, "System collections",
        "Produced by connections\n(Fills, Trades)",
        fill=PANEL, size=10)
    box(ax, 6.8, 0.4, 2.8, 1.7, "Connections",
        "Pluggable importers\n(IBKR in v1)",
        fill=EMERALD_L, edge=EMERALD, size=10)

    # arrows
    arrow(ax, 2.0, 4.5, 4.0, 5.05, lw=1.2)         # pages -> blocks
    arrow(ax, 6.8, 4.5, 6.8, 4.05, lw=1.2)         # blocks -> interface
    arrow(ax, 4.7, 2.7, 1.85, 2.1, lw=1.2)         # iface -> user coll
    arrow(ax, 6.8, 2.7, 5.05, 2.1, lw=1.2)         # iface -> system coll
    arrow(ax, 8.2, 2.0, 8.2, 0.4 + 1.7, lw=0.0, style="-")  # placeholder
    arrow(ax, 8.2, 2.1, 8.2, 2.7, lw=1.0, style="<-")       # connections feed system collections
    arrow(ax, 7.5, 1.25, 6.55, 1.25, lw=1.2)               # connections -> system

    ax.text(5, 5.85, "Concept map", ha="center", va="bottom",
            color=INK, fontsize=13, weight="bold")

    save(fig, "02_concept_map.png")


# ------------------------------------------------------------------------
# Figure 3: Data model (lightweight ER)
# ------------------------------------------------------------------------
def fig_data_model():
    fig, ax = plt.subplots(figsize=(9.8, 6.6))
    setup(ax, 10, 7.2)

    def entity(x, y, w, h, name, rows, key_color=INDIGO):
        ax.add_patch(FancyBboxPatch(
            (x, y), w, h, boxstyle="round,pad=0.01,rounding_size=0.05",
            linewidth=1.0, edgecolor=HAIRLINE, facecolor=SURFACE))
        ax.add_patch(Rectangle((x, y + h - 0.42), w, 0.42,
                               linewidth=0, facecolor=key_color, alpha=0.10))
        ax.text(x + 0.18, y + h - 0.21, name, color=INK,
                fontsize=10.5, weight="bold")
        for i, r in enumerate(rows):
            ax.text(x + 0.18, y + h - 0.6 - i * 0.26, r,
                    color=SUBINK, fontsize=8.4, family="monospace")

    # auth.users at top centre
    entity(2.0, 5.95, 2.4, 0.95, "auth.users",
           ["id (PK)", "email"], key_color=ROSE)
    entity(5.0, 5.95, 3.0, 0.95, "profiles",
           ["user_id (PK FK)",
            "display_name • avatar • tz • theme"], key_color=ROSE)

    # pages
    entity(0.4, 3.55, 3.0, 2.05, "pages",
           ["id (PK)",
            "owner_id, owner_type",
            "title • emoji",
            "page_type ∈ {dashboard,collection}",
            "document  (JSONB Plate doc)",
            "collection_id (FK, nullable)",
            "deleted_at  (soft delete)"])

    # collections
    entity(3.7, 3.55, 2.7, 2.05, "collections",
           ["id (PK)",
            "owner_id, owner_type",
            "name",
            "is_system",
            "managed_by_connection",
            "deleted_at"])

    # collection_fields
    entity(6.7, 3.55, 3.0, 2.05, "collection_fields",
           ["id (PK)",
            "collection_id (FK)",
            "name",
            "type  ∈ text/number/currency/",
            "  date/datetime/select/...",
            "options • config",
            "is_system"])

    # collection_rows
    entity(0.4, 1.05, 3.0, 2.0, "collection_rows",
           ["id (PK)",
            "collection_id (FK)",
            "data (JSONB)",
            "  { fieldId: value, ... }",
            "source ∈ {user, connection:ibkr}",
            "source_external_id",
            "UNIQUE(owner,coll,src_ext_id)"])

    # collection_views
    entity(3.7, 1.05, 2.7, 2.0, "collection_views",
           ["id (PK)",
            "collection_id (FK)",
            "name • type='list' (v1)",
            "config: sort, filters,",
            "  visibleFields, pageSize",
            "is_default • sort_index"])

    # connection_imports + attachments stacked
    entity(6.7, 2.0, 3.0, 1.05, "connection_imports",
           ["connection, filename, status,",
            "rows_added/skipped/updated"])
    entity(6.7, 1.05, 3.0, 0.9, "attachments",
           ["row_id (FK)",
            "storage_path, caption"])

    # relationships (simple lines)
    for (x1, y1, x2, y2) in [
        (3.2, 5.95, 3.2, 5.6),     # auth.users  -> pages
        (5.0, 6.30, 4.4, 5.6),     # profiles    -> auth.users (1-1)
        (3.4, 4.45, 3.7, 4.45),    # pages       -> collections
        (5.05, 4.55, 6.7, 4.55),   # collections -> fields
        (5.05, 4.25, 5.05, 3.05),  # collections -> rows
        (5.05, 4.25, 5.05, 3.05),
        (5.05, 4.05, 5.05, 3.05),  # collections -> views (via x)
        (6.4, 4.55, 6.7, 2.55),    # imports/attachments side
    ]:
        ax.add_line(Line2D([x1, x2], [y1, y2], color=HAIRLINE, lw=1.0))

    ax.text(5, 6.95, "Data model", ha="center", va="bottom",
            color=INK, fontsize=13, weight="bold")
    ax.text(5, 0.3,
            "RLS:  owner_type = 'user' AND owner_id = auth.uid()    (extends to teams in v2 without column rename)",
            ha="center", color=SUBINK, fontsize=8.5, style="italic")

    save(fig, "03_data_model.png")


# ------------------------------------------------------------------------
# Figure 4: The platform seam (Collection interface)
# ------------------------------------------------------------------------
def fig_platform_seam():
    fig, ax = plt.subplots(figsize=(9.5, 5.4))
    setup(ax, 10, 5.6)

    # Left: blocks
    box(ax, 0.4, 4.0, 2.0, 0.8, "Card",   fill=SURFACE, size=9.5)
    box(ax, 0.4, 3.0, 2.0, 0.8, "Chart",  fill=SURFACE, size=9.5)
    box(ax, 0.4, 2.0, 2.0, 0.8, "Table",  fill=SURFACE, size=9.5)
    box(ax, 0.4, 1.0, 2.0, 0.8, "Row",    fill=SURFACE, size=9.5)
    ax.text(1.4, 4.95, "Data-aware blocks", color=SUBINK, fontsize=9, weight="bold", ha="center")

    # Middle: interface
    box(ax, 3.2, 1.4, 3.6, 3.4,
        "Collection interface",
        "list( )\ncount( )\naggregate( )\ngetRow( )",
        fill=AMBER_L, edge=AMBER, size=11.5, sub_size=10)
    ax.text(5.0, 5.0, "One typed contract", color=SUBINK, fontsize=9, weight="bold", ha="center")

    # Right: backing sources
    box(ax, 7.6, 4.0, 2.2, 0.8, "User collections", fill=SURFACE, size=9.5)
    box(ax, 7.6, 3.0, 2.2, 0.8, "System collections", "from Connections", fill=EMERALD_L, edge=EMERALD, size=9.5, sub_size=7.5)
    box(ax, 7.6, 2.0, 2.2, 0.8, "Computed (v2)", fill=PANEL2, size=9.5)
    box(ax, 7.6, 1.0, 2.2, 0.8, "Federated (v2+)", fill=PANEL2, size=9.5)
    ax.text(8.7, 4.95, "Backing sources", color=SUBINK, fontsize=9, weight="bold", ha="center")

    # arrows from blocks into the interface
    for y in (4.4, 3.4, 2.4, 1.4):
        arrow(ax, 2.4, y, 3.2, y, lw=1.0)
    # arrows from interface to backings
    for y in (4.4, 3.4, 2.4, 1.4):
        arrow(ax, 6.8, y, 7.6, y, lw=1.0, color=HAIRLINE)

    ax.text(5, 5.4, "The platform seam:  blocks never know about trading", ha="center",
            color=INK, fontsize=12.5, weight="bold")

    save(fig, "04_platform_seam.png")


# ------------------------------------------------------------------------
# Figure 5: IBKR import + round-trip pipeline
# ------------------------------------------------------------------------
def fig_ibkr_pipeline():
    fig, ax = plt.subplots(figsize=(9.5, 5.6))
    setup(ax, 10, 6)

    # Stages
    box(ax, 0.2, 3.0, 1.7, 1.4, "Activity\nStatement CSV",
        fill=SURFACE, size=10)
    box(ax, 2.2, 3.0, 1.7, 1.4, "Parser",
        "Section-aware\npapaparse\nTZ → UTC",
        fill=SURFACE, size=10, sub_size=8)
    box(ax, 4.2, 3.0, 1.7, 1.4, "Fills",
        "system collection\nupsert on TradeID",
        fill=INDIGO_L, edge=INDIGO_2, size=10, sub_size=8)
    box(ax, 6.2, 3.0, 1.7, 1.4, "Aggregator",
        "per-symbol\nflat → flat\nflip-aware",
        fill=AMBER_L, edge=AMBER, size=10, sub_size=8)
    box(ax, 8.2, 3.0, 1.7, 1.4, "Trades",
        "system collection\nweighted P&L",
        fill=EMERALD_L, edge=EMERALD, size=10, sub_size=8)

    # arrows
    for x in (1.9, 3.9, 5.9, 7.9):
        arrow(ax, x, 3.7, x + 0.3, 3.7, lw=1.4)

    # Below: pipeline detail boxes
    ax.text(5, 2.55, "Round-trip detection per symbol", ha="center",
            color=SUBINK, fontsize=9.5, weight="bold")
    detail = (
        "position = 0\n"
        "for fill in fills_for_symbol:\n"
        "    if |position| < ε:        open new Trade\n"
        "    elif same_direction:      scale into Trade\n"
        "    elif new_position ≈ 0:    close Trade\n"
        "    elif sign unchanged:      partial close\n"
        "    else:                     FLIP — split fill, close, open new"
    )
    ax.text(0.5, 0.5, detail, color=INK, fontsize=8.6, family="monospace",
            va="bottom", ha="left",
            bbox=dict(boxstyle="round,pad=0.5", facecolor=PANEL, edgecolor=HAIRLINE))

    # right side: outputs feed blocks
    box(ax, 7.0, 0.4, 2.9, 1.6, "Trades drives blocks",
        "KPI Cards · Equity curve\nP&L by symbol · Row detail",
        fill=SURFACE, size=10, sub_size=8.5)

    arrow(ax, 9.05, 3.0, 9.05, 2.0, lw=1.2)

    ax.text(5, 5.0, "Connection pipeline:  CSV → Fills → Trades", ha="center",
            color=INK, fontsize=12.5, weight="bold")

    save(fig, "05_ibkr_pipeline.png")


# ------------------------------------------------------------------------
# Figure 6: Vertical extensibility (today vs future)
# ------------------------------------------------------------------------
def fig_verticals():
    fig, ax = plt.subplots(figsize=(9.5, 5.0))
    setup(ax, 10, 5.2)

    # platform foundation
    box(ax, 0.4, 0.4, 9.2, 1.5,
        "Generic platform primitives",
        "Pages  ·  Blocks  ·  Collections  ·  Views  ·  Templates  ·  Connections  ·  Pipelines",
        fill=INDIGO_L, edge=INDIGO_2, size=12, sub_size=10.5)

    # current vertical
    box(ax, 0.4, 2.4, 2.1, 2.2, "Trading",
        "v1\n\nIBKR connection\nFills → Trades pipeline\n3 templates",
        fill=EMERALD_L, edge=EMERALD, size=11, sub_size=8.5)

    # future verticals (semi-transparent)
    for i, (label, sub) in enumerate([
        ("Sales pipelines", "CSV / CRM importers\nDeal-stage pipeline"),
        ("Content calendar", "RSS / Notion importers\nPublishing pipeline"),
        ("Expenses", "Plaid importer\nCategorization pipeline"),
        ("Your vertical", "Bring your own data\nBring your own pipeline"),
    ]):
        x = 2.7 + i * 1.85
        box(ax, x, 2.4, 1.75, 2.2, label, sub,
            fill=PANEL2, edge=HAIRLINE, size=10, sub_size=7.6,
            text=SUBINK, subcolor=SUBINK)

    ax.text(5, 4.85, "One platform, many verticals", ha="center",
            color=INK, fontsize=13, weight="bold")
    ax.text(5, 0.18, "v2+:  ship new verticals by adding Connections + Templates  ·  no platform rewrites",
            ha="center", color=SUBINK, fontsize=9.2, style="italic")

    save(fig, "06_verticals.png")


# ------------------------------------------------------------------------
# Figure 7: Security boundary (RLS)
# ------------------------------------------------------------------------
def fig_security():
    fig, ax = plt.subplots(figsize=(9.5, 4.4))
    setup(ax, 10, 4.6)

    # User A and User B columns
    for i, (label, color, light) in enumerate([
        ("User A — session", INDIGO, INDIGO_L),
        ("User B — session", ROSE,  ROSE_L),
    ]):
        x = 0.4 + i * 5.0
        ax.add_patch(FancyBboxPatch(
            (x, 0.6), 4.6, 3.4, boxstyle="round,pad=0.01,rounding_size=0.08",
            linewidth=0.8, edgecolor=HAIRLINE, facecolor=light, alpha=0.45))
        ax.text(x + 0.2, 3.85, label, color=INK, fontsize=10.5, weight="bold")

    # Database centre
    box(ax, 3.4, 1.4, 3.2, 1.8,
        "Postgres",
        "RLS policy on every owned table:\n"
        "owner_type = 'user'\nAND owner_id = auth.uid()",
        fill=SURFACE, edge=HAIRLINE, size=11, sub_size=9)

    # A reads its data
    arrow(ax, 1.6, 2.3, 3.4, 2.3, lw=1.2, color=INDIGO)
    ax.text(2.5, 2.45, "A's rows  ✓", color=INDIGO, fontsize=8.8, weight="bold")
    # B reads its data
    arrow(ax, 8.4, 2.3, 6.6, 2.3, lw=1.2, color=ROSE)
    ax.text(7.5, 2.45, "B's rows  ✓", color=ROSE, fontsize=8.8, weight="bold")

    # A tries to read B and is denied (dashed)
    a = FancyArrowPatch((1.6, 1.6), (8.0, 1.6), arrowstyle="-|>",
                       mutation_scale=10, color=ARROW, lw=1.0, linestyle=(0, (4, 4)))
    ax.add_patch(a)
    ax.text(5.0, 1.42, "cross-tenant read  ✗  blocked by RLS",
            ha="center", color=SUBINK, fontsize=8.6, style="italic")

    ax.text(5, 4.25, "Security boundary:  Row-Level Security, not WHERE clauses",
            ha="center", color=INK, fontsize=12.5, weight="bold")

    save(fig, "07_security.png")


if __name__ == "__main__":
    fig_system_architecture()
    fig_conceptual_model()
    fig_data_model()
    fig_platform_seam()
    fig_ibkr_pipeline()
    fig_verticals()
    fig_security()
    print("generated:")
    for f in sorted(os.listdir(OUT)):
        print(" -", f)
