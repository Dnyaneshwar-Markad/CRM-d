import streamlit as st
import datetime
import pandas as pd

def contact_form():
    # Form for adding or editing a business partner
    with st.form("contact_form", clear_on_submit=True):
        st.subheader("📋 Business Partner Master Data")

        # --- GENERAL SECTION ---
        with st.expander("🧾 General", expanded= True):
            col1, col2, col3 = st.columns(3)
            with col1:
                right, left = st.columns(2)
                with right:
                    card_type = st.selectbox("Card Type*", ["Customer", "Supplier", "Lead"])
                with left:
                    card_code = st.text_input("Card Code*")
                card_name = st.text_input("Card Name*")
                group_code = st.text_input("Group Code")
                industry_type = st.text_input("Industry Type")
            with col2:
                st.header(""),st.header(""),st.write ("")
                email = st.text_input(" E-mail Address")
                cellular = st.text_input("Cellular")
            with col3:
                date_of_creation = st.date_input("Date of Creation", value=datetime.date.today())
                acc_balance = st.number_input("Acc. Balance", min_value=0.0, step=0.01)
                

        # --- CONTACT PERSON SECTION ---
        with st.expander("👤 Contact Person"):
            col1, col2, col3 = st.columns(3)
            with col1:
                first_name = st.text_input("First Name")
                
            with col2:
                last_name = st.text_input("Last Name")
                email_c = st.text_input("E-mail")
            with col3:
                title = st.text_input("Title/Position")
                cell = st.text_input("Cellolar")
            address_c = st.text_area("Address")

        # --- PAYMENT & ACCOUNTING SECTION ---
        with st.expander("💰 Payment & Accounting"):
            col1, col2, col3 = st.columns([2,1,4])
            with col1:
                payterm = st.text_input("Payterm*")
                price_list = st.text_input("Price List")
                effective_discount = st.slider("Effective Discount",min_value=0, max_value=100, value=25, step=1)
                effective_price = st.select_slider("Effective Price",  ["Low", "Medium", "High"])
            with col2:
                st.write(""),st.write(""),st.write("")
                
                
            with col3:
                right,left = st.columns([1,2])
                with right:
                    st.write(""),st.write("")
                    st.markdown("*P.A.N Number**")
                with left:
                    pan_num = st.text_input('',key="pan_number")
                    
                st.subheader("")
                st.write("Bank Details")
                df = pd.DataFrame({
                    "Field": [ "Bank Name", "IFSC Code", "Account No.", "Account Name"],
                    "Value": ["", "", "", ""]
                })

                edited_df = st.data_editor(df, num_rows="fixed", hide_index=True)

                # st.write("### ✅ Entered Data")
                # st.write(edited_df)
                # bank_name = st.text_input("Bank Name")
                # ifsc_code = st.text_input("IFSC Code")
                # acc_no = st.text_input("Account Number")
                # acc_name = st.text_input("Account Name")

        # --- ADDRESS SECTION ---
        with st.expander("🏢 Address of Organization"):
            st.subheader("Bill To")
            col1, col2 = st.columns(2)
            with col1:
                bill_address_id = st.text_input("Address ID (Bill To)")
                bill_address1 = st.text_area("Address Line 1")
            with col2:
                bill_street = st.text_input("Street")
                bill_city = st.text_input("City")
                bill_zip = st.text_input("Zipcode")
                bill_state = st.text_input("State")
                bill_country = st.text_input("Country")
                gst_type = st.selectbox("GST Type", ["Regular", "Composition", "Unregistered", "Consumer", "Overseas", "Special Economic Zone"])
                gst_in =  st.text_input("GST IN")
        # --- REMARK SECTION ---
        with st.expander("📝 Remark", expanded= True):
            remark = st.text_area("Remark / Notes")

        # --- ACTION BUTTONS ---
        submitted = st.form_submit_button("Save Contact")
        if submitted:
            # Save the contact data to session state
            new_contact = {
                "Card Type": card_type,
                "Card Name": card_name,
                "Group Code": group_code,
                "Card Code": card_code,
                "Date of Creation": date_of_creation,
                "E-mail Address": email,
                "Acc. Balance": acc_balance,
                "Cellular": cellular,
                "Contact Person": {
                    "First Name": first_name,
                    "Last Name": last_name,
                    "Title": title,
                    "E-mail": email_c,
                    "Cellolar": cell,
                    "Address": address_c,
                },
                "Payment & Accounting": {
                    "Payterm": payterm,
                    "Price List": price_list,
                    "Effective Discount": effective_discount,
                    "P.A.N Number": pan_num,
                    "Lowest Discount": lowest_discount,
                    "Effective Price": effective_price,
                    "Bank Details": {
                        "Bank Name": bank_name,
                        "IFSC Code": ifsc_code,
                        "Account Number": acc_no,
                        "Account Name": acc_name,
                    },
                    "Default Priority": default_priority,
                },
                "Address": {
                    "Bill To": {
                        "Address ID": bill_address_id,
                        "Address Line 1": bill_address1,
                        "Street": bill_street,
                        "City": bill_city,
                        "Zipcode": bill_zip,
                        "State": bill_state,
                        "Country": bill_country,
                    },
                },
                "GST Details": {
                    "GST Type": gst_type,
                    "GST IN": gst_in,
                },
                "Remark": remark,
            }
            if "contact_data" not in st.session_state:
                st.session_state.contact_data = []
            st.session_state.contact_data.append(new_contact)

            st.success(f"✅ '{card_name}' has been successfully added to your contacts!")
