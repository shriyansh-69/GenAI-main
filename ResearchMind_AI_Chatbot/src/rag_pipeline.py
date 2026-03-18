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
you are an expert AI research assistant.

Context:
{context}

Question:
{question}

Answer clearly and explain concepts simply.
"""
)





