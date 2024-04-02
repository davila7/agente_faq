import streamlit as st
from judini.codegpt import CodeGPTPlus
from dotenv import load_dotenv
import os
import time
load_dotenv()


# connect with codegpt
api_key= os.getenv('CODEGPT_API_KEY')
agent_id= os.getenv('CODEGPT_AGENT_ID')
org_id= os.getenv('ORG_ID')

st.set_page_config(layout="centered")

st.title("Agent FAQ")
st.markdown("---")

# init chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("How can I help you?"):
    # user message history
    st.session_state.messages.append({"role":"user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            message_placeholder = st.empty()
            full_response = ""


            # connect CodeGPT SDK
            codegpt = CodeGPTPlus(api_key=api_key, org_id=org_id)
            messages = st.session_state.messages

            response_completion = codegpt.chat_completion(agent_id=agent_id, messages=messages, stream=True)

            for response in response_completion:
                time.sleep(0.05)
                full_response += (response or "")
                message_placeholder.markdown(full_response + "|")

            message_placeholder.markdown(full_response)
    
    st.session_state.messages.append({"role":"assistant", "content": full_response})



