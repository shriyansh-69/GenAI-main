#  🧑‍💻 Dynamic Customer Service RAG Chatbot

A Streamlit-based Retireval-Augmented Generation(RAG) chatbot built using FAISS Vector Database Automatically updates its Knwoledge Base Using Scheduled Background Indexing With Hash-Based Deduplication To Ensure Accurate And Up-To-Date Response Without Manual Retraining.

---
## 🌐 Live Demo 

You Can Access The Customer_Service_Chatbot At This Below Link :- <br>

🔗 [Customer Service Chatbot](https://customerservicechatbot69.streamlit.app/)

---

## Project Overview 

This Project builds a Dynamic Customer Service Chatbot That Can:
- Ingests structured Customer Service data (CSV)
- Converts Text Into Semantic embeddings 
- Stores Them In a FAISS Vector database
- Retrieves The Most Revelant Context Using Similarity Search
- Generates Ground Answers Using LLaMA 3 

Unlike traditional static Chatbot, This System:

- Automatically Ingests New Knowledge 
- Prevents Duplicate Indexing
- Updates Periodically Using a Scheduler
- Does Not Require Model Retrianing

The System Follows a Retrieval-Augmented Generation(RAG) architecture.

--- 

## How It Work 

1) Data Ingestion 
Customer support Data Is Loaded From CSV files.

2) Embedding Generation 
Each Document is converted into a 384-dimesional vector using:
sentence-transformers/all-MiniLM-L6-v2 

3) Vector Indexing
Embeddings Are Stored inside a FAISS Vector database.

4) Duplicate Prevention
Each Document Is hased using SHA256 To Prevent re-indexing duplicates.

5) Similarity Search
When a User Asks a Question:
- The Question Is Embedded 
- FAISS preforms similarity search
- Top-k Revelant Documents are Retrieved

6) Response Generation
Retrieved Context Is Passes to LLaMA 3 (via Groq API) To Generate a grounded response.

7) Automatic Updates
APScheduler Periodically updates The Knowledge base without manual retraining

---

## Objectives

- Build a dynamic customer service chatbot using Retrieval-Augmented Generation (RAG).
- Implement semantic search using vector embeddings instead of keyword matching.
- Automatically ingest and update new knowledge without retraining the model.
- Prevent duplicate indexing using hashing mechanisms.
- Generate context-aware, grounded responses using an LLM.
- Design a scalable and production-ready chatbot architecture.


---
## Tech Stack

- **Python 3.11**
- **Streamlit** – Web interface
- **LangChain** – RAG pipeline orchestration
- **FAISS** – Vector database for similarity search
- **HuggingFace Sentence Transformers** – Embedding generation  
  - Model: `sentence-transformers/all-MiniLM-L6-v2` (384D embeddings)
- **LLaMA 3 (via Groq API)** – Response generation
- **APScheduler** – Periodic automatic knowledge updates
- **python-dotenv** – Secure API key management
- **Hashlib (SHA256)** – Duplicate prevention

---

## Structure

```

Extended-Customer-Service-Chatbot/
│
├── app.py                     # Streamlit UI (entry point)
│
├── src/                       # Core logic
│   ├── lang_chain_helper.py
│   └── scheduler.py
│
├── dataset/
│   └── et.csv
│
├── storage/                   # Auto-generated (ignored in Git)
│   ├── faiss_index/
│   └── metadata_store.json
│
├── notebooks/
│   └── dynamic_rag_demo.ipynb
│
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md

```

---

## Conclusion

By combining Vector Similarity Search (FAISS), semantic embeddings, and LLaMA 3 for Response generation, the system delivers accurate, context-aware answers while continuously updating its knowledge base without retraining.

This Project Showcases:

- Pratical NLP And Embedding Usage
- Vector database Implementation
- Dynamic Data Ingestion
- Scalable RAG Architecture 
- Production-ready Chatbot design

It bridges traditional information retrieval techniques with modern LLM-Powered Conversational Systems.



















