import streamlit as st
import pandas as pd
import datetime
import json
import os
import math

st.set_page_config(
    page_title="Life OS v2 — Founder Edition",
    layout="wide",
    page_icon="⚡",
    initial_sidebar_state="collapsed",
)

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=JetBrains+Mono:wght@300;400;500;700&family=Fraunces:ital,opsz,wght@0,9..144,300;1,9..144,300&display=swap');

/* ── RESET & BASE ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"], .stApp {
    font-family: 'Syne', sans-serif;
    background-color: #0a0d14 !important;
    color: #e8e4d9 !important;
}

/* Subtle grain overlay on whole page */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.04'/%3E%3C/svg%3E");
    pointer-events: none;
    z-index: 9999;
    opacity: 0.4;
}

.main .block-container {
    padding: 0 2.5rem 4rem;
    max-width: 1440px;
    background: transparent !important;
}

#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ── HERO BAND ── */
.hero-band {
    background: linear-gradient(135deg, #0f1420 0%, #141928 50%, #0f1420 100%);
    border-bottom: 1px solid rgba(212, 175, 55, 0.15);
    padding: 2.5rem 0 2rem;
    margin: 0 -2.5rem 2.5rem;
    padding-left: 2.5rem;
    padding-right: 2.5rem;
    position: relative;
    overflow: hidden;
}
.hero-band::before {
    content: '';
    position: absolute;
    top: 0; right: 0;
    width: 400px; height: 100%;
    background: radial-gradient(ellipse at right center, rgba(212,175,55,0.06) 0%, transparent 70%);
    pointer-events: none;
}
.hero-band::after {
    content: 'LIFE OS';
    position: absolute;
    right: 2rem;
    top: 50%;
    transform: translateY(-50%);
    font-family: 'Syne', sans-serif;
    font-size: 8rem;
    font-weight: 800;
    color: rgba(212,175,55,0.04);
    letter-spacing: -0.02em;
    line-height: 1;
    pointer-events: none;
    user-select: none;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.8rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    color: #e8e4d9;
    line-height: 1;
}
.hero-title span { color: #d4af37; }
.hero-sub {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    color: rgba(232,228,217,0.35);
    margin-top: 0.6rem;
}
.hero-meta {
    display: flex;
    gap: 2rem;
    margin-top: 1.4rem;
}
.hero-meta-item {
    display: flex;
    flex-direction: column;
}
.hero-meta-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.55rem;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: rgba(232,228,217,0.3);
    margin-bottom: 0.2rem;
}
.hero-meta-value {
    font-family: 'Syne', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    color: #d4af37;
}
.status-dot {
    display: inline-block;
    width: 7px; height: 7px;
    background: #4ade80;
    border-radius: 50%;
    margin-right: 0.4rem;
    animation: blink 2s ease infinite;
    box-shadow: 0 0 6px #4ade80;
}
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.25} }

/* ── SECTION HEADER ── */
.sec-head {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    margin-bottom: 1.2rem;
    padding-bottom: 0.8rem;
    border-bottom: 1px solid rgba(212,175,55,0.12);
}
.sec-icon {
    width: 32px; height: 32px;
    border-radius: 8px;
    background: rgba(212,175,55,0.1);
    border: 1px solid rgba(212,175,55,0.2);
    display: flex; align-items: center; justify-content: center;
    font-size: 0.9rem;
}
.sec-title {
    font-family: 'Syne', sans-serif;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: rgba(232,228,217,0.55);
}
.sec-title span { color: #d4af37; margin-right: 0.3rem; }

/* ── GLASS CARD ── */
.glass-card {
    background: linear-gradient(135deg, rgba(255,255,255,0.03) 0%, rgba(255,255,255,0.01) 100%);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 1.5rem;
    position: relative;
    overflow: hidden;
    margin-bottom: 1rem;
    animation: slideUp 0.5s ease both;
}
.glass-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(212,175,55,0.3), transparent);
}
@keyframes slideUp {
    from { opacity:0; transform: translateY(12px); }
    to   { opacity:1; transform: translateY(0); }
}

/* ── METRIC BLOCK ── */
.metric-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin-bottom: 1.5rem;
}
.metric-block {
    background: linear-gradient(135deg, rgba(255,255,255,0.03), rgba(255,255,255,0.01));
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 1.2rem 1.3rem;
    position: relative;
    overflow: hidden;
    animation: slideUp 0.5s ease both;
}
.metric-block::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 2px;
    border-radius: 0 0 14px 14px;
}
.mb-gold::after  { background: linear-gradient(90deg, #d4af37, #f9c74f); }
.mb-green::after { background: linear-gradient(90deg, #22c55e, #4ade80); }
.mb-blue::after  { background: linear-gradient(90deg, #3b82f6, #60a5fa); }
.mb-rose::after  { background: linear-gradient(90deg, #f43f5e, #fb7185); }

.metric-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.55rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: rgba(232,228,217,0.35);
    margin-bottom: 0.5rem;
}
.metric-value {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    line-height: 1;
    color: #e8e4d9;
}
.metric-value.gold  { color: #d4af37; }
.metric-value.green { color: #4ade80; }
.metric-value.blue  { color: #60a5fa; }
.metric-value.rose  { color: #fb7185; }
.metric-unit {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.55rem;
    color: rgba(232,228,217,0.25);
    margin-top: 0.25rem;
    letter-spacing: 0.1em;
}

/* ── MODE PILLS ── */
.mode-grid {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
    margin-bottom: 1rem;
}
.mode-pill {
    padding: 0.45rem 1rem;
    border-radius: 99px;
    border: 1px solid rgba(255,255,255,0.1);
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.1em;
    color: rgba(232,228,217,0.45);
    cursor: default;
    transition: all 0.2s;
}
.mode-pill.active {
    background: rgba(212,175,55,0.12);
    border-color: rgba(212,175,55,0.4);
    color: #d4af37;
    box-shadow: 0 0 16px rgba(212,175,55,0.1);
}

/* ── PATIENCE RING ── */
.patience-wrap {
    display: flex;
    align-items: center;
    gap: 2rem;
}
.ring-container {
    position: relative;
    width: 120px; height: 120px;
    flex-shrink: 0;
}
.ring-svg { transform: rotate(-90deg); }
.ring-bg { fill: none; stroke: rgba(255,255,255,0.06); stroke-width: 8; }
.ring-fill { fill: none; stroke-width: 8; stroke-linecap: round; transition: stroke-dashoffset 1s ease; }
.ring-label {
    position: absolute;
    inset: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
}
.ring-num {
    font-family: 'Syne', sans-serif;
    font-size: 1.6rem;
    font-weight: 800;
    color: #d4af37;
    line-height: 1;
}
.ring-sub {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.45rem;
    letter-spacing: 0.1em;
    color: rgba(232,228,217,0.3);
    text-transform: uppercase;
    margin-top: 2px;
}
.patience-info { flex: 1; }
.patience-status {
    font-family: 'Syne', sans-serif;
    font-size: 1.3rem;
    font-weight: 700;
    margin-bottom: 0.4rem;
}
.patience-desc {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    color: rgba(232,228,217,0.4);
    letter-spacing: 0.08em;
    line-height: 1.7;
}

/* ── SKILL DAY BADGE ── */
.skill-day-wrap {
    display: flex;
    gap: 0.6rem;
    overflow-x: auto;
    padding-bottom: 0.5rem;
    margin-bottom: 1rem;
}
.skill-day-tile {
    min-width: 90px;
    padding: 0.75rem;
    border-radius: 10px;
    border: 1px solid rgba(255,255,255,0.07);
    text-align: center;
    flex-shrink: 0;
    transition: all 0.2s;
}
.skill-day-tile.today {
    background: rgba(212,175,55,0.1);
    border-color: rgba(212,175,55,0.35);
    box-shadow: 0 0 20px rgba(212,175,55,0.08);
}
.sdt-day {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.52rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: rgba(232,228,217,0.3);
    margin-bottom: 0.35rem;
}
.sdt-skill {
    font-family: 'Syne', sans-serif;
    font-size: 0.72rem;
    font-weight: 700;
    color: #e8e4d9;
}
.skill-day-tile.today .sdt-day { color: #d4af37; }
.skill-day-tile.today .sdt-skill { color: #d4af37; }

/* ── BUILD / CONSUME BARS ── */
.bc-wrap {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
}
.bc-row {
    display: flex;
    align-items: center;
    gap: 1rem;
}
.bc-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    width: 80px;
    flex-shrink: 0;
    color: rgba(232,228,217,0.4);
}
.bc-track {
    flex: 1;
    height: 8px;
    border-radius: 99px;
    background: rgba(255,255,255,0.06);
    overflow: hidden;
}
.bc-fill {
    height: 100%;
    border-radius: 99px;
    transition: width 0.8s ease;
}
.bc-fill-build   { background: linear-gradient(90deg, #d4af37, #f9c74f); }
.bc-fill-consume { background: linear-gradient(90deg, #f43f5e, #fb7185); }
.bc-val {
    font-family: 'Syne', sans-serif;
    font-size: 0.8rem;
    font-weight: 700;
    width: 40px;
    text-align: right;
}

/* ── RATIO BADGE ── */
.ratio-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.6rem 1.2rem;
    border-radius: 99px;
    font-family: 'Syne', sans-serif;
    font-size: 0.85rem;
    font-weight: 700;
    margin-top: 0.75rem;
}
.ratio-win  { background: rgba(74,222,128,0.1); border: 1px solid rgba(74,222,128,0.25); color: #4ade80; }
.ratio-lose { background: rgba(244,63,94,0.1);  border: 1px solid rgba(244,63,94,0.25);  color: #fb7185; }

/* ── WEALTH TABLE ── */
.wealth-table { width: 100%; }
.wealth-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.85rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.05);
}
.wealth-row:last-child { border-bottom: none; }
.wealth-asset {
    display: flex;
    align-items: center;
    gap: 0.75rem;
}
.asset-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
}
.asset-name {
    font-family: 'Syne', sans-serif;
    font-size: 0.85rem;
    font-weight: 600;
    color: #e8e4d9;
}
.asset-tag {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.52rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: rgba(232,228,217,0.3);
    margin-left: 0.5rem;
}
.wealth-amount {
    font-family: 'Syne', sans-serif;
    font-size: 1.1rem;
    font-weight: 800;
    color: #d4af37;
}

/* ── 24H RING CHART ── */
.time-legend {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.6rem;
    margin-top: 1rem;
}
.time-leg-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem;
    color: rgba(232,228,217,0.5);
    letter-spacing: 0.08em;
}
.leg-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    flex-shrink: 0;
}

/* ── INPUTS OVERRIDE ── */
.stSelectbox > div > div {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    color: #e8e4d9 !important;
}
.stNumberInput input, .stTextInput input {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    color: #e8e4d9 !important;
    font-family: 'Syne', sans-serif !important;
}
.stSlider [data-baseweb="slider"] { margin-top: 0.25rem !important; }
.stSlider .rc-slider-track { background: linear-gradient(90deg, #d4af37, #f9c74f) !important; }
.stSlider .rc-slider-handle {
    border: 2px solid #d4af37 !important;
    background: #0a0d14 !important;
    box-shadow: 0 0 8px rgba(212,175,55,0.4) !important;
}
.stTextArea textarea {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 10px !important;
    color: #e8e4d9 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.82rem !important;
    line-height: 1.7 !important;
}
.stTextArea textarea:focus {
    border-color: rgba(212,175,55,0.4) !important;
    box-shadow: 0 0 0 3px rgba(212,175,55,0.08) !important;
}
label, .stSlider label {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.58rem !important;
    letter-spacing: 0.18em !important;
    text-transform: uppercase !important;
    color: rgba(232,228,217,0.35) !important;
    font-weight: 400 !important;
}

/* ── BUTTON ── */
.stButton > button {
    background: linear-gradient(135deg, #d4af37, #f9c74f) !important;
    border: none !important;
    border-radius: 10px !important;
    color: #0a0d14 !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 0.78rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    padding: 0.65rem 1.8rem !important;
    transition: all 0.2s !important;
    box-shadow: 0 4px 20px rgba(212,175,55,0.25) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(212,175,55,0.35) !important;
}

/* ── ALERT OVERRIDES ── */
.stAlert { border-radius: 10px !important; border: none !important; }
[data-testid="stNotification"] { background: rgba(255,255,255,0.04) !important; }

/* ── HR ── */
hr { border-color: rgba(255,255,255,0.05) !important; margin: 1.5rem 0 !important; }

/* ── STAGGER ANIMATIONS ── */
.glass-card:nth-child(1) { animation-delay: 0.05s; }
.glass-card:nth-child(2) { animation-delay: 0.1s; }
.glass-card:nth-child(3) { animation-delay: 0.15s; }
.glass-card:nth-child(4) { animation-delay: 0.2s; }
</style>
""", unsafe_allow_html=True)


# ── Data ────────────────────────────────────────────────────────────────────────
DATA_FILE = "life_os_v2.json"
DEFAULT_DATA = {
    "mode": "Builder Phase",
    "patience_days_required": 30,
    "current_strategy_start": str(datetime.date.today()),
    "build_hours": 0,
    "consume_hours": 0,
    "sleep_mode": "Normal",
    "daily_skill": "Coding",
    "monthly_investing": {"Index Fund": 200, "AI Companies": 100, "Bitcoin": 100},
    "notes": []
}
DAY_SKILL_MAP = {
    "Monday": "Coding", "Tuesday": "Communication", "Wednesday": "Finance",
    "Thursday": "Art", "Friday": "Charts", "Saturday": "Deep Work", "Sunday": "Review"
}
LIFECYCLE_MODES = ["Student Phase", "Student + Work", "Builder Phase", "Operator Phase", "Founder Phase"]
SLEEP_MAP = {"Busy": 6, "Normal": 7, "Relaxed": 8}
SKILLS = ["Coding", "Charts", "Communication", "Finance", "Art", "Deep Work", "Review"]
WEEK_DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
ASSET_COLORS = {"Index Fund": "#3b82f6", "AI Companies": "#a855f7", "Bitcoin": "#f97316"}

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f:
            d = json.load(f)
        for k in DEFAULT_DATA:
            if k not in d:
                d[k] = DEFAULT_DATA[k]
        return d
    return DEFAULT_DATA.copy()

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

data = load_data()
today = datetime.date.today()
day_name = today.strftime("%A")
auto_skill = DAY_SKILL_MAP.get(day_name, "Coding")

# ── HERO BAND ──────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero-band">
  <div class="hero-title">Life OS <span>v2</span></div>
  <div class="hero-sub"><span class="status-dot"></span>Adaptive Compound Engine &nbsp;·&nbsp; Founder Edition</div>
  <div class="hero-meta">
    <div class="hero-meta-item">
      <div class="hero-meta-label">Today</div>
      <div class="hero-meta-value">{today.strftime("%A, %d %b %Y")}</div>
    </div>
    <div class="hero-meta-item">
      <div class="hero-meta-label">Mode</div>
      <div class="hero-meta-value">{data['mode']}</div>
    </div>
    <div class="hero-meta-item">
      <div class="hero-meta-label">Today's Skill</div>
      <div class="hero-meta-value">{auto_skill}</div>
    </div>
    <div class="hero-meta-item">
      <div class="hero-meta-label">Sleep Budget</div>
      <div class="hero-meta-value">{SLEEP_MAP[data['sleep_mode']]} hrs</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)


# ── ROW 1: Mode | Skill wheel ──────────────────────────────────────────────────
col_left, col_right = st.columns([1.4, 1], gap="large")

with col_left:
    # Lifecycle mode
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="sec-head"><div class="sec-icon">⚡</div><div class="sec-title"><span>01</span>Lifecycle Mode</div></div>', unsafe_allow_html=True)

    pills_html = '<div class="mode-grid">'
    for m in LIFECYCLE_MODES:
        active = "active" if m == data["mode"] else ""
        pills_html += f'<div class="mode-pill {active}">{m}</div>'
    pills_html += '</div>'
    st.markdown(pills_html, unsafe_allow_html=True)

    data["mode"] = st.selectbox("Select Mode", LIFECYCLE_MODES, index=LIFECYCLE_MODES.index(data["mode"]), label_visibility="collapsed")

    col_s1, col_s2 = st.columns(2)
    with col_s1:
        data["sleep_mode"] = st.selectbox("Sleep Mode", list(SLEEP_MAP.keys()), index=list(SLEEP_MAP.keys()).index(data["sleep_mode"]))
    with col_s2:
        sleep_hrs = SLEEP_MAP[data["sleep_mode"]]
        st.markdown(f"""
        <div style="padding-top:1.8rem; font-family:'Syne',sans-serif;">
          <div style="font-family:'JetBrains Mono',monospace;font-size:0.55rem;letter-spacing:0.2em;text-transform:uppercase;color:rgba(232,228,217,0.35);margin-bottom:0.3rem">SLEEP BUDGET</div>
          <div style="font-size:2rem;font-weight:800;color:#d4af37;line-height:1">{sleep_hrs}<span style="font-size:0.9rem;color:rgba(232,228,217,0.3);font-weight:400;margin-left:4px">HRS</span></div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    # Skill-per-day system
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="sec-head"><div class="sec-icon">🎯</div><div class="sec-title"><span>02</span>One Skill Per Day</div></div>', unsafe_allow_html=True)

    tiles_html = '<div class="skill-day-wrap">'
    for d_name in WEEK_DAYS:
        skill = DAY_SKILL_MAP[d_name]
        is_today = "today" if d_name == day_name else ""
        tiles_html += f'<div class="skill-day-tile {is_today}"><div class="sdt-day">{d_name[:3].upper()}</div><div class="sdt-skill">{skill}</div></div>'
    tiles_html += '</div>'
    st.markdown(tiles_html, unsafe_allow_html=True)

    manual_skill = st.selectbox("Override Today's Skill", SKILLS, index=SKILLS.index(auto_skill) if auto_skill in SKILLS else 0)
    col_ob1, col_ob2 = st.columns([1,1])
    with col_ob1:
        if st.button("Use Override", use_container_width=True):
            data["daily_skill"] = manual_skill
            st.rerun()
    with col_ob2:
        if st.button("Reset to Auto", use_container_width=True):
            data["daily_skill"] = auto_skill
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)


# ── ROW 2: Patience | Build vs Consume ────────────────────────────────────────
col_p, col_b = st.columns([1, 1.2], gap="large")

with col_p:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="sec-head"><div class="sec-icon">⏳</div><div class="sec-title"><span>03</span>Patience Engine</div></div>', unsafe_allow_html=True)

    strategy_start = datetime.date.fromisoformat(data["current_strategy_start"])
    days_active = (today - strategy_start).days
    required_days = data["patience_days_required"]
    remaining = max(required_days - days_active, 0)
    pct = min(days_active / required_days, 1.0) if required_days > 0 else 1.0
    circumference = 2 * 3.14159 * 46
    offset = circumference * (1 - pct)
    ring_color = "#d4af37" if remaining > 0 else "#4ade80"

    st.markdown(f"""
    <div class="patience-wrap">
      <div class="ring-container">
        <svg class="ring-svg" width="120" height="120" viewBox="0 0 120 120">
          <circle class="ring-bg" cx="60" cy="60" r="46"/>
          <circle class="ring-fill" cx="60" cy="60" r="46"
            stroke="{ring_color}"
            stroke-dasharray="{circumference}"
            stroke-dashoffset="{offset:.1f}"/>
        </svg>
        <div class="ring-label">
          <div class="ring-num">{days_active}</div>
          <div class="ring-sub">of {required_days}d</div>
        </div>
      </div>
      <div class="patience-info">
        <div class="patience-status" style="color:{'#4ade80' if remaining == 0 else '#d4af37'}">
          {'✓ REVIEW UNLOCKED' if remaining == 0 else f'{remaining} DAYS LOCKED'}
        </div>
        <div class="patience-desc">
          {'Strategy review allowed. Change only with a written reason.' if remaining == 0 else 'Stay consistent. Do not switch strategies mid-run.'}
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top:1rem'>", unsafe_allow_html=True)
    new_days = st.slider("Lock Period (days)", 7, 90, required_days, key="patience_slider")
    data["patience_days_required"] = new_days

    if remaining == 0:
        reason = st.text_area("Reason for strategy change", placeholder="Write your justification before switching...", height=80)

    if st.button("Reset Strategy Start to Today"):
        data["current_strategy_start"] = str(today)
        save_data(data)
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_b:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="sec-head"><div class="sec-icon">⚖️</div><div class="sec-title"><span>04</span>Build vs Consume</div></div>', unsafe_allow_html=True)

    build_h = st.number_input("Build Hours Today", min_value=0.0, max_value=16.0, step=0.5, value=float(data.get("build_hours", 0)))
    consume_h = st.number_input("Consume Hours Today", min_value=0.0, max_value=16.0, step=0.5, value=float(data.get("consume_hours", 0)))

    total_bc = build_h + consume_h
    build_pct  = (build_h / total_bc * 100) if total_bc > 0 else 0
    consume_pct = (consume_h / total_bc * 100) if total_bc > 0 else 0
    ratio = round(build_h / consume_h, 2) if consume_h > 0 else build_h

    st.markdown(f"""
    <div class="bc-wrap" style="margin-top:0.5rem">
      <div class="bc-row">
        <div class="bc-label">Build</div>
        <div class="bc-track"><div class="bc-fill bc-fill-build" style="width:{build_pct}%"></div></div>
        <div class="bc-val" style="color:#d4af37">{build_h}h</div>
      </div>
      <div class="bc-row">
        <div class="bc-label">Consume</div>
        <div class="bc-track"><div class="bc-fill bc-fill-consume" style="width:{consume_pct}%"></div></div>
        <div class="bc-val" style="color:#fb7185">{consume_h}h</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    if build_h > consume_h:
        st.markdown(f'<div class="ratio-badge ratio-win">⬆ Builder Ratio {ratio}x — You\'re in build mode</div>', unsafe_allow_html=True)
    elif consume_h > 0:
        st.markdown(f'<div class="ratio-badge ratio-lose">⬇ Consumption Heavy {ratio}x — Rebalance required</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="ratio-badge" style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.1);color:rgba(232,228,217,0.4)">→ Log hours above to calculate ratio</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ── ROW 3: Wealth | 24h Clock ─────────────────────────────────────────────────
col_w, col_t = st.columns([1, 1.1], gap="large")

with col_w:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="sec-head"><div class="sec-icon">💰</div><div class="sec-title"><span>05</span>Wealth Compound Layer</div></div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        index_amt = st.number_input("Index Fund", min_value=0, value=int(data["monthly_investing"].get("Index Fund", 200)), step=50)
    with c2:
        ai_amt = st.number_input("AI Companies", min_value=0, value=int(data["monthly_investing"].get("AI Companies", 100)), step=50)
    with c3:
        btc_amt = st.number_input("Bitcoin", min_value=0, value=int(data["monthly_investing"].get("Bitcoin", 100)), step=50)

    monthly_total = index_amt + ai_amt + btc_amt
    annual_total  = monthly_total * 12
    amounts = {"Index Fund": index_amt, "AI Companies": ai_amt, "Bitcoin": btc_amt}

    rows_html = '<div class="wealth-table">'
    for asset, amt in amounts.items():
        color = ASSET_COLORS[asset]
        pct = round((amt / monthly_total) * 100) if monthly_total > 0 else 0
        rows_html += f"""
        <div class="wealth-row">
          <div class="wealth-asset">
            <div class="asset-dot" style="background:{color}"></div>
            <span class="asset-name">{asset}</span>
            <span class="asset-tag">{pct}%</span>
          </div>
          <span class="wealth-amount">P{amt:,}</span>
        </div>"""
    rows_html += '</div>'
    st.markdown(rows_html, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="display:flex;gap:1rem;margin-top:1rem;padding-top:1rem;border-top:1px solid rgba(255,255,255,0.06)">
      <div>
        <div class="metric-label">Monthly Total</div>
        <div style="font-family:'Syne',sans-serif;font-size:1.6rem;font-weight:800;color:#d4af37">P{monthly_total:,}</div>
      </div>
      <div style="margin-left:auto;text-align:right">
        <div class="metric-label">Annual Projection</div>
        <div style="font-family:'Syne',sans-serif;font-size:1.6rem;font-weight:800;color:#4ade80">P{annual_total:,}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

with col_t:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="sec-head"><div class="sec-icon">🕐</div><div class="sec-title"><span>06</span>24-Hour Allocation</div></div>', unsafe_allow_html=True)

    work_school = st.slider("School / Work Hours", 4, 15, 8)
    skill_hrs   = st.slider("Skill Development Hours", 1, 6, 2)

    buffer_hrs = 24 - sleep_hrs - work_school - skill_hrs

    # Donut chart via HTML/SVG
    segs = [
        ("Sleep",   sleep_hrs,   "#3b82f6"),
        ("Work",    work_school, "#d4af37"),
        ("Skill",   skill_hrs,   "#4ade80"),
        ("Buffer",  max(buffer_hrs, 0), "#6b7280"),
    ]
    total_h = 24
    cx, cy, r_out, r_in = 80, 80, 65, 38

    def polar(cx, cy, r, deg):
        rad = math.radians(deg - 90)
        return cx + r * math.cos(rad), cy + r * math.sin(rad)

    def arc_path(cx, cy, r_out, r_in, start_deg, end_deg):
        large = 1 if (end_deg - start_deg) > 180 else 0
        ox1, oy1 = polar(cx, cy, r_out, start_deg)
        ox2, oy2 = polar(cx, cy, r_out, end_deg)
        ix1, iy1 = polar(cx, cy, r_in, end_deg)
        ix2, iy2 = polar(cx, cy, r_in, start_deg)
        return f"M {ox1:.1f} {oy1:.1f} A {r_out} {r_out} 0 {large} 1 {ox2:.1f} {oy2:.1f} L {ix1:.1f} {iy1:.1f} A {r_in} {r_in} 0 {large} 0 {ix2:.1f} {iy2:.1f} Z"

    paths = []
    angle = 0
    for name, hrs, color in segs:
        if hrs > 0:
            sweep = (hrs / total_h) * 360
            paths.append((arc_path(cx, cy, r_out, r_in, angle, angle + sweep - 1), color))
            angle += sweep

    svg_paths = "\n".join(f'<path d="{p}" fill="{c}" opacity="0.85"/>' for p, c in paths)
    center_label = f"""
    <text x="{cx}" y="{cy-6}" text-anchor="middle" font-family="Syne,sans-serif" font-size="18" font-weight="800" fill="#e8e4d9">24</text>
    <text x="{cx}" y="{cy+12}" text-anchor="middle" font-family="JetBrains Mono,monospace" font-size="8" fill="rgba(232,228,217,0.4)" letter-spacing="2">HRS</text>
    """

    if buffer_hrs < 0:
        err_overlay = f'<text x="{cx}" y="{cy+35}" text-anchor="middle" font-family="JetBrains Mono,monospace" font-size="8" fill="#fb7185">OVER BY {abs(buffer_hrs)}H</text>'
    else:
        err_overlay = ""

    donut_svg = f"""
    <svg width="160" height="160" viewBox="0 0 160 160">
      <rect width="160" height="160" fill="transparent"/>
      {svg_paths}
      {center_label}
      {err_overlay}
    </svg>"""

    legend_html = '<div class="time-legend">'
    for name, hrs, color in segs:
        legend_html += f"""
        <div class="time-leg-item">
          <div class="leg-dot" style="background:{color}"></div>
          <span>{name}: <strong style="color:#e8e4d9">{max(hrs,0)}h</strong></span>
        </div>"""
    legend_html += '</div>'

    cols_donut = st.columns([1, 1.4])
    with cols_donut[0]:
        st.markdown(donut_svg, unsafe_allow_html=True)
    with cols_donut[1]:
        st.markdown(legend_html, unsafe_allow_html=True)
        if buffer_hrs < 0:
            st.markdown(f'<div style="margin-top:0.5rem;padding:0.5rem 0.75rem;background:rgba(244,63,94,0.08);border:1px solid rgba(244,63,94,0.2);border-radius:8px;font-family:JetBrains Mono,monospace;font-size:0.62rem;color:#fb7185">Over-allocated by {abs(buffer_hrs)}h</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="margin-top:0.5rem;padding:0.5rem 0.75rem;background:rgba(74,222,128,0.06);border:1px solid rgba(74,222,128,0.15);border-radius:8px;font-family:JetBrains Mono,monospace;font-size:0.62rem;color:#4ade80">Buffer: {buffer_hrs}h free</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ── SAVE ROW ──────────────────────────────────────────────────────────────────
st.markdown("<div style='margin-top:1rem'>", unsafe_allow_html=True)
col_save, col_msg = st.columns([1, 3])
with col_save:
    if st.button("⟶  Commit OS Snapshot", use_container_width=True):
        data["build_hours"]        = build_h
        data["consume_hours"]      = consume_h
        data["monthly_investing"]  = {"Index Fund": index_amt, "AI Companies": ai_amt, "Bitcoin": btc_amt}
        save_data(data)
        st.success("System state committed.")
st.markdown("</div>", unsafe_allow_html=True)


# ── FOOTER ─────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="margin-top:3rem;padding-top:1.5rem;border-top:1px solid rgba(255,255,255,0.05);
            display:flex;justify-content:space-between;align-items:center;
            font-family:'JetBrains Mono',monospace;font-size:0.55rem;
            letter-spacing:0.2em;color:rgba(232,228,217,0.18);text-transform:uppercase;">
  <span>Life OS v2 · Adaptive Compound Engine</span>
  <span>Build · Reflect · Compound</span>
  <span>{today.strftime('%d %b %Y').upper()}</span>
</div>
""", unsafe_allow_html=True)
