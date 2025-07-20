
import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth, exceptions, initialize_app
import requests
import urllib.parse


if not firebase_admin._apps:
    try:
        cred = credentials.Certificate("chatbot-ea635-5802804fbf3e.json")
        initialize_app(cred)
    except Exception as e:
        st.error("Could not initialize Firebase.")
        st.error(e)
        st.stop()

try:
    client_id = st.secrets["client_id"]
    client_secret = st.secrets["client_secret"]
    redirect_uri = "http://localhost:8501/" 
except KeyError:
    st.error("`client_id` or `client_secret` not found in Streamlit secrets.")
    st.info("Please add them to your .streamlit/secrets.toml file.")
    st.stop()
    
    

def login():
    """Handles the entire login flow."""
    if "user" in st.session_state:
        return

    query_params = st.query_params

    # After redirect from Google, the "state" parameter holds our role_choice
    if "state" in query_params:
        st.session_state["role_choice"] = query_params["state"]

    # The "code" is the authorization code from Google
    code = query_params.get("code")
    if not code:
        return 

    try:
        # Exchange the authorization code for an access token
        token_url = "https://oauth2.googleapis.com/token"
        data = {
            "code": code,
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code"
        }
        token_res = requests.post(token_url, data=data).json()

        # Check for errors in the token response
        if "error" in token_res:
            st.error("Token Request Failed")
            st.json(token_res)
            st.stop()
        
        access_token = token_res["access_token"]
        
        # Use the access token to get user info
        userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
        headers = {"Authorization": f"Bearer {access_token}"}
        userinfo = requests.get(userinfo_url, headers=headers).json()
        email = userinfo.get("email")

        if not email:
            st.error("Could not fetch user email from Google.")
            st.json(userinfo)
            st.stop()

        # Create or update user in Firebase
        try:
            auth.get_user_by_email(email)
            
        except exceptions.FirebaseError:
            auth.create_user(email=email)

        # Store user info in session state
        user_record = auth.get_user_by_email(email)
        admin_emails = st.secrets["admin_emails"]
        role = "admin" if email in admin_emails else "user"
        st.session_state.user = {
            "email": email,
            "role": role,
            "uid": user_record.uid
        }
        
        #  Clear query params to prevent re-using the auth code
        st.query_params.clear()
        st.rerun()

    except Exception as e:
        st.error("An error occurred during the login process.")
        st.exception(e)
        st.stop()


def show_login():
    """Displays the 'Login with Google' button."""
    role_choice = st.session_state.get("role_choice", "User")
    
    # We pass the role_choice in the 'state' parameter
    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": "openid email profile",
        "state": role_choice 
    }
    auth_url = "https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode(params)
    
    st.markdown(
        f'<a href="{auth_url}" target="_self" style="display: inline-block; padding: 10px 20px; background-color: #4285F4; color: white; text-align: center; text-decoration: none; border-radius: 4px; font-weight: bold;">Login with Google</a>',
        unsafe_allow_html=True
    )

def logout():
    """Logs the user out by clearing the session state."""
    st.session_state.pop("user", None)
    st.session_state.pop("role_choice", None)
    st.rerun()

def require_auth():
    """A gatekeeper function to protect pages."""
    if "user" not in st.session_state:
        login()
        if "user" not in st.session_state:
            show_login()
            st.stop()





