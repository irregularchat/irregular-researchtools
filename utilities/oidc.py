import streamlit as st
from authlib.integrations.requests_client import OAuth2Session
from urllib.parse import urlencode
import os
import requests
from dotenv import load_dotenv

load_dotenv()
# OIDC Configurations
OIDC_DISCOVERY_URL = os.getenv("OIDC_DISCOVERY_URL")
OIDC_CLIENT_ID = os.getenv("OIDC_CLIENT_ID")
OIDC_CLIENT_SECRET = os.getenv("OIDC_CLIENT_SECRET")
OIDC_REDIRECT_URI = os.getenv("OIDC_REDIRECT_URI")

print("OIDC_DISCOVERY_URL:", OIDC_DISCOVERY_URL)
print("OIDC_CLIENT_ID:", OIDC_CLIENT_ID)
print("OIDC_CLIENT_SECRET:", OIDC_CLIENT_SECRET)
print("OIDC_REDIRECT_URI:", OIDC_REDIRECT_URI)

# Store session state
if "user" not in st.session_state:
    st.session_state["user"] = None

def get_oidc_config(discovery_url):
    """Fetch OIDC provider configuration."""
    resp = requests.get(discovery_url)
    return resp.json()

oidc_config = get_oidc_config(OIDC_DISCOVERY_URL)
authorize_url = oidc_config["authorization_endpoint"]
token_url = oidc_config["token_endpoint"]
userinfo_url = oidc_config["userinfo_endpoint"]

def authenticate_user(button_key="login_button", login_link_key="oidc_login_button"):
    """Handle OIDC login."""
    def handle_login():
        # Set a flag to indicate that login has been triggered
        st.session_state["login_triggered"] = True

    if st.session_state.get("user") is None:
        st.title("Login with OpenID Connect")
        
        # Build the authorization URL
        params = {
            "client_id": OIDC_CLIENT_ID,
            "response_type": "code",
            "scope": "openid profile email",
            "redirect_uri": OIDC_REDIRECT_URI,
        }
        auth_url = f"{authorize_url}?{urlencode(params)}"

        if st.button("Login", key=button_key, on_click=handle_login):
            # The login logic is now handled in the callback
            pass

        # Display the OIDC login link if login is triggered
        if st.session_state.get("login_triggered"):
            if st.button("OIDC Login", key=login_link_key):
                st.markdown(f"[Click here to login]({auth_url})", unsafe_allow_html=True)

        # Handle redirect
        query_params = st.experimental_get_query_params()
        if "code" in query_params:
            code = query_params["code"][0]

            # Exchange the authorization code for tokens
            client = OAuth2Session(OIDC_CLIENT_ID, OIDC_CLIENT_SECRET, redirect_uri=OIDC_REDIRECT_URI)
            token = client.fetch_token(token_url, code=code)

            # Fetch user info
            userinfo = client.get(userinfo_url, token=token).json()

            # Store user info in session state
            st.session_state["user"] = userinfo

    # Display user info
    if st.session_state.get("user"):
        st.success(f"Logged in as {st.session_state['user']['name']}")
        st.write(st.session_state["user"])
        if st.button("Logout"):
            st.session_state["user"] = None
            st.experimental_set_query_params()  # Clear query params to refresh
            st.rerun()