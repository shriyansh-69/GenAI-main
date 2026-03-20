# -----------------------------------------
# Import's
# -----------------------------------------

import streamlit as st
from src.rag_pipeline import ask_question


# -----------------------------------------
# Style
# -----------------------------------------
st.set_page_config(page_title="ResearchMind AI")

st.title("🧠 Research AI Chatbot")

# Store chat session history
if "message" not in st.session_state:
    st.session_state.messages = []

# Show Previous messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Input Box
query = st.chat_input("Ask your question...")

if query:
    # show user message
    st.session_state.messages.append({"role":"user","content":"query"})
    st.chat_message("user").write(query)

    # generate response 
    with st.spinner("Thinking...."):
        answer = ask_question(query)

    # show bot response 
    st.session_state.messages.append({"role":"assitant","content":answer})
    st.chat_message("assistant").write(answer)

