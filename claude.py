from anthropic import Anthropic
import streamlit as st
import re
import prompts

################################################################################
##                           INITIALIZE APPLICATION                           ##
################################################################################
# Initialize OpenAI Assistant API
client = Anthropic(api_key=st.secrets['CLAUDE_API_KEY'])

if 'messages' not in st.session_state:
    st.session_state.messages = []

################################################################################
##                                 FUNCTIONS                                  ##
################################################################################
# Process the messsage and display it in the chat message container and also append message to chat history
def displayMessage(role, content):
    st.text(content)
    with st.chat_message(role):
        # Split the message by code blocks
        messages = content.split('```')
        for message in messages:
            # If the message is a graphviz diagram, display it as a diagram
            match = re.search('digraph .*{', message)
            if match and message[-2] == '}':
                message = message[match.start():]
                st.graphviz_chart(message)
            else:
                st.write(message)
    st.write('')

def getCompletion(prompt):
    with st.spinner('Thinking ...'):
        try:
            response = client.messages.create(
                model = 'claude-3-opus-20240229',
                max_tokens = 1024,
                system = 'When illustrating a state diagram, use DOT language representation of the state diagram instead.',
                messages = st.session_state.messages
            )
            st.session_state.messages.append({'role': 'assistant', 'content': response.content[0].text})
            st.text(response.content)
            displayMessage('assistant', response.content[0].text)
        except Exception as e:
            st.error(f'Error: {e}')

################################################################################
##                                  LAYOUTS                                   ##
################################################################################
# Create title and subheader for the Streamlit page
st.title('CS 3186 Student Assistant Chatbot')
st.subheader('Using Anthropic Claude API')

# Display chat messages
for message in st.session_state.messages:
    displayMessage(message['role'], message['content'])

with st.sidebar:
    st.write('Features')
    
if st.sidebar.button('Convert NFA to DFA'):
    message = 'I would like to convert NFA to DFA'
    displayMessage('user', message)
    st.session_state.messages.append({'role': 'user', 'content': message})
    getCompletion(message)
    
if st.sidebar.button('Generate a DFA diagram'):
    message = 'I would like to generate a DFA from regular expression or langage'
    displayMessage('user', message)
    st.session_state.messages.append({'role': 'user', 'content': message})
    getCompletion(message)

# Chat input
if prompt := st.chat_input('Ask me anything about CS 3186'):
    # Display user message in chat message container and add to chat history
    displayMessage('user', prompt)
    st.session_state.messages.append({'role': 'user', 'content': prompt})
    getCompletion(prompt)