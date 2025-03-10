import streamlit as st
import os
from dotenv import load_dotenv
from cryptography.fernet import Fernet
from db import get_db_connection  # Import database connection

# Load environment variables
if "general" in st.secrets and "FERNET_KEY" in st.secrets["general"]:
    FERNET_KEY = st.secrets["general"]["FERNET_KEY"]
else:
    load_dotenv()
    FERNET_KEY = os.getenv("FERNET_KEY")

if not FERNET_KEY:
    raise ValueError("⚠️ Encryption key missing! Set FERNET_KEY in `.env` file.")

FERNET_KEY = FERNET_KEY.encode()  # Convert string to bytes
cipher_suite = Fernet(FERNET_KEY)

def encrypt_data(data):
    """Encrypts the given data using Fernet encryption."""
    return cipher_suite.encrypt(data.encode()).decode() if data else None

def decrypt_data(data):
    """Decrypts the given encrypted data using Fernet encryption."""
    return cipher_suite.decrypt(data.encode()).decode() if data else None
    
def insert_candidate(full_name, email, phone, experience, position, location, tech_stack):
    """Insert candidate data into the database with error handling."""
    try:
        encrypted_email = encrypt_data(email)  
        encrypted_phone = encrypt_data(phone)  

        experience = int(experience) if experience else 0  

        conn = get_db_connection()
        cursor = conn.cursor()

        sql = """
        INSERT INTO candidates (full_name, email, phone, experience, position, location, tech_stack)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (full_name, encrypted_email, encrypted_phone, experience, position, location, tech_stack))

        conn.commit()
        cursor.close()
        conn.close()

        st.success("✅ Candidate information has been securely saved in MySQL!")

    except Exception as e:
        st.error(f"❌ Database Error: {str(e)}")

def collect_candidate_info():
    st.subheader("Candidate Information")
    
    full_name = st.text_input("Full Name")
    email = st.text_input("Email Address")
    phone = st.text_input("Phone Number")
    experience = st.selectbox("Years of Experience", options=list(range(0, 31)), index=0)
    if experience is None:
        st.error("⚠️ Experience cannot be empty!")
        return
    experience = int(experience) if experience is not None else 0    
    position = st.text_input("Desired Position(s)")
    location = st.text_input("Current Location")
    tech_stack = st.text_area("Tech Stack (comma-separated)")

    if st.button("Submit Information"):
        # **Validation to Prevent Errors**
        if not full_name or not email or not phone or not position or not location:
            st.error("⚠️ Please fill in all required fields!")
            return
        
        insert_candidate(full_name, email, phone, experience, position, location, tech_stack)
