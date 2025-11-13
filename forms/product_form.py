import streamlit as st

def product_form():
    
    # Initialize session state for product data if not already initialized
    if "product_data" not in st.session_state:
        st.session_state.product_data = []  # Start with an empty list


    with st.form("product_form", clear_on_submit=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            product_name = st.text_input("Product Name *")
            item_type = st.selectbox("Item Type", ["Raw", "Consumable", "Bought out", "Semi-Finished good", "Finished good"])
            sku = st.text_input("SKU Code / Product ID")
        with col2:
            unit_type = st.selectbox("UoM Group", ["KGS", "Liters", "Nos"])
            quantity = st.number_input("Available Quantity", min_value=0, value=0)
            price = st.number_input("Selling Price (₹)", min_value=0.0, value=0.0)
        with col3:
            hsn_code = st.text_input("HSN Code")
            gst_rate = st.selectbox("Valuation Method)", ["FIFO", "Moving Avg", "Standard"])
            status = st.selectbox("Product Status", ["Active", "Inactive"])

        description = st.text_area("Product Description")

        submitted = st.form_submit_button("Add Product")
        if submitted:
            new_product = {
                "Product Name": product_name,
                "Item Type": item_type,
                "SKU": sku,
                "UoM": unit_type,
                "Quantity": quantity,
                "Price (₹)": price,
                "HSN Code": hsn_code,
                "GST Rate": gst_rate,
                "Status": status,
                "Description": description,
            }
            st.session_state.product_data.append(new_product)  # Update session state
            st.success(f"✅ Product '{product_name}' added to inventory successfully!")
            st.session_state.show_product_form = False  # Hide the form after submission
