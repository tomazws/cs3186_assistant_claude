from anthropic import Anthropic
import streamlit as st

################################################################################
##                           INITIALIZE APPLICATION                           ##
################################################################################
# Initialize OpenAI Assistant API
client = Anthropic(api_key=st.secrets['CLAUDE_API_KEY'])

if 'messages' not in st.session_state:
    st.session_state.messages = []

################################################################################
##                                  LAYOUTS                                   ##
################################################################################
# Create title and subheader for the Streamlit page
st.title('CS 3186 Student Assistant Chatbot')
st.subheader('Using Anthropic Claude API')
st.write('Testing')

message = client.messages.create(
    model="claude-3-opus-20240229",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Hello, Claude"}
    ]
)

st.write(message.content)