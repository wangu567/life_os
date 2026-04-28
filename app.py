# Life OS v2 — Founder Edition
# Streamlit App
# Adaptive Compound Engine
# Includes:
# - 24h flexible planner
# - lifecycle modes
# - patience engine
# - one-skill-per-day system
# - build vs consume tracking
# - impulse delay protocol
# - wealth compound layer
# - progress dashboards
# - long-term execution tracking

import streamlit as st
import pandas as pd
import datetime
import json
import os

st.set_page_config(
    page_title="Life OS v2 — Founder Edition",
    layout="wide",
    page_icon="⚡"
)

DATA_FILE = "life_os_v2.json"

DEFAULT_DATA = {
    "mode": "Builder Phase",
    "patience_days_required": 30,
    "current_strategy_start": str(datetime.date.today()),
    "build_hours": 0,
    "consume_hours": 0,
    "sleep_mode": "Normal",
    "daily_skill": "Coding",
    "monthly_investing": {
        "Index Fund": 200,
        "AI Companies": 100,
        "Bitcoin": 100
    },
    "notes": []
}

SKILLS = [
    "Coding",
    "Charts",
    "Communication",
    "Finance",
    "Art"
]

DAY_SKILL_MAP = {
    "Monday": "Coding",
    "Tuesday": "Communication",
    "Wednesday": "Finance",
    "Thursday": "Art",
    "Friday": "Charts",
    "Saturday": "Deep Work",
    "Sunday": "Review"
}

LIFECYCLE_MODES = [
    "Student Phase",
    "Student + Work",
    "Builder Phase",
    "Operator Phase",
    "Founder Phase"
]

SLEEP_MAP = {
    "Busy": 6,
    "Normal": 7,
    "Relaxed": 8
}


def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return DEFAULT_DATA.copy()


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


data = load_data()

today = datetime.date.today()
day_name = today.strftime("%A")
auto_skill = DAY_SKILL_MAP.get(day_name, "Coding")

st.title("⚡ Life OS v2 — Founder Edition")
st.caption("The Long Game | Adaptive Compound Engine")

col1, col2, col3 = st.columns(3)

with col1:
    data["mode"] = st.selectbox("Lifecycle Mode", LIFECYCLE_MODES, index=LIFECYCLE_MODES.index(data["mode"]))

with col2:
    data["sleep_mode"] = st.selectbox("Sleep Mode", list(SLEEP_MAP.keys()))

with col3:
    st.metric("Sleep Hours", f"{SLEEP_MAP[data['sleep_mode']]} hrs")

st.divider()

st.subheader("One Skill Per Day System")
st.info(f"Today's Focus Skill: {auto_skill}")

manual_skill = st.selectbox("Override Skill (if needed)", SKILLS)
if st.button("Use Manual Skill"):
    data["daily_skill"] = manual_skill
else:
    data["daily_skill"] = auto_skill

st.divider()

st.subheader("Patience Engine")

strategy_start = datetime.date.fromisoformat(data["current_strategy_start"])
days_active = (today - strategy_start).days
required_days = data["patience_days_required"]
remaining = max(required_days - days_active, 0)

st.metric("Days Since Current Strategy Started", days_active)
st.metric("Days Remaining Before Strategy Change Allowed", remaining)

if remaining > 0:
    st.warning("Strategy switching locked. Stay consistent.")
else:
    st.success("Strategy review allowed. Change only with written reason.")

reason = st.text_area("If changing strategy, write reason here")

st.divider()

st.subheader("Build vs Consume Ratio")

build = st.number_input("Build Hours Today", min_value=0.0, step=0.5)
consume = st.number_input("Consume Hours Today", min_value=0.0, step=0.5)

ratio = build / consume if consume > 0 else build
st.metric("Builder Ratio", round(ratio, 2))

if build > consume:
    st.success("Builder > Consumer")
else:
    st.warning("Consumption too high")

st.divider()

st.subheader("Wealth Compound Layer")

index_amt = st.number_input("Index Fund", value=200)
ai_amt = st.number_input("AI Companies", value=100)
btc_amt = st.number_input("Bitcoin", value=100)

monthly_total = index_amt + ai_amt + btc_amt
annual_total = monthly_total * 12

st.metric("Monthly Investment", f"P{monthly_total}")
st.metric("Annual Investment", f"P{annual_total}")

st.divider()

st.subheader("24 Hour Allocation")

sleep_hours = SLEEP_MAP[data["sleep_mode"]]
work_school = st.slider("School / Work Hours", 4, 15, 8)
skill_hours = st.slider("Skill Development Hours", 1, 6, 2)

buffer = 24 - sleep_hours - work_school - skill_hours

st.write(f"Sleep: {sleep_hours}h")
st.write(f"School/Work: {work_school}h")
st.write(f"Skill: {skill_hours}h")
st.write(f"Buffer / Rest: {buffer}h")

if buffer < 0:
    st.error("Time allocation exceeds 24 hours.")
else:
    st.success("Balanced schedule")

if st.button("Save Life OS"):
    data["build_hours"] = build
    data["consume_hours"] = consume
    data["monthly_investing"] = {
        "Index Fund": index_amt,
        "AI Companies": ai_amt,
        "Bitcoin": btc_amt
    }
    save_data(data)
    st.success("System saved successfully.")
