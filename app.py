import streamlit as st
import pandas as pd
import json
import datetime
import os
import random
import math

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="The Long Game — Life OS",
    layout="wide",
    initial_sidebar_state="collapsed",
    page_icon="⚡",
)

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;700&family=Bebas+Neue&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"], .stApp {
    font-family: 'Plus Jakarta Sans', sans-serif;
    background-color: #111827 !important;
    color: #f1f5f9 !important;
}
.main .block-container {
    padding: 2rem 2.5rem 4rem;
    max-width: 1500px;
    background-color: #111827 !important;
}
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* HERO */
.hero-header {
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    padding: 0 0 2rem;
    border-bottom: 1px solid rgba(255,255,255,0.07);
    margin-bottom: 2rem;
    animation: fadeIn 0.6s ease;
}
.hero-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 4.5rem;
    letter-spacing: 0.1em;
    line-height: 1;
    background: linear-gradient(135deg, #f9c74f 0%, #f8961e 60%, #f3722c 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-sub {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    color: rgba(255,255,255,0.35);
    letter-spacing: 0.25em;
    text-transform: uppercase;
    margin-top: 0.35rem;
}
.hero-date {
    text-align: right;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    color: rgba(255,255,255,0.3);
    letter-spacing: 0.15em;
    text-transform: uppercase;
    line-height: 2.1;
}
.hero-date span {
    display: block;
    color: #f9c74f;
    font-size: 1.1rem;
    font-weight: 700;
    letter-spacing: 0.04em;
}

/* NAV TABS */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.04) !important;
    border-radius: 10px !important;
    padding: 4px !important;
    gap: 4px !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 7px !important;
    color: rgba(255,255,255,0.45) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.65rem !important;
    letter-spacing: 0.18em !important;
    text-transform: uppercase !important;
    padding: 0.55rem 1.2rem !important;
    transition: all 0.2s !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #f9c74f, #f8961e) !important;
    color: #111827 !important;
    font-weight: 700 !important;
}

/* SECTION LABEL */
.section-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    color: #f9c74f;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.75rem;
}
.section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, rgba(249,199,79,0.3) 0%, transparent 100%);
}

/* STAT CARDS */
.stat-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin-bottom: 2rem;
}
.stat-card {
    background: #1e293b;
    border-radius: 12px;
    padding: 1.3rem 1.4rem;
    border: 1px solid rgba(255,255,255,0.07);
    animation: fadeIn 0.5s ease;
    position: relative;
    overflow: hidden;
}
.stat-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #f9c74f, #f8961e);
}
.stat-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.58rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: rgba(255,255,255,0.35);
    margin-bottom: 0.5rem;
}
.stat-value {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.4rem;
    letter-spacing: 0.04em;
    color: #f1f5f9;
    line-height: 1;
}
.stat-unit {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.55rem;
    color: rgba(255,255,255,0.25);
    margin-top: 0.2rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}

/* SCORE CARD */
.score-card {
    background: #1e293b;
    border-radius: 14px;
    padding: 2rem 1.75rem;
    border: 1px solid rgba(255,255,255,0.07);
    position: relative;
    overflow: hidden;
    animation: fadeIn 0.5s ease;
    height: 100%;
}
.score-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 4px;
    background: linear-gradient(90deg, #f9c74f, #f8961e, #f3722c);
}
.score-number {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 8rem;
    line-height: 1;
    letter-spacing: 0.02em;
    background: linear-gradient(135deg, #f8961e, #f3722c);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.score-denom {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    color: rgba(255,255,255,0.3);
    margin-top: -0.5rem;
    letter-spacing: 0.1em;
}
.score-verdict {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2rem;
    letter-spacing: 0.1em;
    margin-top: 0.75rem;
}
.verdict-elite { color: #22c55e; }
.verdict-solid  { color: #f8961e; }
.verdict-reset  { color: #ef4444; }

/* PROGRESS BAR */
.progress-track {
    background: rgba(255,255,255,0.08);
    border-radius: 99px;
    height: 7px;
    margin-top: 1rem;
    overflow: hidden;
}
.progress-fill {
    height: 100%;
    border-radius: 99px;
    transition: width 0.9s cubic-bezier(0.25, 1, 0.5, 1);
}
.progress-fill-elite { background: linear-gradient(90deg, #22c55e, #4ade80); }
.progress-fill-solid { background: linear-gradient(90deg, #f8961e, #f9c74f); }
.progress-fill-reset { background: linear-gradient(90deg, #ef4444, #fca5a5); }

/* PILLAR PANEL */
.pillar-panel {
    background: #1e293b;
    border-radius: 14px;
    border: 1px solid rgba(255,255,255,0.07);
    overflow: hidden;
    margin-bottom: 1rem;
    transition: box-shadow 0.2s;
}
.pillar-panel:hover { box-shadow: 0 0 0 1px rgba(249,199,79,0.2); }
.pillar-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1rem 1.25rem;
    border-bottom: 1px solid rgba(255,255,255,0.06);
}
.pillar-header-name {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.1rem;
    letter-spacing: 0.12em;
    color: #f1f5f9;
}
.pillar-header-tag {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.55rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    padding: 0.2rem 0.6rem;
    border-radius: 99px;
    font-weight: 600;
}
.pillar-task-list { padding: 0.6rem 0; }
.pillar-task-row {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.5rem 1.25rem;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 0.82rem;
    border-bottom: 1px solid rgba(255,255,255,0.04);
    transition: background 0.15s;
}
.pillar-task-row:last-child { border-bottom: none; }
.pillar-pts-badge {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.6rem;
    font-weight: 700;
    margin-left: auto;
    padding: 0.15rem 0.5rem;
    border-radius: 4px;
    background: rgba(249,199,79,0.1);
    color: #f9c74f;
    letter-spacing: 0.08em;
}

/* CHECKBOXES */
.stCheckbox { margin-bottom: 0 !important; }
.stCheckbox label {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    color: rgba(255,255,255,0.75) !important;
}
.stCheckbox label p { color: rgba(255,255,255,0.75) !important; }

/* BUTTONS */
.stButton > button {
    background: linear-gradient(135deg, #f9c74f, #f8961e) !important;
    border: none !important;
    border-radius: 8px !important;
    color: #111827 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.78rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    padding: 0.6rem 1.4rem !important;
    transition: all 0.2s !important;
    box-shadow: 0 2px 12px rgba(248,150,30,0.3) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(248,150,30,0.45) !important;
}

/* TEXT AREA */
.stTextArea textarea {
    background: #0f172a !important;
    border: 1.5px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    color: #f1f5f9 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.88rem !important;
    line-height: 1.8 !important;
    padding: 1rem !important;
    transition: border-color 0.2s !important;
}
.stTextArea textarea:focus {
    border-color: #f8961e !important;
    box-shadow: 0 0 0 3px rgba(248,150,30,0.1) !important;
}
.stTextArea label {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.6rem !important;
    letter-spacing: 0.2em !important;
    text-transform: uppercase !important;
    color: rgba(255,255,255,0.35) !important;
}

/* QUOTE CARD */
.quote-card {
    background: linear-gradient(135deg, #f9c74f 0%, #f8961e 100%);
    border-radius: 12px;
    padding: 1.6rem;
    box-shadow: 0 4px 24px rgba(248,150,30,0.25);
}

/* ANALYTICS CARD */
.analytics-card {
    background: #1e293b;
    border-radius: 12px;
    padding: 1.5rem;
    border: 1px solid rgba(255,255,255,0.07);
    height: 100%;
}
.analytics-card-title {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.58rem;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: rgba(255,255,255,0.35);
    margin-bottom: 1.2rem;
}

/* HABIT GRID */
.habit-grid-wrap { display: flex; flex-direction: column; gap: 0.5rem; }
.habit-row { display: flex; align-items: center; gap: 0.6rem; }
.habit-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.58rem;
    color: rgba(255,255,255,0.4);
    letter-spacing: 0.1em;
    width: 110px;
    text-transform: uppercase;
    flex-shrink: 0;
}
.habit-cells { display: flex; gap: 3px; flex-wrap: wrap; }
.habit-cell {
    width: 16px;
    height: 16px;
    border-radius: 3px;
    transition: transform 0.1s;
}
.habit-cell:hover { transform: scale(1.3); }
.habit-done  { background: #f8961e; }
.habit-miss  { background: rgba(255,255,255,0.07); }
.habit-na    { background: transparent; border: 1px dashed rgba(255,255,255,0.1); }

/* WEEKLY BAR */
.weekly-bars { display: flex; align-items: flex-end; gap: 6px; height: 80px; margin-bottom: 0.4rem; }
.weekly-bar-wrap { display: flex; flex-direction: column; align-items: center; flex: 1; height: 100%; justify-content: flex-end; }
.weekly-bar {
    width: 100%;
    border-radius: 4px 4px 0 0;
    background: linear-gradient(180deg, #f9c74f, #f8961e);
    transition: height 0.6s ease;
    min-height: 3px;
    position: relative;
}
.weekly-bar-elite { background: linear-gradient(180deg, #4ade80, #22c55e); }
.weekly-bar-solid  { background: linear-gradient(180deg, #f9c74f, #f8961e); }
.weekly-bar-reset  { background: linear-gradient(180deg, #fca5a5, #ef4444); }
.weekly-bar-empty  { background: rgba(255,255,255,0.06); }
.weekly-day-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.52rem;
    color: rgba(255,255,255,0.3);
    letter-spacing: 0.1em;
    margin-top: 0.35rem;
    text-transform: uppercase;
}
.weekly-score-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.55rem;
    color: rgba(255,255,255,0.5);
    margin-bottom: 2px;
}

/* PILLAR SCORE BAR */
.pillar-score-row {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 0.85rem;
}
.pillar-score-name {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.58rem;
    letter-spacing: 0.12em;
    color: rgba(255,255,255,0.45);
    text-transform: uppercase;
    width: 80px;
    flex-shrink: 0;
}
.pillar-score-track {
    flex: 1;
    background: rgba(255,255,255,0.07);
    border-radius: 99px;
    height: 6px;
    overflow: hidden;
}
.pillar-score-fill {
    height: 100%;
    border-radius: 99px;
    transition: width 0.8s ease;
}
.pillar-score-pct {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.6rem;
    color: rgba(255,255,255,0.5);
    width: 30px;
    text-align: right;
    flex-shrink: 0;
}

/* DATAFRAME */
.stDataFrame { background: #1e293b !important; border-radius: 12px !important; overflow: hidden !important; }
.stDataFrame th { background: #0f172a !important; color: rgba(255,255,255,0.4) !important; font-size: 0.65rem !important; letter-spacing: 0.1em !important; }
.stDataFrame td { color: #f1f5f9 !important; font-size: 0.8rem !important; }

/* ALERTS */
.stAlert { border-radius: 8px !important; border: none !important; }

/* DIVIDER */
hr { border-color: rgba(255,255,255,0.06) !important; margin: 1.5rem 0 !important; }

/* ANIMATIONS */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(8px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0.3; }
}
.live-dot {
    display: inline-block;
    width: 7px; height: 7px;
    background: #4ade80;
    border-radius: 50%;
    margin-right: 0.5rem;
    animation: pulse 2s ease infinite;
    box-shadow: 0 0 6px #4ade80;
}

/* PILLAR COLOR ACCENTS */
.tag-foundation { background: rgba(249,199,79,0.12); color: #f9c74f; }
.tag-health      { background: rgba(34,197,94,0.12);  color: #4ade80; }
.tag-wealth      { background: rgba(59,130,246,0.12); color: #60a5fa; }
.tag-growth      { background: rgba(168,85,247,0.12); color: #c084fc; }
.tag-mission     { background: rgba(248,150,30,0.12); color: #f8961e; }
.tag-mastery     { background: rgba(244,63,94,0.12);  color: #fb7185; }

.fill-foundation { background: #f9c74f; }
.fill-health      { background: #4ade80; }
.fill-wealth      { background: #60a5fa; }
.fill-growth      { background: #c084fc; }
.fill-mission     { background: #f8961e; }
.fill-mastery     { background: #fb7185; }

/* ADD TASK FORM */
.add-task-form {
    background: #0f172a;
    border-radius: 10px;
    padding: 1rem 1.25rem;
    border: 1px dashed rgba(255,255,255,0.1);
    margin-top: 0.5rem;
}
</style>
""", unsafe_allow_html=True)


# ── Data & helpers ─────────────────────────────────────────────────────────────
DATA_FILE = "tlg_life_os_v4.json"

DEFAULT_DATA = {
    "history": [],
    "streak": 0,
    "best_score": 0,
    "total_days": 0,
    "custom_tasks": {},      # pillar_key -> [{name, pts}]
}

PILLAR_META = {
    "foundation": {"label": "Personal Foundation", "icon": "🏛",  "tag_cls": "tag-foundation", "fill_cls": "fill-foundation", "color": "#f9c74f"},
    "health":     {"label": "Health & Body",        "icon": "⚡",  "tag_cls": "tag-health",      "fill_cls": "fill-health",      "color": "#4ade80"},
    "wealth":     {"label": "Financial Life",       "icon": "💰",  "tag_cls": "tag-wealth",      "fill_cls": "fill-wealth",      "color": "#60a5fa"},
    "growth":     {"label": "Skill & Growth",       "icon": "📈",  "tag_cls": "tag-growth",      "fill_cls": "fill-growth",      "color": "#c084fc"},
    "mission":    {"label": "TLG Mission",          "icon": "🎯",  "tag_cls": "tag-mission",     "fill_cls": "fill-mission",     "color": "#f8961e"},
    "mastery":    {"label": "Mastery & Mind",       "icon": "🧠",  "tag_cls": "tag-mastery",     "fill_cls": "fill-mastery",     "color": "#fb7185"},
}

DEFAULT_TASKS = {
    "foundation": [{"name": "Morning Routine",       "pts": 15, "id": "morning"}],
    "health":     [{"name": "Workout / Training",    "pts": 15, "id": "workout"}],
    "wealth":     [{"name": "Finance Review",        "pts": 20, "id": "finance"}],
    "growth":     [{"name": "Skill Development",     "pts": 20, "id": "skill"}],
    "mission":    [{"name": "TLG Project Progress",  "pts": 20, "id": "tlg"}],
    "mastery":    [{"name": "Night Reflection",      "pts": 10, "id": "reflect"}],
}

CEO_QUOTES = [
    "The system you build today runs the life you'll live tomorrow.",
    "Discipline is the bridge between goals and accomplishment.",
    "Every day is a vote for who you are becoming.",
    "Execution is the strategy that beats all strategies.",
    "Your future self is watching every decision you make today.",
    "The Long Game is won by showing up when it's inconvenient.",
    "You don't rise to the level of your goals — you fall to the level of your systems.",
    "Small wins compound. The math is on your side.",
    "Clarity is power. Execution is everything.",
]

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            d = json.load(f)
        for k in DEFAULT_DATA:
            if k not in d:
                d[k] = DEFAULT_DATA[k]
        return d
    return dict(DEFAULT_DATA)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_all_tasks(data):
    """Merge default + custom tasks per pillar."""
    all_tasks = {}
    for pillar_key in PILLAR_META:
        base = [dict(t) | {"pillar": pillar_key, "is_custom": False} for t in DEFAULT_TASKS[pillar_key]]
        custom = [dict(t) | {"pillar": pillar_key, "is_custom": True} for t in data.get("custom_tasks", {}).get(pillar_key, [])]
        all_tasks[pillar_key] = base + custom
    return all_tasks

def compute_max_score(all_tasks):
    return sum(t["pts"] for tasks in all_tasks.values() for t in tasks)

def get_task_key(pillar, task):
    return f"{pillar}__{task.get('id', task['name'])}"

def calc_streak(history):
    sorted_dates = sorted(
        [datetime.date.fromisoformat(e["date"]) for e in history],
        reverse=True
    )
    streak_count = 0
    expected = datetime.date.today()
    for d in sorted_dates:
        if d == expected:
            streak_count += 1
            expected -= datetime.timedelta(days=1)
        else:
            break
    return streak_count

# ── Session state ──────────────────────────────────────────────────────────────
if "data" not in st.session_state:
    st.session_state.data = load_data()
if "saved_today" not in st.session_state:
    st.session_state.saved_today = False
if "show_add_task" not in st.session_state:
    st.session_state.show_add_task = {}

data = st.session_state.data
today_str = datetime.date.today().strftime("%d %b %Y").upper()
day_name  = datetime.date.today().strftime("%A").upper()
all_tasks  = get_all_tasks(data)
max_score  = compute_max_score(all_tasks)

# ── HERO HEADER ────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero-header">
  <div>
    <div class="hero-title">THE LONG GAME</div>
    <div class="hero-sub">⚡ Life Operating System &nbsp;·&nbsp; Founder Edition &nbsp;·&nbsp; v4.0</div>
  </div>
  <div class="hero-date">
    <span class="live-dot"></span> LIVE SESSION
    <span>{day_name}</span>
    {today_str}
  </div>
</div>
""", unsafe_allow_html=True)

# ── STAT CARDS ─────────────────────────────────────────────────────────────────
best   = data.get("best_score", 0)
total  = data.get("total_days", 0)
streak = data.get("streak", 0)
avg_score = round(sum(e["score"] for e in data["history"]) / len(data["history"]), 0) if data["history"] else 0

st.markdown("""<div class="stat-grid">
  <div class="stat-card">
    <div class="stat-label">Current Streak</div>
    <div class="stat-value">{}</div>
    <div class="stat-unit">CONSECUTIVE DAYS</div>
  </div>
  <div class="stat-card">
    <div class="stat-label">Best Score</div>
    <div class="stat-value">{}</div>
    <div class="stat-unit">ALL-TIME HIGH</div>
  </div>
  <div class="stat-card">
    <div class="stat-label">Days Logged</div>
    <div class="stat-value">{}</div>
    <div class="stat-unit">TOTAL SESSIONS</div>
  </div>
  <div class="stat-card">
    <div class="stat-label">Average Score</div>
    <div class="stat-value">{}</div>
    <div class="stat-unit">ROLLING AVERAGE</div>
  </div>
</div>""".format(streak, best, total, int(avg_score)), unsafe_allow_html=True)

# ── TABS ───────────────────────────────────────────────────────────────────────
tab_today, tab_weekly, tab_monthly, tab_habits, tab_history = st.tabs([
    "TODAY", "WEEKLY", "MONTHLY", "HABIT MAP", "HISTORY"
])


# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — TODAY
# ══════════════════════════════════════════════════════════════════════════════
with tab_today:
    col_score, col_tasks = st.columns([1, 2], gap="large")

    # Collect checkbox states
    checked = {}
    task_list_flat = []
    for pillar_key, tasks in all_tasks.items():
        for t in tasks:
            tk = get_task_key(pillar_key, t)
            task_list_flat.append((pillar_key, t, tk))

    # Score column
    with col_score:
        st.markdown('<div class="section-label">PERFORMANCE SCORE</div>', unsafe_allow_html=True)

        # We need to read checkbox values — they're rendered below, so we pre-read from session state
        score = 0
        for pillar_key, t, tk in task_list_flat:
            if st.session_state.get(f"cb_{tk}", False):
                score += t["pts"]

        # Normalize to 100
        score_pct = round((score / max_score) * 100) if max_score > 0 else 0

        if score_pct >= 85:
            verdict_cls, verdict_txt, bar_cls = "verdict-elite", "STRONG DAY", "progress-fill-elite"
        elif score_pct >= 60:
            verdict_cls, verdict_txt, bar_cls = "verdict-solid", "DECENT DAY", "progress-fill-solid"
        else:
            verdict_cls, verdict_txt, bar_cls = "verdict-reset", "RESET NEEDED", "progress-fill-reset"

        st.markdown(f"""
        <div class="score-card">
          <div class="score-number">{score_pct}</div>
          <div class="score-denom">/ 100 — ({score} / {max_score} RAW PTS)</div>
          <div class="score-verdict {verdict_cls}">{verdict_txt}</div>
          <div class="progress-track">
            <div class="progress-fill {bar_cls}" style="width:{score_pct}%"></div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Pillar breakdown
        st.markdown('<div class="section-label">PILLAR BREAKDOWN</div>', unsafe_allow_html=True)
        pillar_scores_html = ""
        for pillar_key, meta in PILLAR_META.items():
            tasks_p = all_tasks[pillar_key]
            pillar_max = sum(t["pts"] for t in tasks_p)
            pillar_earned = sum(t["pts"] for t in tasks_p if st.session_state.get(f"cb_{get_task_key(pillar_key, t)}", False))
            pct = round((pillar_earned / pillar_max) * 100) if pillar_max > 0 else 0
            pillar_scores_html += f"""
            <div class="pillar-score-row">
              <div class="pillar-score-name">{meta['icon']} {pillar_key.upper()}</div>
              <div class="pillar-score-track">
                <div class="pillar-score-fill {meta['fill_cls']}" style="width:{pct}%"></div>
              </div>
              <div class="pillar-score-pct">{pct}%</div>
            </div>"""
        st.markdown(f'<div style="animation:fadeIn 0.5s ease">{pillar_scores_html}</div>', unsafe_allow_html=True)

    # Task pillars column
    with col_tasks:
        st.markdown('<div class="section-label">DAILY EXECUTION PROTOCOL</div>', unsafe_allow_html=True)

        for pillar_key, meta in PILLAR_META.items():
            tasks_p = all_tasks[pillar_key]
            pillar_max = sum(t["pts"] for t in tasks_p)
            pillar_earned = sum(t["pts"] for t in tasks_p if st.session_state.get(f"cb_{get_task_key(pillar_key, t)}", False))

            tag_html = f'<span class="pillar-header-tag {meta["tag_cls"]}">{pillar_key.upper()} · {pillar_earned}/{pillar_max} PTS</span>'
            st.markdown(f"""
            <div class="pillar-panel">
              <div class="pillar-header">
                <div class="pillar-header-name">{meta['icon']} {meta['label'].upper()}</div>
                {tag_html}
              </div>
            </div>
            """, unsafe_allow_html=True)

            # Checkboxes for each task
            for t in tasks_p:
                tk = get_task_key(pillar_key, t)
                col_cb, col_pts = st.columns([5, 1])
                with col_cb:
                    checked[tk] = st.checkbox(
                        t["name"],
                        key=f"cb_{tk}",
                        help=f"+{t['pts']} pts"
                    )
                with col_pts:
                    st.markdown(
                        f'<div style="padding-top:0.45rem; font-family:JetBrains Mono,monospace; '
                        f'font-size:0.65rem; color:#f9c74f; font-weight:700; letter-spacing:0.08em;">'
                        f'+{t["pts"]}</div>',
                        unsafe_allow_html=True
                    )

            # Add Task toggle
            show_key = f"show_add_{pillar_key}"
            if show_key not in st.session_state:
                st.session_state[show_key] = False

            col_add, _ = st.columns([2, 5])
            with col_add:
                if st.button(f"+ Add Task", key=f"btn_add_{pillar_key}"):
                    st.session_state[show_key] = not st.session_state[show_key]

            if st.session_state[show_key]:
                with st.container():
                    st.markdown('<div class="add-task-form">', unsafe_allow_html=True)
                    c1, c2, c3 = st.columns([4, 1, 1])
                    with c1:
                        new_name = st.text_input("Task Name", key=f"new_name_{pillar_key}", placeholder="e.g. Cold shower", label_visibility="collapsed")
                    with c2:
                        new_pts = st.number_input("Pts", min_value=1, max_value=50, value=10, key=f"new_pts_{pillar_key}", label_visibility="collapsed")
                    with c3:
                        if st.button("✓ Save", key=f"save_task_{pillar_key}"):
                            if new_name.strip():
                                custom_id = f"custom_{pillar_key}_{len(data['custom_tasks'].get(pillar_key, []))}"
                                if pillar_key not in data["custom_tasks"]:
                                    data["custom_tasks"][pillar_key] = []
                                data["custom_tasks"][pillar_key].append({
                                    "name": new_name.strip(),
                                    "pts": int(new_pts),
                                    "id": custom_id
                                })
                                save_data(data)
                                st.session_state.data = data
                                st.session_state[show_key] = False
                                st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)

            st.markdown("<div style='margin-bottom:0.75rem'></div>", unsafe_allow_html=True)

    st.markdown("---")

    # Reflection + commit
    col_ref, col_quote = st.columns([2, 1], gap="large")

    with col_ref:
        st.markdown('<div class="section-label">CEO REFLECTION LOG</div>', unsafe_allow_html=True)
        reflection = st.text_area(
            "WHAT DID I LEARN TODAY?",
            placeholder="Write your daily reflection here...\n\nWhat worked? What would you do differently? What insight did you unlock?",
            height=150,
            label_visibility="visible"
        )
        col_btn, col_msg = st.columns([1, 3])
        with col_btn:
            save_clicked = st.button("⟶  COMMIT DAY", use_container_width=True)

        if save_clicked:
            if not reflection.strip():
                st.warning("Add a reflection before committing the day.")
            else:
                task_snapshot = {}
                for pillar_key, t, tk in task_list_flat:
                    task_snapshot[tk] = st.session_state.get(f"cb_{tk}", False)

                record = {
                    "date":       datetime.date.today().isoformat(),
                    "score":      score_pct,
                    "raw_score":  score,
                    "max_score":  max_score,
                    "tasks":      task_snapshot,
                    "reflection": reflection.strip(),
                }
                existing_dates = [e["date"] for e in data["history"]]
                if record["date"] in existing_dates:
                    idx = existing_dates.index(record["date"])
                    data["history"][idx] = record
                else:
                    data["history"].append(record)

                data["best_score"] = max(data.get("best_score", 0), score_pct)
                data["total_days"] = len(data["history"])
                data["streak"]     = calc_streak(data["history"])
                save_data(data)
                st.session_state.data = data
                st.session_state.saved_today = True
                st.rerun()

        if st.session_state.saved_today:
            st.markdown("""
            <div style="margin-top:0.75rem; padding:0.85rem 1.1rem;
                        background:rgba(34,197,94,0.08); border:1.5px solid rgba(34,197,94,0.2);
                        border-left:4px solid #22c55e; border-radius:8px;
                        font-family:'Plus Jakarta Sans',sans-serif; font-size:0.83rem;
                        color:#4ade80; font-weight:600;">
              ✓ Day committed — entry saved to your history
            </div>""", unsafe_allow_html=True)

    with col_quote:
        st.markdown('<div class="section-label">FOUNDER SIGNAL</div>', unsafe_allow_html=True)
        quote = random.choice(CEO_QUOTES)
        st.markdown(f"""
        <div class="quote-card" style="animation: fadeIn 0.6s ease; margin-top:0.2rem;">
          <div style="font-family:'Plus Jakarta Sans',sans-serif; font-size:0.95rem;
                      line-height:1.8; color:#111827; font-style:italic; font-weight:500;">
            "{quote}"
          </div>
          <div style="margin-top:1rem; font-family:'JetBrains Mono',monospace;
                      font-size:0.58rem; letter-spacing:0.2em; color:rgba(17,24,39,0.45);
                      text-transform:uppercase;">
            — THE LONG GAME OS
          </div>
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — WEEKLY
# ══════════════════════════════════════════════════════════════════════════════
with tab_weekly:
    st.markdown('<div class="section-label">WEEKLY PERFORMANCE</div>', unsafe_allow_html=True)

    today = datetime.date.today()
    week_start = today - datetime.timedelta(days=today.weekday())  # Monday
    week_days = [week_start + datetime.timedelta(days=i) for i in range(7)]
    day_labels = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]

    history_map = {e["date"]: e for e in data["history"]}

    # Weekly bar chart
    bars_html = '<div class="weekly-bars">'
    for i, d in enumerate(week_days):
        ds = d.isoformat()
        entry = history_map.get(ds)
        if entry:
            sc = entry["score"]
            h_pct = max(5, sc)
            bar_cls = "weekly-bar-elite" if sc >= 85 else ("weekly-bar-solid" if sc >= 60 else "weekly-bar-reset")
            score_lbl = f'<div class="weekly-score-label">{sc}</div>'
        else:
            h_pct = 4
            bar_cls = "weekly-bar-empty"
            score_lbl = ""
        bars_html += f"""
        <div class="weekly-bar-wrap">
          {score_lbl}
          <div class="weekly-bar {bar_cls}" style="height:{h_pct}%"></div>
          <div class="weekly-day-label">{day_labels[i]}</div>
        </div>"""
    bars_html += "</div>"

    col_wk1, col_wk2 = st.columns([2, 1], gap="large")
    with col_wk1:
        st.markdown(f'<div class="analytics-card"><div class="analytics-card-title">SCORE BY DAY — CURRENT WEEK</div>{bars_html}</div>', unsafe_allow_html=True)

    with col_wk2:
        week_entries = [history_map[d.isoformat()] for d in week_days if d.isoformat() in history_map]
        days_logged  = len(week_entries)
        week_avg     = round(sum(e["score"] for e in week_entries) / days_logged, 0) if week_entries else 0
        elite_days   = sum(1 for e in week_entries if e["score"] >= 85)

        st.markdown(f"""
        <div class="analytics-card">
          <div class="analytics-card-title">WEEK SUMMARY</div>
          <div style="margin-bottom:1.2rem">
            <div class="stat-label">Days Logged This Week</div>
            <div style="font-family:'Bebas Neue',sans-serif; font-size:2.8rem; color:#f1f5f9; line-height:1">{days_logged}<span style="font-size:1.2rem; color:rgba(255,255,255,0.3)"> / 7</span></div>
          </div>
          <div style="margin-bottom:1.2rem">
            <div class="stat-label">Weekly Average</div>
            <div style="font-family:'Bebas Neue',sans-serif; font-size:2.8rem; color:#f9c74f; line-height:1">{int(week_avg)}</div>
          </div>
          <div>
            <div class="stat-label">Elite Days (85+)</div>
            <div style="font-family:'Bebas Neue',sans-serif; font-size:2.8rem; color:#4ade80; line-height:1">{elite_days}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-label">PILLAR PERFORMANCE — THIS WEEK</div>', unsafe_allow_html=True)

    # Pillar breakdown for the week
    col_pillars = st.columns(len(PILLAR_META), gap="small")
    for i, (pillar_key, meta) in enumerate(PILLAR_META.items()):
        pillar_tasks = all_tasks[pillar_key]
        total_possible = sum(t["pts"] for t in pillar_tasks) * max(1, days_logged)
        total_earned   = 0
        for entry in week_entries:
            for t in pillar_tasks:
                tk = get_task_key(pillar_key, t)
                if entry.get("tasks", {}).get(tk, False):
                    total_earned += t["pts"]
        completion_pct = round((total_earned / total_possible) * 100) if total_possible > 0 else 0

        with col_pillars[i]:
            st.markdown(f"""
            <div style="background:#1e293b; border-radius:10px; padding:1.1rem; border:1px solid rgba(255,255,255,0.07); text-align:center;">
              <div style="font-size:1.5rem; margin-bottom:0.4rem">{meta['icon']}</div>
              <div style="font-family:'JetBrains Mono',monospace; font-size:0.55rem; color:rgba(255,255,255,0.35); letter-spacing:0.15em; text-transform:uppercase; margin-bottom:0.6rem">{pillar_key.upper()}</div>
              <div style="font-family:'Bebas Neue',sans-serif; font-size:2rem; color:{meta['color']}; line-height:1">{completion_pct}%</div>
              <div style="background:rgba(255,255,255,0.07); border-radius:99px; height:4px; margin-top:0.5rem; overflow:hidden">
                <div style="height:100%; width:{completion_pct}%; background:{meta['color']}; border-radius:99px; transition:width 0.8s ease"></div>
              </div>
            </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — MONTHLY
# ══════════════════════════════════════════════════════════════════════════════
with tab_monthly:
    st.markdown('<div class="section-label">MONTHLY ANALYTICS</div>', unsafe_allow_html=True)

    now = datetime.date.today()
    month_start = now.replace(day=1)
    days_in_month = (now.replace(month=now.month % 12 + 1, day=1) - datetime.timedelta(days=1)).day if now.month < 12 else 31
    month_days = [month_start + datetime.timedelta(days=i) for i in range(days_in_month)]
    month_entries = [history_map.get(d.isoformat()) for d in month_days if history_map.get(d.isoformat())]

    col_m1, col_m2, col_m3 = st.columns(3, gap="large")

    with col_m1:
        m_avg = round(sum(e["score"] for e in month_entries) / len(month_entries), 1) if month_entries else 0
        m_elite = sum(1 for e in month_entries if e["score"] >= 85)
        m_solid = sum(1 for e in month_entries if 60 <= e["score"] < 85)
        m_reset = sum(1 for e in month_entries if e["score"] < 60)
        st.markdown(f"""
        <div class="analytics-card">
          <div class="analytics-card-title">MONTH OVERVIEW — {now.strftime('%B %Y').upper()}</div>
          <div style="display:grid; grid-template-columns:1fr 1fr; gap:1rem">
            <div>
              <div class="stat-label">Days Logged</div>
              <div style="font-family:'Bebas Neue',sans-serif; font-size:2.4rem; color:#f1f5f9; line-height:1">{len(month_entries)}</div>
            </div>
            <div>
              <div class="stat-label">Month Average</div>
              <div style="font-family:'Bebas Neue',sans-serif; font-size:2.4rem; color:#f9c74f; line-height:1">{int(m_avg)}</div>
            </div>
            <div>
              <div class="stat-label">Elite Days</div>
              <div style="font-family:'Bebas Neue',sans-serif; font-size:2.4rem; color:#4ade80; line-height:1">{m_elite}</div>
            </div>
            <div>
              <div class="stat-label">Reset Days</div>
              <div style="font-family:'Bebas Neue',sans-serif; font-size:2.4rem; color:#ef4444; line-height:1">{m_reset}</div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    with col_m2:
        # Score distribution bars
        st.markdown('<div class="analytics-card"><div class="analytics-card-title">SCORE DISTRIBUTION</div>', unsafe_allow_html=True)
        bins = [(85, 100, "85–100", "#4ade80"), (60, 84, "60–84", "#f9c74f"), (0, 59, "0–59", "#ef4444")]
        for lo, hi, lbl, color in bins:
            count = sum(1 for e in month_entries if lo <= e["score"] <= hi)
            pct = round((count / len(month_entries)) * 100) if month_entries else 0
            st.markdown(f"""
            <div style="margin-bottom:0.75rem">
              <div style="display:flex; justify-content:space-between; font-family:'JetBrains Mono',monospace; font-size:0.6rem; color:rgba(255,255,255,0.4); margin-bottom:0.3rem">
                <span>{lbl}</span><span>{count} days</span>
              </div>
              <div style="background:rgba(255,255,255,0.07); border-radius:99px; height:6px; overflow:hidden">
                <div style="height:100%; width:{pct}%; background:{color}; border-radius:99px; transition:width 0.8s ease"></div>
              </div>
            </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_m3:
        # Best streak this month
        month_date_set = {e["date"] for e in month_entries}
        best_month_streak = 0
        curr_run = 0
        for d in month_days:
            if d.isoformat() in month_date_set:
                curr_run += 1
                best_month_streak = max(best_month_streak, curr_run)
            else:
                curr_run = 0

        completion_rate = round((len(month_entries) / now.day) * 100) if now.day > 0 else 0
        st.markdown(f"""
        <div class="analytics-card">
          <div class="analytics-card-title">CONSISTENCY METRICS</div>
          <div style="margin-bottom:1.2rem">
            <div class="stat-label">Completion Rate</div>
            <div style="font-family:'Bebas Neue',sans-serif; font-size:2.6rem; color:#f8961e; line-height:1">{completion_rate}%</div>
            <div style="background:rgba(255,255,255,0.07); border-radius:99px; height:5px; margin-top:0.4rem; overflow:hidden">
              <div style="height:100%; width:{completion_rate}%; background:#f8961e; border-radius:99px"></div>
            </div>
          </div>
          <div>
            <div class="stat-label">Best Streak This Month</div>
            <div style="font-family:'Bebas Neue',sans-serif; font-size:2.6rem; color:#c084fc; line-height:1">{best_month_streak} <span style="font-size:1rem; color:rgba(255,255,255,0.3)">DAYS</span></div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    # Monthly calendar heatmap
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-label">CALENDAR HEATMAP</div>', unsafe_allow_html=True)

    cal_html = '<div style="display:flex; flex-wrap:wrap; gap:6px; padding:1.25rem; background:#1e293b; border-radius:12px; border:1px solid rgba(255,255,255,0.07)">'
    for d in month_days:
        entry = history_map.get(d.isoformat())
        if entry:
            sc = entry["score"]
            opacity = 0.3 + (sc / 100) * 0.7
            color = "#4ade80" if sc >= 85 else ("#f9c74f" if sc >= 60 else "#ef4444")
            bg = color
            opacity_style = f"opacity:{opacity}"
            title = f"{d.strftime('%d %b')}: {sc}"
        else:
            bg = "rgba(255,255,255,0.06)"
            opacity_style = ""
            title = d.strftime('%d %b')

        is_today = "border:2px solid #f9c74f;" if d == now else ""
        cal_html += f'<div title="{title}" style="width:32px; height:32px; border-radius:6px; background:{bg}; {is_today} {opacity_style}; display:flex; align-items:center; justify-content:center; font-family:JetBrains Mono,monospace; font-size:0.55rem; color:rgba(255,255,255,0.5);">{d.day}</div>'

    cal_html += "</div>"
    st.markdown(cal_html, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — HABIT MAP
# ══════════════════════════════════════════════════════════════════════════════
with tab_habits:
    st.markdown('<div class="section-label">HABIT CONSISTENCY MAP — LAST 30 DAYS</div>', unsafe_allow_html=True)

    last_30 = [datetime.date.today() - datetime.timedelta(days=i) for i in range(29, -1, -1)]
    history_map_30 = {e["date"]: e for e in data["history"]}

    # Build per-task habit grid
    st.markdown('<div style="background:#1e293b; border-radius:14px; padding:1.5rem; border:1px solid rgba(255,255,255,0.07)">', unsafe_allow_html=True)

    for pillar_key, meta in PILLAR_META.items():
        tasks_p = all_tasks[pillar_key]
        for t in tasks_p:
            tk = get_task_key(pillar_key, t)
            cells_html = '<div class="habit-cells">'
            done_count = 0
            for d in last_30:
                entry = history_map_30.get(d.isoformat())
                if entry:
                    done = entry.get("tasks", {}).get(tk, False)
                    cls  = "habit-done" if done else "habit-miss"
                    if done:
                        done_count += 1
                else:
                    cls = "habit-na"
                cells_html += f'<div class="habit-cell {cls}" title="{d.strftime("%d %b")}"></div>'
            cells_html += "</div>"

            pct = round((done_count / 30) * 100)
            pct_color = meta["color"]

            st.markdown(f"""
            <div style="display:flex; align-items:center; gap:0.75rem; margin-bottom:0.6rem; padding:0.5rem 0; border-bottom:1px solid rgba(255,255,255,0.04)">
              <div style="width:150px; flex-shrink:0">
                <div style="font-family:'JetBrains Mono',monospace; font-size:0.58rem; color:{pct_color}; letter-spacing:0.1em; text-transform:uppercase">{pillar_key.upper()}</div>
                <div style="font-family:'Plus Jakarta Sans',sans-serif; font-size:0.78rem; color:rgba(255,255,255,0.7); font-weight:500; margin-top:1px">{t['name']}</div>
              </div>
              {cells_html}
              <div style="font-family:'Bebas Neue',sans-serif; font-size:1.2rem; color:{pct_color}; margin-left:0.5rem; min-width:40px">{pct}%</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="display:flex; align-items:center; gap:1.5rem; font-family:'JetBrains Mono',monospace; font-size:0.6rem; color:rgba(255,255,255,0.3); letter-spacing:0.12em">
      <span><span style="display:inline-block;width:12px;height:12px;border-radius:3px;background:#f8961e;vertical-align:middle;margin-right:5px"></span>COMPLETED</span>
      <span><span style="display:inline-block;width:12px;height:12px;border-radius:3px;background:rgba(255,255,255,0.07);vertical-align:middle;margin-right:5px"></span>MISSED</span>
      <span><span style="display:inline-block;width:12px;height:12px;border-radius:3px;border:1px dashed rgba(255,255,255,0.15);vertical-align:middle;margin-right:5px"></span>NOT LOGGED</span>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — HISTORY
# ══════════════════════════════════════════════════════════════════════════════
with tab_history:
    st.markdown('<div class="section-label">MISSION LOG — SESSION HISTORY</div>', unsafe_allow_html=True)

    if data["history"]:
        history_df = pd.DataFrame([
            {
                "Date":       e["date"],
                "Score":      e["score"],
                "Rating":     "⚡ ELITE" if e["score"] >= 85 else ("✓ SOLID" if e["score"] >= 60 else "↺ RESET"),
                "Tasks Done": sum(1 for v in e.get("tasks", {}).values() if v),
                "Reflection": (e["reflection"][:90] + "…") if len(e.get("reflection", "")) > 90 else e.get("reflection", ""),
            }
            for e in sorted(data["history"], key=lambda x: x["date"], reverse=True)
        ])

        st.dataframe(
            history_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Score": st.column_config.ProgressColumn(
                    "Score", min_value=0, max_value=100, format="%d"
                ),
            }
        )

        col_exp, col_clear = st.columns([1, 1])
        with col_clear:
            if st.button("↺  CLEAR ALL HISTORY"):
                data["history"]    = []
                data["streak"]     = 0
                data["best_score"] = 0
                data["total_days"] = 0
                save_data(data)
                st.session_state.data = data
                st.session_state.saved_today = False
                st.rerun()
    else:
        st.markdown("""
        <div style="text-align:center; padding:4rem 2rem; color:rgba(255,255,255,0.2);
                    font-family:'JetBrains Mono',monospace; font-size:0.75rem; letter-spacing:0.2em">
          NO SESSIONS LOGGED YET — COMMIT YOUR FIRST DAY TO BEGIN
        </div>
        """, unsafe_allow_html=True)


# ── FOOTER ─────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="margin-top:3rem; padding-top:1.5rem; border-top:1px solid rgba(255,255,255,0.06);
            display:flex; justify-content:space-between; align-items:center;
            font-family:'JetBrains Mono',monospace; font-size:0.58rem;
            letter-spacing:0.2em; color:rgba(255,255,255,0.18); text-transform:uppercase;">
  <span>THE LONG GAME — LIFE OS · FOUNDER EDITION</span>
  <span>BUILD · REFLECT · EVOLVE</span>
  <span>V4.0 · {today_str}</span>
</div>
""", unsafe_allow_html=True)