import streamlit as st
from simple_salesforce import Salesforce, SalesforceAuthenticationFailed
import pandas as pd
import requests

# UI Title
st.title("🔐 Salesforce Login and Data Fetcher")

# Salesforce credentials
username = st.text_input("Username", placeholder="Enter Salesforce username")
password = st.text_input("Password", placeholder="Enter Salesforce password", type="password")
security_token = st.text_input("Security Token", placeholder="Enter Salesforce security token", type="password")
domain = st.selectbox("Select Domain", ["login", "test"])  # login = production, test = sandbox

# Initialize session state
if "sf" not in st.session_state:
    st.session_state.sf = None
    st.session_state.logged_in = False

# Login button
if st.button("Login"):
    try:
        # Use the user inputs for credentials
        sf = Salesforce(
            username=username,
            password=password,
            security_token=security_token,
            domain=domain  # Use the selected domain
        )
        st.session_state.sf = sf
        st.session_state.logged_in = True
        st.success("✅ Salesforce Login Successful!")
    except SalesforceAuthenticationFailed:
        st.session_state.sf = None
        st.session_state.logged_in = False
        st.error("❌ Salesforce Login Failed. Please check your credentials.")

# Fetch data button (only active if logged in)
if st.session_state.logged_in:
    if st.button("Fetch Data"):
        try:
            # Call your FastAPI backend
            api_url = "http://localhost:8000/get-full-csv"  # Update with your deployed API URL if needed
            response = requests.get(api_url)

            if response.status_code == 200:
                data = response.json()
                df_api = pd.DataFrame(data)
                st.success("✅ Data Fetched from FastAPI API!")
                st.dataframe(df_api)
            else:
                st.error(f"❌ API responded with status code: {response.status_code}")
        except Exception as e:
            st.error(f"❌ Error fetching from API: {e}")
