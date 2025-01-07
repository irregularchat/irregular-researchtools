import streamlit as st
from authlib.integrations.requests_client import OAuth2Session
from urllib.parse import urlencode
import os
import requests

# OIDC Configurations
OIDC_DISCOVERY_URL = "https://<your-idp>/.well-known/openid-configuration"
CLIENT_ID = os.getenv("OIDC_CLIENT_ID")
CLIENT_SECRET = os.getenv("OIDC_CLIENT_SECRET")
REDIRECT_URI = "http://localhost:8501/redirect"  # Update with your app's redirect URL

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

# Handle OIDC login
if st.session_state["user"] is None:
    st.title("Login with OpenID Connect")
    
    # Build the authorization URL
    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "scope": "openid profile email",
        "redirect_uri": REDIRECT_URI,
    }
    auth_url = f"{authorize_url}?{urlencode(params)}"

    if st.button("Login"):
        st.write(f"Redirecting to {auth_url}")
        st.experimental_set_query_params(redirect_to=auth_url)

    # Handle redirect
    query_params = st.experimental_get_query_params()
    if "code" in query_params:
        code = query_params["code"][0]

        # Exchange the authorization code for tokens
        client = OAuth2Session(CLIENT_ID, CLIENT_SECRET, redirect_uri=REDIRECT_URI)
        token = client.fetch_token(token_url, code=code)

        # Fetch user info
        userinfo = client.get(userinfo_url, token=token).json()

        # Store user info in session state
        st.session_state["user"] = userinfo

# Display user info
if st.session_state["user"]:
    st.success(f"Logged in as {st.session_state['user']['name']}")
    st.write(st.session_state["user"])
    if st.button("Logout"):
        st.session_state["user"] = None
        st.experimental_rerun()