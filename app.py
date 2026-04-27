import streamlit as st
import pandas as pd
import json
import datetime
import os
import random
import math

st.set_page_config(
    page_title="The Long Game — Life OS",
    layout="wide",
    initial_sidebar_state="collapsed",
    page_icon="⚡",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;700&family=Bebas+Neue&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"], .stApp {
    font-family: 'Plus Jakarta Sans', sans-serif;
    background-color: #0d1117 !important;
    color: #f1f5f9 !important;
}
.main .block-container {
    padding: 2rem 2.5rem 4rem;
    max-width: 1500px;
    background-color: #0d1117 !important;
}
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

.hero-header {
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    padding: 0 0 2rem;
    border-bottom: 1px solid rgba(255,255,255,0.07);
    margin-bottom: 2rem;
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

.stat-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 1rem;
    margin-bottom: 2rem;
}
.stat-card {
    background: #1e293b;
    border-radius: 12px;
    padding: 1.3rem 1.4rem;
    border: 1px solid rgba(255,255,255,0.07);
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
    font-size: 2.2rem;
    letter-spacing: 0.04em;
    color: #f1f5f9;
    line-height: 1;
}
.stat-unit {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.52rem;
    color: rgba(255,255,255,0.25);
    margin-top: 0.2rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}

.score-card {
    background: #1e293b;
    border-radius: 14px;
    padding: 2rem 1.75rem;
    border: 1px solid rgba(255,255,255,0.07);
    position: relative;
    overflow: hidden;
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
    font-size: 7rem;
    line-height: 1;
    letter-spacing: 0.02em;
    background: linear-gradient(135deg, #f8961e, #f3722c);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.score-denom {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    color: rgba(255,255,255,0.3);
    margin-top: -0.5rem;
    letter-spacing: 0.08em;
}
.score-verdict {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.8rem;
    letter-spacing: 0.1em;
    margin-top: 0.75rem;
}
.verdict-elite { color: #22c55e; }
.verdict-solid  { color: #f8961e; }
.verdict-reset  { color: #ef4444; }

.progress-track {
    background: rgba(255,255,255,0.08);
    border-radius: 99px;
    height: 7px;
    margin-top: 1rem;
    overflow: hidden;
}
.progress-fill { height: 100%; border-radius: 99px; }
.progress-fill-elite { background: linear-gradient(90deg, #22c55e, #4ade80); }
.progress-fill-solid { background: linear-gradient(90deg, #f8961e, #f9c74f); }
.progress-fill-reset { background: linear-gradient(90deg, #ef4444, #fca5a5); }

.pillar-panel {
    background: #1e293b;
    border-radius: 14px;
    border: 1px solid rgba(255,255,255,0.07);
    overflow: hidden;
    margin-bottom: 0.75rem;
}
.pillar-panel:hover { box-shadow: 0 0 0 1px rgba(249,199,79,0.2); }
.pillar-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.9rem 1.25rem;
    border-bottom: 1px solid rgba(255,255,255,0.06);
}
.pillar-header-name {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1rem;
    letter-spacing: 0.12em;
    color: #f1f5f9;
}
.pillar-header-tag {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.55rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    padding: 0.2rem 0.6rem;
    border-radius: 99px;
    font-weight: 600;
}

.stCheckbox label {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    color: rgba(255,255,255,0.75) !important;
}
.stCheckbox label p { color: rgba(255,255,255,0.75) !important; }

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
    box-shadow: 0 2px 12px rgba(248,150,30,0.3) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(248,150,30,0.45) !important;
}

.stTextArea textarea {
    background: #0f172a !important;
    border: 1.5px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    color: #f1f5f9 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.88rem !important;
    line-height: 1.8 !important;
    padding: 1rem !important;
}
.stTextArea textarea:focus { border-color: #f8961e !important; }
.stTextArea label {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.6rem !important;
    letter-spacing: 0.2em !important;
    text-transform: uppercase !important;
    color: rgba(255,255,255,0.35) !important;
}

.stNumberInput input, .stTextInput input {
    background: #0f172a !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 8px !important;
    color: #f1f5f9 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

.stSlider label {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.6rem !important;
    letter-spacing: 0.18em !important;
    text-transform: uppercase !important;
    color: rgba(255,255,255,0.4) !important;
}

.stSelectbox label {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.6rem !important;
    letter-spacing: 0.18em !important;
    text-transform: uppercase !important;
    color: rgba(255,255,255,0.4) !important;
}

.quote-card {
    background: linear-gradient(135deg, #f9c74f 0%, #f8961e 100%);
    border-radius: 12px;
    padding: 1.6rem;
    box-shadow: 0 4px 24px rgba(248,150,30,0.25);
}

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

.pillar-score-row {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 0.85rem;
}
.pillar-score-name {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.55rem;
    letter-spacing: 0.1em;
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
.pillar-score-fill { height: 100%; border-radius: 99px; }
.pillar-score-pct {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.6rem;
    color: rgba(255,255,255,0.5);
    width: 30px;
    text-align: right;
    flex-shrink: 0;
}

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

.habit-cell {
    width: 16px; height: 16px;
    border-radius: 3px;
    display: inline-block;
}
.habit-done  { background: #f8961e; }
.habit-miss  { background: rgba(255,255,255,0.07); }
.habit-na    { background: transparent; border: 1px dashed rgba(255,255,255,0.1); }

hr { border-color: rgba(255,255,255,0.06) !important; margin: 1.5rem 0 !important; }

.live-dot {
    display: inline-block;
    width: 7px; height: 7px;
    background: #4ade80;
    border-radius: 50%;
    margin-right: 0.5rem;
    animation: pulse 2s ease infinite;
    box-shadow: 0 0 6px #4ade80;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0.3; }
}
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(8px); }
    to   { opacity: 1; transform: translateY(0); }
}

.growth-milestone {
    background: #1e293b;
    border-radius: 10px;
    padding: 1.1rem 1.25rem;
    border: 1px solid rgba(255,255,255,0.07);
    border-left: 3px solid;
    margin-bottom: 0.75rem;
}
.schedule-block {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    margin-bottom: 8px;
}
.schedule-time {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.6rem;
    color: rgba(255,255,255,0.4);
    width: 90px;
    flex-shrink: 0;
    padding-top: 3px;
    letter-spacing: 0.05em;
}
.schedule-content {
    flex: 1;
    border-radius: 0 8px 8px 0;
    padding: 8px 12px;
    border-left: 3px solid;
}
.schedule-title {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 0.82rem;
    font-weight: 600;
    color: #f1f5f9;
    margin-bottom: 2px;
}
.schedule-meta {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.58rem;
    color: rgba(255,255,255,0.4);
    letter-spacing: 0.05em;
}
</style>
""", unsafe_allow_html=True)


# ── Data & Constants ──────────────────────────────────────────────────────────
DATA_FILE = "tlg_life_os.json"

DEFAULT_DATA = {
    "history": [],
    "streak": 0,
    "best_score": 0,
    "total_days": 0,
    "custom_tasks": {},
    "schedule_config": {
        "skill_hours": 2.0,
        "school_hours": 6.0,
        "sleep_hours": 7.0,
        "skill_start": "07:00",
        "wake_time": "05:00",
    }
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
    "foundation": [
        {"name": "Morning Routine + Movement", "pts": 15, "id": "morning"},
        {"name": "Evening Wind-Down Ritual",   "pts": 10, "id": "winddown"},
    ],
    "health": [
        {"name": "Exercise / Training",        "pts": 15, "id": "workout"},
        {"name": "Healthy Meals Tracked",      "pts": 10, "id": "nutrition"},
    ],
    "wealth": [
        {"name": "Finance / Markets Review",   "pts": 20, "id": "finance"},
        {"name": "BCom Study Session",         "pts": 15, "id": "bcom"},
    ],
    "growth": [
        {"name": "Skill Block Completed",      "pts": 25, "id": "skill"},
        {"name": "Read / Learn (30+ min)",     "pts": 10, "id": "read"},
    ],
    "mission": [
        {"name": "TLG Project Progress",       "pts": 20, "id": "tlg"},
        {"name": "Content / Network Action",   "pts": 10, "id": "content"},
    ],
    "mastery": [
        {"name": "Weekly Review (Sunday)",     "pts": 15, "id": "review"},
        {"name": "Night Reflection Log",       "pts": 10, "id": "reflect"},
    ],
}

SKILL_SCHEDULE = {
    "Mon": {"pair": "Coding + Charts",         "color": "#378ADD", "focus": "Build systems · Read market structure"},
    "Tue": {"pair": "Communication + Art",     "color": "#D4537E", "focus": "Write · Sketch · Record voice"},
    "Wed": {"pair": "Coding + Finance",        "color": "#534AB7", "focus": "Build fintech tools · Study models"},
    "Thu": {"pair": "Communication + Art",     "color": "#D4537E", "focus": "Repetition = mastery · Pitch practice"},
    "Fri": {"pair": "Coding + Charts",         "color": "#378ADD", "focus": "Builder day · Dominate the week"},
    "Sat": {"pair": "TLG Deep Work (4h+)",     "color": "#f9c74f", "focus": "All skills · Build real things"},
    "Sun": {"pair": "Review + Strategy",       "color": "#4ade80", "focus": "Audit · Fix · Plan next moves"},
}

SKILL_COLORS = {
    "Coding":         "#378ADD",
    "Charts":         "#1D9E75",
    "Communication":  "#D85A30",
    "Finance":        "#534AB7",
    "Art":            "#BA7517",
}

SKILL_WEEKLY_HOURS = {
    "Coding": 3.0,
    "Charts": 2.0,
    "Communication": 2.0,
    "Finance": 1.0,
    "Art": 2.0,
}

MILESTONES = {
    1: {
        "title": "Foundation",
        "color": "#378ADD",
        "items": [
            "First coding projects live and deployed",
            "Market basics solid — can read charts confidently",
            "Personal brand identity emerging",
            "Art style forming, creative voice developing",
            "BCom Finance Year 1 complete",
        ]
    },
    2: {
        "title": "Momentum",
        "color": "#1D9E75",
        "items": [
            "Side income from digital builds or freelance",
            "Pitching investors or clients with confidence",
            "730+ hours of focused skill practice logged",
            "Consistent content presence established",
            "Financial models built from scratch",
        ]
    },
    3: {
        "title": "Leverage",
        "color": "#534AB7",
        "items": [
            "Fintech tool in market with real users",
            "Audience of 1,000+ engaged followers",
            "TLG platform MVP launched",
            "Creative identity distinct and recognisable",
            "BCom Finance degree complete",
        ]
    },
    4: {
        "title": "Compound",
        "color": "#D85A30",
        "items": [
            "Skills intersecting powerfully — rare combination",
            "Revenue systems running semi-automatically",
            "Museum / gallery vision beginning to take shape",
            "Network of investors and builders established",
            "Multiple income streams active",
        ]
    },
    5: {
        "title": "Founder",
        "color": "#f9c74f",
        "items": [
            "Builder + Investor + Artist + Operator",
            "3,650+ hours invested across all skills",
            "TLG is a real platform and business",
            "Rare combination — wins long term",
            "The Long Game paid off",
        ]
    },
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
    "Code = Build. Charts = Understand. Finance = Decide. Art = Differentiate.",
    "Most people learn one skill. You are building five. That's the advantage.",
    "BCom + Code + Art + Communication = Founder Leverage. That wins.",
]


# ── Helpers ────────────────────────────────────────────────────────────────────
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            d = json.load(f)
        for k in DEFAULT_DATA:
            if k not in d:
                d[k] = DEFAULT_DATA[k]
        if "schedule_config" not in d:
            d["schedule_config"] = DEFAULT_DATA["schedule_config"]
        return d
    return dict(DEFAULT_DATA)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_all_tasks(data):
    all_tasks = {}
    for pk in PILLAR_META:
        base   = [dict(t) | {"pillar": pk, "is_custom": False} for t in DEFAULT_TASKS[pk]]
        custom = [dict(t) | {"pillar": pk, "is_custom": True}  for t in data.get("custom_tasks", {}).get(pk, [])]
        all_tasks[pk] = base + custom
    return all_tasks

def compute_max_score(all_tasks):
    return sum(t["pts"] for tasks in all_tasks.values() for t in tasks)

def get_task_key(pillar, task):
    return f"{pillar}__{task.get('id', task['name'])}"

def calc_streak(history):
    sorted_dates = sorted([datetime.date.fromisoformat(e["date"]) for e in history], reverse=True)
    streak_count, expected = 0, datetime.date.today()
    for d in sorted_dates:
        if d == expected:
            streak_count += 1
            expected -= datetime.timedelta(days=1)
        else:
            break
    return streak_count

def time_add(base_str, hours):
    h, m = map(int, base_str.split(":"))
    total_minutes = h * 60 + m + int(hours * 60)
    total_minutes = total_minutes % (24 * 60)
    return f"{total_minutes // 60:02d}:{total_minutes % 60:02d}"

def fmt_time(t_str):
    h, m = map(int, t_str.split(":"))
    suffix = "am" if h < 12 else "pm"
    h12 = h % 12 or 12
    return f"{h12}:{m:02d}{suffix}" if m > 0 else f"{h12}{suffix}"

def build_schedule(cfg, day_name):
    wake       = cfg.get("wake_time", "05:00")
    skill_s    = cfg.get("skill_start", "07:00")
    skill_h    = cfg.get("skill_hours", 2.0)
    school_h   = cfg.get("school_hours", 6.0)

    is_sat = day_name == "Sat"
    is_sun = day_name == "Sun"

    if is_sat:
        skill_h_actual = min(skill_h * 2, 4.0)
    elif is_sun:
        skill_h_actual = 2.0
    else:
        skill_h_actual = skill_h

    skill_e    = time_add(skill_s, skill_h_actual)
    buf1_e     = time_add(skill_e, 0.5)
    school_s   = buf1_e if not (is_sat or is_sun) else None
    school_e   = time_add(school_s, school_h) if school_s else None

    blocks = []

    blocks.append({
        "time": f"{fmt_time(wake)} – {fmt_time(skill_s)}",
        "title": "Morning prep + movement",
        "meta":  "Wake · hygiene · light breakfast · 20–30 min walk",
        "cat":   "life",
        "color": "#854F0B",
        "bg":    "rgba(133,79,11,0.1)",
    })

    skill_info = SKILL_SCHEDULE[day_name]
    blocks.append({
        "time": f"{fmt_time(skill_s)} – {fmt_time(skill_e)}",
        "title": f"Skill block — {skill_info['pair']}",
        "meta":  skill_info["focus"] + f" · {skill_h_actual:.0f}h deep work · no notifications",
        "cat":   "skill",
        "color": skill_info["color"],
        "bg":    f"rgba(255,255,255,0.05)",
    })

    blocks.append({
        "time": f"{fmt_time(skill_e)} – {fmt_time(buf1_e)}",
        "title": "Buffer — transition",
        "meta":  "Eat · stretch · reset before school",
        "cat":   "buffer",
        "color": "#888780",
        "bg":    "rgba(136,135,128,0.08)",
    })

    if not (is_sat or is_sun):
        blocks.append({
            "time": f"{fmt_time(school_s)} – {fmt_time(school_e)}",
            "title": "School / BCom Finance",
            "meta":  f"{school_h:.0f}h · Finance lectures = direct skill reinforcement",
            "cat":   "school",
            "color": "#3B6D11",
            "bg":    "rgba(59,109,17,0.1)",
        })
        debrief_e = time_add(school_e, 0.5)
        blocks.append({
            "time": f"{fmt_time(school_e)} – {fmt_time(debrief_e)}",
            "title": "Debrief walk",
            "meta":  "Mental reset · process the day",
            "cat":   "buffer",
            "color": "#888780",
            "bg":    "rgba(136,135,128,0.08)",
        })
        life_s = debrief_e
        blocks.append({
            "time": f"{fmt_time(life_s)} – {fmt_time(time_add(life_s, 3.0))}",
            "title": "Life duties block",
            "meta":  "Chores · errands · admin · family · meals",
            "cat":   "life",
            "color": "#854F0B",
            "bg":    "rgba(133,79,11,0.1)",
        })
        personal_s = time_add(life_s, 3.0)
        blocks.append({
            "time": f"{fmt_time(personal_s)} – {fmt_time(time_add(personal_s, 2.0))}",
            "title": "Connection + personal time",
            "meta":  "Friends · calls · journaling · relaxed meals",
            "cat":   "life",
            "color": "#854F0B",
            "bg":    "rgba(133,79,11,0.1)",
        })
        wind_s = time_add(personal_s, 2.0)
        blocks.append({
            "time": f"{fmt_time(wind_s)} – {fmt_time(time_add(wind_s, 1.0))}",
            "title": "Wind-down routine",
            "meta":  "No screens · plan tomorrow · reflection log",
            "cat":   "mastery",
            "color": "#fb7185",
            "bg":    "rgba(251,113,133,0.08)",
        })
    elif is_sat:
        blocks.append({
            "time": f"{fmt_time(buf1_e)} – {fmt_time(time_add(buf1_e, 1.0))}",
            "title": "Break + proper meal",
            "meta":  "Recharge · walk outside · no screens",
            "cat":   "buffer",
            "color": "#888780",
            "bg":    "rgba(136,135,128,0.08)",
        })
        blocks.append({
            "time": f"{fmt_time(time_add(buf1_e, 1.0))} – {fmt_time(time_add(buf1_e, 4.0))}",
            "title": "Life duties — batch everything",
            "meta":  "Groceries · cleaning · errands · admin",
            "cat":   "life",
            "color": "#854F0B",
            "bg":    "rgba(133,79,11,0.1)",
        })
        blocks.append({
            "time": f"{fmt_time(time_add(buf1_e, 4.0))} – {fmt_time(time_add(buf1_e, 7.0))}",
            "title": "Free / social / rest",
            "meta":  "The reason you work hard · connection · fun",
            "cat":   "life",
            "color": "#854F0B",
            "bg":    "rgba(133,79,11,0.1)",
        })
    else:
        blocks.append({
            "time": f"{fmt_time(buf1_e)} – {fmt_time(time_add(buf1_e, 2.0))}",
            "title": "Weekly review + strategy",
            "meta":  "Audit last week · set goals · fix weak areas · plan Mon–Fri",
            "cat":   "mastery",
            "color": "#fb7185",
            "bg":    "rgba(251,113,133,0.08)",
        })
        blocks.append({
            "time": f"{fmt_time(time_add(buf1_e, 2.0))} – {fmt_time(time_add(buf1_e, 5.0))}",
            "title": "Rest + connection + recharge",
            "meta":  "Family · friends · nature · full mental reset",
            "cat":   "life",
            "color": "#854F0B",
            "bg":    "rgba(133,79,11,0.1)",
        })
        blocks.append({
            "time": f"{fmt_time(time_add(buf1_e, 5.0))} – {fmt_time(time_add(buf1_e, 7.0))}",
            "title": "Meal prep + week preparation",
            "meta":  "Prep meals · pack bag · review Monday plan",
            "cat":   "life",
            "color": "#854F0B",
            "bg":    "rgba(133,79,11,0.1)",
        })

    return blocks


# ── Session state ──────────────────────────────────────────────────────────────
if "data" not in st.session_state:
    st.session_state.data = load_data()
if "saved_today" not in st.session_state:
    st.session_state.saved_today = False

data       = st.session_state.data
today      = datetime.date.today()
today_str  = today.strftime("%d %b %Y").upper()
day_name   = today.strftime("%A").upper()
day_abbr   = today.strftime("%a")
all_tasks  = get_all_tasks(data)
max_score  = compute_max_score(all_tasks)
history_map = {e["date"]: e for e in data["history"]}


# ── HERO ───────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero-header">
  <div>
    <div class="hero-title">THE LONG GAME</div>
    <div class="hero-sub">⚡ Life Operating System &nbsp;·&nbsp; Founder Edition &nbsp;·&nbsp; BCom Finance + Builder Stack</div>
  </div>
  <div class="hero-date">
    <span class="live-dot"></span> LIVE SESSION
    <span>{day_name}</span>
    {today_str}
  </div>
</div>
""", unsafe_allow_html=True)

# ── STAT CARDS ─────────────────────────────────────────────────────────────────
best      = data.get("best_score", 0)
total_d   = data.get("total_days", 0)
streak    = data.get("streak", 0)
avg_score = round(sum(e["score"] for e in data["history"]) / len(data["history"]), 0) if data["history"] else 0
cfg       = data.get("schedule_config", DEFAULT_DATA["schedule_config"])
yr1_hours = round(cfg.get("skill_hours", 2.0) * 365)

st.markdown(f"""<div class="stat-grid">
  <div class="stat-card">
    <div class="stat-label">Current Streak</div>
    <div class="stat-value">{streak}</div>
    <div class="stat-unit">Consecutive Days</div>
  </div>
  <div class="stat-card">
    <div class="stat-label">Best Score</div>
    <div class="stat-value">{best}</div>
    <div class="stat-unit">All-Time High</div>
  </div>
  <div class="stat-card">
    <div class="stat-label">Days Logged</div>
    <div class="stat-value">{total_d}</div>
    <div class="stat-unit">Total Sessions</div>
  </div>
  <div class="stat-card">
    <div class="stat-label">Average Score</div>
    <div class="stat-value">{int(avg_score)}</div>
    <div class="stat-unit">Rolling Average</div>
  </div>
  <div class="stat-card">
    <div class="stat-label">Yr 1 Skill Hours</div>
    <div class="stat-value">{yr1_hours}</div>
    <div class="stat-unit">Projected @ {cfg.get('skill_hours',2):.1f}h/day</div>
  </div>
</div>""", unsafe_allow_html=True)


# ── TABS ───────────────────────────────────────────────────────────────────────
tab_today, tab_schedule, tab_growth, tab_weekly, tab_habits, tab_history = st.tabs([
    "TODAY", "SCHEDULE", "5-YEAR GROWTH", "WEEKLY", "HABIT MAP", "HISTORY"
])


# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — TODAY
# ══════════════════════════════════════════════════════════════════════════════
with tab_today:
    col_score, col_tasks = st.columns([1, 2], gap="large")

    task_list_flat = [(pk, t, get_task_key(pk, t)) for pk, tasks in all_tasks.items() for t in tasks]

    with col_score:
        st.markdown('<div class="section-label">PERFORMANCE SCORE</div>', unsafe_allow_html=True)

        score = sum(t["pts"] for pk, t, tk in task_list_flat if st.session_state.get(f"cb_{tk}", False))
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
          <div class="score-denom">/ 100 &nbsp;·&nbsp; {score} / {max_score} raw pts</div>
          <div class="score-verdict {verdict_cls}">{verdict_txt}</div>
          <div class="progress-track">
            <div class="progress-fill {bar_cls}" style="width:{score_pct}%"></div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-label">PILLAR BREAKDOWN</div>', unsafe_allow_html=True)

        pillar_html = ""
        for pk, meta in PILLAR_META.items():
            tasks_p = all_tasks[pk]
            p_max    = sum(t["pts"] for t in tasks_p)
            p_earned = sum(t["pts"] for t in tasks_p if st.session_state.get(f"cb_{get_task_key(pk, t)}", False))
            pct      = round((p_earned / p_max) * 100) if p_max > 0 else 0
            pillar_html += f"""
            <div class="pillar-score-row">
              <div class="pillar-score-name">{meta['icon']} {pk.upper()}</div>
              <div class="pillar-score-track">
                <div class="pillar-score-fill {meta['fill_cls']}" style="width:{pct}%"></div>
              </div>
              <div class="pillar-score-pct">{pct}%</div>
            </div>"""
        st.markdown(pillar_html, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        skill_today = SKILL_SCHEDULE.get(day_abbr, SKILL_SCHEDULE["Mon"])
        st.markdown(f"""
        <div style="background:#1e293b; border-radius:10px; padding:1rem 1.25rem; border:1px solid rgba(255,255,255,0.07); border-left:3px solid {skill_today['color']}">
          <div style="font-family:'JetBrains Mono',monospace; font-size:0.55rem; letter-spacing:0.2em; text-transform:uppercase; color:rgba(255,255,255,0.35); margin-bottom:0.4rem">TODAY'S SKILL PAIR</div>
          <div style="font-family:'Bebas Neue',sans-serif; font-size:1.4rem; color:{skill_today['color']}; letter-spacing:0.08em">{skill_today['pair']}</div>
          <div style="font-family:'Plus Jakarta Sans',sans-serif; font-size:0.78rem; color:rgba(255,255,255,0.5); margin-top:0.3rem">{skill_today['focus']}</div>
        </div>
        """, unsafe_allow_html=True)

    with col_tasks:
        st.markdown('<div class="section-label">DAILY EXECUTION PROTOCOL</div>', unsafe_allow_html=True)

        for pk, meta in PILLAR_META.items():
            tasks_p  = all_tasks[pk]
            p_max    = sum(t["pts"] for t in tasks_p)
            p_earned = sum(t["pts"] for t in tasks_p if st.session_state.get(f"cb_{get_task_key(pk, t)}", False))

            st.markdown(f"""
            <div class="pillar-panel">
              <div class="pillar-header">
                <div class="pillar-header-name">{meta['icon']} {meta['label'].upper()}</div>
                <span class="pillar-header-tag {meta['tag_cls']}">{pk.upper()} · {p_earned}/{p_max} PTS</span>
              </div>
            </div>
            """, unsafe_allow_html=True)

            for t in tasks_p:
                tk = get_task_key(pk, t)
                c1, c2 = st.columns([5, 1])
                with c1:
                    st.checkbox(t["name"], key=f"cb_{tk}", help=f"+{t['pts']} pts")
                with c2:
                    st.markdown(
                        f'<div style="padding-top:0.45rem; font-family:JetBrains Mono,monospace; '
                        f'font-size:0.65rem; color:#f9c74f; font-weight:700;">+{t["pts"]}</div>',
                        unsafe_allow_html=True
                    )

            show_key = f"show_add_{pk}"
            if show_key not in st.session_state:
                st.session_state[show_key] = False

            ca, _ = st.columns([2, 5])
            with ca:
                if st.button(f"+ Add", key=f"btn_add_{pk}"):
                    st.session_state[show_key] = not st.session_state[show_key]

            if st.session_state[show_key]:
                c1, c2, c3 = st.columns([4, 1, 1])
                with c1:
                    new_name = st.text_input("Task", key=f"new_name_{pk}", placeholder="Task name", label_visibility="collapsed")
                with c2:
                    new_pts = st.number_input("Pts", min_value=1, max_value=50, value=10, key=f"new_pts_{pk}", label_visibility="collapsed")
                with c3:
                    if st.button("✓", key=f"save_{pk}"):
                        if new_name.strip():
                            cid = f"custom_{pk}_{len(data['custom_tasks'].get(pk, []))}"
                            if pk not in data["custom_tasks"]:
                                data["custom_tasks"][pk] = []
                            data["custom_tasks"][pk].append({"name": new_name.strip(), "pts": int(new_pts), "id": cid})
                            save_data(data)
                            st.session_state.data = data
                            st.session_state[show_key] = False
                            st.rerun()

            st.markdown("<div style='margin-bottom:0.5rem'></div>", unsafe_allow_html=True)

    st.markdown("---")
    col_ref, col_quote = st.columns([2, 1], gap="large")

    with col_ref:
        st.markdown('<div class="section-label">CEO REFLECTION LOG</div>', unsafe_allow_html=True)
        reflection = st.text_area(
            "WHAT DID I LEARN TODAY?",
            placeholder="Write your daily reflection...\n\nWhat worked? What would you do differently? What insight did you unlock today?",
            height=140,
        )
        c_btn, _ = st.columns([1, 3])
        with c_btn:
            if st.button("⟶  COMMIT DAY", use_container_width=True):
                if not reflection.strip():
                    st.warning("Add a reflection before committing the day.")
                else:
                    task_snap = {tk: st.session_state.get(f"cb_{tk}", False) for _, _, tk in task_list_flat}
                    record = {
                        "date": today.isoformat(),
                        "score": score_pct,
                        "raw_score": score,
                        "max_score": max_score,
                        "tasks": task_snap,
                        "reflection": reflection.strip(),
                    }
                    existing = [e["date"] for e in data["history"]]
                    if record["date"] in existing:
                        data["history"][existing.index(record["date"])] = record
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
                        background:rgba(34,197,94,0.08); border-left:4px solid #22c55e;
                        border-radius:8px; font-size:0.83rem; color:#4ade80; font-weight:600;">
              ✓ Day committed — entry saved
            </div>""", unsafe_allow_html=True)

    with col_quote:
        st.markdown('<div class="section-label">FOUNDER SIGNAL</div>', unsafe_allow_html=True)
        quote = random.choice(CEO_QUOTES)
        st.markdown(f"""
        <div class="quote-card">
          <div style="font-family:'Plus Jakarta Sans',sans-serif; font-size:0.93rem; line-height:1.8; color:#111827; font-style:italic; font-weight:500;">"{quote}"</div>
          <div style="margin-top:1rem; font-family:'JetBrains Mono',monospace; font-size:0.55rem; letter-spacing:0.2em; color:rgba(17,24,39,0.45); text-transform:uppercase;">— THE LONG GAME OS</div>
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — SCHEDULE
# ══════════════════════════════════════════════════════════════════════════════
with tab_schedule:
    st.markdown('<div class="section-label">TIME ALLOCATION SETTINGS</div>', unsafe_allow_html=True)

    cfg = data.get("schedule_config", dict(DEFAULT_DATA["schedule_config"]))

    col_s1, col_s2, col_s3, col_s4 = st.columns(4)
    with col_s1:
        wake_options = [f"{h:02d}:00" for h in range(4, 9)]
        wake_idx = wake_options.index(cfg.get("wake_time", "05:00")) if cfg.get("wake_time", "05:00") in wake_options else 1
        new_wake = st.selectbox("WAKE TIME", wake_options, index=wake_idx)
    with col_s2:
        skill_start_options = [f"{h:02d}:00" for h in range(5, 11)]
        ss_val = cfg.get("skill_start", "07:00")
        ss_idx = skill_start_options.index(ss_val) if ss_val in skill_start_options else 2
        new_skill_start = st.selectbox("SKILL BLOCK START", skill_start_options, index=ss_idx)
    with col_s3:
        new_skill_h = st.slider("SKILL HOURS / DAY", min_value=1.0, max_value=4.0, value=float(cfg.get("skill_hours", 2.0)), step=0.5)
    with col_s4:
        new_school_h = st.slider("SCHOOL / WORK HOURS", min_value=4.0, max_value=10.0, value=float(cfg.get("school_hours", 6.0)), step=0.5)

    if st.button("SAVE SCHEDULE CONFIG"):
        data["schedule_config"] = {
            "wake_time":   new_wake,
            "skill_start": new_skill_start,
            "skill_hours": new_skill_h,
            "school_hours": new_school_h,
        }
        save_data(data)
        st.session_state.data = data
        cfg = data["schedule_config"]
        st.success("Schedule saved.")
        st.rerun()

    # Time budget summary
    skill_h   = float(cfg.get("skill_hours", 2.0))
    school_h  = float(cfg.get("school_hours", 6.0))
    sleep_h   = 7.0
    life_h    = 9.0
    buffer_h  = 24.0 - skill_h - school_h - sleep_h - life_h
    buffer_h  = max(0, buffer_h)

    budget_html = f"""
    <div style="display:grid; grid-template-columns:repeat(6,1fr); gap:10px; margin:1.25rem 0 2rem;">
      <div class="stat-card"><div class="stat-label">Skill block</div><div class="stat-value" style="color:#378ADD">{skill_h:.1f}h</div></div>
      <div class="stat-card"><div class="stat-label">School / work</div><div class="stat-value" style="color:#3B6D11">{school_h:.1f}h</div></div>
      <div class="stat-card"><div class="stat-label">Sleep</div><div class="stat-value" style="color:#534AB7">7h</div></div>
      <div class="stat-card"><div class="stat-label">Life duties</div><div class="stat-value" style="color:#854F0B">9h</div></div>
      <div class="stat-card"><div class="stat-label">Buffer / rest</div><div class="stat-value" style="color:#888780">{buffer_h:.1f}h</div></div>
      <div class="stat-card"><div class="stat-label">Total</div><div class="stat-value">24h</div></div>
    </div>"""
    st.markdown(budget_html, unsafe_allow_html=True)

    st.markdown('<div class="section-label">DAILY SCHEDULE — SELECT DAY</div>', unsafe_allow_html=True)

    day_list   = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    sel_day_idx = day_list.index(day_abbr) if day_abbr in day_list else 0
    sel_day     = st.radio("Day", day_list, index=sel_day_idx, horizontal=True, label_visibility="collapsed")

    blocks = build_schedule(cfg, sel_day)

    st.markdown('<div style="background:#1e293b; border-radius:14px; padding:1.5rem; border:1px solid rgba(255,255,255,0.07);">', unsafe_allow_html=True)
    for b in blocks:
        st.markdown(f"""
        <div class="schedule-block">
          <div class="schedule-time">{b['time']}</div>
          <div class="schedule-content" style="background:{b['bg']}; border-left-color:{b['color']}">
            <div class="schedule-title">{b['title']}</div>
            <div class="schedule-meta">{b['meta']}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Legend
    st.markdown("""
    <div style="display:flex; gap:1.5rem; margin-top:1rem; font-family:'JetBrains Mono',monospace; font-size:0.6rem; color:rgba(255,255,255,0.35); letter-spacing:0.1em; flex-wrap:wrap;">
      <span><span style="display:inline-block;width:10px;height:10px;border-radius:2px;background:#378ADD;vertical-align:middle;margin-right:5px"></span>SKILL</span>
      <span><span style="display:inline-block;width:10px;height:10px;border-radius:2px;background:#3B6D11;vertical-align:middle;margin-right:5px"></span>SCHOOL</span>
      <span><span style="display:inline-block;width:10px;height:10px;border-radius:2px;background:#854F0B;vertical-align:middle;margin-right:5px"></span>LIFE</span>
      <span><span style="display:inline-block;width:10px;height:10px;border-radius:2px;background:#fb7185;vertical-align:middle;margin-right:5px"></span>MASTERY</span>
      <span><span style="display:inline-block;width:10px;height:10px;border-radius:2px;background:#888780;vertical-align:middle;margin-right:5px"></span>BUFFER</span>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — 5-YEAR GROWTH
# ══════════════════════════════════════════════════════════════════════════════
with tab_growth:
    st.markdown('<div class="section-label">PROJECTED 5-YEAR SKILL GROWTH</div>', unsafe_allow_html=True)

    cfg_g     = data.get("schedule_config", DEFAULT_DATA["schedule_config"])
    skill_h_g = float(cfg_g.get("skill_hours", 2.0))

    # Calculate projected hours per skill
    total_skill_hours_per_week = skill_h_g * 5 + (skill_h_g * 2) + 2  # Mon-Fri + Sat double + Sun review
    skill_ratios = {"Coding": 3, "Charts": 2, "Communication": 2, "Finance": 1, "Art": 2}
    ratio_sum = sum(skill_ratios.values())

    weekly_per_skill = {k: (v / ratio_sum) * total_skill_hours_per_week for k, v in skill_ratios.items()}
    yearly_per_skill = {k: v * 52 for k, v in weekly_per_skill.items()}

    years = [0, 1, 2, 3, 4, 5]

    # Stat summary row
    total_5yr = round(skill_h_g * 365 * 5)
    coding_5yr = round(yearly_per_skill["Coding"] * 5)
    days_tracked = len(data["history"])
    actual_hours = round(days_tracked * skill_h_g)

    st.markdown(f"""
    <div style="display:grid; grid-template-columns:repeat(4,1fr); gap:10px; margin-bottom:2rem;">
      <div class="stat-card"><div class="stat-label">5-Year Total Hours</div><div class="stat-value" style="color:#f9c74f">{total_5yr:,}</div><div class="stat-unit">All skills combined</div></div>
      <div class="stat-card"><div class="stat-label">Coding Hours (5yr)</div><div class="stat-value" style="color:#378ADD">{coding_5yr:,}</div><div class="stat-unit">Primary leverage skill</div></div>
      <div class="stat-card"><div class="stat-label">Days Tracked</div><div class="stat-value" style="color:#4ade80">{days_tracked}</div><div class="stat-unit">Real sessions logged</div></div>
      <div class="stat-card"><div class="stat-label">Hours Invested</div><div class="stat-value" style="color:#c084fc">{actual_hours}</div><div class="stat-unit">Actual @ {skill_h_g:.1f}h/day</div></div>
    </div>""", unsafe_allow_html=True)

    # Growth chart using Plotly via streamlit
    try:
        import plotly.graph_objects as go

        fig = go.Figure()
        for skill, color in SKILL_COLORS.items():
            y_vals = [round(yearly_per_skill[skill] * yr) for yr in years]
            fig.add_trace(go.Scatter(
                x=[f"Year {y}" if y > 0 else "Now" for y in years],
                y=y_vals,
                name=skill,
                line=dict(color=color, width=2.5),
                mode="lines+markers",
                marker=dict(size=7),
                fill="tozeroy",
                fillcolor=color.replace("#", "rgba(") + ",0.05)" if "#" in color else color,
            ))
            # Override fill properly
            fig.data[-1].fillcolor = f"rgba({int(color[1:3],16)},{int(color[3:5],16)},{int(color[5:7],16)},0.06)"

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="JetBrains Mono", color="rgba(255,255,255,0.5)", size=11),
            legend=dict(
                orientation="h",
                yanchor="bottom", y=1.02,
                xanchor="left", x=0,
                font=dict(size=11),
                bgcolor="rgba(0,0,0,0)",
            ),
            xaxis=dict(gridcolor="rgba(255,255,255,0.06)", showline=False, tickfont=dict(size=11)),
            yaxis=dict(gridcolor="rgba(255,255,255,0.06)", showline=False, title="Cumulative Hours", titlefont=dict(size=10)),
            margin=dict(l=10, r=10, t=40, b=10),
            height=320,
        )
        st.plotly_chart(fig, use_container_width=True)
    except ImportError:
        # Fallback: simple bar chart with st metrics
        st.info("Install plotly for the growth chart: pip install plotly")
        for skill, color in SKILL_COLORS.items():
            yr5 = round(yearly_per_skill[skill] * 5)
            pct = min(100, round((yr5 / 1500) * 100))
            st.markdown(f"""
            <div style="display:flex; align-items:center; gap:12px; margin-bottom:10px;">
              <div style="width:120px; font-family:'JetBrains Mono',monospace; font-size:0.65rem; color:{color}">{skill.upper()}</div>
              <div style="flex:1; background:rgba(255,255,255,0.07); border-radius:99px; height:8px; overflow:hidden">
                <div style="width:{pct}%; height:100%; background:{color}; border-radius:99px"></div>
              </div>
              <div style="width:60px; font-family:'Bebas Neue',sans-serif; font-size:1rem; color:{color}">{yr5}h</div>
            </div>""", unsafe_allow_html=True)

    # Proficiency bars at year 5
    st.markdown('<div class="section-label" style="margin-top:1.5rem">PROJECTED PROFICIENCY AT YEAR 5</div>', unsafe_allow_html=True)
    proficiency = {"Coding": 92, "Charts": 80, "Communication": 81, "Finance": 62, "Art": 78}
    prof_desc   = {
        "Coding":        f"~{round(yearly_per_skill['Coding']*5):,}h · elite builder · fintech systems",
        "Charts":        f"~{round(yearly_per_skill['Charts']*5):,}h · strong analyst · visual finance",
        "Communication": f"~{round(yearly_per_skill['Communication']*5):,}h · confident speaker · pitching",
        "Finance":       f"~{round(yearly_per_skill['Finance']*5):,}h · solid foundation · BCom + practice",
        "Art":           f"~{round(yearly_per_skill['Art']*5):,}h · distinct identity · creative brand",
    }

    bars_html = ""
    for skill, pct in proficiency.items():
        color = SKILL_COLORS[skill]
        actual_pct = min(100, round(pct * (skill_h_g / 2.0)))
        bars_html += f"""
        <div style="display:flex; align-items:center; gap:12px; margin-bottom:10px;">
          <div style="width:130px; font-family:'JetBrains Mono',monospace; font-size:0.62rem; color:{color}; text-transform:uppercase;">{skill}</div>
          <div style="flex:1; background:rgba(255,255,255,0.07); border-radius:99px; height:8px; overflow:hidden">
            <div style="width:{actual_pct}%; height:100%; background:{color}; border-radius:99px;"></div>
          </div>
          <div style="width:38px; font-family:'Bebas Neue',sans-serif; font-size:1.1rem; color:{color}; text-align:right">{actual_pct}%</div>
          <div style="font-family:'JetBrains Mono',monospace; font-size:0.55rem; color:rgba(255,255,255,0.35); flex:1">{prof_desc[skill]}</div>
        </div>"""

    st.markdown(f'<div style="background:#1e293b; border-radius:12px; padding:1.5rem; border:1px solid rgba(255,255,255,0.07);">{bars_html}</div>', unsafe_allow_html=True)

    # Milestones
    st.markdown('<div class="section-label" style="margin-top:2rem">YEAR-BY-YEAR MILESTONES</div>', unsafe_allow_html=True)

    for yr, ms in MILESTONES.items():
        hrs_logged = round(yearly_per_skill.get("Coding", 0) * yr)
        items_html = "".join(f'<div style="font-family:Plus Jakarta Sans,sans-serif; font-size:0.8rem; color:rgba(255,255,255,0.65); padding:3px 0; padding-left:14px; position:relative"><span style="position:absolute;left:0;color:{ms[\'color\']}">›</span>{item}</div>' for item in ms["items"])

        col_yr, col_content = st.columns([1, 4], gap="small")
        with col_yr:
            st.markdown(f"""
            <div style="background:#1e293b; border-radius:10px; padding:1.1rem; border:1px solid rgba(255,255,255,0.07); border-top:3px solid {ms['color']}; text-align:center; height:100%">
              <div style="font-family:'JetBrains Mono',monospace; font-size:0.55rem; color:rgba(255,255,255,0.3); letter-spacing:0.2em; text-transform:uppercase">Year</div>
              <div style="font-family:'Bebas Neue',sans-serif; font-size:3.5rem; color:{ms['color']}; line-height:1">{yr}</div>
              <div style="font-family:'Bebas Neue',sans-serif; font-size:1.1rem; color:{ms['color']}; letter-spacing:0.1em">{ms['title']}</div>
              <div style="font-family:'JetBrains Mono',monospace; font-size:0.55rem; color:rgba(255,255,255,0.25); margin-top:0.5rem">{hrs_logged:,}h coding</div>
            </div>
            """, unsafe_allow_html=True)
        with col_content:
            st.markdown(f"""
            <div style="background:#1e293b; border-radius:10px; padding:1.25rem; border:1px solid rgba(255,255,255,0.07); height:100%">
              {items_html}
            </div>
            """, unsafe_allow_html=True)
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # Hidden formula
    st.markdown("""
    <div style="margin-top:2rem; background:#1e293b; border-radius:12px; padding:1.5rem 2rem; border:1px solid rgba(255,255,255,0.07); text-align:center;">
      <div style="font-family:'JetBrains Mono',monospace; font-size:0.58rem; letter-spacing:0.3em; text-transform:uppercase; color:rgba(255,255,255,0.25); margin-bottom:1rem">THE HIDDEN FORMULA</div>
      <div style="display:flex; justify-content:center; gap:2rem; flex-wrap:wrap;">
        <div style="text-align:center"><div style="font-family:'Bebas Neue',sans-serif; font-size:1.5rem; color:#378ADD; letter-spacing:0.1em">CODE</div><div style="font-family:'JetBrains Mono',monospace; font-size:0.6rem; color:rgba(255,255,255,0.3); letter-spacing:0.15em">= BUILD</div></div>
        <div style="font-family:'Bebas Neue',sans-serif; font-size:1.5rem; color:rgba(255,255,255,0.15); align-self:center">+</div>
        <div style="text-align:center"><div style="font-family:'Bebas Neue',sans-serif; font-size:1.5rem; color:#1D9E75; letter-spacing:0.1em">CHARTS</div><div style="font-family:'JetBrains Mono',monospace; font-size:0.6rem; color:rgba(255,255,255,0.3); letter-spacing:0.15em">= UNDERSTAND</div></div>
        <div style="font-family:'Bebas Neue',sans-serif; font-size:1.5rem; color:rgba(255,255,255,0.15); align-self:center">+</div>
        <div style="text-align:center"><div style="font-family:'Bebas Neue',sans-serif; font-size:1.5rem; color:#D85A30; letter-spacing:0.1em">COMMS</div><div style="font-family:'JetBrains Mono',monospace; font-size:0.6rem; color:rgba(255,255,255,0.3); letter-spacing:0.15em">= INFLUENCE</div></div>
        <div style="font-family:'Bebas Neue',sans-serif; font-size:1.5rem; color:rgba(255,255,255,0.15); align-self:center">+</div>
        <div style="text-align:center"><div style="font-family:'Bebas Neue',sans-serif; font-size:1.5rem; color:#534AB7; letter-spacing:0.1em">FINANCE</div><div style="font-family:'JetBrains Mono',monospace; font-size:0.6rem; color:rgba(255,255,255,0.3); letter-spacing:0.15em">= DECIDE</div></div>
        <div style="font-family:'Bebas Neue',sans-serif; font-size:1.5rem; color:rgba(255,255,255,0.15); align-self:center">+</div>
        <div style="text-align:center"><div style="font-family:'Bebas Neue',sans-serif; font-size:1.5rem; color:#BA7517; letter-spacing:0.1em">ART</div><div style="font-family:'JetBrains Mono',monospace; font-size:0.6rem; color:rgba(255,255,255,0.3); letter-spacing:0.15em">= DIFFERENTIATE</div></div>
        <div style="font-family:'Bebas Neue',sans-serif; font-size:1.5rem; color:rgba(255,255,255,0.15); align-self:center">=</div>
        <div style="text-align:center"><div style="font-family:'Bebas Neue',sans-serif; font-size:1.5rem; color:#f9c74f; letter-spacing:0.1em">FOUNDER LEVERAGE</div><div style="font-family:'JetBrains Mono',monospace; font-size:0.6rem; color:rgba(255,255,255,0.3); letter-spacing:0.15em">THE REAL GOAL</div></div>
      </div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — WEEKLY
# ══════════════════════════════════════════════════════════════════════════════
with tab_weekly:
    st.markdown('<div class="section-label">WEEKLY PERFORMANCE</div>', unsafe_allow_html=True)

    week_start = today - datetime.timedelta(days=today.weekday())
    week_days  = [week_start + datetime.timedelta(days=i) for i in range(7)]
    day_labels = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]

    MAX_BAR = 120
    bars_html = f'<div style="display:flex; align-items:flex-end; gap:8px; height:{MAX_BAR+40}px;">'
    for i, d in enumerate(week_days):
        entry    = history_map.get(d.isoformat())
        is_today = (d == today)
        border   = "border: 2px solid #f9c74f;" if is_today else ""
        if entry:
            sc = entry["score"]
            px = max(6, int((sc / 100) * MAX_BAR))
            bg = "linear-gradient(180deg,#4ade80,#22c55e)" if sc >= 85 else ("linear-gradient(180deg,#f9c74f,#f8961e)" if sc >= 60 else "linear-gradient(180deg,#fca5a5,#ef4444)")
            lbl = f'<div style="font-family:JetBrains Mono,monospace;font-size:0.6rem;color:rgba(255,255,255,0.6);text-align:center;margin-bottom:4px">{sc}</div>'
        else:
            px, bg, lbl = 4, "rgba(255,255,255,0.07)", '<div style="height:18px"></div>'

        bars_html += f"""
        <div style="flex:1; display:flex; flex-direction:column; align-items:center; justify-content:flex-end; height:100%">
          {lbl}
          <div style="width:100%; height:{px}px; background:{bg}; border-radius:5px 5px 0 0; {border} box-sizing:border-box;"></div>
          <div style="font-family:JetBrains Mono,monospace; font-size:0.55rem; color:{'#f9c74f' if is_today else 'rgba(255,255,255,0.3)'}; letter-spacing:0.1em; margin-top:6px; text-transform:uppercase; font-weight:{'700' if is_today else '400'}">{day_labels[i]}</div>
        </div>"""
    bars_html += "</div>"

    col_w1, col_w2 = st.columns([2, 1], gap="large")
    with col_w1:
        st.markdown(f'<div style="background:#1e293b; border-radius:12px; padding:1.5rem; border:1px solid rgba(255,255,255,0.07);"><div class="analytics-card-title">SCORE BY DAY — CURRENT WEEK</div>{bars_html}</div>', unsafe_allow_html=True)
    with col_w2:
        week_entries = [history_map[d.isoformat()] for d in week_days if d.isoformat() in history_map]
        days_log     = len(week_entries)
        w_avg        = round(sum(e["score"] for e in week_entries) / days_log, 0) if week_entries else 0
        elite_d      = sum(1 for e in week_entries if e["score"] >= 85)

        st.markdown(f"""
        <div class="analytics-card">
          <div class="analytics-card-title">WEEK SUMMARY</div>
          <div style="margin-bottom:1.2rem"><div class="stat-label">Days Logged</div>
            <div style="font-family:'Bebas Neue',sans-serif; font-size:2.6rem; color:#f1f5f9; line-height:1">{days_log}<span style="font-size:1.2rem; color:rgba(255,255,255,0.3)"> / 7</span></div></div>
          <div style="margin-bottom:1.2rem"><div class="stat-label">Weekly Average</div>
            <div style="font-family:'Bebas Neue',sans-serif; font-size:2.6rem; color:#f9c74f; line-height:1">{int(w_avg)}</div></div>
          <div><div class="stat-label">Elite Days (85+)</div>
            <div style="font-family:'Bebas Neue',sans-serif; font-size:2.6rem; color:#4ade80; line-height:1">{elite_d}</div></div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-label">PILLAR PERFORMANCE — THIS WEEK</div>', unsafe_allow_html=True)

    col_pillars = st.columns(len(PILLAR_META), gap="small")
    for i, (pk, meta) in enumerate(PILLAR_META.items()):
        tasks_p       = all_tasks[pk]
        total_possible = sum(t["pts"] for t in tasks_p) * max(1, days_log)
        total_earned   = sum(
            t["pts"]
            for entry in week_entries
            for t in tasks_p
            if entry.get("tasks", {}).get(get_task_key(pk, t), False)
        )
        cpct = round((total_earned / total_possible) * 100) if total_possible > 0 else 0
        with col_pillars[i]:
            st.markdown(f"""
            <div style="background:#1e293b; border-radius:10px; padding:1.1rem; border:1px solid rgba(255,255,255,0.07); text-align:center;">
              <div style="font-size:1.4rem; margin-bottom:0.4rem">{meta['icon']}</div>
              <div style="font-family:'JetBrains Mono',monospace; font-size:0.52rem; color:rgba(255,255,255,0.35); letter-spacing:0.12em; text-transform:uppercase; margin-bottom:0.5rem">{pk}</div>
              <div style="font-family:'Bebas Neue',sans-serif; font-size:1.8rem; color:{meta['color']}; line-height:1">{cpct}%</div>
              <div style="background:rgba(255,255,255,0.07); border-radius:99px; height:4px; margin-top:0.5rem; overflow:hidden">
                <div style="height:100%; width:{cpct}%; background:{meta['color']}; border-radius:99px"></div>
              </div>
            </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — HABIT MAP
# ══════════════════════════════════════════════════════════════════════════════
with tab_habits:
    st.markdown('<div class="section-label">HABIT CONSISTENCY MAP — LAST 30 DAYS</div>', unsafe_allow_html=True)

    last_30 = [today - datetime.timedelta(days=i) for i in range(29, -1, -1)]

    st.markdown('<div style="background:#1e293b; border-radius:14px; padding:1.5rem; border:1px solid rgba(255,255,255,0.07)">', unsafe_allow_html=True)
    for pk, meta in PILLAR_META.items():
        for t in all_tasks[pk]:
            tk         = get_task_key(pk, t)
            cells_html = '<div style="display:flex; gap:3px; flex-wrap:wrap;">'
            done_count = 0
            for d in last_30:
                entry = history_map.get(d.isoformat())
                if entry:
                    done = entry.get("tasks", {}).get(tk, False)
                    cls  = "habit-done" if done else "habit-miss"
                    if done: done_count += 1
                else:
                    cls = "habit-na"
                cells_html += f'<div class="habit-cell {cls}" title="{d.strftime("%d %b")}"></div>'
            cells_html += "</div>"

            pct = round((done_count / 30) * 100)
            st.markdown(f"""
            <div style="display:flex; align-items:center; gap:0.75rem; margin-bottom:0.6rem; padding:0.5rem 0; border-bottom:1px solid rgba(255,255,255,0.04)">
              <div style="width:170px; flex-shrink:0">
                <div style="font-family:'JetBrains Mono',monospace; font-size:0.55rem; color:{meta['color']}; letter-spacing:0.1em; text-transform:uppercase">{pk.upper()}</div>
                <div style="font-family:'Plus Jakarta Sans',sans-serif; font-size:0.78rem; color:rgba(255,255,255,0.7); font-weight:500; margin-top:1px">{t['name']}</div>
              </div>
              {cells_html}
              <div style="font-family:'Bebas Neue',sans-serif; font-size:1.2rem; color:{meta['color']}; margin-left:0.5rem; min-width:42px">{pct}%</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="display:flex; gap:1.5rem; margin-top:1rem; font-family:'JetBrains Mono',monospace; font-size:0.6rem; color:rgba(255,255,255,0.3); letter-spacing:0.12em">
      <span><span style="display:inline-block;width:12px;height:12px;border-radius:3px;background:#f8961e;vertical-align:middle;margin-right:5px"></span>COMPLETED</span>
      <span><span style="display:inline-block;width:12px;height:12px;border-radius:3px;background:rgba(255,255,255,0.07);vertical-align:middle;margin-right:5px"></span>MISSED</span>
      <span><span style="display:inline-block;width:12px;height:12px;border-radius:3px;border:1px dashed rgba(255,255,255,0.15);vertical-align:middle;margin-right:5px"></span>NOT LOGGED</span>
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 6 — HISTORY
# ══════════════════════════════════════════════════════════════════════════════
with tab_history:
    st.markdown('<div class="section-label">MISSION LOG — SESSION HISTORY</div>', unsafe_allow_html=True)

    if data["history"]:
        df = pd.DataFrame([{
            "Date":       e["date"],
            "Score":      e["score"],
            "Rating":     "⚡ ELITE" if e["score"] >= 85 else ("✓ SOLID" if e["score"] >= 60 else "↺ RESET"),
            "Tasks Done": sum(1 for v in e.get("tasks", {}).values() if v),
            "Reflection": (e["reflection"][:90] + "…") if len(e.get("reflection", "")) > 90 else e.get("reflection", ""),
        } for e in sorted(data["history"], key=lambda x: x["date"], reverse=True)])

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={"Score": st.column_config.ProgressColumn("Score", min_value=0, max_value=100, format="%d")},
        )

        if st.button("↺  CLEAR ALL HISTORY"):
            data.update({"history": [], "streak": 0, "best_score": 0, "total_days": 0})
            save_data(data)
            st.session_state.data = data
            st.session_state.saved_today = False
            st.rerun()
    else:
        st.markdown("""
        <div style="text-align:center; padding:4rem 2rem; color:rgba(255,255,255,0.2);
                    font-family:'JetBrains Mono',monospace; font-size:0.75rem; letter-spacing:0.2em">
          NO SESSIONS LOGGED YET — COMMIT YOUR FIRST DAY TO BEGIN
        </div>""", unsafe_allow_html=True)


# ── FOOTER ─────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="margin-top:3rem; padding-top:1.5rem; border-top:1px solid rgba(255,255,255,0.06);
            display:flex; justify-content:space-between; align-items:center;
            font-family:'JetBrains Mono',monospace; font-size:0.58rem;
            letter-spacing:0.2em; color:rgba(255,255,255,0.18); text-transform:uppercase;">
  <span>THE LONG GAME — LIFE OS · BCOM FINANCE + FOUNDER STACK</span>
  <span>BUILD · REFLECT · EVOLVE</span>
  <span>V5.0 · {today_str}</span>
</div>
""", unsafe_allow_html=True)