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

    data_path = os.path.join(base_dir, "data", "arxiv_cs.json")

    with open(data_path, "r", encoding="utf-8") as f:
        papers = json.load(f)

    texts = []

    for p in papers:
        text = p.get("abstract")

        if text and isinstance(text, str) and len(text.strip()) > 20:
            texts.append(text)

    print("Valid texts:", len(texts))

    if len(texts) == 0:
        raise ValueError("No valid abstracts found in dataset")

    vectorstore = FAISS.from_texts(texts[:5000], embeddings)
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
You are an expert AI assistant specialized in Computer Science research.

Your responsibilities:
- Answer ONLY using the provided context.
- Focus on topics like Machine Learning, AI, Data Science, Algorithms, and Computer Science research.
- If the question is NOT related to Computer Science, politely say:
  "This assistant is designed for Computer Science research questions."

Rules:
- Be clear, concise, and accurate
- Use simple and easy-to-understand language
- Do NOT make up information
- If the answer is not in the context, say: "I don't know"
- Avoid unnecessary explanations
- Keep answers relevant to the question

Context:
{context}

Question:
{question}

Answer:
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
    thanks = ["thank", "thanks", "appreciate"]
    goodbye = ["bye", "goodbye", "see you", "exit", "quit"]

    # Greeting
    if any(q.startswith(g) for g in greetings):
        return {"answer": "Hello! 👋 How can I help you with research today?", "type": "no_source"}

    # Thank you
    if any(word in q for word in thanks):
        return {"answer": "You're welcome! 😊", "type": "no_source"}

    # Goodbye
    if any(word in q for word in goodbye):
        return {"answer": "Goodbye! 👋", "type": "no_source"}

    # CSV intent
    if q in intent_dict:
        return {"answer": intent_dict[q], "type": "intent"}

    # RAG
    result = qa_chain.run(query)
    return {"answer": result, "type": "rag"}

# CLI 
if __name__ == "__main__":
    while True:
        q = input("Ask: ")
        if q.lower() == "exit":
            break
        print("\n", ask_question(q), "\n")

