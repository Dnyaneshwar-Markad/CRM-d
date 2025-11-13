import streamlit as st
from forms.contact_form import contact_form

def business_partner():
    # Initialize session state for page navigation
    if "show_contact_form" not in st.session_state:
        st.session_state.show_contact_form = False

    if "contact_data" not in st.session_state:
        st.session_state.contact_data = []

    # If the contact form is being displayed
    if st.session_state.show_contact_form:
        if st.button("Back to Contact List"):
            st.session_state.show_contact_form = False
        else:
            contact_form()
        return

    # Display the contact list
    if st.button("Add New Contact"):
        st.session_state.show_contact_form = True

    if st.session_state.contact_data:
        for i, contact in enumerate(st.session_state.contact_data):
            st.write(f"**{i+1}. {contact['Card Name']}** - {contact['Card Type']}")
            st.write(f"Email: {contact['E-mail Address']}, Cellular: {contact['Cellular']}")
            if st.button(f"Edit {contact['Card Name']}", key=f"edit_{i}"):
                st.session_state.show_contact_form = True
            if st.button(f"Delete {contact['Card Name']}", key=f"delete_{i}"):
                st.session_state.contact_data.pop(i)
    else:
        st.info("No contacts available. Use the 'Add New Contact' button to add a contact.")


