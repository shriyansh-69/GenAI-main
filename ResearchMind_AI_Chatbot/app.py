# -----------------------------------------
# Import's
# -----------------------------------------

import streamlit as st
from src.rag_pipeline import ask_question,retriever

# -----------------------------------------
# Style
# -----------------------------------------
st.set_page_config(page_title="ResearchMind AI")

st.title("🧠 Computer Science Research AI Chatbot")
st.caption("Ask questions about Computer Science research papers")

# -----------------------------------------
# Store chat session history
# -----------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------------------
# Show Previous messages
# -----------------------------------------
for msg in st.session_state.messages:
    avatar = "🧠" if msg["role"] == "assistant" else "👱"
    with st.chat_message(msg["role"], avatar=avatar):
        st.write(msg["content"])


# -----------------------------------------
# Input box
# -----------------------------------------
query = st.chat_input("Ask your question...")

if query:
    # show user message
    st.session_state.messages.append({"role":"user","content": query})
    st.chat_message("user",avatar="👱").write(query)

    # generate response 
    with st.spinner("Thinking...."):
        response = ask_question(query)
    
    answer = response["answer"]
    response_type = response["type"]

    # show bot response 
    st.session_state.messages.append({"role":"assistant","content": answer})
    st.chat_message("assistant",avatar="🧠").write(answer) 

    # ---------- Show sources Only When Needed ----------
    if response_type != "no_source":
        docs = retriever.get_relevant_documents(query)

        with st.expander("📄 View Sources"):
            for i, doc in enumerate(docs):
                st.markdown(f"**Source {i+1}:**")
                st.write(doc.page_content[:300])
                st.markdown("---")





