import streamlit as st
import pandas as pd
from datetime import date

st.title("📚 Attendance Planner (Auto Timetable)")

# ===== WEEKLY TIMETABLE =====
timetable = {
    "Monday": ["NLP", "SE", "CIP", "DL"],
    "Tuesday": ["ML", "SE Lab"],
    "Wednesday": ["NLP", "DL", "IT Lab"],
    "Thursday": ["SE", "CIP", "Comm Skills"],
    "Friday": ["ML", "Comm Skills"]
}

# ===== STORAGE =====
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(
        columns=["Date", "Subject", "Status"]
    )

# ===== SELECT DATE =====
st.subheader("📅 Mark Attendance")

selected_date = st.date_input("Select Date", date.today())
day_name = selected_date.strftime("%A")

# ===== SHOW SUBJECTS =====
if day_name in timetable:

    st.write("### Subjects on", day_name)

    for subject in timetable[day_name]:

        status = st.selectbox(
            subject,
            ["Present", "Absent", "Cancelled"],
            key=f"{selected_date}-{subject}"
        )

        if st.button(f"Save {subject}", key=f"btn-{subject}"):

            new_row = pd.DataFrame(
                [[selected_date, subject, status]],
                columns=["Date", "Subject", "Status"]
            )

            st.session_state.data = pd.concat(
                [st.session_state.data, new_row],
                ignore_index=True
            )

            st.success(f"{subject} saved!")

else:
    st.info("No classes today 🎉")

# ===== RECORDS =====
st.subheader("📋 Attendance Records")
st.dataframe(st.session_state.data)

# ===== SUMMARY =====
st.subheader("📊 Attendance Summary")

df = st.session_state.data
valid = df[df["Status"] != "Cancelled"]

total = len(valid)
present = len(valid[valid["Status"] == "Present"])

percentage = (present / total) * 100 if total > 0 else 0

st.metric("Attendance %", f"{percentage:.2f}%")

# ===== STIPEND STATUS =====
if percentage >= 75:
    st.success("🎉 Eligible for FULL stipend")
elif percentage >= 70:
    st.warning("⚠ Eligible with Medical Certificate")
else:
    st.error("❌ Not Eligible")

# ===== RESET =====
if st.button("Reset All Data"):
    st.session_state.data = pd.DataFrame(
        columns=["Date", "Subject", "Status"]
    )