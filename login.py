import streamlit as st
import mysql.connector

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
       
        /* Fixing Font & Color of "Login" */
        .login-title {
            color: #004aad !important;
            font-size: 28px !important;
            font-weight: bold !important;
            font-family: 'Poppins', sans-serif !important;
            margin-bottom: 10px !important;
            padding: 0px !important;
        }
        /* Style Login Button */
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

# Right Half - Login Form
with col2:
    st.markdown("<div class='login-container'>", unsafe_allow_html=True)
    st.markdown("<h2 class='login-title'>Login</h2>", unsafe_allow_html=True)  

    username = st.text_input("Username", placeholder="Enter your username")  
    password = st.text_input("Password", type="password", placeholder="Enter your password")  

    if st.button("Login"):
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",
            database="ai_mock_interview"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            st.success("✅ Login Successful!")
        else:
            st.error("❌ Invalid Credentials!")

    # Signup Link
    col1, col2 = st.columns([0.5, 1])  
    with col1:
        st.write("Don't have an account?")
    with col2:
        st.page_link("pages/signup.py", label="Create an account")

    st.markdown("</div>", unsafe_allow_html=True)  # Close login container

verify_otp.py

import streamlit as st
import mysql.connector
from otp_auth import verify_otp, send_otp
import time

# Hide Sidebar Completely & Use Full Screen
st.markdown("""
    <style>
        [data-testid="stSidebar"], [data-testid="stSidebarNav"] {
            display: none !important;
        }
        /* Full-screen layout */
        .main-container {
            display: flex;
            height: 100vh;
        }
        .left-half, .right-half {
            flex: 1;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        /* Fixing Font & Color of "Verify OTP" */
        .otp-title {
            color: #004aad !important;
            font-size: 28px !important;
            font-weight: bold !important;
            font-family: 'Poppins', sans-serif !important;
            margin-bottom: 10px !important;
            padding: 0px !important;
        }
        /* Style Buttons */
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

# Right Half - OTP Verification Form
with col2:
    st.markdown("<div class='otp-container'>", unsafe_allow_html=True)
    st.markdown("<h2 class='otp-title'>Verify OTP</h2>", unsafe_allow_html=True)

    if "signup_email" not in st.session_state:
        st.error("⚠️ No signup data found. Please sign up again.")
        st.switch_page("pages/signup.py")

    email = st.session_state["signup_email"]
    username = st.session_state["signup_username"]
    password = st.session_state["signup_password"]

    st.success(f"✅ OTP sent successfully to {email}!")

    otp_input = st.text_input("Enter OTP", placeholder="Enter the OTP received", type="password", autocomplete="off")

    # Buttons Layout
    col1, col2 = st.columns([1, 1])  
    with col1:
        verify_clicked = st.button("Verify OTP")
    with col2:
        resend_clicked = st.button("Resend OTP")

    # Handle Verify OTP
    if verify_clicked:
        if verify_otp(email, otp_input):
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="1234",
                database="ai_mock_interview"
            )
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                        (username, email, password))
            conn.commit()
            conn.close()

            st.success("✅ Account Created Successfully!")
            time.sleep(2)
            st.switch_page("login.py")  # Redirect to login page
        else:
            st.error("❌ Invalid OTP!")

    # Handle Resend OTP
    if resend_clicked:
        send_otp(email)
        st.markdown("<div style='text-align: center; width: 100%;'><span style='color: green; font-weight: bold;'>✅ New OTP Sent!</span></div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)  # Close OTP container

otp_auth.py

import random
import smtplib

user_db = {}  

def send_otp(email):
    otp = str(random.randint(1000, 9999))
    user_db[email] = otp

    sender_email = "smart.carrer.prep25@gmail.com"
    sender_password = "rxyi vtlp pxtf ahqs"

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)

        message = f"Subject: Your OTP Code\n\nYour OTP is: {otp}"
        server.sendmail(sender_email, email, message)
        server.quit()

        return True  
    except Exception as e:
        print("Error sending email:", e)
        return False  
def verify_otp(email, entered_otp):
    return email in user_db and user_db[email] == entered_otp