# --------------------------------------------------------   Import's   -----------------------------------------------------------
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.embeddings import  HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
from pathlib import Path
import hashlib
import datetime
import json

# -----------------------------------------------------------  API-Key   --------------------------------------------------------------------
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")



# ----------------------------------------------------   Large-Language Model(LLM)   --------------------------------------------------------------------
llm = ChatGroq(
    api_key=os.environ["GROQ_API_KEY"],
    model="llama-3.1-8b-instant",
    temperature=0.1
)


embeddings =  HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Base Directory
base_dir =  Path(__file__).resolve().parent.parent

# Dataset Path(Relative Path)
data_path = base_dir/ "dataset" / "et.csv"

# FAISS Index Path
vectordb_file_path = base_dir/"faiss_index"

# meta Data Path
metadata_path = base_dir/ "metadata_store.json"


# Hashing Function
def generate_hash(text):
    return hashlib.sha256(text.encode()).hexdigest()


# Creating And Updating   VectorDB
def create_vector_db():
    loader = CSVLoader(
        file_path=str(data_path),
        encoding="utf-8",
        csv_args={
            "delimiter": ",",
            "quotechar": '"'
        }
    )

    documents = loader.load()

    # Load existing hashes 
    if metadata_path.exists():
        with open(metadata_path,"r") as f:
            stored_hashes = set(json.load(f))
    else:
        stored_hashes = set()

    new_documents = []
    new_hashes = set()

    for doc in documents:
        doc_hash = generate_hash(doc.page_content)
        if doc_hash not in stored_hashes:
            new_documents.append(doc)
            new_hashes.add(doc_hash) 

    if not new_documents:
        current_timer = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{current_timer}] No New Documents To add.")
        return
    
        
    if os.path.exists(vectordb_file_path):
        vectordb = FAISS.load_local(
            str(vectordb_file_path),
            embeddings,
            allow_dangerous_deserialization = True
        )
        vectordb.add_documents(new_documents)
    else:
        vectordb = FAISS.from_documents(new_documents, embeddings)
    
    vectordb.save_local(str(vectordb_file_path))

    # Updated Metadata file
    stored_hashes.update(new_hashes)
    with open(metadata_path,"w") as f:
        json.dump(list(stored_hashes),f)

    
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
    print(f"[{current_time}] Added {len(new_documents)} new Documents. ")
 

def get_qa_chain():

    vectordb = FAISS.load_local(
    vectordb_file_path,
    embeddings,
    allow_dangerous_deserialization=True
    )
    

    retriever = vectordb.as_retriever(search_kwargs={"k": 4})

    prompt = PromptTemplate(
        template="""
        Answer the question ONLY using the context below.
        If the answer is not found, say "I don't know."

        CONTEXT:
        {context}

        QUESTION:
        {question}
        """,
        input_variables=["context", "question"]
    )

    chain = (
        {
            "context": retriever,
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
    )

    return chain


if __name__ == "__main__":
    create_vector_db()
    chain = get_qa_chain()
    print(chain.invoke("Who are you?"))
