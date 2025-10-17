import streamlit as st
import pandas as pd

# Custom CSS to reduce input field width in Quote Details
st.markdown("""
    <style>
    div[data-testid="column"] input, 
    div[data-testid="column"] textarea, 
    div[data-testid="column"] select {
        max-width: 220px;
        min-width: 120px;
        width: 100% !important;
        margin-bottom: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

def salesorder_form() :
        
    st.set_page_config(page_title="Order Form", layout="wide")

    st.title("🧾 Order Form")

    # --- Quote Details ---
    st.subheader("Order Details")
    col1, col2, col3 = st.columns([1, 1, 1])  # Equal width columns

    with col1:
        subject = st.text_input("Subject *")
        contact_name = st.text_input("Contact Name *")
        organization_name = st.text_input("Organization Name *")

    with col2:
        shipping = st.text_input("Shipping")
        campaign_source = st.text_input("Campaign Source")
        assign_to = st.text_input("Assign To")

    with col3:
        due_until = st.date_input("due Until")  
        opportunity_name = st.text_input("Opportunity Name")
        price_list = st.selectbox("price list", ["PL 1", "PL 2", "PL 3", "PL 4"])


    # --- Address Details ---
    st.markdown("---")
    st.subheader("Address Details")

    col1, col2 = st.columns(2)

    with col1:
        copy_billing = st.checkbox("Copy Billing Address From Contact")
        billing_address = st.text_area("Billing Address")

    with col2:
        copy_shipping = st.checkbox("Copy Shipping Address From Contact")
        shipping_address = st.text_area("Shipping Address")

    # --- Product Details ---
    st.markdown("---")
    st.subheader("Product Details")

    # Table structure
    if "products" not in st.session_state:
        st.session_state.products = pd.DataFrame(columns=["Product", "Description", "Quantity", "UOM", "Unit Price", "Tax Code", "Subtotal"])

    with st.form("add_product_form", clear_on_submit=True):
        c1, c2, c3, c4, c5, c6 = st.columns([2, 3, 1, 1, 1, 1])
        product = c1.text_input("Product")
        description = c2.text_input("Product Description")
        quantity = c3.number_input("Quantity", min_value=0, step=1)
        uom = c4.text_input("UOM")
        unit_price = c5.number_input("Unit Price", min_value=0.0, step=0.01)
        tax_code = c6.text_input("Tax Code")
        submitted = st.form_submit_button("Add Product +")

        if submitted:
            subtotal = quantity * unit_price
            new_row = {
                "Product": product,
                "Description": description,
                "Quantity": quantity,
                "UOM": uom,
                "Unit Price": unit_price,
                "Tax Code": tax_code,
                "Subtotal": subtotal,
            }
            st.session_state.products = pd.concat([st.session_state.products, pd.DataFrame([new_row])], ignore_index=True)

    if not st.session_state.products.empty:
        st.dataframe(st.session_state.products, use_container_width=True)
        total = st.session_state.products["Subtotal"].sum()
        st.write(f"### 💰 Total: {total:.2f}")

    # --- Description Details ---
    st.markdown("---")
    st.subheader("Description Details")
    description = st.text_area("Description")

    # --- Action Buttons ---
    st.markdown("---")
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("✅ Add and New"):
            st.success("Order saved successfully! Ready for next entry.")
            st.session_state.products = pd.DataFrame(columns=["Product", "Description", "Quantity", "UOM", "Unit Price", "Tax Code", "Subtotal"])
    with col2:
        if st.button("❌ Cancel"):
            st.warning("Order cancelled.")

