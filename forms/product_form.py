import streamlit as st

def product_form():
    st.header("📦 Add Product / Inventory Item")

    with st.form("product_form", clear_on_submit=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            product_name = st.text_input("Product Name *")
            category = st.selectbox("Category", ["Fertilizer", "Seeds", "Pesticides", "Machinery", "Other"])
            sku = st.text_input("SKU Code / Product ID")
        with col2:
            unit_type = st.selectbox("Unit Type", ["KG", "Liters", "Packets", "Pieces", "Bags"])
            quantity = st.number_input("Available Quantity", min_value=0)
            price = st.number_input("Selling Price (₹)", min_value=0.0)
        with col3:
            hsn_code = st.text_input("HSN Code")
            gst_rate = st.selectbox("GST Rate (%)", [0, 5, 12, 18, 28])
            status = st.selectbox("Product Availability", ["Available", "Out of Stock"])

        description = st.text_area("Product Description")

        submitted = st.form_submit_button("Add Product")
        if submitted:
            st.success(f"✅ Product '{product_name}' added to inventory successfully!")
