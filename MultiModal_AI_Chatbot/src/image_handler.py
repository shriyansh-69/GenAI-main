# This File Is For Image Handling Logic Of Chatbot

from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def process_image(user_input,image):

    if not user_input:
        user_input = "Describe this image"

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[user_input,   image]
    )


    return response.text