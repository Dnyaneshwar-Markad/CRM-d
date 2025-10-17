import streamlit as st

from forms.vendor_form import vendor_form
from forms.contact_form import contact_form
from forms.product_form import product_form
from forms.lead_form import lead_form
from forms.quotation_form import quotation_form
from forms.salesorder_form import salesorder_form

# st.set_page_config(page_title="DMS Admin Dashboard", layout="wide")

st.title("🏠 CRM Admin Dashboard")

# Sidebar Navigation
st.sidebar.header("Navigation")
menu = st.sidebar.radio(
    "Choose Form:",
    ["Create Quotation", "Add Order","Add Vendor", "Add Contact", "Add Product", "Add Lead"]
)

# Routing
if menu == "Create Quotation":
    quotation_form()
elif menu == "Add Order":
    salesorder_form()
elif menu == "Add Vendor":
    vendor_form()
elif menu == "Add Contact":
    contact_form()
elif menu == "Add Product":
    product_form()
elif menu == "Add Lead":
    lead_form()
