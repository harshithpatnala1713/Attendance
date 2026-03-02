import streamlit as st
import pandas as pd
from datetime import date

st.title("📚 Smart Attendance Planner")

# ===== DEFAULT SUBJECT LIST =====
default_subjects = [
    "NLP", "SE", "CIP", "DL",
    "ML", "SE Lab", "IT Lab",
    "Comm Skills"
]

# ===== STORE SUBJECT DATABASE =====
if "subjects" not in st.session_state:
    st.session_state.subjects = default_subjects.copy()

# ===== REGULAR TIMETABLE =====
timetable = {
    "Monday": ["NLP", "SE", "CIP", "DL"],
    "Tuesday": ["ML", "SE Lab"],
    "Wednesday": ["NLP", "DL", "IT Lab"],
    "Thursday": ["SE", "CIP", "Comm Skills"],
    "Friday": ["ML", "Comm Skills"]
}

# ===== ATTENDANCE STORAGE =====
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(
        columns=["Date", "Subject", "Status"]
    )

# =====================================================
# ADD NEW SUBJECT (DATABASE UPDATE)
# =====================================================
st.subheader("➕ Add New Course")

new_subject = st.text_input("Enter new course name")

if st.button("Add Course"):
    if new_subject != "":
        if new_subject not in st.session_state.subjects:
            st.session_state.subjects.append(new_subject)
            st.success("Course added successfully!")
        else:
            st.warning("Course already exists")
    else:
        st.warning("Enter a course name")

# =====================================================
# SELECT DATE
# =====================================================
st.subheader("📅 Select Date")
selected_date = st.date_input("Date", date.today())
day_name = selected_date.strftime("%A")

# =====================================================
# REGULAR CLASSES
# =====================================================
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

# =====================================================
# EXTRA CLASS (DROPDOWN FROM DATABASE)
# =====================================================
st.subheader("➕ Add Extra Class")

extra_subject = st.selectbox(
    "Select Subject",
    st.session_state.subjects
)

extra_status = st.selectbox(
    "Status",
    ["Present", "Absent", "Cancelled"],
    key="extra_status"
)

if st.button("Add Extra Class"):

    new_row = pd.DataFrame(
        [[selected_date, extra_subject, extra_status]],
        columns=["Date", "Subject", "Status"]
    )

    st.session_state.data = pd.concat(
        [st.session_state.data, new_row],
        ignore_index=True
    )

    st.success("Extra class added!")

# =====================================================
# RECORDS
# =====================================================
st.subheader("📋 Attendance Records")
st.dataframe(st.session_state.data)

# =====================================================
# SUMMARY
# =====================================================
st.subheader("📊 Attendance Summary")

df = st.session_state.data
valid = df[df["Status"] != "Cancelled"]

total = len(valid)
present = len(valid[valid["Status"] == "Present"])

percentage = (present / total) * 100 if total > 0 else 0

st.metric("Attendance %", f"{percentage:.2f}%")

# =====================================================
# STIPEND STATUS
# =====================================================
if percentage >= 75:
    st.success("🎉 Eligible for FULL stipend")
elif percentage >= 70:
    st.warning("⚠ Eligible with Medical Certificate")
else:
    st.error("❌ Not Eligible")

# =====================================================
# RESET
# =====================================================
if st.button("Reset All Data"):
    st.session_state.data = pd.DataFrame(
        columns=["Date", "Subject", "Status"]
    )