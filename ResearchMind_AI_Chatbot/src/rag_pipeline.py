# This file for retrieving the answer based on the question the user asked 

# -----------------------------------------
# Import the libraries 
# ----------------------------------------- 

import os
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain_groq import ChatGroq

# -----------------------------------------
# Load env variables
# ----------------------------------------- 

load_dotenv()

# -----------------------------------------
# Base Path
# ----------------------------------------- 

base_dir = os.path.dirname(os.path.dirname(__file__))
vector_path = os.path.join(base_dir,"vector_store")

# -----------------------------------------
# Load embeddings
# ----------------------------------------- 

embeddings = HuggingFaceEmbeddings(
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
)

# -----------------------------------------
# Load FAISS
# ----------------------------------------- 

vectorstore = FAISS.load_local(
    vector_path,
    embeddings,
    allow_dangerous_deserialization = True
)   

retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

# -----------------------------------------
# Prompt
# ----------------------------------------- 

prompt = PromptTemplate(
    input_variables=["context","question"],
    template="""
You are an expert AI research assistant.

Use the context to answer.

If unsure, say you don't know.

Context:
{context}

Question:
{question}

Give:
- Clear explanation
- Key points
- Simple language
"""
)

# -----------------------------------------
# LLM (Groq)
# ----------------------------------------- 

llm = ChatGroq(
    groq_api_key = os.getenv("GROQ_API_KEY"),
    model_name = "llama-3.1-8b-instant"
)

# -----------------------------------------
# RAG Chain
# -----------------------------------------  

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever = retriever,
    chain_type="stuff",
    chain_type_kwargs={"prompt" : prompt}
)


# -----------------------------------------
# Ask Function
# ----------------------------------------- 


def ask_question(query):
    return qa_chain.run(query)

# CLI 
if __name__ == "__main__":
    while True:
        q = input("Ask: ")
        if q.lower() == "exit":
            break
        print("\n", ask_question(q), "\n")

