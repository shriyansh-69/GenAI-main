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
import pandas as pd

# -----------------------------------------
# Load env variables
# ----------------------------------------- 

load_dotenv()

# -----------------------------------------
# Base Path
# ----------------------------------------- 

base_dir = os.path.dirname(os.path.dirname(__file__))
vector_path = os.path.join(base_dir,"vector_store")

# Load the intent file 
csv_path = os.path.join(base_dir,"data","intents.csv")
try:
    df = pd.read_csv(csv_path,on_bad_lines='skip')
    intent_dict = dict(zip(df["question"], df["answer"]))
except Exception as e:
    print("CSV Load Error:", e)
    intent_dict = {}



# -----------------------------------------
# Load embeddings
# ----------------------------------------- 

embeddings = HuggingFaceEmbeddings(
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
)

# -----------------------------------------
# Load FAISS
# ----------------------------------------- 

if not os.path.exists(vector_path):
    print("Vector store not found. Creating...")

    import json

    data_path = os.path.join(base_dir, "data", "arxiv_cs_clean.json")

    with open(data_path, "r", encoding="utf-8") as f:
        papers = json.load(f)

    texts = [p["clean_abstract"] for p in papers if p.get("clean_abstract")]

    vectorstore = FAISS.from_texts(texts[:5000], embeddings)  # limit for cloud
    vectorstore.save_local(vector_path)

else:
    vectorstore = FAISS.load_local(
        vector_path,
        embeddings,
        allow_dangerous_deserialization=True
    )

retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

# -----------------------------------------
# Prompt
# ----------------------------------------- 

prompt = PromptTemplate(
    input_variables=["context","question"],
    template="""
You are an expert AI research assistant.

Rules:
- Answer clearly and concisely
- Use simple language
- If unsure, say "I don't know"
- Use context properly

Context:
{context}

Question:
{question}
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
    q = query.lower().strip()

    greetings = ["hi", "hello", "hey", "good morning", "good evening"]

    # Exact match or startswith
    if any(q == greet or q.startswith(greet) for greet in greetings):
        return "Hello! 👋 How can I help you with research today?"

    # CSV intent
    if q in intent_dict:
        return intent_dict[q]

    # RAG fallback
    return qa_chain.run(query)

# CLI 
if __name__ == "__main__":
    while True:
        q = input("Ask: ")
        if q.lower() == "exit":
            break
        print("\n", ask_question(q), "\n")

