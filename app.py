import streamlit as st
import pandas as pd
import json
import datetime
import os
import random

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="The Long Game — Life OS",
    layout="wide",
    initial_sidebar_state="collapsed",
    page_icon="⚡",
)

# ── CSS: Warm light theme — navy page, cream cards, strong contrast ───────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;700&family=Bebas+Neue&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

/* ── Global Reset ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

/* ── Page background: deep navy-slate ── */
html, body, [class*="css"], .stApp {
    font-family: 'Plus Jakarta Sans', sans-serif;
    background-color: #1b2340 !important;
    color: #1e2a3a !important;
}

/* ── Main container ── */
.main .block-container {
    padding: 2rem 2.5rem 4rem;
    max-width: 1400px;
    background-color: #1b2340 !important;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ── Hero header — sits on navy, white text ── */
.hero-header {
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    padding: 0 0 2.5rem;
    border-bottom: 2px solid rgba(255,255,255,0.08);
    margin-bottom: 2.5rem;
    animation: fadeIn 0.6s ease;
}
.hero-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 5rem;
    letter-spacing: 0.08em;
    line-height: 1;
    background: linear-gradient(135deg, #f9c74f 0%, #f8961e 60%, #f3722c 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-sub {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    color: rgba(255,255,255,0.45);
    letter-spacing: 0.22em;
    text-transform: uppercase;
    margin-top: 0.4rem;
}
.hero-date {
    text-align: right;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    color: rgba(255,255,255,0.35);
    letter-spacing: 0.15em;
    text-transform: uppercase;
    line-height: 2;
}
.hero-date span {
    display: block;
    color: #f9c74f;
    font-size: 1.15rem;
    font-weight: 700;
    letter-spacing: 0.04em;
}

/* ── Section headers ── */
.section-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    color: #f9c74f;
    margin-bottom: 1.2rem;
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

/* ── STAT CARDS — white cards on navy ── */
.stat-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin-bottom: 2.5rem;
}
.stat-card {
    background: #ffffff;
    border-radius: 12px;
    padding: 1.4rem 1.5rem;
    box-shadow: 0 4px 24px rgba(0,0,0,0.25);
    animation: fadeIn 0.5s ease;
    position: relative;
    overflow: hidden;
}
.stat-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 4px;
    background: linear-gradient(90deg, #f9c74f, #f8961e);
}
.stat-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #7c8db0;
    margin-bottom: 0.5rem;
}
.stat-value {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.6rem;
    letter-spacing: 0.04em;
    color: #1b2340;
    line-height: 1;
}
.stat-unit {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.6rem;
    color: #a0aec0;
    margin-top: 0.2rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}

/* ── SCORE CARD ── */
.score-card {
    background: #ffffff;
    border-radius: 12px;
    padding: 2rem 1.75rem;
    box-shadow: 0 4px 24px rgba(0,0,0,0.25);
    position: relative;
    overflow: hidden;
    animation: fadeIn 0.5s ease;
}
.score-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 5px;
    background: linear-gradient(90deg, #f9c74f, #f8961e, #f3722c);
}
.score-number {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 9rem;
    line-height: 1;
    letter-spacing: 0.02em;
    background: linear-gradient(135deg, #f8961e, #f3722c);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.score-denom {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1rem;
    color: #a0aec0;
    margin-top: -0.5rem;
    letter-spacing: 0.1em;
}
.score-verdict {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.4rem;
    letter-spacing: 0.1em;
    margin-top: 0.75rem;
}
.verdict-elite { color: #22c55e; }
.verdict-solid { color: #f8961e; }
.verdict-reset { color: #ef4444; }

/* ── Progress bar ── */
.progress-track {
    background: #edf2f7;
    border-radius: 99px;
    height: 8px;
    margin-top: 1.25rem;
    overflow: hidden;
    width: 100%;
}
.progress-fill {
    height: 100%;
    border-radius: 99px;
    transition: width 0.9s cubic-bezier(0.25, 1, 0.5, 1);
}
.progress-fill-elite { background: linear-gradient(90deg, #22c55e, #4ade80); }
.progress-fill-solid { background: linear-gradient(90deg, #f8961e, #f9c74f); }
.progress-fill-reset { background: linear-gradient(90deg, #ef4444, #fca5a5); }

/* ── TASK PANEL — white card ── */
.task-panel {
    background: #ffffff;
    border-radius: 12px;
    padding: 1.5rem 1.75rem;
    box-shadow: 0 4px 24px rgba(0,0,0,0.25);
}
.task-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.85rem 0;
    border-bottom: 1px solid #edf2f7;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 0.875rem;
    font-weight: 500;
    transition: all 0.15s;
}
.task-row:last-child { border-bottom: none; }
.task-row:hover { background: #fffbf0; border-radius: 6px; padding-left: 0.5rem; padding-right: 0.5rem; }
.task-tag {
    background: #f0f4ff;
    border-radius: 4px;
    padding: 0.2rem 0.55rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.58rem;
    color: #7c8db0;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}
.task-pts {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    font-weight: 700;
    margin-left: 0.75rem;
    min-width: 2.5rem;
    text-align: right;
}

/* ── PILLAR CARDS ── */
.pillar-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 1rem;
    margin-top: 0.5rem;
}
.pillar-card {
    background: #ffffff;
    border-radius: 12px;
    padding: 1.4rem 1.2rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.2);
    position: relative;
    overflow: hidden;
    transition: transform 0.2s, box-shadow 0.2s;
    animation: fadeIn 0.6s ease;
}
.pillar-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 30px rgba(0,0,0,0.3);
}
.pillar-card::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 4px;
    border-radius: 0 0 12px 12px;
}
.pillar-very-high::after { background: linear-gradient(90deg, #f9c74f, #f8961e); }
.pillar-high::after       { background: linear-gradient(90deg, #22c55e, #4ade80); }
.pillar-medium::after     { background: linear-gradient(90deg, #3b82f6, #60a5fa); }
.pillar-low::after        { background: #cbd5e0; }

.pillar-name {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #a0aec0;
    margin-bottom: 0.6rem;
    line-height: 1.5;
}
.pillar-level {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.6rem;
    letter-spacing: 0.08em;
}
.level-very-high { color: #f8961e; }
.level-high       { color: #22c55e; }
.level-medium     { color: #3b82f6; }
.level-low        { color: #a0aec0; }

/* ── REFLECTION CARD ── */
.reflection-card {
    background: #ffffff;
    border-radius: 12px;
    padding: 1.75rem;
    box-shadow: 0 4px 24px rgba(0,0,0,0.25);
}
.stTextArea textarea {
    background: #f8faff !important;
    border: 1.5px solid #e2e8f0 !important;
    border-radius: 8px !important;
    color: #1e2a3a !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.9rem !important;
    line-height: 1.8 !important;
    padding: 1rem !important;
    transition: border-color 0.2s !important;
}
.stTextArea textarea:focus {
    border-color: #f8961e !important;
    box-shadow: 0 0 0 3px rgba(248,150,30,0.12) !important;
}
.stTextArea textarea::placeholder { color: #a0aec0 !important; }
.stTextArea label {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.65rem !important;
    letter-spacing: 0.18em !important;
    text-transform: uppercase !important;
    color: #7c8db0 !important;
    font-weight: 600 !important;
}

/* ── CHECKBOXES — must be visible on navy background ── */
.stCheckbox {
    background: rgba(255,255,255,0.06);
    border-radius: 8px;
    padding: 0.6rem 0.75rem;
    margin-bottom: 0.3rem;
    transition: background 0.15s;
}
.stCheckbox:hover { background: rgba(255,255,255,0.1); }
.stCheckbox label {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.9rem !important;
    font-weight: 500 !important;
    color: #e2eaf8 !important;
}
.stCheckbox label p { color: #e2eaf8 !important; }

/* ── BUTTONS ── */
.stButton > button {
    background: linear-gradient(135deg, #f9c74f, #f8961e) !important;
    border: none !important;
    border-radius: 8px !important;
    color: #1b2340 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.8rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    padding: 0.65rem 1.5rem !important;
    transition: all 0.2s !important;
    box-shadow: 0 2px 12px rgba(248,150,30,0.35) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(248,150,30,0.45) !important;
}

/* ── DIVIDER ── */
hr { border-color: rgba(255,255,255,0.08) !important; margin: 2rem 0 !important; }

/* ── QUOTE CARD ── */
.quote-card {
    background: linear-gradient(135deg, #f9c74f 0%, #f8961e 100%);
    border-radius: 12px;
    padding: 1.75rem;
    box-shadow: 0 4px 24px rgba(248,150,30,0.35);
}

/* ── ANIMATIONS ── */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
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

/* ── DATAFRAME ── */
.stDataFrame {
    background: #ffffff !important;
    border-radius: 12px !important;
    overflow: hidden !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.2) !important;
}
.stDataFrame table { font-family: 'Plus Jakarta Sans', sans-serif !important; font-size: 0.82rem !important; }
.stDataFrame th { background: #f8faff !important; color: #7c8db0 !important; font-size: 0.7rem !important; letter-spacing: 0.1em !important; }
.stDataFrame td { color: #1e2a3a !important; }

/* ── ALERTS ── */
.stAlert { border-radius: 8px !important; border: none !important; }
</style>
""", unsafe_allow_html=True)


# ── Persistence helpers ────────────────────────────────────────────────────────
DATA_FILE = "life_os_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"history": [], "streak": 0, "best_score": 0, "total_days": 0}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


# ── Task definitions ──────────────────────────────────────────────────────────
TASKS = [
    {"key": "morning",  "label": "Morning Routine",       "tag": "FOUNDATION", "pts": 15},
    {"key": "workout",  "label": "Workout / Health",       "tag": "HEALTH",     "pts": 15},
    {"key": "finance",  "label": "Finance Review",         "tag": "WEALTH",     "pts": 20},
    {"key": "skill",    "label": "Skill Development",      "tag": "GROWTH",     "pts": 20},
    {"key": "tlg",      "label": "TLG Project Progress",   "tag": "MISSION",    "pts": 20},
    {"key": "reflect",  "label": "Night Reflection",       "tag": "MASTERY",    "pts": 10},
]

PILLARS = [
    {"name": "Personal\nFoundation", "level": "Very High",  "cls": "very-high"},
    {"name": "Financial\nLife",       "level": "High",       "cls": "high"},
    {"name": "Career +\nAcademics",   "level": "Medium",     "cls": "medium"},
    {"name": "TLG\nProject",          "level": "Very High",  "cls": "very-high"},
    {"name": "Skill\nStack",          "level": "Very High",  "cls": "very-high"},
]

CEO_QUOTES = [
    "The system you build today runs the life you'll live tomorrow.",
    "Discipline is the bridge between goals and accomplishment.",
    "Every day is a vote for who you are becoming.",
    "Execution is the strategy that beats all strategies.",
    "Your future self is watching every decision you make today.",
    "The Long Game is won by showing up when it's inconvenient.",
]


# ── State init ────────────────────────────────────────────────────────────────
if "data" not in st.session_state:
    st.session_state.data = load_data()
if "saved_today" not in st.session_state:
    st.session_state.saved_today = False


data = st.session_state.data
today_str = datetime.date.today().strftime("%d %b %Y").upper()
day_name  = datetime.date.today().strftime("%A").upper()


# ══════════════════════════════════════════════════════════════════════════════
# HERO HEADER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="hero-header">
  <div>
    <div class="hero-title">THE LONG GAME</div>
    <div class="hero-sub">⚡ Life Operating System &nbsp;·&nbsp; Founder Edition</div>
  </div>
  <div class="hero-date">
    <span class="live-dot"></span> LIVE SESSION
    <span>{day_name}</span>
    {today_str}
  </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# STATS ROW
# ══════════════════════════════════════════════════════════════════════════════
best  = data.get("best_score", 0)
total = data.get("total_days", 0)
streak = data.get("streak", 0)
avg_score = round(
    sum(e["score"] for e in data["history"]) / len(data["history"]), 0
) if data["history"] else 0

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


# ══════════════════════════════════════════════════════════════════════════════
# MAIN LAYOUT: Score (left) | Tasks (right)
# ══════════════════════════════════════════════════════════════════════════════
col_score, col_tasks = st.columns([1, 2], gap="large")

# ── Task checkboxes ───────────────────────────────────────────────────────────
with col_tasks:
    st.markdown('<div class="section-label">DAILY EXECUTION PROTOCOL</div>', unsafe_allow_html=True)
    checked = {}
    for t in TASKS:
        checked[t["key"]] = st.checkbox(
            f"{t['label']}   [ {t['pts']} pts ]",
            key=f"task_{t['key']}"
        )

score = sum(t["pts"] for t in TASKS if checked.get(t["key"]))

# ── Score display ─────────────────────────────────────────────────────────────
with col_score:
    st.markdown('<div class="section-label">PERFORMANCE SCORE</div>', unsafe_allow_html=True)

    if score >= 85:
        verdict_cls = "verdict-elite"
        verdict_txt = "ELITE DAY"
        bar_cls     = "progress-fill-elite"
    elif score >= 60:
        verdict_cls = "verdict-solid"
        verdict_txt = "SOLID PROGRESS"
        bar_cls     = "progress-fill-solid"
    else:
        verdict_cls = "verdict-reset"
        verdict_txt = "RESET NEEDED"
        bar_cls     = "progress-fill-reset"

    pct = int((score / 100) * 100)

    st.markdown(f"""
    <div class="score-card">
      <div class="score-number">{score}</div>
      <div class="score-denom">/ 100 POINTS</div>
      <div class="score-verdict {verdict_cls}">{verdict_txt}</div>
      <div class="progress-track">
        <div class="progress-fill {bar_cls}" style="width:{pct}%"></div>
      </div>
    </div>
    """, unsafe_allow_html=True)


# ── Task breakdown visual ─────────────────────────────────────────────────────
with col_tasks:
    st.markdown("<br>", unsafe_allow_html=True)
    rows_html = ""
    for t in TASKS:
        done = checked.get(t["key"])
        icon = "✓" if done else "○"
        icon_color = "#22c55e" if done else "#cbd5e0"
        name_color = "#1e2a3a" if done else "#6b7280"
        pts_color  = "#f8961e" if done else "#a0aec0"
        rows_html += f"""
        <div class="task-row">
          <span style="color:{icon_color}; margin-right:0.75rem; font-weight:700; font-size:1rem;">{icon}</span>
          <span style="flex:1; color:{name_color}; font-weight:{'600' if done else '400'}">{t['label']}</span>
          <span class="task-tag">{t['tag']}</span>
          <span class="task-pts" style="color:{pts_color}">+{t['pts']}</span>
        </div>"""
    st.markdown(f'<div class="task-panel" style="margin-top:0.75rem">{rows_html}</div>', unsafe_allow_html=True)


st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# CEO REFLECTION
# ══════════════════════════════════════════════════════════════════════════════
col_ref, col_quote = st.columns([2, 1], gap="large")

with col_ref:
    st.markdown('<div class="section-label">CEO REFLECTION LOG</div>', unsafe_allow_html=True)
    reflection = st.text_area(
        "WHAT DID I LEARN TODAY?",
        placeholder="Write your daily reflection here...\n\nWhat worked? What would you do differently? What insight did you unlock?",
        height=160,
        label_visibility="visible"
    )

    col_btn, col_msg = st.columns([1, 3])
    with col_btn:
        save_clicked = st.button("⟶  COMMIT DAY", use_container_width=True)

    if save_clicked:
        if not reflection.strip():
            st.warning("Add a reflection before committing the day.")
        else:
            # Build record
            record = {
                "date":       datetime.date.today().isoformat(),
                "score":      score,
                "tasks":      {t["key"]: checked.get(t["key"], False) for t in TASKS},
                "reflection": reflection.strip(),
            }
            # Update history (no duplicate dates)
            existing_dates = [e["date"] for e in data["history"]]
            if record["date"] in existing_dates:
                idx = existing_dates.index(record["date"])
                data["history"][idx] = record
            else:
                data["history"].append(record)

            # Update stats
            data["best_score"] = max(data.get("best_score", 0), score)
            data["total_days"] = len(data["history"])

            # Streak calc
            sorted_dates = sorted(
                [datetime.date.fromisoformat(e["date"]) for e in data["history"]],
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
            data["streak"] = streak_count

            save_data(data)
            st.session_state.data = data
            st.session_state.saved_today = True
            st.rerun()

    if st.session_state.saved_today:
        st.markdown("""
        <div style="margin-top:0.75rem; padding:0.85rem 1.1rem;
                    background:#f0fdf4; border:1.5px solid #bbf7d0;
                    border-left:4px solid #22c55e; border-radius:8px;
                    font-family:'Plus Jakarta Sans',sans-serif; font-size:0.85rem;
                    color:#15803d; font-weight:600;">
          ✓ Day committed — entry saved to your history
        </div>
        """, unsafe_allow_html=True)

with col_quote:
    st.markdown('<div class="section-label">FOUNDER SIGNAL</div>', unsafe_allow_html=True)
    quote = random.choice(CEO_QUOTES)
    st.markdown(f"""
    <div class="quote-card" style="animation: fadeIn 0.6s ease; margin-top:0.2rem;">
      <div style="font-family:'Plus Jakarta Sans',sans-serif; font-size:1rem;
                  line-height:1.75; color:#1b2340; font-style:italic; font-weight:500;">
        "{quote}"
      </div>
      <div style="margin-top:1rem; font-family:'JetBrains Mono',monospace;
                  font-size:0.6rem; letter-spacing:0.2em; color:rgba(27,35,64,0.5);
                  text-transform:uppercase;">
        — THE LONG GAME OS
      </div>
    </div>
    """, unsafe_allow_html=True)


st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# LIFE PILLARS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-label">LIFE PILLARS — STRATEGIC FOCUS MAP</div>', unsafe_allow_html=True)

pillar_html = '<div class="pillar-grid">'
for p in PILLARS:
    level_key = p["level"].lower().replace(" ", "-")
    pillar_html += f"""
    <div class="pillar-card pillar-{level_key}">
      <div class="pillar-name">{p['name'].replace(chr(10), '<br>')}</div>
      <div class="pillar-level level-{level_key}">{p['level'].upper()}</div>
    </div>"""
pillar_html += '</div>'
st.markdown(pillar_html, unsafe_allow_html=True)


st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# HISTORY LOG
# ══════════════════════════════════════════════════════════════════════════════
if data["history"]:
    st.markdown('<div class="section-label">MISSION LOG — SESSION HISTORY</div>', unsafe_allow_html=True)

    history_df = pd.DataFrame([
        {
            "Date":       e["date"],
            "Score":      e["score"],
            "Rating":     "ELITE" if e["score"] >= 85 else ("SOLID" if e["score"] >= 60 else "RESET"),
            "Tasks Done": sum(1 for v in e["tasks"].values() if v),
            "Reflection": (e["reflection"][:80] + "…") if len(e["reflection"]) > 80 else e["reflection"],
        }
        for e in sorted(data["history"], key=lambda x: x["date"], reverse=True)
    ])

    st.dataframe(
        history_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Score": st.column_config.ProgressColumn(
                "Score", min_value=0, max_value=100, format="%d pts"
            ),
        }
    )

    if st.button("↺  CLEAR ALL HISTORY"):
        data["history"]   = []
        data["streak"]    = 0
        data["best_score"]= 0
        data["total_days"]= 0
        save_data(data)
        st.session_state.data = data
        st.session_state.saved_today = False
        st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div style="margin-top:3rem; padding-top:1.5rem; border-top:1px solid #1a2030;
            display:flex; justify-content:space-between; align-items:center;
            font-family:'JetBrains Mono',monospace; font-size:0.6rem;
            letter-spacing:0.2em; color:#2d3748; text-transform:uppercase;">
  <span>THE LONG GAME — LIFE OS &nbsp;·&nbsp; FOUNDER EDITION</span>
  <span>BUILD · REFLECT · EVOLVE</span>
  <span>V3.0 &nbsp;·&nbsp; {today_str}</span>
</div>
""", unsafe_allow_html=True)