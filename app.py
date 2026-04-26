import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="The Long Game — Life OS",
    layout="wide"
)

st.title("The Long Game — Life Operating System")
st.subheader("Founder Dashboard")

st.markdown("---")

# DAILY PERFORMANCE SECTION

st.header("Daily Performance Score")

task1 = st.checkbox("Morning Routine Completed")
task2 = st.checkbox("Workout / Health Task Completed")
task3 = st.checkbox("Finance Review Completed")
task4 = st.checkbox("Skill Development Completed")
task5 = st.checkbox("TLG Project Progress Completed")
task6 = st.checkbox("Night Reflection Completed")

score = 0

if task1:
    score += 15

if task2:
    score += 15

if task3:
    score += 20

if task4:
    score += 20

if task5:
    score += 20

if task6:
    score += 10

st.markdown("---")

st.subheader(f"Today's Score: {score}/100")

if score >= 85:
    st.success("Strong Day")
elif score >= 60:
    st.warning("Decent Day")
else:
    st.error("Reset Needed")

st.markdown("---")

# CEO REFLECTION SECTION

st.header("CEO Reflection")

reflection = st.text_area(
    "What did I learn today?",
    placeholder="Write your daily reflection here..."
)

if reflection:
    st.info("Reflection saved mentally — future version will store permanently.")

st.markdown("---")

# PILLARS SECTION

st.header("Life Pillars")

pillars_data = pd.DataFrame({
    "Pillar": [
        "Personal Foundation",
        "Financial Life",
        "Career + Academics",
        "TLG Project",
        "Skill Stack"
    ],
    "Focus Level": [
        "High",
        "High",
        "Medium",
        "Very High",
        "Very High"
    ]
})

st.dataframe(pillars_data, use_container_width=True)

st.markdown("---")

st.success("Version 2 Live — Your system is evolving.")
```
