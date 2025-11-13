import streamlit as st
import pandas as pd
from forms.product_form import product_form
from forms.item_master import item_master

def inventory_page():
    # Initialize session state for page navigation
    if "show_product_form" not in st.session_state:
        st.session_state.show_product_form = False
        
    # Initialize session state for selected product
    if "selected_product_index" not in st.session_state:
        st.session_state.selected_product_index = None  # No product selected initially

    if "product_data" not in st.session_state:
        st.session_state.product_data = []  # Initialize product data if not already set

    # If a product is selected, show the item_master form
    if st.session_state.selected_product_index is not None:
        # Add "Back to Product List" button above the item_master form
        st.write("###### Welcome to Inventory Management")
        if st.button("Back to Product List"):
            st.session_state.selected_product_index = None  # Deselect the product and go back to the list
            return  # Exit the function to avoid rendering the item_master form

        selected_product = st.session_state.product_data[st.session_state.selected_product_index]
        st.header(f"📦 Edit Product: {selected_product['Product Name']}")
        item_master(selected_product)  # Pass the selected product to the item_master form

    # If the product form is being displayed
    elif st.session_state.show_product_form:
        # Add "Back to Product List" button above the product_form
        st.write("###### Welcome to Inventory Management")
        if st.button("Back to Product List"):
            st.session_state.show_product_form = False  # Switch back to the product list
            return  # Exit the function to avoid rendering the product_form

        st.header("📦 Add New Product")
        product_form()  # Display the product form

    # Display the product list
    else:
        # Add New Item button and Search Bar with Dropdown in the same row
        col1, col2, col3 = st.columns([1, 1.5, 0.5])  # Adjust column widths
        with col1:
            st.write("###### Welcome to Inventory Management")
            if st.button("Add New Item"):
                st.session_state.show_product_form = True  # Switch to the product form
        with col2:
            search_query = st.text_input("Search by Product Name", value="", placeholder="🔎 Enter product name")
        with col3:
            # Dynamically populate the dropdown with unique item types
            item_types = list(set(product["Item Type"] for product in st.session_state.product_data))
            item_types.insert(0, "All")  # Add "All" option to the dropdown
            selected_type = st.selectbox("Filter by Type", options=item_types)

        # Display the product list as a table
        st.subheader("Product List")
        if "product_data" in st.session_state and st.session_state.product_data:
            # Filter products based on the search query and selected type
            filtered_products = [
                product for product in st.session_state.product_data
                if (search_query.lower() in product["Product Name"].lower())
                and (selected_type == "All" or product["Item Type"] == selected_type)
            ]

            if filtered_products:
                # Create a header row for the product list
                header_col0, header_col1, header_col2, header_col3, header_col5, header_col4 = st.columns([1, 3, 3, 3, 3, 2])
                with header_col0:
                    st.write("***Sr.No***")
                with header_col1:
                    st.write("**Product Name**")
                with header_col2:
                    st.write("**SKU**")
                with header_col3:
                    st.write("**Quantity**")
                with header_col5:
                    st.write("**Price (₹)**")
                with header_col4:
                    st.write("**Activity**")

                # Add an "Edit" column with buttons
                for i, product in enumerate(filtered_products):
                    col0, col1, col2, col3, col5, col4 = st.columns([1, 3, 3, 3, 3, 2])  # Adjust column widths
                    with col0:
                        st.write(f"{i+1}")
                    with col1:
                        st.write(product["Product Name"])
                    with col2:
                        st.write(product["SKU"])
                    with col3:
                        st.write(product["Quantity"])
                    with col5:
                        st.write(product["Price (₹)"])
                    with col4:
                        left, right = st.columns(2)
                        with left:  
                        # Add "Edit" button
                            if st.button("🛠️", key=f"edit_{i}"):
                            # Find the index of the product in the original product_data
                                st.session_state.selected_product_index = st.session_state.product_data.index(product)
                                break
                        with right:
                        # Add "Delete" button
                            if st.button("☠️", key=f"delete_{i}"):
                                # Remove the product from the session state
                                st.session_state.product_data.remove(product)
                                
                                
            else:
                st.warning("No products match your search query.")
        else:
            st.info("No products added yet. Use the 'Add New Item' button to add products.")