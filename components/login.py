import streamlit as st
import hashlib

def login():
    st.title("Login")

    account_number = st.text_input("Enter your account number (hash):")

    if st.button("Login"):
        if validate_account_number(account_number):
            st.session_state["logged_in"] = True
            st.session_state["account_number"] = account_number
            st.experimental_rerun()
        else:
            st.error("Invalid account number. Please try again.")

def validate_account_number(account_number):
    # Placeholder validation logic
    # In a real application, you would check the account number against a database or other data source
    return len(account_number) == 64 and all(c in "0123456789abcdef" for c in account_number)

def logout():
    st.session_state["logged_in"] = False
    st.session_state["account_number"] = None
    st.experimental_rerun()
