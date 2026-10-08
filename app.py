import html as _html
import math

import streamlit as st
import pandas as pd

from search.client import SerpApiClient
from analysis.evidence import collect_evidence
from analysis.signals import (
    calculate_signals,
    calculate_confidence,
    calculate_trend_momentum,
)
from analysis.gap_detector import (
    detect_gap,
    calculate_opportunity_score,
    classify_opportunity,
)
from analysis.report import build_report


st.set_page_config(
    page_title="GapFinder",
    page_icon="🔎",
    layout="wide",
)

client = SerpApiClient()


# ==================================================================
# Visual design
# ------------------------------------------------------------------
# Palette (mineral, low-saturation):
#   paper   #EDEFEA   page ground
#   panel   #E2E6E0   sidebar
#   ink     #1F2B2E   text
#   soft    #5A6A6D   secondary text
#   teal    #3B6860   technology / primary action
#   slate   #66778F   commercial supply
#   ochre   #A9843C   the gap itself
# Type: Libre Franklin (interface) + Source Serif 4 (verdicts)
# ==================================================================

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Libre+Franklin:wght@400;500;600&family=Source+Serif+4:opsz,wght@8..60,400;8..60,500&display=swap');

.stApp {
    --gf-paper: #EDEFEA;
    --gf-panel: #E2E6E0;
    --gf-ink: #1F2B2E;
    --gf-soft: #5A6A6D;
    --gf-rule: #C8CFC9;
    --gf-track: #D6DCD6;
    --gf-teal: #3B6860;
    --gf-teal-deep: #2F544E;
    --gf-slate: #66778F;
    --gf-ochre: #A9843C;
    --gf-sans: 'Libre Franklin', 'Helvetica Neue', Arial, sans-serif;
    --gf-serif: 'Source Serif 4', Georgia, 'Times New Roman', serif;
    color-scheme: light;
    color: var(--gf-ink);
    font-family: var(--gf-sans);
}
.stApp,
.stApp [data-testid="stAppViewContainer"],
.stApp [data-testid="stHeader"] {
    background: var(--gf-paper) !important;
}
.stApp ::selection { background: rgba(59, 104, 96, .25); }

/* Streamlit chrome */
.stApp [data-testid="stDecoration"],
.stApp [data-testid="stDeployButton"],
.stApp #MainMenu,
.stApp footer { display: none !important; }

.stApp .block-container,
.stApp [data-testid="stMainBlockContainer"] {
    max-width: 1040px;
    padding: 2.5rem 2.25rem 6rem;
}

/* Base text */
.stApp p, .stApp li, .stApp label, .stApp summary,
.stApp [data-testid="stMarkdownContainer"] {
    font-family: var(--gf-sans);
    color: var(--gf-ink);
}
.stApp [data-testid="stMarkdownContainer"] p {
    font-size: .98rem;
    line-height: 1.65;
}
.stApp [data-testid="stMarkdownContainer"] ul {
    padding-left: 1.1rem;
    max-width: 44rem;
}
.stApp [data-testid="stMarkdownContainer"] li {
    margin: .45rem 0;
    line-height: 1.6;
    font-size: .98rem;
}
.stApp [data-testid="stMarkdownContainer"] li::marker { color: var(--gf-ochre); }
.stApp code {
    background: #DCE2DC;
    color: var(--gf-ink);
    padding: .12rem .4rem;
    border-radius: 2px;
    font-size: .84em;
}

/* Header */
.gf-head { padding: .25rem 0 1.5rem; }
.gf-brand { display: flex; align-items: center; gap: .85rem; }
.gf-logo { position: relative; width: 36px; height: 22px; flex: none; }
.gf-logo i {
    position: absolute; top: 0; width: 22px; height: 22px;
    border-radius: 50%; box-sizing: border-box;
}
.gf-logo i:first-child { left: 0; background: var(--gf-teal); }
.gf-logo i:last-child { right: 0; border: 2.5px solid var(--gf-slate); }
.gf-wordmark {
    font-size: 2.1rem; font-weight: 600;
    letter-spacing: -.03em; line-height: 1.1;
}
.gf-tag {
    font-family: var(--gf-serif);
    font-size: 1.25rem; line-height: 1.4;
    margin-top: 1.1rem; max-width: 34rem;
}
.gf-lede {
    font-size: .93rem; line-height: 1.65; color: var(--gf-soft);
    margin-top: .6rem; max-width: 38rem;
}

/* Input */
.stApp [data-testid="stTextInput"] { max-width: 46rem; }
.stApp [data-testid="stTextInput"] label p {
    font-size: .82rem; font-weight: 500; color: var(--gf-soft);
}
.stApp [data-testid="stTextInput"] [data-baseweb="input"] {
    background: transparent !important;
    border: 0 !important;
    border-bottom: 1px solid var(--gf-ink) !important;
    border-radius: 0 !important;
    box-shadow: none !important;
}
.stApp [data-testid="stTextInput"] [data-baseweb="base-input"] {
    background: transparent !important;
    border: 0 !important;
}
.stApp [data-testid="stTextInput"] [data-baseweb="input"]:focus-within {
    border-bottom-color: var(--gf-teal) !important;
    box-shadow: 0 1px 0 0 var(--gf-teal) !important;
}
.stApp [data-testid="stTextInput"] input {
    font-family: var(--gf-sans);
    font-size: 1.12rem;
    padding: .6rem 0 !important;
    color: var(--gf-ink) !important;
    -webkit-text-fill-color: var(--gf-ink);
    background: transparent !important;
}
.stApp [data-testid="stTextInput"] input::placeholder {
    color: #8A9799 !important;
    -webkit-text-fill-color: #8A9799;
}

/* Button */
.stApp .stButton > button {
    background: var(--gf-teal);
    border: 1px solid var(--gf-teal);
    border-radius: 3px;
    padding: .55rem 1.3rem;
    box-shadow: none;
    transition: background .15s ease;
}
.stApp .stButton > button p {
    color: #F2F5F0; font-size: .92rem; font-weight: 500;
}
.stApp .stButton > button:hover,
.stApp .stButton > button:focus,
.stApp .stButton > button:active {
    background: var(--gf-teal-deep);
    border-color: var(--gf-teal-deep);
    box-shadow: none;
}
.stApp .stButton > button:focus-visible {
    outline: 2px solid var(--gf-ink); outline-offset: 2px;
}

/* Spinner */
.stApp [data-testid="stSpinner"] p { color: var(--gf-soft); font-size: .92rem; }

/* Sidebar */
.stApp [data-testid="stSidebar"] {
    background: var(--gf-panel);
    border-right: 1px solid var(--gf-rule);
}
.gf-side-title { font-weight: 600; font-size: 1rem; margin-bottom: 1.1rem; }
.gf-side-row {
    display: flex; justify-content: space-between; align-items: baseline;
    gap: 1rem; font-size: .85rem; color: var(--gf-soft);
}
.gf-side-row b {
    color: var(--gf-ink); font-size: 1.15rem; font-weight: 500;
    font-variant-numeric: tabular-nums;
}
.gf-side-meter {
    height: 4px; background: #C6CDC7; margin: .6rem 0 .95rem;
}
.gf-side-meter div { height: 100%; background: var(--gf-teal); }
.gf-side-note {
    font-size: .78rem; line-height: 1.55; color: var(--gf-soft); margin-top: 1.1rem;
}

/* Sections */
.gf-rule { border-top: 1px solid var(--gf-rule); margin: 1.9rem 0 .4rem; }
.gf-sec-title { font-size: 1rem; font-weight: 600; line-height: 1.3; }
.gf-sec-note {
    font-size: .82rem; line-height: 1.55; color: var(--gf-soft);
    margin-top: .4rem; max-width: 15rem;
}

/* Verdict */
.gf-class {
    font-family: var(--gf-serif); font-size: 2rem; font-weight: 500;
    letter-spacing: -.01em; line-height: 1.2;
}
.gf-meter {
    height: 3px; background: var(--gf-track);
    margin: .9rem 0 0; max-width: 38rem;
}
.gf-meter div { height: 100%; background: var(--gf-teal); }
.gf-verdict {
    font-family: var(--gf-serif); font-size: 1.1rem; line-height: 1.65;
    max-width: 38rem; margin-top: .9rem;
}

/* Notes */
.gf-note {
    border-left: 3px solid var(--gf-ochre);
    padding: .15rem 0 .15rem .9rem; margin: .5rem 0;
    font-size: .92rem; line-height: 1.55; max-width: 40rem;
}
.gf-note-ok { border-left-color: var(--gf-teal); }

/* Gap span */
.gf-span { margin: 1.7rem 0 .3rem; }
.gf-span-legend {
    display: flex; flex-wrap: wrap; gap: .4rem 1.7rem;
    font-size: .88rem; margin-bottom: 1.1rem;
}
.gf-span-legend b {
    font-weight: 600; font-variant-numeric: tabular-nums; margin-left: .35rem;
}
.gf-dot {
    display: inline-block; width: .72rem; height: .72rem; border-radius: 50%;
    box-sizing: border-box; margin-right: .45rem; vertical-align: -1px;
}
.gf-dot-tech { background: var(--gf-teal); }
.gf-dot-supply { background: var(--gf-paper); border: 2px solid var(--gf-slate); }
.gf-span-plot { position: relative; height: 24px; margin: 0 10px; }
.gf-span-plot::before {
    content: ""; position: absolute; left: 0; right: 0; top: 50%;
    border-top: 1px solid rgba(31, 43, 46, .45);
}
.gf-span-gap {
    position: absolute; top: 6px; height: 12px;
    background: repeating-linear-gradient(135deg,
        rgba(169, 132, 60, .62) 0 3px, rgba(169, 132, 60, .2) 3px 6px);
}
.gf-span-gap.gf-span-surplus {
    background: repeating-linear-gradient(135deg,
        rgba(102, 119, 143, .45) 0 3px, rgba(102, 119, 143, .14) 3px 6px);
}
.gf-pt {
    position: absolute; top: 50%; width: 16px; height: 16px;
    border-radius: 50%; box-sizing: border-box;
    transform: translate(-50%, -50%);
    box-shadow: 0 0 0 3px var(--gf-paper);
}
.gf-pt-tech { background: var(--gf-teal); }
.gf-pt-supply { background: var(--gf-paper); border: 2.5px solid var(--gf-slate); }
.gf-span-scale {
    display: flex; justify-content: space-between; margin: .55rem 10px 0;
    font-size: .72rem; color: var(--gf-soft); font-variant-numeric: tabular-nums;
}
.gf-span-cap {
    font-size: .82rem; line-height: 1.55; color: var(--gf-soft);
    margin-top: .9rem; max-width: 36rem;
}

/* Figures */
.gf-figs {
    display: grid;
    grid-template-columns: repeat(var(--cols), minmax(0, 1fr));
    column-gap: 1.6rem; margin-top: 1.5rem;
}
.gf-fig { border-top: 1px solid var(--gf-rule); padding: .75rem 0 .3rem; }
.gf-fig-label { font-size: .8rem; color: var(--gf-soft); }
.gf-fig-value {
    font-size: 1.6rem; font-weight: 500; letter-spacing: -.02em;
    line-height: 1.3; font-variant-numeric: tabular-nums; margin-top: .1rem;
}
.gf-fig-value span {
    font-size: .82rem; font-weight: 400; color: var(--gf-soft); margin-left: .2rem;
}

/* Bars */
.gf-bars { display: flex; flex-direction: column; gap: .8rem; }
.gf-bar {
    display: grid; grid-template-columns: 150px minmax(0, 1fr) 44px;
    align-items: center; column-gap: 1rem;
}
.gf-bar-label { font-size: .9rem; }
.gf-bar-track { height: 6px; background: var(--gf-track); border-radius: 1px; overflow: hidden; }
.gf-bar-fill { height: 100%; }
.gf-bar-value {
    text-align: right; font-size: .9rem; color: var(--gf-soft);
    font-variant-numeric: tabular-nums;
}
.gf-cap { font-size: .82rem; line-height: 1.55; color: var(--gf-soft); margin-top: 1.1rem; }

/* Expanders */
.stApp [data-testid="stExpander"] { margin-top: 0; }
.stApp [data-testid="stExpander"] details {
    border: 0 !important;
    border-bottom: 1px solid var(--gf-rule) !important;
    border-radius: 0 !important;
    background: transparent !important;
}
.stApp [data-testid="stExpander"] summary { padding: .9rem 0; }
.stApp [data-testid="stExpander"] summary p {
    font-size: .95rem; font-weight: 500; color: var(--gf-ink);
}
.stApp [data-testid="stExpander"] summary:hover p { color: var(--gf-teal); }
.stApp [data-testid="stExpander"] summary:focus-visible {
    outline: 2px solid var(--gf-teal); outline-offset: 2px;
}
.stApp [data-testid="stExpander"] [data-testid="stExpanderDetails"] { padding: .2rem 0 1rem; }

/* Records inside expanders */
.gf-rec { padding: .85rem 0; border-bottom: 1px solid var(--gf-rule); }
.gf-rec:first-child { padding-top: .2rem; }
.gf-rec:last-child { border-bottom: 0; }
.gf-rec-title { font-weight: 500; font-size: .95rem; line-height: 1.4; }
.gf-rec-meta { font-size: .82rem; color: var(--gf-soft); margin-top: .25rem; }
.gf-rec-meta span + span {
    border-left: 1px solid var(--gf-rule); margin-left: .65rem; padding-left: .65rem;
}
.gf-rec-body {
    font-size: .87rem; line-height: 1.6; color: var(--gf-soft);
    margin-top: .35rem; max-width: 44rem;
}
.stApp a.gf-link {
    display: inline-block; margin-top: .45rem; font-size: .84rem;
    color: var(--gf-teal); text-decoration: underline;
    text-decoration-thickness: 1px; text-underline-offset: 3px;
}
.stApp a.gf-link:hover { color: var(--gf-teal-deep); }
.stApp a.gf-link:focus-visible { outline: 2px solid var(--gf-teal); outline-offset: 2px; }
.gf-empty { font-size: .88rem; color: var(--gf-soft); padding: .3rem 0; }

/* Search strategy */
.gf-q {
    display: grid; grid-template-columns: 110px minmax(0, 1fr); gap: 1rem;
    padding: .6rem 0; border-bottom: 1px solid var(--gf-rule); font-size: .88rem;
    align-items: baseline;
}
.gf-q:last-child { border-bottom: 0; }
.gf-q-engine { color: var(--gf-soft); }
.gf-q code { justify-self: start; word-break: break-word; }

@media (max-width: 720px) {
    .stApp .block-container,
    .stApp [data-testid="stMainBlockContainer"] { padding: 1.5rem 1.1rem 4rem; }
    .gf-figs { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .gf-bar { grid-template-columns: 105px minmax(0, 1fr) 38px; column-gap: .75rem; }
    .gf-class { font-size: 1.6rem; }
    .gf-q { grid-template-columns: 1fr; gap: .2rem; }
}
@media (prefers-reduced-motion: reduce) {
    .stApp * { transition: none !important; }
}
</style>
"""


# ==================================================================
# Rendering helpers (presentation only)
# ==================================================================

def md(markup, target=st):
    """Render an HTML snippet. Lines are flattened so Markdown never
    mistakes indented markup for a code block."""
    flat = " ".join(
        line.strip() for line in markup.splitlines() if line.strip()
    )
    target.markdown(flat, unsafe_allow_html=True)


def esc(value):
    """Escape text for HTML. `$` is encoded so Markdown does not try
    to read pairs of dollar signs as math."""
    return _html.escape(str(value), quote=True).replace("$", "&#36;")


def num(value):
    try:
        n = float(value)
    except (TypeError, ValueError):
        return 0.0
    return n if math.isfinite(n) else 0.0


def fmt(value):
    n = num(value)
    return str(int(n)) if n == int(n) else f"{n:.1f}"


def pct(value):
    return max(0.0, min(100.0, num(value)))


def show(value):
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return fmt(value)
    return esc(value)


def figure(label, value, suffix=""):
    unit = f"<span>{esc(suffix)}</span>" if suffix else ""
    return (
        '<div class="gf-fig">'
        f'<div class="gf-fig-label">{esc(label)}</div>'
        f'<div class="gf-fig-value">{show(value)}{unit}</div>'
        "</div>"
    )


def figures(items, columns):
    cells = "".join(figure(*item) for item in items)
    return f'<div class="gf-figs" style="--cols:{columns}">{cells}</div>'


def bars(rows, maximum=100, color="var(--gf-teal)"):
    top = maximum if maximum else 1
    lines = []
    for label, value in rows:
        width = max(0.0, min(100.0, num(value) / top * 100))
        lines.append(
            '<div class="gf-bar">'
            f'<div class="gf-bar-label">{esc(label)}</div>'
            '<div class="gf-bar-track">'
            f'<div class="gf-bar-fill" style="width:{width:.1f}%;'
            f'background:{color}"></div></div>'
            f'<div class="gf-bar-value">{fmt(value)}</div>'
            "</div>"
        )
    return '<div class="gf-bars">' + "".join(lines) + "</div>"


def note(text, tone="warn"):
    return f'<div class="gf-note gf-note-{tone}">{esc(text)}</div>'


def gap_span(tech, supply):
    """One track from 0 to 100: where the technology sits, where the
    commercial supply sits, and the distance between them."""
    t, s = pct(tech), pct(supply)
    lo, hi = min(t, s), max(t, s)
    span_class = "gf-span-gap" if t >= s else "gf-span-gap gf-span-surplus"
    scale = "".join(f"<span>{n}</span>" for n in (0, 25, 50, 75, 100))
    return (
        '<div class="gf-span">'
        '<div class="gf-span-legend">'
        '<div><i class="gf-dot gf-dot-tech"></i>Technology strength'
        f"<b>{fmt(tech)}</b></div>"
        '<div><i class="gf-dot gf-dot-supply"></i>Commercial supply'
        f"<b>{fmt(supply)}</b></div>"
        "</div>"
        '<div class="gf-span-plot">'
        f'<div class="{span_class}" style="left:{lo:.1f}%;'
        f'width:{hi - lo:.1f}%"></div>'
        f'<div class="gf-pt gf-pt-supply" style="left:{s:.1f}%"></div>'
        f'<div class="gf-pt gf-pt-tech" style="left:{t:.1f}%"></div>'
        "</div>"
        f'<div class="gf-span-scale">{scale}</div>'
        '<div class="gf-span-cap">The shaded stretch is the distance between '
        "what the technology can do and what is already for sale.</div>"
        "</div>"
    )


def record(title, body=None, meta=None, link=None, link_text="Open"):
    parts = [f'<div class="gf-rec"><div class="gf-rec-title">{esc(title)}</div>']
    if meta:
        cells = "".join(f"<span>{esc(m)}</span>" for m in meta if m)
        if cells:
            parts.append(f'<div class="gf-rec-meta">{cells}</div>')
    if body:
        parts.append(f'<div class="gf-rec-body">{esc(body)}</div>')
    if link and str(link).startswith(("http://", "https://")):
        parts.append(
            f'<a class="gf-link" href="{esc(link)}" target="_blank" '
            f'rel="noopener noreferrer">{esc(link_text)}</a>'
        )
    parts.append("</div>")
    return "".join(parts)


def records(items):
    if not items:
        return '<div class="gf-empty">No records returned for this source.</div>'
    return "".join(items)


def section(title, description=None):
    """Margin-note layout: title on the left, content on the right.
    Returns the right-hand column to be used as a context manager."""
    md('<div class="gf-rule"></div>')
    left, right = st.columns([1, 3], gap="large")
    with left:
        text = f'<div class="gf-sec-title">{esc(title)}</div>'
        if description:
            text += f'<div class="gf-sec-note">{esc(description)}</div>'
        md(text)
    return right


md(CSS)


# ==================================================================
# Header
# ==================================================================

md(
    """
    <div class="gf-head">
      <div class="gf-brand">
        <div class="gf-logo" aria-hidden="true"><i></i><i></i></div>
        <div class="gf-wordmark" role="heading" aria-level="1">GapFinder</div>
      </div>
      <div class="gf-tag">Discover commercialization gaps in emerging technology</div>
      <div class="gf-lede">
        GapFinder connects research, patents, market supply,
        public demand, industry activity, and hiring signals
        to identify potential commercialization opportunities.
      </div>
    </div>
    """
)


# ==================================================================
# Sidebar
# ==================================================================

searches_used = client.searches_used()
searches_remaining = client.searches_remaining()

budget_total = num(searches_used) + num(searches_remaining)
budget_share = (
    num(searches_used) / budget_total * 100 if budget_total else 0
)

md(
    f"""
    <div class="gf-side-title">Search budget</div>
    <div class="gf-side-row">Tracked searches used<b>{show(searches_used)}</b></div>
    <div class="gf-side-meter"><div style="width:{pct(budget_share):.1f}%"></div></div>
    <div class="gf-side-row">Tracked searches remaining<b>{show(searches_remaining)}</b></div>
    <div class="gf-side-note">Cached searches do not consume new API requests.</div>
    """,
    st.sidebar,
)


# ==================================================================
# Input
# ==================================================================

query = st.text_input(
    "Technology or research idea",
    placeholder="e.g. graphene water purification for rural communities",
)

analyze = st.button(
    "Analyze Opportunity",
    type="primary",
)


if analyze:

    if not query.strip():
        md(note("Please enter a technology or research idea."))
        st.stop()

    else:

        with st.spinner("Investigating the opportunity..."):

            evidence = collect_evidence(query)

            failed_sources = []

            if evidence["research"]["papers_found"] == 0:
                failed_sources.append("Research")

            if evidence["patents"]["patents_found"] == 0:
                failed_sources.append("Patents")

            if evidence["market"]["products_found"] == 0:
                failed_sources.append("Commercial Supply")

            if evidence["industry"]["articles_found"] == 0:
                failed_sources.append("Industry")

            if evidence["jobs"]["jobs_found"] == 0:
                failed_sources.append("Hiring")

            signals = calculate_signals(evidence)

            confidence = calculate_confidence(evidence)

            trend_momentum = calculate_trend_momentum(
                evidence["demand"]
            )

            gap = detect_gap(
                signals,
                trend_momentum,
            )

            opportunity_score = calculate_opportunity_score(
                signals,
                gap,
            )

            opportunity = classify_opportunity(
                opportunity_score,
            )

            report = build_report(
                query,
                evidence,
                signals,
                gap,
                confidence,
            )

        if failed_sources:
            md(
                note(
                    "Limited evidence returned for: "
                    + ", ".join(failed_sources)
                    + ". Scores may be less reliable."
                )
            )

        # ----------------------------------------------
        # Opportunity
        # ----------------------------------------------

        if gap["gap_score"] >= 70:
            verdict = (
                "Strong opportunity: the evidence indicates a meaningful mismatch "
                "between technology or market interest and current commercial supply."
            )
        elif gap["gap_score"] >= 50:
            verdict = (
                "Promising opportunity: several signals support commercialization, "
                "but the market gap is not yet strongly established."
            )
        elif gap["gap_score"] >= 30:
            verdict = (
                "Early opportunity: some supporting evidence exists, but stronger "
                "demand, adoption, or supply-gap evidence is needed."
            )
        else:
            verdict = (
                "Limited opportunity: current evidence does not indicate a strong "
                "commercialization gap."
            )

        with section(
            "Opportunity assessment",
            "Where the technology stands against what the market already offers.",
        ):
            md(
                f'<div class="gf-class">{esc(opportunity)}</div>'
                '<div class="gf-meter" role="img" '
                f'aria-label="Opportunity score {fmt(opportunity_score)} of 100">'
                f'<div style="width:{pct(opportunity_score):.1f}%"></div></div>'
                f'<div class="gf-verdict">{esc(verdict)}</div>'
            )

            if gap["emerging_gap_bonus"] > 0:
                md(
                    note(
                        "Emerging-market signal: demand is rising while commercial "
                        "supply remains relatively limited.",
                        "ok",
                    )
                )

            md(
                gap_span(gap["technology_strength"], gap["supply_strength"])
                + figures(
                    [
                        ("Opportunity score", opportunity_score, "/100"),
                        ("Commercialization gap", gap["gap_score"], "/100"),
                        ("Technology strength", gap["technology_strength"], "/100"),
                        ("Evidence confidence", confidence, "/100"),
                    ],
                    4,
                )
                + figures(
                    [
                        ("Demand", signals["demand"], "/100"),
                        ("Commercial supply", signals["market"], "/100"),
                        ("Signal convergence", gap["convergence"], "/100"),
                    ],
                    3,
                )
            )


        # ----------------------------------------------
        # Signals
        # ----------------------------------------------

        with section("Market signals", "Each signal is scored from 0 to 100."):
            md(
                bars(
                    [
                        ("Research", signals["research"]),
                        ("Patents", signals["patents"]),
                        ("Market supply", signals["market"]),
                        ("Demand", signals["demand"]),
                        ("Industry", signals["industry"]),
                        ("Hiring", signals["jobs"]),
                    ]
                )
            )


        # ----------------------------------------------
        # Findings
        # ----------------------------------------------

        with section("Key findings"):
            st.markdown(
                "\n".join(f"- {finding}" for finding in report["findings"])
            )


        # ----------------------------------------------
        # Evidence Quality
        # ----------------------------------------------

        quality_rows = [
            ("Research", evidence["research"]["papers_found"]),
            ("Patents", evidence["patents"]["patents_found"]),
            ("Commercial supply", evidence["market"]["products_found"]),
            ("Industry", evidence["industry"]["articles_found"]),
            ("Hiring", evidence["jobs"]["jobs_found"]),
        ]

        with section(
            "Evidence quality",
            "How many records each source returned.",
        ):
            md(
                bars(
                    quality_rows,
                    maximum=max([1] + [num(v) for _, v in quality_rows]),
                    color="var(--gf-slate)",
                )
                + '<div class="gf-cap">Evidence quality reflects the amount of '
                "independently retrieved evidence, not statistical certainty.</div>"
            )


        # ----------------------------------------------
        # Conclusion
        # ----------------------------------------------

        with section(
            "Commercialization assessment",
            "How the signals combine into a conclusion.",
        ):
            md(
                figures(
                    [
                        ("Signal convergence", gap["convergence"], "/100"),
                        ("Strong independent signals", gap["strong_signals"], "/5"),
                        ("Trend momentum", gap["trend_momentum"], "/100"),
                        ("Emerging gap bonus", gap["emerging_gap_bonus"], "/15"),
                    ],
                    4,
                )
            )

            st.write(report["conclusion"])


        # ----------------------------------------------
        # Methodology + Search Strategy
        # ----------------------------------------------

        with section("Method"):

            with st.expander(
                "How GapFinder calculates the opportunity"
            ):
                st.write(
                    "GapFinder combines research maturity, patent activity, "
                    "public demand, industry activity, hiring activity, "
                    "and commercial supply."
                )

                st.write(
                    "The core opportunity comes from the mismatch between "
                    "technology strength and commercial supply."
                )

                st.write(
                    "Signal convergence increases confidence when several "
                    "independent signals support the same conclusion."
                )

                st.write(
                    "A rising-demand and low-supply combination receives "
                    "an additional emerging-gap bonus."
                )

            with st.expander("View search strategy"):

                st.write(
                    "GapFinder generated these queries:"
                )

                md(
                    "".join(
                        '<div class="gf-q">'
                        f'<div class="gf-q-engine">{esc(engine.capitalize())}</div>'
                        f"<code>{esc(search_query)}</code>"
                        "</div>"
                        for engine, search_query in evidence["queries"].items()
                    )
                )


        # ----------------------------------------------
        # Evidence
        # ----------------------------------------------

        evidence_labels = {
            "research_papers": "Research papers",
            "patents": "Patents",
            "products": "Products",
            "trend": "Demand trend",
            "news_articles": "News articles",
            "companies_hiring": "Companies hiring",
        }

        with section(
            "Evidence",
            "The records behind the scores. Up to five are listed per source.",
        ):
            md(
                figures(
                    [
                        (label, report["evidence"][name])
                        for name, label in evidence_labels.items()
                    ],
                    3,
                )
            )

            md('<div style="height:1.4rem"></div>')

            # Research
            with st.expander(
                f"Research evidence ({evidence['research']['papers_found']} papers)"
            ):
                md(
                    records(
                        [
                            record(
                                paper.get("title") or "Untitled paper",
                                body=(paper.get("snippet") or "")[:300],
                                link=paper.get("link"),
                                link_text="View paper",
                            )
                            for paper in evidence["research"]["papers"][:5]
                        ]
                    )
                )

            # Patents
            with st.expander(
                f"Patent evidence ({evidence['patents']['patents_found']} patents)"
            ):
                md(
                    records(
                        [
                            record(
                                patent.get("title") or "Untitled patent",
                                body=(patent.get("snippet") or "")[:300],
                                link=patent.get("link"),
                                link_text="View patent",
                            )
                            for patent in evidence["patents"]["patents"][:5]
                        ]
                    )
                )

            # Commercial Supply
            with st.expander(
                f"Commercial supply ({evidence['market']['products_found']} products)"
            ):
                md(
                    records(
                        [
                            record(
                                product.get("title") or "Unnamed product",
                                meta=[
                                    product.get("price") or "Price unavailable",
                                    product.get("source") or "Unknown seller",
                                ],
                            )
                            for product in evidence["market"]["products"][:5]
                        ]
                    )
                )

            # Industry Activity
            with st.expander(
                f"Industry activity ({evidence['industry']['articles_found']} articles)"
            ):
                md(
                    records(
                        [
                            record(
                                article.get("title") or "Untitled article",
                                meta=[article.get("source")],
                                link=article.get("link"),
                                link_text="Read article",
                            )
                            for article in evidence["industry"]["articles"][:5]
                        ]
                    )
                )

            # Hiring Activity
            with st.expander(
                f"Hiring activity ({evidence['jobs']['jobs_found']} jobs)"
            ):
                md(
                    records(
                        [
                            record(
                                job.get("title") or "Untitled job",
                                meta=[
                                    job.get("company_name") or "Unknown company",
                                    job.get("location"),
                                ],
                            )
                            for job in evidence["jobs"]["jobs"][:5]
                        ]
                    )
                )