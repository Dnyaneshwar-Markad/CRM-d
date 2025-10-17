import streamlit as st
import datetime

def contact_form():
    st.header("👨‍💼 Add Contact")

    with st.form("contact_form", clear_on_submit=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            emp_id = st.text_input("ID *")
            emp_name = st.text_input("First Name *")
            contact_no = st.text_input("Contact Number *")
            
        with col2:
            role = st.selectbox("Role", ["Admin", "Employee", "Lead", "Vendor"])
            emp_namel = st.text_input("Last Name *")
            email = st.text_input("Email ID *")
            
        with col3:
            joining_date = st.date_input("Joining Date", datetime.date.today())
            left, right = st.columns(2)
            with left:
                dob = st.date_input("Date of Birth")
            with right:
                gender = st.selectbox("Gender",["Male","Female","Other"])
            status = st.selectbox("Status", ["Active", "Inactive"])

        address = st.text_area("Address")

        submitted = st.form_submit_button("Save Contact")
        if submitted:
            st.success(f"✅'{emp_name}' has been successfully added!! to your contacts.")
