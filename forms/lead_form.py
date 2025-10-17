import streamlit as st
from datetime import datetime

def lead_form():
    st.header("🧾 Add Lead")

    with st.form("lead_form", clear_on_submit=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            lead_code = st.text_input("Lead Code *")
            company_name = st.text_input("Company Name")
            contact_no = st.text_input("Contact Number *")
        with col2:
            lead_name = st.text_input("Lead Name *")
            email = st.text_input("Email ID")
            source = st.selectbox("Lead Source", ["Website", "Referral", "Advertisement", "Walk-in", "Other"])    
        with col3:
            create_on = datetime.now()
            st.write("**Created On:**")
            st.write( create_on.strftime('%Y-%m-%d %H:%M:%S'))
            assign_to = st.text_input("Assign To (Employee Name)")
            lead_stage = st.selectbox("Lead Stage", ["New", "Qualified", "In Discussion", "Closed Won", "Closed Lost"])
            
        # --- Address Details ---
        st.markdown("---")
        st.subheader("Address Details")
        col1, col2 = st.columns(2)
        with col1:
            street = st.text_input("Street")
            state = st.text_input("State")
            country = st.text_input("Country")
        with col2:
            city = st.text_input("City")
            zip_code = st.text_input("Zip Code")
        
        # --- Remarks / Notes ---
        st.markdown("---")
        remarks = st.text_area("Remarks / Notes")

        submitted = st.form_submit_button("Submit Lead")
        if submitted:
            st.success(f"✅ Lead '{lead_name}' added successfully!")
