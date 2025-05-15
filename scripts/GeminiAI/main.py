import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

try:
  chave = os.getenv('API_KEY')
  genai.configure(api_key=chave)
  model = genai.GenerativeModel('gemini-1.5-flash')
  response = model.generate_content("What is the meaning of life?")
  print(response)
except Exception as e:
  print(f'{type(e).__name__}: {e}')
