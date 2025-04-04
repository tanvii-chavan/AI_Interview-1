import streamlit as st
import re
import mysql.connector
from otp_auth import send_otp  # Import only send_otp function

# Hide Sidebar Completely & Use Full Screen
st.markdown("""
    <style>
        [data-testid="stSidebar"], [data-testid="stSidebarNav"], .st-emotion-cache-1f391y8 {
            display: none !important;
        }
        /* Full-screen layout */
        .main-container {
            display: flex;
            height: 100vh; /* Full viewport height */
        }
        .left-half, .right-half {
            flex: 1;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
       
        /* Fixing Font & Color of "Signup" */
        .signup-title {
            color: #004aad !important;
            font-size: 28px !important;
            font-weight: bold !important;
            font-family: 'Poppins', sans-serif !important;
            margin-bottom: 10px !important;
            padding: 0px !important;
        }
        /* Style Signup Button */
        .stButton>button {
            background-color: #004aad !important;
            color: white !important;
            width: 100%;
            padding: 12px;
            font-size: 18px;
            font-weight: bold;
            font-family: 'Poppins', sans-serif;
            border-radius: 8px;
            border: none;
            transition: 0.3s;
        }
        .stButton>button:hover {
            background-color: #00338c !important;
        }
        /* Fix Textbox Behavior */
        .stTextInput>div>div>input {
            border-radius: 8px !important;
            font-size: 16px !important;
            padding: 10px !important;
            border: 1px solid #cccccc !important;
        }
        /* Hide Extra Eye Icon */
        input::-ms-reveal,
        input::-webkit-contacts-auto-fill-button,
        input::-webkit-credentials-auto-fill-button {
            display: none !important;
        }
   
    </style>
""", unsafe_allow_html=True)

# Full-Screen Layout: Two Equal Columns
col1, col2 = st.columns(2)

# Left Half - Image
with col1:
    st.image("images/login.jpg", use_container_width=True)  # Add your image path

# Right Half - Signup Form
with col2:
    st.markdown("<div class='signup-container'>", unsafe_allow_html=True)
    st.markdown("<h2 class='signup-title'>Sign Up</h2>", unsafe_allow_html=True)  

    # Password validation function
    def is_valid_password(password):
        return (re.search(r'[A-Z]', password) and
                re.search(r'\d', password) and
                re.search(r'[!@#$%^&*(),.?\":{}|<>]', password) and
                len(password) >= 8)

    # **Signup Form**
    with st.form("signup_form"):
        username = st.text_input("Username", placeholder="Enter your username")
        email = st.text_input("Email", placeholder="Enter your email", autocomplete="off")
        password = st.text_input("Password", type="password", placeholder="Enter your password", autocomplete="off")
        confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password", autocomplete="off")
        submit_button = st.form_submit_button("Sign Up")

    # **Signup Logic**
    if submit_button:
        if not username or not email or not password or not confirm_password:
            st.warning("⚠️ Please fill all fields!")
        elif password != confirm_password:
            st.error("❌ Passwords do not match!")
        elif not is_valid_password(password):
            st.error("❌ Password must have at least 1 uppercase, 1 number, 1 special character & be 8+ characters long.")
        else:
            # Store user details temporarily
            st.session_state["signup_username"] = username
            st.session_state["signup_email"] = email
            st.session_state["signup_password"] = password

            # Send OTP
            if send_otp(email):
                st.switch_page("pages/verify_otp.py")

    st.markdown("</div>", unsafe_allow_html=True)  # Close signup container
