import streamlit as st
import pandas as pd
import json,csv,os
from datetime import datetime
from activity import activities
from forms.activity_form import activity_page  # ✅ Import your activity form

DATA_PATH = os.path.join("data", "activities.csv")

def load_activities_from_csv():
    if os.path.exists(DATA_PATH):
        return pd.read_csv(DATA_PATH)
    return pd.DataFrame()
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


def get_default_stage(stage_id):
    return {
        "id": stage_id,
        "startDate": datetime.now().date(),
        "closingDate": datetime.now().date(),
        "salesEmployee": "",
        "stage": "Lead",
        "percent": "",
        "potentialAmount": "",
        "weightedAmount": "",
        "showBPsDocs": False,
        "documentType": "Sales Quotation",
        "docNo": "",
        # "activities": "",
        "owner": "",
    }


def lead_form(existing_data=None, lead_stages=None):
    """Displays the lead form and returns updated data on submit."""

    if lead_stages is None:
        lead_stages = [get_default_stage(1)]

    st.title("📝 Edit Lead" if existing_data is not None else "➕ Create New Lead")

    # -------------------- BASIC INFORMATION --------------------
    st.markdown("#### Basic Information")
    c1, c2 = st.columns(2)
    with c1:
        name = st.text_input("Name", value=existing_data["Name"] if existing_data else "",help="Enter the full name of the Lead/Opportunity.")
        mobile = st.text_input("Mobile Number", value=existing_data["Mobile"] if existing_data else "", help="Enter the contact mobile number.")
        email = st.text_input("Business Email", value=existing_data["Email"] if existing_data else "", help="Enter a valid business email address.")
    with c2:
        # --- Initialize the list of industries in session state ---
        if "industry_types" not in st.session_state:
            st.session_state.industry_types = [
                "", "Agriculture", "Manufacturing", "Retail", "IT",
                "Healthcare", "Finance", "Education", "Other"
            ]

        # --- Auto-append any existing industry from DB if missing ---
        if existing_data and existing_data.get("Industry"):
            current_industry = existing_data["Industry"]
            if current_industry not in st.session_state.industry_types:
                st.session_state.industry_types.append(current_industry)

        # --- Add "+ Add new" option at the end ---
        industry_options = st.session_state.industry_types + ["+ Add new..."]

        # --- Determine default selection safely ---
        selected_industry = (
            existing_data["Industry"]
            if existing_data and existing_data.get("Industry") in industry_options
            else ""
        )

        # --- Main selectbox ---
        industry = st.selectbox(
            "Industry Type",
            industry_options,
            index=industry_options.index(selected_industry) if selected_industry in industry_options else 0,
            key="industry_select",
            help="Select the industry type relevant to the Lead.",
        )

        # --- Handle new option creation ---
        if industry == "+ Add new...":
            st.info("Add a new Industry Type below:")
            new_indus = st.text_input("Enter new Industry Type:")
            if st.button("Save New Industry Type"):
                if new_indus and new_indus not in st.session_state.industry_types:
                    st.session_state.industry_types.append(new_indus)
                    st.success(f"✅ Added: {new_indus}")
                    st.rerun()
                elif new_indus in st.session_state.industry_types:
                    st.warning("Industry already exists.")
                else:
                    st.error("Please enter a valid name.")
        

        # --- Address input below ---
        address = st.text_area(
            "Address",
            value=existing_data["Address"] if existing_data else "",
            height=125
        )




    # -------------------- GENERAL SECTION --------------------
    with st.expander("General"):
        gc1, gc2 = st.columns(2)
        with gc1:
            potentialAmount = st.number_input(
                "Potential Amount", min_value=0, step=1000,
                value=int(existing_data["PotentialAmount"]) if existing_data else 0
            )
            owner = st.text_input("Owner", value=existing_data["Owner"] if existing_data else "")
            # --- Initialize Source options ---
            if "lead_sources" not in st.session_state:
                st.session_state.lead_sources = ["", "Web", "Referral", "Cold Call", "Other"]

            # --- Auto-add source from existing data if missing ---
            if existing_data and existing_data.get("Source"):
                current_source = existing_data["Source"]
                if current_source not in st.session_state.lead_sources:
                    st.session_state.lead_sources.append(current_source)

            # --- Add "+ Add new" option ---
            source_options = st.session_state.lead_sources + ["+ Add new..."]

            # --- Determine default safely ---
            selected_source = (
                existing_data["Source"]
                if existing_data and existing_data.get("Source") in source_options
                else ""
            )

            # --- Main selectbox ---
            source = st.selectbox(
                "Source",
                source_options,
                index=source_options.index(selected_source) if selected_source in source_options else 0,
                key="source_select",
                help="Select or define a new source for this Lead."
            )

            # --- Handle new source creation ---
            if source == "+ Add new...":
                st.info("Add a new Source below:")
                new_source = st.text_input("Enter new Source Name:")
                if st.button("Save New Source"):
                    if new_source and new_source not in st.session_state.lead_sources:
                        st.session_state.lead_sources.append(new_source)
                        st.success(f"✅ Added: {new_source}")
                        st.rerun()
                    elif new_source in st.session_state.lead_sources:
                        st.warning("Source already exists.")
                    else:
                        st.error("Please enter a valid name.")

        with gc2:
            sales = st.text_input("Sales Employee", value=existing_data["Sales"] if existing_data else "")
            interest = st.number_input(
                "Interest", min_value=0.00, step=1.00,
                value=float(existing_data["Interest"]) if existing_data and str(existing_data["Interest"]).strip() != "" else 0.0
            )
            information = st.text_area("Information", value=existing_data["Information"] if existing_data else "", height=100)


    # -------------------- STAGES SECTION --------------------
    with st.expander("Stage", expanded=False):
        st.write("#### Lead Stages")
        
        activities_df = load_activities_from_csv()
        
        for stage in lead_stages:
            stage["potentialAmount"] = potentialAmount
            stage["weightedAmount"] = potentialAmount * interest / 100 if interest else 0


        # Display stages in editable form
        updated_stages = st.data_editor(
            lead_stages,
            num_rows="dynamic",
            key="stages_editor",           
            use_container_width=True
        )
        lead_stages = updated_stages

        # --- Now show a clickable "Activity" column ---
        # --- Now show a clickable "Activity" column ---
        st.divider()
        st.markdown("#### 🎯 Click Activity to Open Activity Form")

        # Load all activities once
        if os.path.exists("data/activities.csv"):
            activities_df = pd.read_csv("data/activities.csv")
        else:
            activities_df = pd.DataFrame(columns=["Stage"])

        # Ensure Stage column exists
        if "Stage" not in activities_df.columns:
            activities_df["Stage"] = ""

        for idx, stage in enumerate(lead_stages):
            stage_name = stage.get("stage", "Lead")

            cols = st.columns([2, 2, 2, 1, 1])
            with cols[0]:
                st.write(f"**Stage:** {stage_name}")
            with cols[1]:
                st.write(f"**Start Date:** {stage.get('startDate', '')}")
            with cols[2]:
                st.write(f"**Sales Employee:** {stage.get('salesEmployee', '')}")
            with cols[3]:
                st.write(f"**Owner:** {stage.get('owner', '')}")
            with cols[4]:
                if st.button("📝", key=f"activity_btn_{idx}", help=f"Open activities for {stage_name}"):
                    st.session_state.show_activity_for_stage = stage_name
                    st.session_state.show_activity_modal = True

            # --- Filter related activities for this stage ---
            related_activities = activities_df[activities_df["Stage"] == stage_name]

            if not related_activities.empty:
                st.markdown(f"###### 📋 Activities for: {stage_name}")

                # Show limited relevant columns
                columns_to_show = [
                    "Activity", "Subject", "Assigned To", "Start", "End", "Priority", "Activity Stage"
                ]
                valid_columns = [col for col in columns_to_show if col in related_activities.columns]
                st.dataframe(related_activities[valid_columns], use_container_width=True, hide_index=True)
            else:
                st.info(f"No activities logged yet for **{stage_name}**.")



        # --- Show activity form inline if button clicked ---
        if st.session_state.get("show_activity_modal", False):
            st.markdown("---")
            st.markdown("### 🧾 Activity Form")
            stage_id = st.session_state.get("show_activity_for_stage")
            activity_page(stage_name=stage_name)

            if st.button("Close Activity Form", key="close_activity_form"):
                st.session_state.show_activity_modal = False
    # -------------------- STATUS SECTION --------------------
    with st.expander("Status and General"):
        status = st.radio(
            "Status", ["Open", "Won", "Lost"],
            index=["Open", "Won", "Lost"].index(existing_data["Status"])
            if existing_data and existing_data["Status"] in ["Open", "Won", "Lost"]
            else 0,
            horizontal=True
        )
        lossReason = ""
        if status == "Lost":
            lossReason = st.text_area("Loss Reason", value=existing_data["LossReason"] if existing_data else "")

        sc1, sc2, sc3 = st.columns(3)
        with sc1:
            bpChannelCode = st.text_input("BP Channel Code", value=existing_data["BPChannelCode"] if existing_data else "")
        with sc2:
            bpChannelName = st.text_input("BP Channel Name", value=existing_data["BPChannelName"] if existing_data else "")
        with sc3:
            bpChannelContact = st.text_input("BP Channel Contact", value=existing_data["BPChannelContact"] if existing_data else "")

    # -------------------- SUBMIT --------------------
    submit = st.button("💾 Save Lead")

    if submit:
        updated_data = {
            "Name": name,
            "Mobile": mobile,
            "Email": email,
            "Industry": industry,
            "Address": address,
            "PotentialAmount": potentialAmount,
            "Owner": owner,
            "Source": source,
            "Sales": sales,
            "Interest": interest,
            "Information": information,
            "Status": status,
            "LossReason": lossReason,
            "BPChannelCode": bpChannelCode,
            "BPChannelName": bpChannelName,
            "BPChannelContact": bpChannelContact,
            "Stages": json.dumps(lead_stages, default=str)
        }
        return updated_data, lead_stages

    return None, lead_stages

# # forms/lead_form.py
# import streamlit as st
# import json
# from datetime import datetime

# def get_default_stage(stage_id):
#     return {
#         "id": stage_id,
#         "startDate": datetime.now().date(),
#         "closingDate": datetime.now().date(),
#         "salesEmployee": "",
#         "stage": "Lead",
#         "percent": 0,
#         "potentialAmount": 0.0,
#         "weightedAmount": 0.0,
#         "showBPsDocs": False,
#         "documentType": "Sales Quotation",
#         "docNo": "",
#         "activities": st.text_input("",key=f"activity_stage_{stage_id}"),
#         "owner": "",
#     }

# def lead_form(existing_data=None, lead_stages=None):
#     """Displays the lead form and returns updated data on submit."""

#     if lead_stages is None:
#         lead_stages = [get_default_stage(1)]

#     st.title("📝 Edit Lead" if existing_data is not None else "➕ Create New Lead")


#     st.markdown("#### Basic Information")
#     c1, c2 = st.columns(2)
#     with c1:
#         name = st.text_input("Name", value=existing_data["Name"] if existing_data is not None else "")
#         mobile = st.text_input("Mobile Number", value=existing_data["Mobile"] if existing_data is not None else "")
#         email = st.text_input("Business Email", value=existing_data["Email"] if existing_data is not None else "")
#     with c2:
#         industry = st.text_input("Industry Type", value=existing_data["Industry"] if existing_data is not None else "")
#         address = st.text_area("Address", value=existing_data["Address"] if existing_data is not None else "", height=125)

#     with st.expander("General"):
#         gc1, gc2 = st.columns(2)
#         with gc1:
#             potentialAmount = st.number_input(
#                 "Potential Amount", min_value=0.0, step=1000.0,
#                 value=float(existing_data["PotentialAmount"]) if existing_data is not None else 0.0
#             )
#             owner = st.text_input("Owner", value=existing_data["Owner"] if existing_data is not None else "")
#             source = st.selectbox(
#                 "Source", ["", "Web", "Referral", "Cold Call", "Other"],
#                 index=["", "Web", "Referral", "Cold Call", "Other"].index(existing_data["Source"])
#                 if existing_data is not None and existing_data["Source"] in ["", "Web", "Referral", "Cold Call", "Other"]
#                 else 0
#             )
#         with gc2:
#             sales = st.text_input("Sales Employee", value=existing_data["Sales"] if existing_data is not None else "")
#             interest = st.text_input("Interest", value=existing_data["Interest"] if existing_data is not None else "")
#             information = st.text_area("Information", value=existing_data["Information"] if existing_data is not None else "", height=100)

#     with st.expander("Stage", expanded=True):
#         st.write("#### Lead Stages")
#         updated_stages = st.data_editor(
#             lead_stages,
#             num_rows="dynamic",
#             key="stages_editor",
#             use_container_width=True
#         )
#         lead_stages = updated_stages

#     with st.expander("Status and General"):
#         status = st.radio("Status", ["Open", "Won", "Lost"],
#                         index=["Open", "Won", "Lost"].index(existing_data["Status"])
#                         if existing_data is not None and existing_data["Status"] in ["Open", "Won", "Lost"]
#                         else 0,
#                         horizontal=True)
#         lossReason = ""
#         if status == "Lost":
#             lossReason = st.text_area("Loss Reason", value=existing_data["LossReason"] if existing_data is not None else "")

#         sc1, sc2, sc3 = st.columns(3)
#         with sc1:
#             bpChannelCode = st.text_input("BP Channel Code", value=existing_data["BPChannelCode"] if existing_data is not None else "")
#         with sc2:
#             bpChannelName = st.text_input("BP Channel Name", value=existing_data["BPChannelName"] if existing_data is not None else "")
#         with sc3:
#             bpChannelContact = st.text_input("BP Channel Contact", value=existing_data["BPChannelContact"] if existing_data is not None else "")

#     submit = st.button("💾 Save Lead")

#     if submit:
#         updated_data = {
#             "Name": name,
#             "Mobile": mobile,
#             "Email": email,
#             "Industry": industry,
#             "Address": address,
#             "PotentialAmount": potentialAmount,
#             "Owner": owner,
#             "Source": source,
#             "Sales": sales,
#             "Interest": interest,
#             "Information": information,
#             "Status": status,
#             "LossReason": lossReason,
#             "BPChannelCode": bpChannelCode,
#             "BPChannelName": bpChannelName,
#             "BPChannelContact": bpChannelContact,
#             "Stages": json.dumps(lead_stages, default=str)
#         }
#         return updated_data, lead_stages

#     return None, lead_stages
