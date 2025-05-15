import os
from dotenv import load_dotenv
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

load_dotenv()

try:
    chave = os.getenv('API_KEY')
    genai.configure(api_key=chave)
    model = genai.GenerativeModel('gemini-1.5-flash')
    ytt_api = YouTubeTranscriptApi()
    transcript = ytt_api.get_transcript('3ykbBCzpJwU', languages=['pt'])

    text = '' 
    for i in transcript:
        text += i['text'] + ' '
    
    response = model.generate_content(f"Resuma esse texto transcrito em 500 palavras: \n {text}")
    print(response.text)
except Exception as e:
    print(f'{type(e).__name__}: {e}')
