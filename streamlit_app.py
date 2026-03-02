import streamlit as st
import pandas as pd
from datetime import date

st.title("📚 Attendance Planner (Auto Timetable)")

# ---------- WEEKLY TIMETABLE ----------
timetable = {
    "Monday": ["NLP", "SE", "CIP", "DL"],
    "Tuesday": ["ML", "SE Lab"],
    "Wednesday": ["NLP", "DL", "IT Lab"],
    "Thursday": ["SE", "CIP", "Comm Skills"],
    "Friday": ["ML", "Comm Skills"]
}

# ---------- STORAGE ----------
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(
        columns=["Date", "Subject", "Status"]
    )

# ---------- SELECT DATE ----------
st.subheader("📅 Mark Attendance")

selected_date = st.date_input("Select Date", date.today())

day_name = selected_date.strftime("%A")

if day_name in timetable:
    today_subjects = timetable[day_name]

    st.write(f"### Subjects on {day_name}")

    for subject in today_subjects:
        status = st.selectbox(
            f"{subject}",
            ["Present", "Absent", "Cancelled"],
            key=f"{selected_date}-{subject}"
        )

        if st.button(f"Save {subject}", key=f"btn-{subject}"):

            new_row = pd.DataFrame(
                [[selected_date, subject, status]],
                columns=["Date