import streamlit as st
from chatbot import Chatbot

st.set_page_config(page_title="AI Chatbot", layout="centered")

st.title("🤖 Free AI Chatbot (OpenRouter)")

# Initialize chatbot
if "bot" not in st.session_state:
    st.session_state.bot = Chatbot()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User input
user_input = st.chat_input("Type your message...")

if user_input:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # ⏳ Loading spinner
    with st.spinner("Thinking..."):
        reply = st.session_state.bot.get_response(user_input)

    # Show bot response
    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.write(reply)