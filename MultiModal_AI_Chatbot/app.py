import streamlit as st
from src.chatbot import get_response, generate_image
from PIL import Image

st.title("MultiModal AI Chatbot")

# Mode Selection Option
mode = st.selectbox("Select Mode", ["Chat", "Image Generation"])

# User input
user_input = st.text_input("Enter Your Question")

# Image upload (Only Useful In Chatbot Mode)
uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png"])

if st.button("Send"):

    if not user_input:
        st.warning("Please enter a prompt!")

    else:
        # 🔹 Image Generation Mode
        if mode == "Image Generation":
            response = generate_image(user_input)
            st.write("### Generated Output:")
            st.write(response)

        # 🔹 Chat Mode
        else:
            image = None

            if uploaded_file:
                image = Image.open(uploaded_file)
                st.image(image, caption="Uploaded Image")

            response = get_response(user_input, image)

            st.write("### Response:")
            st.write(response)