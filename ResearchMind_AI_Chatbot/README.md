# 🧠 ResearchMind AI Chatbot


A Streamlit-based AI chatbot that answers complex Computer Science questions using research papers from the arXiv dataset with Retrieval-Augmented Generation (RAG).

---

## 🌐 Live Demo

You Can Access The ResearchMind_AI_Chatbot At This Below Link :- <br>

🔗 [ResearchMind_AI_Chatbot](https://researchmindaichatbot.streamlit.app/) # Not Working Right Now

---

## 📌 Project Overview

This project uses the arXiv dataset (Computer Science papers) to build an intelligent chatbot capable of answering technical questions, explaining concepts, and summarizing research.

It combines semantic search with Large Language Models to provide accurate and context-aware responses.

---

## ⚙️ How It Works

- Research papers are filtered from arXiv dataset (Computer Science domain)
- Abstracts are cleaned using NLP preprocessing:
  - Lowercasing  
  - Regex cleaning  
  - Stopword removal  
  - Lemmatization  
- Text is converted into embeddings using HuggingFace models  
- FAISS vector database is created for fast similarity search  
- User query is embedded and matched with relevant documents  
- Retrieved context is passed to LLM (Groq - LLaMA 3)  
- Final answer is generated using RAG pipeline  
- CSV-based intents handle greetings and basic queries  

---

## 🧱 Tech Stack

- Python 3.11  
- Streamlit  
- LangChain  
- FAISS  
- HuggingFace Embeddings  
- Groq LLM (LLaMA 3)  
- NLTK  
- Pandas  

---

## 📂 Project Structure

```
ResearchMind_AI_Chatbot/
│
├── app.py
├── requirements.txt
├── README.md
├── .env
├── .gitignore
│
├── data/
│   ├── arxiv_cs.json
│   ├── arxiv_cs_clean.json
│   └── intents.csv
│
├── src/
│   ├── preprocess.py
│   ├── vectorstore.py
│   ├── rag_pipeline.py
│
├── vector_store/   # (generated, ignored in git)
│
├── notebook/
│   └── demo.ipynb

```