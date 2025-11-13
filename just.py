# import streamlit as st

# # --- Initialize session state ---
# if "selected_type" not in st.session_state:
#     st.session_state.selected_type = None  # No type selected initially
# if "selected_address" not in st.session_state:
#     st.session_state.selected_address = None  # No address selected initially
# if "addresses" not in st.session_state:
#     st.session_state.addresses = {
#         "Bill-To": [],
#         "Ship-To": [],
#     }

# # --- Layout: two main columns ---
# left, right = st.columns([1, 3])

# # ===================== LEFT PANEL =====================
# with left:
#     st.markdown("### 🧾 Addresses")

#     # --- BILL TO Section ---
#     st.markdown("**Bill-To**")
#     for addr in st.session_state.addresses["Bill-To"]:
#         if st.button(addr["AddressID"], key=f"bill_{addr['AddressID']}"):
#             st.session_state.selected_type = "Bill-To"
#             st.session_state.selected_address = addr["AddressID"]

#     if st.button("+ New Bill-To"):
#         new_id = "define new"
#         st.session_state.addresses["Bill-To"].append({"AddressID": new_id})
#         st.session_state.selected_type = "Bill-To"
#         st.session_state.selected_address = new_id
#         st.rerun()

#     st.markdown("---")

#     # --- SHIP TO Section ---
#     st.markdown("**Ship-To**")
#     for addr in st.session_state.addresses["Ship-To"]:
#         if st.button(addr["AddressID"], key=f"ship_{addr['AddressID']}"):
#             st.session_state.selected_type = "Ship-To"
#             st.session_state.selected_address = addr["AddressID"]

#     if st.button("+ New Ship-To"):
#         new_id = "define new"
#         st.session_state.addresses["Ship-To"].append({"AddressID": new_id})
#         st.session_state.selected_type = "Ship-To"
#         st.session_state.selected_address = new_id
#         st.rerun()

# # ===================== RIGHT PANEL =====================
# with right:
#     if st.session_state.selected_type and st.session_state.selected_address:
#         st.markdown(f"### 🏠 {st.session_state.selected_type} Details")
#         st.markdown(f"**Selected Address:** {st.session_state.selected_address}")

#         with st.form(key="address_form", clear_on_submit=False):
#             col1, col2 = st.columns(2)
#             with col1:
#                 address_code = st.text_input(
#                     "Address Code", 
#                     value=st.session_state.selected_address, 
#                     key="address_code"
#                 )
#                 street = st.text_input("Street")
#                 building = st.text_input("Building / Floor")
#                 city = st.text_input("City")
#                 state = st.text_input("State")
#             with col2:
#                 zip_code = st.text_input("Zip Code")
#                 country = st.text_input("Country")
#                 gst_type = st.text_input("GST Type")
#                 gst_in = st.text_input("GSTIN")

#             submitted = st.form_submit_button("💾 Save")
#             if submitted:
#                 # Prevent saving if AddressID is still "define new"
#                 if address_code == "define new":
#                     st.error("Please change the Address Code before saving.")
#                 else:
#                     # Update the selected address with the new details
#                     for addr in st.session_state.addresses[st.session_state.selected_type]:
#                         if addr["AddressID"] == st.session_state.selected_address:
#                             addr.update({
#                                 "AddressID": address_code,
#                                 "Street": street,
#                                 "Building": building,
#                                 "City": city,
#                                 "State": state,
#                                 "Zip Code": zip_code,
#                                 "Country": country,
#                                 "GST Type": gst_type,
#                                 "GSTIN": gst_in,
#                             })
#                             break
#                     # Update the session state to reflect the new AddressID
#                     st.session_state.selected_address = address_code
#                     st.success(f"{st.session_state.selected_type} '{address_code}' saved successfully!")
#     else:
#         st.markdown("### 🏠 Address Details")
#         st.info("Select or add a new address to view details.")
# # from streamlit_modal import Modal
# # import streamlit as st

# # st.title("Opportunity Form")

# # modal = Modal("Add Activity", key="activity_modal")
# # if st.button("Add Activity"):
# #     modal.open()

# # if modal.is_open():
# #     with modal.container():
# #         st.write("Enter activity details:")
# #         act_type = st.selectbox("Type", ["Call", "Meeting", "Email"])
# #         note = st.text_area("Notes")
# #         if st.button("Submit Activity"):
# #             st.success(f"Added activity: {act_type}")
# #             modal.close()
import streamlit as st

# Session state for storing options
if "options" not in st.session_state:
    st.session_state.options = ["Lead", "Contacted", "Negotiation", "Closed"]

st.title("🧠 Smart Selectbox (Add Inside Dropdown)")

# Append “Add new” option
options_with_add = st.session_state.options + ["➕ Add new..."]

# Render selectbox
selected = st.selectbox("Select Stage:", options_with_add, key="stage_select")

# If user chooses "Add new..."
if selected == "➕ Add new...":
    st.info("Add a new stage below:")
    new_stage = st.text_input("Enter new stage name:")
    if st.button("Save New Stage"):
        if new_stage and new_stage not in st.session_state.options:
            st.session_state.options.append(new_stage)
            st.success(f"Added: {new_stage}")
            st.rerun()
        elif new_stage in st.session_state.options:
            st.warning("Stage already exists.")
        else:
            st.error("Please enter a valid name.")
else:
    st.write(f"✅ Selected stage: **{selected}**")
