# This File Sever As The Main Logic For Application

from google import genai
import os
from src.image_handler import process_image
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def get_response(user_input, image):

    # if image exists -> use image handler
    if image:
        return process_image(user_input, image)
    
    prompt = """
You are an expert AI assitant.

Rules:o
- Answer clearly
- use simple language
- be concise
- If unsure, say "I don't know" 

Question:
{user_input}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt 
    )

    return response.text