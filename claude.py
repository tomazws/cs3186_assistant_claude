from anthropic import Anthropic
import streamlit as st
import re
import base64
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
        for item in content:
            if item['type'] == 'image':
                pass
                #st.image(item['source']['data'])
            elif item['type'] == 'text':
                # Split the message by code blocks
                messages = item['text'].split('```')
                for i in range(len(messages)):
                    message = messages[i]
                    if i % 2 == 0:
                        st.write(message)
                    else:
                        # If the message is a graphviz diagram, display it as a diagram
                        match = re.search('digraph .*{', message)
                        if match and message[-2] == '}':
                            message = message[match.start():]
                            st.graphviz_chart(message)
                        else:
                            st.code(message)
    st.write('')

def getCompletion():
    with st.spinner('Thinking ...'):
        try:
            response = client.messages.create(
                model = 'claude-3-opus-20240229',
                max_tokens = 1024,
                system = 'When illustrating a state diagram, use DOT language representation of the state diagram instead.',
                messages = st.session_state.messages
            )
            content = [
                {
                    'type': 'text',
                    'text': response.content[0].text
                }
            ]
            st.text(response.content)
            displayMessage('assistant', content)
            st.session_state.messages.append({'role': 'assistant', 'content': content})
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
    content = [
        {
            'type': 'text',
            'text': 'I would like to convert NFA to DFA'
        }
    ]
    displayMessage('user', content)
    st.session_state.messages.append({'role': 'user', 'content': content})
    getCompletion()
    
if st.sidebar.button('Generate a DFA diagram'):
    content = [
        {
            'type': 'text',
            'text': 'I would like to generate a DFA from regular expression or langage'
        }
    ]
    displayMessage('user', content)
    st.session_state.messages.append({'role': 'user', 'content': content})
    getCompletion()

# File uploader
uploaded_image = st.sidebar.file_uploader('Upload an image', type=['png', 'jpg', 'jpeg', 'gif'])

# Chat input
if prompt := st.chat_input('Ask me anything about CS 3186'):
    content = []

    # If there are files uploaded
    if uploaded_image is not None:
        # Convert the image's byte data into base64
        # image_data = base64.b64encode(uploaded_image.getvalue()).decode("utf-8")
        # st.write('-----------------')
        # st.write(uploaded_image.type)

        content.append({
            'type': 'image',
            'source': {
                'type': 'base64',
                'media_type': uploaded_image.type,
                'data': base64.b64encode(uploaded_image.getvalue()).decode("utf-8")
            }
        })

    # Display user message in chat message container and add to chat history
    content.append({
        'type': 'text',
        'text': prompt
    })
    displayMessage('user', content)
    st.session_state.messages.append({'role': 'user', 'content': content})
    getCompletion()