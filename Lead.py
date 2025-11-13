# forms/leadpage.py
import streamlit as st
import pandas as pd
import os, json
from datetime import datetime
from forms.lead_form import lead_form, get_default_stage

st.markdown("""
<style>
input, textarea, select {
  padding: 4px 8px;
  border-radius: 5px;
  border: 1px solid #bdbdbd;
  font-size: 13px;
  background: #f7f7f7;
  box-shadow: none;
  margin-bottom: 4px !important;
}

input:focus, textarea:focus, select:focus {
  border-color: #017cff;
  outline: none;
}

label {
  font-size: 13px;
  color: #424242;
  font-weight: 500;
  margin-bottom: 2px;
}

.stTextInput, .stNumberInput, .stTextArea, .stSelectbox {
  margin-bottom: 8px !important;
}

.stTextInput > div > input,
.stNumberInput > div > input,
.stTextArea > div > textarea,
.stSelectbox > div > select {
  background: #f4f8fb !important;
  border-radius: 5px !important;
  border: 1px solid #d0d7de !important;
  font-size: 13px !important;
  padding: 4px 8px !important;
}
</style>
""", unsafe_allow_html=True)

def lead_page():
    os.makedirs("data", exist_ok=True)
    file_path = "data/leads.csv"

    all_cols = [
        "Sr.No", "Name", "Mobile", "Email", "Industry", "Address",
        "PotentialAmount", "Owner", "Source", "Sales", "Interest", "Information",
        "Status", "LossReason", "BPChannelCode", "BPChannelName", "BPChannelContact",
        "Stages"
    ]

    if not os.path.exists(file_path):
        leads_df = pd.DataFrame(columns=all_cols)
        leads_df.to_csv(file_path, index=False)
    else:
        try:
            leads_df = pd.read_csv(file_path)
        except pd.errors.EmptyDataError:
            leads_df = pd.DataFrame(columns=all_cols)

    for col in all_cols:
        if col not in leads_df.columns:
            leads_df[col] = pd.NA

    # --- STATE DEFAULTS ---
    if "show_form" not in st.session_state:
        st.session_state.show_form = False
    if "selected_lead" not in st.session_state:
        st.session_state.selected_lead = None
    if "lead_stages" not in st.session_state:
        st.session_state.lead_stages = []

    # ========================
    # LEAD LIST PAGE
    # ========================
    if not st.session_state.show_form:
        st.title("📋 Leads")
        c1, c2 = st.columns([1, 3])
        with c1:
            if st.button("➕ Create New Lead"):
                st.session_state.show_form = True
                st.session_state.selected_lead = None
                st.session_state.lead_stages = [get_default_stage(1)]
        with c2:
            st.write(f"Total leads: **{len(leads_df)}**")
            q = st.text_input("Search by Name or Mobile", "")
            if q:
                df_filtered = leads_df[
                    leads_df["Name"].astype(str).str.lower().str.contains(q.lower()) |
                    leads_df["Mobile"].astype(str).str.contains(q)
                ]
            else:
                df_filtered = leads_df

        if df_filtered.empty:
            st.info("No leads found.")
            return

        df_filtered = df_filtered.sort_values(by="Sr.No", ascending=False).reset_index(drop=True)

        for _, row in df_filtered.iterrows():
            with st.container(border=True):
                c1, c2, c3 = st.columns([3, 3, 1])
                with c1:
                    st.markdown(f"**{row['Name']}**  \n📱 {row['Mobile']}  \n🏭 {row['Industry']}")
                with c2:
                    st.markdown(f"💰 Potential: {row['PotentialAmount']}  \n👤 Owner: {row['Owner']}  \n📊 Status: {row['Status']}")
                with c3:
                    if st.button("Edit", key=f"view_{row['Sr.No']}"):
                        st.session_state.show_form = True
                        st.session_state.selected_lead = row["Sr.No"]
                        try:
                            st.session_state.lead_stages = json.loads(row["Stages"])
                        except Exception:
                            st.session_state.lead_stages = [get_default_stage(1)]
        return

    # ========================
    # LEAD FORM PAGE
    # ========================
    if st.session_state.selected_lead:
        lead_row = leads_df.loc[leads_df["Sr.No"] == st.session_state.selected_lead].iloc[0]
        lead_data = lead_row.to_dict()
    else:
        lead_data = None

    updated_data, updated_stages = lead_form(existing_data=lead_data, lead_stages=st.session_state.lead_stages)

    if updated_data is not None:
        if st.session_state.selected_lead:
            # update existing
            idx = leads_df.index[leads_df["Sr.No"] == st.session_state.selected_lead][0]
            for k, v in updated_data.items():
                leads_df.loc[idx, k] = v
        else:
            # create new
            new_sr = (leads_df["Sr.No"].max() if not leads_df.empty else 0) + 1
            updated_data["Sr.No"] = new_sr
            leads_df = pd.concat([leads_df, pd.DataFrame([updated_data])], ignore_index=True)

        leads_df.to_csv(file_path, index=False)
        st.success("✅ Lead saved successfully!")
        st.session_state.show_form = False
        st.session_state.selected_lead = None
        st.session_state.lead_stages = []

    if st.button("⬅️ Back to Lead List"):
        st.session_state.show_form = False
        st.session_state.selected_lead = None
