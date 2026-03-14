## This File Is For Creating The Embedding For Word Or Sentence's That Are Stored In Vector DB


# Importing The Esstinal Library
import json
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings


# Loading The Cleaned Dataset 
with open('data/arxiv_cs_clean.json',"r",encoding="utf-8") as f:
    papers = json.load(f)

# Extracting The Text 
texts = [paper["clean_abstract"] for paper in papers]

print(f"Loaded {len(texts)} Document's")
