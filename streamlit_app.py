import streamlit as st
import pandas as pd
from datetime import date

st.title("📚 Attendance Planner & Stipend Calculator")

subjects = [
    "CIP", "NLP", "SE", "ML",
    "DL", "Comm", "SE Lab", "ML Lab"
]

if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(
        columns=["Date", "Subject", "Status"]
    )

st.subheader("➕ Add Class Entry")

col1, col2, col3 = st.columns(3)

with col1:
    entry_date = st.date_input("Date", date.today())

with col2:
    subject = st.selectbox("Subject", subjects)

with col3:
    status = st.selectbox(
        "Status",
        ["Present", "Absent", "Cancelled"]
    )

if st.button("Add Entry"):
    new_row = pd.DataFrame(
        [[entry_date, subject, status]],
        columns=["Date", "Subject", "Status"]
    )

    st.session_state.data = pd.concat(
        [st.session_state.data, new_row],
        ignore_index=True
    )

st.subheader("📋 Records")
st.dataframe(st.session_state.data)

st.subheader("📊 Attendance Summary")

df = st.session_state.data
valid = df[df["Status"] != "Cancelled"]

total = len(valid)
present = len(valid[valid["Status"] == "Present"])

percentage = 0
if total > 0:
    percentage = (present / total) * 100

st.metric("Attendance %", f"{percentage:.2f}%")

if percentage >= 75:
    st.success("🎉 Eligible for FULL stipend")
elif percentage >= 70:
    st.warning("⚠ Eligible with Medical Certificate")
else:
    st.error("❌ Not Eligible")

if st.button("Reset Data"):
    st.session_state.data = pd.DataFrame(
        columns=["Date", "Subject", "Status"]
    )