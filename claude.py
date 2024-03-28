from anthropic import Anthropic
import streamlit as streamlit
import uuid

################################################################################
##                           INITIALIZE APPLICATION                           ##
################################################################################
# Initialize OpenAI Assistant API
client = Anthropic(api_key=st.secrets['CLAUDE_API_KEY'])

# Initialize session state variables
if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if 'thread' not in st.session_state:
    st.session_state.thread = client.beta.threads.create(
        metadata={
            'session_id': st.session_state.session_id,
        }
    )

if 'messages' not in st.session_state:
    st.session_state.messages = []