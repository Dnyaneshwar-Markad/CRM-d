import streamlit as st
import pandas as pd

def item_master(product):
    # st.header("📦 Item Master / Inventory Item")

    # default warehouses (edit codes/names as needed)
    default_warehouses = [
        {"Whs Code": "WH1", "Whs Name": "Main Warehouse", "Committed": 10, "Ordered": 5, "Available": 85},
        {"Whs Code": "WH2", "Whs Name": "Warehouse A", "Committed": 5, "Ordered": 10, "Available": 35},
        {"Whs Code": "WH3", "Whs Name": "Warehouse B", "Committed": 2, "Ordered": 3, "Available": 20},
    ]

    with st.form("item_master", clear_on_submit=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            product_name = st.text_input("Item Name *", value=product["Product Name"])
            item_type = st.selectbox("Item Type", ["Raw", "Consumable", "Bought out", "Semi-Finished good", "Finished good"], index=["Raw", "Consumable", "Bought out", "Semi-Finished good", "Finished good"].index(product["Item Type"]))
            sku = st.text_input("SKU Code / Product ID", value=product.get("SKU", ""))
        with col2:
            unit_type = st.selectbox("UoM Group", ["KGS", "Liters", "Nos"], index=["KGS", "Liters", "Nos"].index(product["UoM"]))
            quantity = st.number_input("Available Quantity", min_value=0, value=product["Quantity"])
            price = st.number_input("Selling Price (₹)", min_value=0.0, value=product["Price (₹)"])
        with col3:
            hsn_code = st.text_input("HSN Code", value=product.get("HSN Code", ""))
            gst_rate = st.selectbox("Valuation Method)", ["FIFO", "Moving Avg", "Standard"], index=["FIFO", "Moving Avg", "Standard"].index(product["GST Rate"]))
            status = st.selectbox("Product Status", ["Active", "Inactive"], index=["Active", "Inactive"].index(product["Status"]))

        description = st.text_area("Item Description", value=product.get("Description", ""))

        # Display warehouse quantities
        st.markdown("**Warehouse Quantities**")
        df = pd.DataFrame(default_warehouses)  # Convert warehouse data to a DataFrame
        st.table(df)  # Display the table

        submitted = st.form_submit_button("Update Item")
        if submitted:
            # Update the product in session state
            product.update({
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
            })
            st.success(f"✅ Item '{product_name}' updated successfully!")
            st.session_state.show_product_form = False  # Hide the form after submission