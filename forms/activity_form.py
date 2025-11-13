import streamlit as st
import datetime
import os
import pandas as pd

# ---------- Helper: Save activity data ----------
def save_activity(activity_data, stage_name):
    os.makedirs("data", exist_ok=True)
    file_path = "data/activities.csv"

    # Add Stage column before saving
    activity_data["Stage"] = stage_name

    new_row = pd.DataFrame([activity_data])

    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        df = pd.concat([df, new_row], ignore_index=True)
    else:
        df = new_row

    df.to_csv(file_path, index=False)


# ---------- Styling ----------
st.markdown("""
<style>
div[data-testid="stVerticalBlock"] > div {
    padding-top: 0rem;
    padding-bottom: 0rem;
    margin-bottom: 0rem;
}
.stSelectbox, .stTextInput, .stDateInput, .stNumberInput {
    margin-bottom: -10px !important;
}
label {
    font-size: 0.9rem !important;
    margin-bottom: 2px !important;
}
.sap-yellow input, .sap-yellow select {
    background-color: #fff5cc !important;
}
</style>
""", unsafe_allow_html=True)


# ---------- Main Form ----------
def activity_page(stage_name=None):
    """Activity form for creating & saving activities per stage."""
    st.set_page_config(page_title="Activity", layout="centered")

    # Compact layout for main info
    col1, _, col3 = st.columns([1.5, 0.5, 1.5])
    with col1:
        right, left = st.columns(2)
        with right:
            activity = st.selectbox("Activity", ["Phone Call", "Meeting", "Task", "Note", "Campaign", "Other"])
        with left:
            recurrence = st.selectbox("Recurrence", ["None", "Daily", "Weekly", "Monthly"])
        with right:
            activity_type = st.selectbox("Type", ["General", "Sales", "Support"])
        subject = st.text_input("Subject")
        col11, col12 = st.columns(2)
        with col11:
            assigned_to_user = st.selectbox("Assigned To", ["User", "Manager", "Admin"])
        with col12:
            assigned_by = st.text_input("Assigned By")

    with col3:
        right, left = st.columns(2)
        with right:
            activity_stage = st.selectbox("Activity Stage", ["Not Started", "In Progress", "Deferred", "Completed", "Waiting for Input"], index=0)
        with left:
            number = st.text_input("Number", value="1364")
        col31, col32 = st.columns(2)
        with col31:
            bp_code = st.text_input("BP Code")
        with col32:
            bp_type = st.selectbox("BP Type", ["Lead", "Customer", "Vendor"], index=0)
        bp_name = st.text_input("BP Name")
        contact_person = st.text_input("Contact Person")

    # ========== Expander: General ==========
    with st.expander("📋 General", expanded=False):
        colA, colB = st.columns([1, 1])
        with colA:
            now = datetime.datetime.now()
            default_start_date = now.date()
            default_start_time = now.time().replace(second=0, microsecond=0)
            default_end_date = now.date()
            default_end_time = (now + datetime.timedelta(hours=1)).time().replace(second=0, microsecond=0)

            right, left = st.columns(2)
            with right:
                start_date = st.date_input("Start Date", value=default_start_date)
            with left:
                start_time = st.time_input("Start Time", value=default_start_time)
            right1, left1 = st.columns(2)
            with right1:
                end_date = st.date_input("End Date", value=default_end_date)
            with left1:
                end_time = st.time_input("End Time", value=default_end_time)

            start_dt = datetime.datetime.combine(start_date, start_time)
            end_dt = datetime.datetime.combine(end_date, end_time)

            if end_dt <= start_dt:
                st.error("⚠️ End date/time must be after start date/time.")
                duration_display = "Invalid"
            else:
                duration = end_dt - start_dt
                total_minutes = int(duration.total_seconds() // 60)
                hours, minutes = divmod(total_minutes, 60)
                duration_display = f"{hours}h {minutes}m" if hours else f"{minutes} min"

            right2, left2 = st.columns(2)
            with right2:
                st.text_input("Duration", duration_display, disabled=True)
            with left2:
                reminder_check = st.checkbox("Reminder")
            reminder_time = st.text_input("Reminder (e.g. 15 Minutes)", "15 Minutes" if reminder_check else "")
        with colB:
            priority = st.selectbox("Priority", ["Low", "Normal", "High"], index=1)
            meeting_location = st.text_input("Meeting Location")

        st.text_area("Activity Content", placeholder="Enter notes or call summary here...", height=150)

    # ========== Footer Buttons ==========
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 5])
    with col_btn1:
        if st.button("Add"):
            new_activity = {
                "Activity": activity,
                "Recurrence": recurrence,
                "Type": activity_type,
                "Subject": subject,
                "Assigned To": assigned_to_user,
                "Assigned By": assigned_by,
                "Activity Stage": activity_stage,
                "Number": number,
                "BP Code": bp_code,
                "BP Type": bp_type,
                "BP Name": bp_name,
                "Contact Person": contact_person,
                "Priority": priority,
                "Meeting Location": meeting_location,
                "Duration": duration_display,
                "Reminder": reminder_time,
                "Start": str(start_dt),
                "End": str(end_dt),
            }

            # ✅ Save to CSV with stage name from lead form
            if stage_name:
                save_activity(new_activity, stage_name)
            else:
                save_activity(new_activity, "Unknown")

            st.success("✅ Activity added and saved successfully!")

            if "activities" not in st.session_state:
                st.session_state.activities = []
            st.session_state.activities.append(new_activity)
            st.session_state.show_activity_form = False

    with col_btn2:
        if st.button("Cancel"):
            st.session_state.show_activity_form = False

    with col_btn3:
        st.button("Follow Up")
