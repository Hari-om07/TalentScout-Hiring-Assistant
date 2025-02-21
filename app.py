import streamlit as st
import openai
import os
from dotenv import load_dotenv
from candidate_info import collect_candidate_info
from chatbot import generate_questions

# Load OpenAI API Key
load_dotenv()
OPENAI_API_KEY = st.secrets["general"]["OPENAI_API_KEY"]

# Check if API key is available
if not OPENAI_API_KEY:
    st.error("⚠️ OpenAI API key is missing! Please set it in your `.env` file.")
else:
    openai.api_key = OPENAI_API_KEY

# Streamlit UI Setup
st.title("TalentScout Hiring Assistant 🤖")
st.write("Welcome! I will guide you through an initial screening process.")

# Call function from candidate_info.py
collect_candidate_info()

# Collect tech stack input
tech_stack_input = st.text_input("Enter Tech Stack (comma-separated)", "Python, Django")

# Add a number input form
with st.form("my_form"):
    user_input = st.text_input("Enter a number:")
    submit = st.form_submit_button("Submit")

if submit:
    st.write(f"Received input: {user_input}")

    if user_input:  # Check if input is provided
        try:
            number = int(user_input)  # Convert safely
            st.success(f"Your number is {number}")
        except ValueError:
            st.error("Please enter a valid number.")
    else:
        st.error("Number field cannot be empty!")

# Generate questions when button is clicked
if st.button("Generate Questions"):
    tech_stack = [tech.strip() for tech in tech_stack_input.split(",")]
    questions = generate_questions(tech_stack)

    if questions:
        st.subheader("Generated Interview Questions:")
        st.write(questions) 

# Initialize Session State for Chat Messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Previous Messages
for message in st.session_state.messages:
    st.write(f"{message['role']}: {message['content']}")

# Handle user input
if user_input := st.chat_input("Ask something..."):
    
    # **Exit Mechanism**
    exit_keywords = ["exit", "quit", "bye"]
    if any(word in user_input.lower() for word in exit_keywords):
        st.write("🤖: Thank you for your time. We'll get back to you soon!")
        st.stop()  # Stop execution before appending the message

    # Store user input in session
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Generate response using OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=st.session_state.messages
    )

    reply = response["choices"][0]["message"]["content"]
    st.session_state.messages.append({"role": "assistant", "content": reply})

    # Display chatbot response
    st.write(f"🤖: {reply}")
