import streamlit as st

from forms.activity_form import activity_page
from home import home_page
from inventory import inventory_page
from sales import sales_page
from quotation import quotation_page
from business_partner import business_partner
from Lead import lead_page
from activity import activities

from forms.item_master import item_master
from forms.vendor_form import vendor_form
from forms.contact_form import contact_form
from forms.product_form import product_form
from forms.lead_form import lead_form
from forms.quotation_form import quotation_form
from forms.salesorder_form import salesorder_form

st.set_page_config(page_title="CRM Admin Dashboard", layout="wide")

# initialize session state keys and defaults
if "main_menu" not in st.session_state:
    st.session_state.main_menu = "Home"
if "sales_sub" not in st.session_state:
    st.session_state.sales_sub = "Sales"
if "activities_sub" not in st.session_state:
    st.session_state.activities_sub = "Calls"
if "inventory_sub" not in st.session_state:
    st.session_state.inventory_sub = "Inventory"
if "service_sub" not in st.session_state:
    st.session_state.service_sub = "Warenty & Services"# changed default to match inv_options

# callbacks to mark last-chosen main module (so UI knows which expander the user used)
def select_sales():
    st.session_state.main_menu = "Sales"
    st.session_state.inventory_sub = "Inventory"
    st.session_state.management_sub = "Contacts"
    st.session_state.service_sub = "Warenty & Services"


def select_inventory():
    st.session_state.main_menu = "Inventory"
    st.session_state.sales_sub = "Sales"
    st.session_state.management_sub = "Contacts"
    st.session_state.service_sub = "Warenty & Services"


def select_master():
    st.session_state.main_menu = "Customer Management"
    st.session_state.sales_sub = "Sales"
    st.session_state.inventory_sub = "Inventory"
    st.session_state.service_sub = "Warenty & Services"


def select_service():
    st.session_state.main_menu = "Warenty & Services"
    st.session_state.sales_sub = "Sales"
    st.session_state.inventory_sub = "Inventory"
    st.session_state.management_sub = "Contacts"


def go_home():
    st.session_state.main_menu = "Home"
    st.session_state.sales_sub = "Sales"
    st.session_state.inventory_sub = "Inventory"
    st.session_state.management_sub = "Contacts"
    st.session_state.service_sub = "Warenty & Services"


# Sidebar: Home button + expanders for Sales, Activities, Inventory
st.sidebar.title("Modules")
st.sidebar.button("Home", on_click=go_home)

with st.sidebar.expander("Sales", expanded=False):
    sales_options = ["Business Leads", "Quotations", "Orders"]
    sales_sub = st.selectbox(
        "Sales Submodule",
        sales_options,
        index=0,
        key="sales_sub",
        on_change=select_sales
    )


with st.sidebar.expander("Inventory", expanded=False):
    inv_options = ["Items","Inventory Actions"] #["Items", "Vendors", "Purchase Orders"]
    inventory_sub = st.selectbox(
        "Inventory Submodule",
        inv_options,
        index=0,  # No default selection
        key="inventory_sub",
        on_change=select_inventory
    )

with st.sidebar.expander("Master", expanded=False):
    management_option = ["Contacts","Activities"]
    management_sub = st.selectbox(
        "Master Submodule",
        management_option,
        index=0,
        key="management_sub",
        on_change=select_master
    )

with st.sidebar.expander("Warenty & Services", expanded=False):
    srv_options = ["Near Expiring", "Customer feedback", "Service agent", "Service Reports"]
    service_sub = st.selectbox(
        "Warenty & Services Submodule",
        srv_options,
        index=0,  # No default selection
        key="service_sub",
        on_change=select_service
    )


# Main routing based on the last chosen module (set by callbacks above)
main = st.session_state.main_menu

if main == "Home":
    home_page()
    
    
    
elif main == "Customer Management":
    sub = st.session_state.management_sub
    if sub == "Contacts":
        business_partner()
        st.info("Lead view (implement form/list)")
    elif sub == "Activities":
        st.title("📞 Activities")
        activities()
    
        

elif main == "Sales":
    sub = st.session_state.sales_sub
    if sub == "Orders":
        st.title("🪙 Sales")
        sales_page()
    elif sub == "Quotations":
        st.title("📜 Quotation")
        quotation_page()
    elif sub == "Business Leads":
        lead_page()

elif main == "Inventory":
    inv = st.session_state.inventory_sub
    if inv == "Items":
        st.title("🏬 Inventory")
        inventory_page()
    elif inv == "Inventory Actions":
        st.info("Inventory Actions view (implement form/list) comming soon!")
    # elif inv == "Item Master":
    #     st.title("📚 Item Masters")
    #     item_master("")
    # elif inv == "Vendors":
    #     st.title("🏷️ Vendors")
    #     vendor_form()
    # elif inv == "Purchase Orders":
    #     st.title("🧾 Purchase Orders")
    #     st.info("Purchase Orders view (implement form/list)")
        
        
elif main == "Warenty & Services":
    srv = st.session_state.service_sub
    st.title("🧑‍🔧 Warenty & Services")
    if srv == "Near Expiring":
        st.info("Near Expiring view (implement form/list)")
    elif srv == "Customer feedback":
        st.info("Customer feedback view (implement form/list)")
    elif srv == "Service agent":
        st.info("Service agent view (implement form/list)")
    elif srv == "Service Reports":
        st.info("Service Reports view (implement form/list)")

elif main == "Reports":
    st.title("📊 Reports")
    st.info("Select a report from sidebar (or implement a Reports expander)")
