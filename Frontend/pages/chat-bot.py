import streamlit as st
from streamlit_chat import message
import requests

st.set_page_config(
    page_title="Doc Bot",
    page_icon=":robot:"
)

API_URL = "http://127.0.0.1:8000/chat"


st.header("Doc Bot")


if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

def query(payload):
    response = requests.post(API_URL,json=payload )
    
    return response.json()




user_input = ''
input_text = st.text_input("You: ","Hello, how are you?", key="input")
if st.button("generate"):
    user_input = input_text

    if user_input:
        payload = {
    "message": user_input
    }
        output = query(payload)

        st.session_state.past.append(user_input)
        st.session_state.generated.append(output["reply"]+'\n\n do let me know if you need any more assistance')

    if st.session_state['generated']:

        for i in range(len(st.session_state['generated'])-1, -1, -1):
            message(st.session_state["generated"][i], key=str(i))
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
