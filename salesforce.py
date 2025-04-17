import streamlit as st
from simple_salesforce import Salesforce, SalesforceAuthenticationFailed
import pandas as pd

# UI Title
st.title("🔐 Salesforce Login and Data Fetcher")

# User Input for Salesforce Login
username = st.text_input("Username", placeholder="Enter Salesforce username")
password = st.text_input("Password", placeholder="Enter Salesforce password", type="password")
security_token = st.text_input("Security Token", placeholder="Enter Salesforce security token", type="password")
domain = st.selectbox("Select Domain", ["login", "test"])  # login for prod, test for sandbox

# Store Salesforce session in Streamlit state
if "sf" not in st.session_state:
    st.session_state.sf = None

# Login Button
if st.button("Login"):
    try:
        sf = Salesforce(
            username=username,
            password=password,
            security_token=security_token,
            domain=domain
        )
        st.session_state.sf = sf
        st.success("✅ Login Successful!")
    except SalesforceAuthenticationFailed:
        st.session_state.sf = None
        st.error("❌ Login Failed! Check your credentials.")

# Fetch data after successful login
if st.session_state.sf:
    if st.button("Fetch Data"):
        try:
            # Example: Replace this SOQL query with your actual Salesforce object/query
            query = "SELECT Id, Name FROM Account LIMIT 10"
            result = st.session_state.sf.query(query)
            records = result["records"]

            # Convert to DataFrame for display
            df = pd.DataFrame(records).drop(columns="attributes")
            st.dataframe(df)
        except Exception as e:
            st.error(f"Error fetching data: {e}")
