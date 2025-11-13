import streamlit as st
import pandas as pd
from forms.quotation_form import quotation_form

def quotation_page():
    # Initialize session state for page navigation
    if "show_quotation_form" not in st.session_state:
        st.session_state.show_quotation_form = False

    # Initialize session state for selected quotation
    if "selected_quotation_index" not in st.session_state:
        st.session_state.selected_quotation_index = None  # No quotation selected initially

    if "quotation_data" not in st.session_state:
        st.session_state.quotation_data = []  # Initialize quotation data if not already set

    # If a quotation is selected, show the quotation_form
    if st.session_state.selected_quotation_index is not None:
        # Add "Back to Quotation List" button above the quotation_form
        if st.button("Back to Quotation List"):
            st.session_state.selected_quotation_index = None  # Deselect the quotation and go back to the list
            return  # Exit the function to avoid rendering the quotation_form

        selected_quotation = st.session_state.quotation_data[st.session_state.selected_quotation_index]
        st.header(f"🧾 Edit Quotation: {selected_quotation['Subject']}")
        quotation_form()  # Call the quotation_form for editing

    # If the quotation form is being displayed
    elif st.session_state.show_quotation_form:
        # Add "Back to Quotation List" button above the quotation_form
        if st.button("Back to Quotation List"):
            st.session_state.show_quotation_form = False  # Switch back to the quotation list
            return  # Exit the function to avoid rendering the quotation_form

        st.header("🧾 New Quotation")
        quotation_form()  # Display the quotation form

    # Display the quotation list
    else:
        # Add New Quotation button and Search Bar with Dropdown in the same row
        col1, col2, col3 = st.columns([1.5, 2, 0.5])  # Adjust column widths
        with col1:
            st.write("###### Welcome to Quotation Management")
            if st.button("New Quotation"):
                st.session_state.show_quotation_form = True  # Switch to the quotation form
        with col2:
            search_query = st.text_input("Search by Subject", value="", placeholder="🔎 Enter subject")
        with col3:
            # Dynamically populate the dropdown with unique statuses
            statuses = list(set(quote["Status"] for quote in st.session_state.quotation_data))
            statuses.insert(0, "All")  # Add "All" option to the dropdown
            selected_status = st.selectbox("Filter by Status", options=statuses)

        # Display the quotation list as a table
        st.subheader("Quotation List")
        if "quotation_data" in st.session_state and st.session_state.quotation_data:
            # Filter quotations based on the search query and selected status
            filtered_quotations = [
                quote for quote in st.session_state.quotation_data
                if (search_query.lower() in quote["Subject"].lower())
                and (selected_status == "All" or quote["Status"] == selected_status)
            ]

            if filtered_quotations:
                # Create a header row for the quotation list
                header_col0, header_col1, header_col2, header_col3, header_col4, header_col5 = st.columns([1, 3, 3, 3, 3, 2])
                with header_col0:
                    st.write("***Sr.No***")
                with header_col1:
                    st.write("**Subject**")
                with header_col2:
                    st.write("**Contact Name**")
                with header_col3:
                    st.write("**Organization Name**")
                with header_col4:
                    st.write("**Status**")
                with header_col5:
                    st.write("**Activity**")

                # Add an "Edit" and "Delete" column with buttons
                for i, quote in enumerate(filtered_quotations):
                    col0, col1, col2, col3, col4, col5 = st.columns([1, 3, 3, 3, 3, 2])  # Adjust column widths
                    with col0:
                        st.write(f"{i+1}")
                    with col1:
                        st.write(quote["Subject"])
                    with col2:
                        st.write(quote["Contact Name"])
                    with col3:
                        st.write(quote["Organization Name"])
                    with col4:
                        st.write(quote["Status"])
                    with col5:
                        left, right = st.columns(2)
                        with left:
                            # Add "Edit" button
                            if st.button("🛠️", key=f"edit_{i}"):
                                # Find the index of the quotation in the original quotation_data
                                st.session_state.selected_quotation_index = st.session_state.quotation_data.index(quote)
                                break
                        with right:
                            # Add "Delete" button
                            if st.button("🗑️", key=f"delete_{i}"):
                                # Remove the quotation from the session state
                                st.session_state.quotation_data.remove(quote)
            else:
                st.warning("No quotations match your search query.")
        else:
            st.info("No quotations added yet. Use the 'New Quotation' button to add quotations.")