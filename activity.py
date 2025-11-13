import streamlit as st
import pandas as pd
import os
from forms.activity_form import activity_page

DATA_PATH = os.path.join("data", "activities.csv")

def load_activities_from_csv():
    if os.path.exists(DATA_PATH):
        return pd.read_csv(DATA_PATH).to_dict("records")
    return []

def save_activities_to_csv(activities):
    df = pd.DataFrame(activities)
    df.to_csv(DATA_PATH, index=False)

def activities():
    if "show_activity_form" not in st.session_state:
        st.session_state.show_activity_form = False
    if "selected_activity_index" not in st.session_state:
        st.session_state.selected_activity_index = None

    # Always load latest from file
    st.session_state.activities = load_activities_from_csv()

    # CASE 1: Edit
    if st.session_state.selected_activity_index is not None:
        if st.button("⬅️ Back to Activity List"):
            st.session_state.selected_activity_index = None
            return
        st.header("✏️ Edit Activity")
        activity_page()

    # CASE 2: Add New
    elif st.session_state.show_activity_form:
        if st.button("⬅️ Back to Activity List"):
            st.session_state.show_activity_form = False
            return
        st.header("📝 New Activity")
        activity_page()

    # CASE 3: Show List
    else:
        col1, col2 = st.columns([1.2, 2])
        with col1:
            st.write("###### Welcome to Activity Management")
            if st.button("➕ New Activity"):
                st.session_state.show_activity_form = True
        with col2:
            search_query = st.text_input("Search by Subject", value="", placeholder="🔎 Search activity...")

        st.subheader("📋 Activity List")

        activities = st.session_state.activities
        if activities:
            filtered_activities = [
                act for act in activities
                if search_query.lower() in str(act.get("Subject", "") or "").lower()
            ]


            if filtered_activities:
                headers = ["Sr.No", "Subject", "BP Name", "Assigned To", "Stage", "Priority", "Actions"]
                header_cols = st.columns([1, 2, 2, 2, 2, 1.5, 2])
                for col, title in zip(header_cols, headers):
                    col.markdown(f"**{title}**")

                for i, act in enumerate(filtered_activities):
                    c0, c1, c2, c3, c4, c5, c6 = st.columns([1, 2, 2, 2, 2, 1.5, 2])
                    with c0:
                        st.write(i + 1)
                    with c1:
                        st.write(act.get("Subject", ""))
                    with c2:
                        st.write(act.get("BP Name", ""))
                    with c3:
                        st.write(act.get("Assigned To", ""))
                    with c4:
                        st.write(act.get("Stage", ""))
                    with c5:
                        st.write(act.get("Priority", ""))
                    with c6:
                        left, right = st.columns(2)
                        with left:
                            if st.button("🛠️", key=f"edit_{i}"):
                                st.session_state.selected_activity_index = i
                        with right:
                            if st.button("🗑️", key=f"delete_{i}"):
                                st.session_state.activities.pop(i)
                                save_activities_to_csv(st.session_state.activities)
            else:
                st.warning("No matching activities found.")
        else:
            st.info("No activities added yet. Click **New Activity** to create one.")
