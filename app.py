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

# ── CSS: Dark command-center aesthetic ────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;700&family=Bebas+Neue&family=Space+Grotesk:wght@300;400;500;600&display=swap');

/* ── Global Reset ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
    background-color: #080a0f;
    color: #c8d0e0;
}

/* ── Main container ── */
.main .block-container {
    padding: 2rem 2.5rem 4rem;
    max-width: 1400px;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ── Hero header ── */
.hero-header {
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    padding: 0 0 2.5rem;
    border-bottom: 1px solid #1a2030;
    margin-bottom: 2.5rem;
    animation: fadeIn 0.6s ease;
}
.hero-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 5rem;
    letter-spacing: 0.08em;
    line-height: 1;
    background: linear-gradient(135deg, #f5a623 0%, #f7c06e 50%, #e8870a 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-shadow: none;
}
.hero-sub {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    color: #4a5568;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin-top: 0.4rem;
}
.hero-date {
    text-align: right;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    color: #2d3748;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    line-height: 1.8;
}
.hero-date span {
    display: block;
    color: #f5a623;
    font-size: 1.1rem;
    font-weight: 700;
    letter-spacing: 0.05em;
}

/* ── Section headers ── */
.section-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    color: #f5a623;
    margin-bottom: 1.2rem;
    display: flex;
    align-items: center;
    gap: 0.75rem;
}
.section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, #1e2535 0%, transparent 100%);
}

/* ── Score card ── */
.score-card {
    background: #0d1117;
    border: 1px solid #1a2030;
    border-radius: 4px;
    padding: 2rem;
    position: relative;
    overflow: hidden;
    animation: fadeIn 0.5s ease;
}
.score-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #f5a623, #e8870a, transparent);
}
.score-number {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 8rem;
    line-height: 1;
    letter-spacing: 0.02em;
    background: linear-gradient(135deg, #f5a623, #f7c06e);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.score-denom {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.5rem;
    color: #2d3748;
    margin-top: -1rem;
}
.score-verdict {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.2rem;
    letter-spacing: 0.1em;
    margin-top: 0.5rem;
}
.verdict-elite { color: #48bb78; }
.verdict-solid { color: #f5a623; }
.verdict-reset { color: #fc4c4c; }

/* ── Progress bar ── */
.progress-track {
    background: #111827;
    border-radius: 2px;
    height: 6px;
    margin-top: 1.5rem;
    overflow: hidden;
    width: 100%;
}
.progress-fill {
    height: 100%;
    border-radius: 2px;
    transition: width 0.8s cubic-bezier(0.25, 1, 0.5, 1);
}
.progress-fill-elite { background: linear-gradient(90deg, #48bb78, #68d391); }
.progress-fill-solid { background: linear-gradient(90deg, #f5a623, #f7c06e); }
.progress-fill-reset { background: linear-gradient(90deg, #fc4c4c, #feb2b2); }

/* ── Task rows ── */
.task-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.9rem 0;
    border-bottom: 1px solid #111827;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    letter-spacing: 0.05em;
    transition: all 0.2s;
}
.task-row:last-child { border-bottom: none; }
.task-row:hover { background: rgba(245, 166, 35, 0.03); padding-left: 0.5rem; }
.task-tag {
    background: #1a2030;
    border-radius: 2px;
    padding: 0.2rem 0.5rem;
    font-size: 0.6rem;
    color: #4a5568;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}
.task-pts {
    color: #4a5568;
    font-size: 0.7rem;
}

/* ── Pillar cards ── */
.pillar-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 1rem;
    margin-top: 0.5rem;
}
.pillar-card {
    background: #0d1117;
    border: 1px solid #1a2030;
    border-radius: 4px;
    padding: 1.25rem 1rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s, transform 0.2s;
    animation: fadeIn 0.6s ease;
}
.pillar-card:hover {
    border-color: #f5a623;
    transform: translateY(-2px);
}
.pillar-card::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 2px;
}
.pillar-very-high::after { background: #f5a623; }
.pillar-high::after { background: #68d391; }
.pillar-medium::after { background: #63b3ed; }
.pillar-low::after { background: #4a5568; }

.pillar-name {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #6b7280;
    margin-bottom: 0.5rem;
}
.pillar-level {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.5rem;
    letter-spacing: 0.1em;
}
.level-very-high { color: #f5a623; }
.level-high { color: #68d391; }
.level-medium { color: #63b3ed; }
.level-low { color: #4a5568; }

/* ── Streak & stat cards ── */
.stat-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin-bottom: 2.5rem;
}
.stat-card {
    background: #0d1117;
    border: 1px solid #1a2030;
    border-radius: 4px;
    padding: 1.2rem 1.4rem;
    animation: fadeIn 0.5s ease;
}
.stat-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #4a5568;
    margin-bottom: 0.4rem;
}
.stat-value {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.2rem;
    letter-spacing: 0.05em;
    color: #f5a623;
    line-height: 1;
}
.stat-unit {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    color: #2d3748;
    margin-top: 0.1rem;
}

/* ── Reflection area ── */
.stTextArea textarea {
    background: #0d1117 !important;
    border: 1px solid #1a2030 !important;
    border-radius: 4px !important;
    color: #c8d0e0 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.8rem !important;
    letter-spacing: 0.03em !important;
    line-height: 1.8 !important;
    padding: 1rem !important;
    transition: border-color 0.2s !important;
}
.stTextArea textarea:focus {
    border-color: #f5a623 !important;
    box-shadow: 0 0 0 1px rgba(245, 166, 35, 0.15) !important;
}
.stTextArea label {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.7rem !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
    color: #4a5568 !important;
}

/* ── Checkboxes ── */
.stCheckbox label {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.8rem !important;
    letter-spacing: 0.05em !important;
    color: #9aa3b0 !important;
}
.stCheckbox input:checked + label { color: #c8d0e0 !important; }

/* ── Buttons ── */
.stButton > button {
    background: transparent !important;
    border: 1px solid #f5a623 !important;
    border-radius: 2px !important;
    color: #f5a623 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.7rem !important;
    letter-spacing: 0.2em !important;
    text-transform: uppercase !important;
    padding: 0.6rem 1.5rem !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: rgba(245, 166, 35, 0.08) !important;
    transform: translateY(-1px) !important;
}

/* ── Divider ── */
hr { border-color: #1a2030 !important; margin: 2rem 0 !important; }

/* ── Alert overrides ── */
.stAlert { border-radius: 4px !important; border-left-width: 3px !important; }

/* ── Selectbox ── */
.stSelectbox select, .stSelectbox > div > div {
    background: #0d1117 !important;
    border-color: #1a2030 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.8rem !important;
    color: #c8d0e0 !important;
}

/* ── Animations ── */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(8px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0.4; }
}
.live-dot {
    display: inline-block;
    width: 6px; height: 6px;
    background: #f5a623;
    border-radius: 50%;
    margin-right: 0.5rem;
    animation: pulse 2s ease infinite;
}

/* ── History table ── */
.stDataFrame {
    border: 1px solid #1a2030 !important;
    border-radius: 4px !important;
    overflow: hidden !important;
}
.stDataFrame table {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.75rem !important;
}
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
        icon = "▪" if not done else "▸"
        color = "#f5a623" if done else "#2d3748"
        name_color = "#c8d0e0" if done else "#4a5568"
        rows_html += f"""
        <div class="task-row">
          <span style="color:{color}; margin-right:0.75rem;">{icon}</span>
          <span style="flex:1; color:{name_color}">{t['label']}</span>
          <span class="task-tag">{t['tag']}</span>
          <span class="task-pts" style="margin-left:1rem; color:{'#f5a623' if done else '#2d3748'}">+{t['pts']}</span>
        </div>"""
    st.markdown(f'<div style="margin-top:0.5rem">{rows_html}</div>', unsafe_allow_html=True)


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
        <div style="margin-top:0.75rem; padding:0.75rem 1rem;
                    background:#0d1117; border:1px solid #1a3020;
                    border-left:3px solid #48bb78; border-radius:4px;
                    font-family:'JetBrains Mono',monospace; font-size:0.75rem;
                    color:#68d391; letter-spacing:0.05em;">
          ▸ DAY COMMITTED — ENTRY LOCKED TO HISTORY
        </div>
        """, unsafe_allow_html=True)

with col_quote:
    st.markdown('<div class="section-label">FOUNDER SIGNAL</div>', unsafe_allow_html=True)
    quote = random.choice(CEO_QUOTES)
    st.markdown(f"""
    <div style="background:#0d1117; border:1px solid #1a2030;
                border-left:3px solid #f5a623; border-radius:4px;
                padding:1.5rem; margin-top:0.2rem;
                animation: fadeIn 0.6s ease;">
      <div style="font-family:'Space Grotesk',sans-serif; font-size:0.95rem;
                  line-height:1.7; color:#9aa3b0; font-style:italic;">
        "{quote}"
      </div>
      <div style="margin-top:1rem; font-family:'JetBrains Mono',monospace;
                  font-size:0.6rem; letter-spacing:0.2em; color:#2d3748;">
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