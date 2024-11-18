import os

import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai


# Load environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="Chatbot",
    page_icon=":brain:",  # Favicon emoji
    layout="centered",  # Page layout option
)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Set up Google Gemini-Pro AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')


# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role


# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])


# Custom CSS styling for the title and sidebar
st.markdown(
    """
    <style>
    .custom-title {
        font-size: 46px;
        text-align: left;
        font-weight:bold;
        font-family: Open Sans;
        background: -webkit-linear-gradient(rgb(188, 12, 241), rgb(212, 4, 4));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-left:10px;

    }
        .span{
        font-size: 42px;
        
        
        
    }

    </style>
    """,
    unsafe_allow_html=True
)


# Display the chatbot's title on the page
# Display Main title
st.markdown("<p class='span'><span class='custom-title'>Chatbot </span></p>", unsafe_allow_html=True)


# Display the chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)


# Input field for user's message
user_prompt = st.chat_input("Ask me anything...")



if user_prompt:
    # Add user's message to chat and display it
    st.chat_message("user").markdown(user_prompt)

    # Send user's message to Gemini-Pro and get the response
    gemini_response = st.session_state.chat_session.send_message(user_prompt)

    # Display Gemini-Pro's response
    with st.chat_message("assistant"):
        st.markdown(gemini_response.text)