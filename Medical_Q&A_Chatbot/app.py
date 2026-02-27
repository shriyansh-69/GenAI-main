# app.py
# This File Is For Creating The Interface For Application To Make IT More Attractive And Interactive 

# Interface Library
import streamlit as st

# Function's From Different File's 
from src.entity_recognition import  extract_entities
from src.retriever import retrieve_answer

st.set_page_config(page_title="Medical Q&A Chatbot", layout="centered",page_icon="🩺")

st.title("🧑‍⚕️ Medical Q&A Chatbot")
st.write("Ask medical questions based on the MedQuAD Dataset.")

# User Input 
query = st.text_input("Enter your medical question:")

if query:
    #  Retrieve answer from dataset
    answer = retrieve_answer(query)

    st.subheader("ANSWER")
    st.write(answer)

    # Extract Medical entities
    entities = extract_entities(query)

    st.subheader("Detected Medical Entities")

    entities = extract_entities(query)

    if any(entities.values()):
        for entity_type, values in entities.items():
            if values:
                st.write(f"**{entity_type}:** {', '.join(values)}")
    else:
        st.write("No medical entities detected.")



st.markdown("----")
st.caption(
    "⚠️ This chatbot is for educational purposes only and not a substitute for professional medical advice."
)




