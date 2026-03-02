import streamlit as st
import pandas as pd
from datetime import date

st.title("📚 Flexible Attendance Planner")

# ===== REGULAR TIMETABLE =====
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
st.subheader("📅 Select Date")
selected_date = st.date_input("Date", date.today())
day_name = selected_date.strftime("%A")

# ===== REGULAR CLASSES =====
st.subheader("📖 Regular Classes")

if day_name in timetable:

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
    st.info("No regular classes today")

# ===== EXTRA CLASS SECTION =====
st.subheader("➕ Add Extra Class (Weekend / Special)")

extra_subject = st.text_input("Subject name")

extra_status = st.selectbox(
    "Status",
    ["Present", "Absent", "Cancelled"],
    key="extra_status"
)

if st.button("Add Extra Class"):

    if extra_subject != "":

        new_row = pd.DataFrame(
            [[selected_date, extra_subject, extra_status]],
            columns=["Date", "Subject", "Status"]
        )

        st.session_state.data = pd.concat(
            [st.session_state.data, new_row],
            ignore_index=True
        )

        st.success("Extra class added!")

    else:
        st.warning("Enter subject name")

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