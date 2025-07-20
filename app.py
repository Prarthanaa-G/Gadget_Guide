import streamlit as st
from firebase_auth import login, logout, show_login
from chatbot_ui import chatbot_ui
from admin_ui import admin_ui
from htmlTemplates import css 

def main():
    st.set_page_config(page_title="Support Bot", layout="wide")
    
    st.write(css, unsafe_allow_html=True)
    
    login()

    if "user" in st.session_state:
        # This part of the code runs only when the user is successfully logged in.
        
        user = st.session_state["user"]

        st.sidebar.success(f"Logged in as: {user['email']}")
        if st.sidebar.button("Logout"):
            logout()

        # Route to the correct UI based on the role chosen before login
        if st.session_state.get("role_choice") == "Admin":
            if user.get("role") == "admin":
                admin_ui()
            else:
                st.error("Access Denied. You are not an authorized admin.")
                st.info("Please log out and sign in with an admin account.")
        else:
            chatbot_ui()
            
    else:
        # --- LOGIN VIEW ---

        st.title("Welcome to Gadget Guide 👋")
        st.markdown("# *Your Electronics Support AI Assistant* 💻")
        st.markdown("Please select your role and log in to continue.")

        # Let the user select a role
        role = st.radio(
            "",
            ["User", "Admin"],
            key="role_selection",
            horizontal=True,
        )

        # Persist role choice in session state
        if 'role_choice' not in st.session_state or st.session_state.role_choice != role:
            st.session_state.role_choice = role

        st.write("---")
        
        show_login()
        

if __name__ == "__main__":
    main()


