import streamlit as st
import pandas as pd
from forms.salesorder_form import salesorder_form

def sales_page():
    # Initialize session state for page navigation
    if "show_sales_form" not in st.session_state:
        st.session_state.show_sales_form = False

    # Initialize session state for selected sales order
    if "selected_sales_index" not in st.session_state:
        st.session_state.selected_sales_index = None  # No sales order selected initially

    if "sales_data" not in st.session_state:
        st.session_state.sales_data = []  # Initialize sales order data if not already set

    # If a sales order is selected, show the salesorder_form
    if st.session_state.selected_sales_index is not None:
        # Add "Back to Sales List" button above the salesorder_form
        if st.button("Back to Sales List"):
            st.session_state.selected_sales_index = None  # Deselect the sales order and go back to the list
            return  # Exit the function to avoid rendering the salesorder_form

        selected_sales = st.session_state.sales_data[st.session_state.selected_sales_index]
        st.header(f"🧾 Edit Sales Order: {selected_sales['Subject']}")
        salesorder_form()  # Call the salesorder_form for editing

    # If the sales form is being displayed
    elif st.session_state.show_sales_form:
        # Add "Back to Sales List" button above the salesorder_form
        if st.button("Back to Sales List"):
            st.session_state.show_sales_form = False  # Switch back to the sales list
            return  # Exit the function to avoid rendering the salesorder_form
        
        st.header("🧾 New Sales Order")
        salesorder_form()  # Display the sales order form

    # Display the sales order list
    else:
        # Add New Sales Order button and Search Bar with Dropdown in the same row
        col1, col2, col3 = st.columns([1.5, 2, 0.5])  # Adjust column widths
        with col1:
            st.write("###### Welcome to Sales Management")
            if st.button("New Sales Order"):
                st.session_state.show_sales_form = True  # Switch to the sales order form
        with col2:
            search_query = st.text_input("Search by Subject", value="", placeholder="🔎 Enter subject")
        with col3:
            # Dynamically populate the dropdown with unique statuses
            statuses = list(set(order["Status"] for order in st.session_state.sales_data))
            statuses.insert(0, "All")  # Add "All" option to the dropdown
            selected_status = st.selectbox("Filter by Status", options=statuses)

        # Display the sales order list as a table
        st.subheader("Sales Order List")
        if "sales_data" in st.session_state and st.session_state.sales_data:
            # Filter sales orders based on the search query and selected status
            filtered_sales = [
                order for order in st.session_state.sales_data
                if (search_query.lower() in order["Subject"].lower())
                # and (selected_status == "All" or order["Status"] == selected_status)
            ]

            if filtered_sales:
                # Create a header row for the sales order list
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
                for i, order in enumerate(filtered_sales):
                    col0, col1, col2, col3, col4, col5 = st.columns([1, 3, 3, 3, 3, 2])  # Adjust column widths
                    with col0:
                        st.write(f"{i+1}")
                    with col1:
                        st.write(order["Subject"])
                    with col2:
                        st.write(order["Contact Name"])
                    with col3:
                        st.write(order["Organization Name"])
                    with col4:
                        st.write(order["Status"])
                    with col5:
                        left, right = st.columns(2)
                        with left:
                            # Add "Edit" button
                            if st.button("🛠️", key=f"edit_{i}"):
                                # Find the index of the sales order in the original sales_data
                                st.session_state.selected_sales_index = st.session_state.sales_data.index(order)
                                break
                        with right:
                            # Add "Delete" button
                            if st.button("🗑️", key=f"delete_{i}"):
                                # Remove the sales order from the session state
                                st.session_state.sales_data.remove(order)

            else:
                st.warning("No sales orders match your search query.")
        else:
            st.info("No sales orders added yet. Use the 'Add New Sales Order' button to add sales orders.") 