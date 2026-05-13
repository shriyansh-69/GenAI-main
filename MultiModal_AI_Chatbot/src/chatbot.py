# This File Sever As The MAin Logic For Application

from google import genai
import os
from src.image_handler import process_image
from dotenv import load_dotenv
import time


load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def get_response(user_input, image=None):

    # if image exists -> use image handler
    if image:
        return process_image(user_input, image)
    
    prompt = f"""
You are an expert AI assistant.

Rules:
- Answer clearly
- Use simple language
- Be concise
- If unsure, say "I don't know"

Question:
{user_input}
"""

    response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
)

    return response.text


# Image Generation 
def generate_image(prompt):

    if not prompt:
        return "Please enter a valid prompt."

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"""
You are an AI image generation assistant.

Generate  a realistic image for this prompt:

{prompt}
"""
        )

        return response.text

    except Exception as e:
        return f"Gemini Error: {str(e)}"