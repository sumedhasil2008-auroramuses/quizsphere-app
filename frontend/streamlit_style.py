"""
Look and feel for the Streamlit version of QuizSphere (used by streamlit_app.py).

Streamlit draws its pages in the browser, so the styling here is a block of
CSS (colours, sizes) plus small SVG drawings (flowers, score ring, badges).
All of it is built and sent from Python.
"""

import html
import math
import random

GOLD = "#fbbf24"
TOPIC_COLORS = {"math": "#fbbf24", "gk": "#34d399", "web": "#22d3ee", "mix": "#93b4ff"}
PETALS = ["#f472b6", "#c084fc", "#fbbf24", "#fda4af", "#f9fafb", "#fb7185"]

CREDIT = "Front-end developer: <b>Sumedha Sil</b> · SRM KTR · CSE Core · RA2611003011378"


def esc(text):
    """Make text safe to put inside HTML (so a quiz title can't break the page)."""
    return html.escape(str(text))


# ------------------------------------------------------------------ page CSS

CSS = """
<style>
:root { --gold:#fbbf24; --gold-dark:#b45309; --card:#1d1712; --border:#3a3029; --soft:#c7d2fe; --muted:#a8a29e; }
.stApp { background:#0b0907; color:#fff; }
[data-testid="stHeader"] { background:transparent; }
[data-testid="stToolbar"], [data-testid="stDecoration"] { display:none; }
.block-container { max-width:1040px; padding-top:1.2rem; padding-bottom:1rem; position:relative; z-index:2; }
h1, h2, h3, h4, p, label, li, span { color:#fff; }
h1 { font-weight:800 !important; letter-spacing:-.02em; }
[data-testid="stMarkdownContainer"] p { color:#e7e5e4; }
[data-testid="stWidgetLabel"] p { color:#fff !important; font-weight:600; }
[data-testid="stCaptionContainer"] p, .qs-muted { color:var(--muted) !important; }

/* buttons */
[data-testid^="stBaseButton-primary"] { background:var(--gold) !important; color:#0b0907 !important; border:0 !important;
  font-weight:700 !important; box-shadow:0 4px 0 var(--gold-dark); border-radius:12px !important; }
[data-testid^="stBaseButton-primary"] p { color:#0b0907 !important; }
[data-testid^="stBaseButton-primary"]:hover { filter:brightness(1.08); }
[data-testid^="stBaseButton-secondary"] { background:rgba(255,255,255,.06) !important; color:#fff !important;
  border:1px solid rgba(255,255,255,.18) !important; border-radius:12px !important; }
[data-testid^="stBaseButton-secondary"]:hover { border-color:var(--gold) !important; }
[data-testid="stBaseButton-tertiary"] p { color:var(--soft) !important; }
[data-testid="stBaseButton-tertiary"]:hover p { color:var(--gold) !important; }

/* text boxes, selects, radios */
[data-baseweb="input"], [data-baseweb="base-input"], [data-baseweb="select"] > div, [data-baseweb="textarea"],
[data-testid="stTextInputRootElement"], [data-testid="stNumberInputContainer"], [data-testid="stNumberInputField"],
[data-testid="stSelectbox"] [data-baseweb="select"] > div, [data-testid="stTextInputRootElement"] > div {
  background:#14100c !important; border-color:var(--border) !important; color:#fff !important; }
[data-testid="stTextInputRootElement"]:focus-within { border-color:var(--gold) !important; }
[data-testid="stSelectbox"] div, [data-testid="stNumberInput"] button { color:#fff !important; }
[data-testid="stNumberInput"] button { background:#2a211a !important; border-color:var(--border) !important; }
input, textarea { color:#fff !important; -webkit-text-fill-color:#fff !important; }
input::placeholder, textarea::placeholder { color:#78716c !important; -webkit-text-fill-color:#78716c !important; }
[data-testid="stRadio"] label p { color:#fff !important; font-size:1.02rem; }
/* answer choices: one box per option, gold when chosen */
[data-testid="stElementContainer"]:has([data-testid="stRadioGroup"][aria-orientation="vertical"]),
[data-testid="stRadio"]:has([aria-orientation="vertical"]), [data-testid="stRadioGroup"][aria-orientation="vertical"],
[data-testid="stRadioGroup"][aria-orientation="vertical"] > div { width:100% !important; align-items:stretch !important; }
[data-testid="stRadioGroup"][aria-orientation="vertical"] [data-testid="stRadioOption"] { display:flex; background:#14100c;
  border:1px solid var(--border); border-radius:12px; padding:.75rem 1rem; margin-bottom:.5rem; width:100%; cursor:pointer; }
[data-testid="stRadioGroup"][aria-orientation="vertical"] [data-testid="stRadioOption"]:hover { border-color:#78716c; }
[data-testid="stRadioGroup"] [data-testid="stRadioOption"]:has(input:checked) { border-color:var(--gold); background:#2a211a; }

/* bordered containers = "glass" cards */
.st-key-card, [class*="st-key-card"] { background:var(--card); border:1px solid var(--border) !important;
  border-radius:18px; padding:1.1rem 1.2rem; }
[data-testid="stMetric"] { background:var(--card); border:1px solid var(--border); border-radius:18px; padding:1rem 1.2rem; }
[data-testid="stMetricValue"] { color:var(--gold) !important; font-weight:800; }
[data-testid="stMetricLabel"] p { color:var(--muted) !important; }
[data-testid="stProgressBarTrack"] { background:#3a3029 !important; }
[data-testid="stProgressBarTrack"] > div { background:var(--gold) !important; }
[data-testid="stHeaderActionElements"] { display:none !important; }
/* subject / number pickers (segmented controls) */
[data-testid="stButtonGroup"] button { background:#14100c !important; border-color:var(--border) !important; }
[data-testid="stButtonGroup"] button p { color:var(--soft) !important; }
[data-testid="stButtonGroup"] button[aria-checked="true"] { background:var(--gold) !important; border-color:var(--gold) !important; }
[data-testid="stButtonGroup"] button[aria-checked="true"] p { color:#0b0907 !important; font-weight:700; }
/* question number buttons: small and tight so the numbers fit */
.st-key-card_palette [data-testid^="stBaseButton"] { padding:.25rem 0 !important; min-height:2.3rem; min-width:0 !important; }
.st-key-card_palette [data-testid="stHorizontalBlock"] { gap:.35rem !important; }
.st-key-card_palette [data-testid="stColumn"] { min-width:0 !important; }
[data-testid="stAlert"] { border-radius:12px; }
hr { border-color:var(--border) !important; }

/* small pieces of the design */
.qs-eyebrow { color:var(--gold); font-size:.78rem; font-weight:800; letter-spacing:.14em; text-transform:uppercase; margin:0; }
.qs-pill { display:inline-block; padding:.18rem .7rem; border-radius:999px; font-size:.78rem; font-weight:700;
  border:1px solid currentColor; margin-right:.35rem; }
.qs-hero h1 { font-size:3.2rem; line-height:1.08; margin:.4rem 0 1rem; }
.qs-hero .accent { color:var(--gold); }
.qs-lead { color:var(--soft) !important; font-size:1.12rem; }
.qs-logo { display:flex; align-items:center; gap:.55rem; font-weight:800; font-size:1.35rem; color:#fff; padding-top:.35rem; }
.qs-card { background:var(--card); border:1px solid var(--border); border-radius:18px; padding:1.1rem 1.25rem; margin-bottom:.7rem; }
.qs-card h3 { margin:.45rem 0 .25rem; font-size:1.15rem; }
.qs-card p { color:var(--soft) !important; margin:0; }
.qs-num { display:inline-block; background:#2a2016; color:var(--gold); font-weight:800; padding:.2rem .6rem; border-radius:8px; }
.qs-row { display:flex; justify-content:space-between; align-items:center; gap:1rem; }
.qs-score { font-size:1.7rem; font-weight:800; color:var(--gold); }
.qs-pass { color:#34d399; font-weight:800; font-size:.85rem; }
.qs-fail { color:#f87171; font-weight:800; font-size:.85rem; }
.qs-wrong { border-color:#f87171 !important; }

/* score ring */
.qs-ring circle.fill { stroke-dasharray:327; animation:qs-ring 1.4s ease-out forwards; }
@keyframes qs-ring { from { stroke-dashoffset:327; } }

/* trophy */
.qs-trophy { animation:qs-turn 3s ease-in-out infinite; transform-origin:center; display:inline-block; }
@keyframes qs-turn { 0%,100% { transform:rotateY(0deg); } 50% { transform:rotateY(180deg); } }

/* badge coins: hover to flip */
.qs-badges { display:grid; grid-template-columns:repeat(6,1fr); gap:.6rem; margin:.6rem 0 0; }
.qs-coin { perspective:600px; height:132px; }
.qs-coin .in { position:relative; width:100%; height:100%; transition:transform .6s; transform-style:preserve-3d; }
.qs-coin:hover .in { transform:rotateY(180deg); }
.qs-coin .face { position:absolute; inset:0; margin:auto; width:126px; height:126px; border-radius:50%;
  backface-visibility:hidden; display:flex; flex-direction:column; align-items:center; justify-content:center;
  text-align:center; padding:.6rem; border:3px solid #4a4036; background:#1a1612; }
.qs-coin .back { transform:rotateY(180deg); font-size:.78rem; color:var(--soft); }
.qs-coin.on .face { border-color:var(--gold); background:#3b2a10; }
.qs-coin.new .face { box-shadow:0 0 0 3px #22d3ee, 0 0 24px rgba(34,211,238,.45); }
.qs-coin.new .in { animation:qs-spin 1.6s ease-out 1; }
@keyframes qs-spin { from { transform:rotateY(720deg); } }
.qs-coin .icon { font-size:1.45rem; font-weight:800; color:#a8a29e; }
.qs-coin.on .icon { color:var(--gold); }
.qs-coin .name { font-size:.82rem; font-weight:700; }
.qs-coin .state { font-size:.72rem; font-weight:700; color:#a8a29e; }
.qs-coin.on .state { color:var(--gold); }
.qs-coin.new .state { color:#22d3ee; }

/* leaderboard */
.qs-podium { display:flex; justify-content:center; align-items:flex-end; gap:1rem; margin:1rem 0 1.5rem; }
.qs-spot { text-align:center; width:200px; }
.qs-avatar { width:64px; height:64px; border-radius:50%; margin:0 auto .4rem; display:flex; align-items:center;
  justify-content:center; font-weight:800; color:#0b0907; font-size:1.2rem; }
.qs-block { border:1px solid var(--border); background:var(--card); border-radius:14px 14px 0 0; display:flex;
  align-items:center; justify-content:center; font-size:2.2rem; font-weight:800; margin-top:.5rem; }
.qs-meter { height:6px; background:#3a3029; border-radius:6px; overflow:hidden; margin-top:.4rem; }
.qs-meter span { display:block; height:100%; background:var(--gold); }
.qs-me { border:2px solid var(--gold) !important; }
.qs-tag { font-size:.7rem; font-weight:700; padding:.05rem .45rem; border-radius:999px; margin-left:.35rem;
  border:1px solid #a8a29e; color:#a8a29e; }
.qs-tag.you { border-color:var(--gold); color:var(--gold); }

/* table */
.qs-table { width:100%; border-collapse:collapse; background:var(--card); border:1px solid var(--border); border-radius:14px; overflow:hidden; }
.qs-table th { background:#1c140d; color:var(--gold); text-align:left; font-size:.75rem; letter-spacing:.08em;
  text-transform:uppercase; padding:.7rem .9rem; }
.qs-table td { padding:.65rem .9rem; border-top:1px solid var(--border); color:#fff; }
.qs-table tr:hover td { background:#2a211a; }

/* password strength */
.qs-strength { display:flex; gap:6px; margin:.3rem 0 .2rem; }
.qs-strength span { flex:1; height:7px; border-radius:4px; background:#3a3029; }

/* footer credit */
.qs-footer { text-align:center; border-top:1px solid var(--border); margin-top:2.5rem; padding:1rem 0 .4rem; }
.qs-footer .credit { color:var(--gold) !important; font-weight:600; margin:0; }
.qs-footer .copy { color:var(--muted) !important; font-size:.85rem; margin:.2rem 0 0; }

/* flower border: fixed on the left and right of the window */
.qs-side { position:fixed; top:0; bottom:0; width:calc((100vw - 1040px) / 2); overflow:hidden; pointer-events:none; z-index:0; }
.qs-side.left { left:0; } .qs-side.right { right:0; }
.qs-vine { position:absolute; top:0; height:100%; width:30px; }
.qs-side.left .qs-vine { right:6px; } .qs-side.right .qs-vine { left:6px; }
.qs-float { position:absolute; bottom:-60px; animation-name:qs-up; animation-timing-function:linear; animation-iteration-count:infinite; }
.qs-float svg, .qs-vine-flower svg { animation:qs-twirl 14s linear infinite; }
.qs-vine-flower { position:absolute; }
@keyframes qs-up { from { transform:translateY(0) translateX(0); } 50% { transform:translateY(-55vh) translateX(10px); }
                   to { transform:translateY(-115vh) translateX(0); } }
@keyframes qs-twirl { to { transform:rotate(360deg); } }
@media (max-width:1180px) { .qs-side { display:none; } }
@media (max-width:760px) { .qs-badges { grid-template-columns:repeat(3,1fr); } .qs-hero h1 { font-size:2.3rem; } }
</style>
"""


# ------------------------------------------------------------------ drawings

def flower_svg(size=30, colour="#f472b6", petals=6, centre=GOLD):
    """A flower drawn with rounded petals around a centre."""
    c = size / 2
    parts = []
    for i in range(petals):
        angle = 360 * i / petals
        parts.append(f'<ellipse cx="{c}" cy="{c - size * 0.24}" rx="{size * 0.15}" ry="{size * 0.25}" '
                     f'fill="{colour}" fill-opacity=".88" stroke="{colour}" transform="rotate({angle} {c} {c})"/>')
    parts.append(f'<circle cx="{c}" cy="{c}" r="{size * 0.15}" fill="{centre}"/>')
    return f'<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}">{"".join(parts)}</svg>'


def flower_border():
    """HTML for the flower vines and floating flowers on both sides of the page."""
    rnd = random.Random(7)   # same pattern every time the page reloads
    sides = []
    for side in ("left", "right"):
        vine_flowers, floaters = [], []
        for i in range(12):
            colour = PETALS[(i + (3 if side == "right" else 0)) % len(PETALS)]
            vine_flowers.append(f'<div class="qs-vine-flower" style="top:{i * 9 + 2}vh;{"right" if side == "left" else "left"}:-2px">'
                                f'{flower_svg(rnd.randint(22, 30), colour, rnd.choice((5, 6, 8)))}</div>')
        for lane in range(3):                     # 3 lanes, 2 flowers each, evenly spaced: never overlap
            for k in range(2):
                duration = 26 + lane * 5
                edge = "left" if side == "left" else "right"     # lanes start from the window edge, away from the vine
                floaters.append(
                    f'<div class="qs-float" style="{edge}:{8 + lane * 26}%;animation-duration:{duration}s;'
                    f'animation-delay:-{k * duration / 2 + lane * 3}s;opacity:{0.55 + 0.15 * (lane % 2)}">'
                    f'{flower_svg(rnd.randint(20, 32), rnd.choice(PETALS), rnd.choice((5, 6, 8)))}</div>')
        stem_x = 15
        path = " ".join(f"{'M' if y == 0 else 'L'} {stem_x + 6 * math.sin(y / 40):.1f} {y}" for y in range(0, 2001, 20))
        vine = (f'<svg class="qs-vine" viewBox="0 0 30 2000" preserveAspectRatio="none">'
                f'<path d="{path}" stroke="#1f6f4d" stroke-width="2" fill="none"/></svg>')
        sides.append(f'<div class="qs-side {side}">{"".join(floaters)}<div class="qs-vine" style="height:100%">'
                     f'{vine}{"".join(vine_flowers)}</div></div>')
    return "".join(sides)


def big_flower(size=320):
    """The large turning flower on the Home page (three rings of petals around a "?")."""
    c = size / 2
    rings = [(12, 0.46, "#3b2a10", "#fbbf24", 60), (10, 0.34, "#4a1d34", "#f472b6", -45), (8, 0.23, "#2e1f47", "#c084fc", 35)]
    out = [f'<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" style="max-width:100%">',
           f'<circle cx="{c}" cy="{c}" r="{c - 6}" fill="#16110b"/>']
    for n, length, fill, edge, seconds in rings:
        L = size * length
        petals = "".join(
            f'<path d="M {c} {c} Q {c + L * 0.45} {c - L * 0.2} {c + L} {c} Q {c + L * 0.45} {c + L * 0.2} {c} {c} Z" '
            f'fill="{fill}" stroke="{edge}" stroke-width="2" transform="rotate({360 * i / n} {c} {c})"/>' for i in range(n))
        direction = "" if seconds > 0 else "reverse"
        out.append(f'<g style="transform-origin:{c}px {c}px;animation:qs-twirl {abs(seconds)}s linear infinite {direction}">'
                   f'{petals}</g>')
    out.append(f'<circle cx="{c}" cy="{c}" r="{size * 0.1}" fill="#fbbf24" stroke="#fde68a" stroke-width="3"/>')
    out.append(f'<text x="{c}" y="{c + size * 0.045}" text-anchor="middle" font-size="{size * 0.12}" '
               f'font-weight="800" fill="#0b0907" font-family="sans-serif">?</text></svg>')
    return "".join(out)


def score_ring(percent, passed):
    colour = GOLD if passed else "#f87171"
    offset = 327 * (1 - percent / 100)
    return (f'<svg class="qs-ring" width="150" height="150" viewBox="0 0 120 120">'
            f'<circle cx="60" cy="60" r="52" fill="none" stroke="#3a3029" stroke-width="12"/>'
            f'<circle class="fill" cx="60" cy="60" r="52" fill="none" stroke="{colour}" stroke-width="12" '
            f'stroke-linecap="round" transform="rotate(-90 60 60)" style="stroke-dashoffset:{offset}"/>'
            f'<text x="60" y="68" text-anchor="middle" font-size="24" font-weight="800" fill="#fff" '
            f'font-family="sans-serif">{percent}%</text></svg>')


TROPHY = ('<span class="qs-trophy"><svg width="120" height="150" viewBox="0 0 100 140">'
          '<path d="M20 8 H80 C80 44 68 62 50 66 C32 62 20 44 20 8 Z" fill="#fbbf24" stroke="#b45309" stroke-width="3"/>'
          '<path d="M20 16 C4 16 6 44 26 46" fill="none" stroke="#fbbf24" stroke-width="6"/>'
          '<path d="M80 16 C96 16 94 44 74 46" fill="none" stroke="#fbbf24" stroke-width="6"/>'
          '<rect x="45" y="64" width="10" height="28" fill="#f59e0b"/><path d="M36 92 H64 L60 104 H40 Z" fill="#f59e0b"/>'
          '<rect x="26" y="104" width="48" height="16" rx="3" fill="#b45309"/>'
          '<text x="50" y="40" text-anchor="middle" font-size="22" fill="#0b0907">★</text></svg></span>')


def badge_coins(badges, unlocked, fresh=()):
    coins = []
    for b in badges:
        on = b["id"] in unlocked
        new = b["id"] in fresh
        state = "New!" if new else ("Unlocked" if on else "Locked")
        cls = "qs-coin" + (" on" if on else "") + (" new" if new else "")
        coins.append(f'<div class="{cls}"><div class="in">'
                     f'<div class="face"><div class="icon">{esc(b["icon"])}</div><div class="name">{esc(b["name"])}</div>'
                     f'<div class="state">{state}</div></div>'
                     f'<div class="face back"><div class="name">{esc(b["name"])}</div>{esc(b["desc"])}</div>'
                     f'</div></div>')
    return f'<div class="qs-badges">{"".join(coins)}</div>'


def pill(text, colour):
    return f'<span class="qs-pill" style="color:{colour}">{esc(text)}</span>'
