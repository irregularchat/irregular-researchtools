import streamlit as st
import hashlib
import uuid

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

def create_account():
    st.title("Create Account")

    if st.button("Generate Account Number"):
        account_number = generate_account_number()
        st.write(f"Your account number (hash) is: {account_number}")
        st.write("Please save this account number securely. You will need it to log in.")

def generate_account_number():
    return hashlib.sha256(uuid.uuid4().bytes).hexdigest()
