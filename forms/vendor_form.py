import streamlit as st
from datetime import datetime

# Custom CSS to reduce input field width in Quote Details

# st.markdown("""
#     <style>
#     div[data-testid="column"] input, 
#     div[data-testid="column"] textarea, 
#     div[data-testid="column"] select {
#         max-width: 220px;
#         min-width: 120px;
#         width: 100% !important;
#         margin-bottom: 0.5rem;
#     }
#     </style>
# """, unsafe_allow_html=True)


def vendor_form():
    st.header("Add Vendor")
    
    with st.form("vendor_form", clear_on_submit=True):
        
        st.subheader("Venddor Details")
        col1, col2, col3 = st.columns([1, 1, 1])  # Equal width columns
        with col1:
            vendor_no = st.text_input("Vendor Number *")
            cnt_person = st.text_input("Contact Person *")
            website = st.text_input("Website")
            
            
        with col2:
            vendor_name = st.text_input("Vendor Name *")
            contact_number = st.text_input("Contact Number *")
            gst_number = st.text_input("GST Number")
        with col3:
            create_on = datetime.now()
            st.write("**Created On:**")
            st.write( create_on.strftime('%Y-%m-%d %H:%M:%S'))
            email = st.text_input("Email ID")
            vendor_type = st.selectbox("Vendor Type", ["Local", "International", "Distributor", "Retailer"])
            
        
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
        
        # --- Description Details ---
        st.markdown("---")
        st.subheader("Description Details")
        description = st.text_area("Description")
        
    
        submit = st.form_submit_button("Save Vendor")
        if submit:
            st.success(f"Vendor '{vendor_name}' added successfully ✅")
        
