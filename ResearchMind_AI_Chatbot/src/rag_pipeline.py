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


