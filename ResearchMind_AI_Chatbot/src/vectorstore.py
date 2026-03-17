## This File Is For Creating The Embedding For Word Or Sentence's That Are Stored In Vector DB


# Importing The Esstinal Library
import json
import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


# Using The Absolute Path 
base_dir = os.path.dirname(os.path.dirname(__file__))
data_path = os.path.join(base_dir,"data","arxiv_cs.json")

# Loading The Cleaned Dataset 
with open(data_path,"r",encoding="utf-8") as f:
    papers = json.load(f)

print(len(papers))


# Extracting The Text 
texts = []

for paper in papers:
    text = paper.get("abstract")

    if text and text.strip():
        texts.append(text)

print(f"Loaded {len(texts)} Document's")

# Load Embedding Model
embeddings = HuggingFaceEmbeddings(
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
)


# Generating text embeddings And Stored Them In FAISS
vectorstore = FAISS.from_texts(texts,embeddings)

# Defining The Path To Save The vector store
vector_path = os.path.join(base_dir, "vector_store")

# Create a folder if it does not exist
os.makedirs(vector_path,exist_ok=True)

#Save FAISS index locally
vectorstore.save_local(vector_path)

print("FAISS vector store created successfully!")
print(f"Saved at: {vector_path}")