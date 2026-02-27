import streamlit as st
from src.lang_chain_helper import get_qa_chain
from src.scheduler import start_scheduler

st.set_page_config(page_title="NullClass Service Chatbot", page_icon="🤖")

if "start_scheduler" not in st.session_state:
    start_scheduler()
    st.session_state.scheduler_started = True
 

st.title("NullClass Service Chatbot 🤖")

# Intialize Chat History 
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


if prompt := st.chat_input("Ask Your Question:- "):

    st.chat_message("user").write(prompt)
    st.session_state.messages.append({"role":"user","content" : prompt})

    chain = get_qa_chain()
    response = chain.invoke(prompt)
    answer =  response.content

    st.chat_message("assistant").write(answer)
    st.session_state.messages.append({"role":"assistant","content":answer})


    


   


    



