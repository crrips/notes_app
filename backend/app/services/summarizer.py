import os

from google import genai

PROMPT_BEGIN = '''
You are a text analyst working for a company that is interested in summarizing text.
Your restriction is 256 characters. You can get not enough information to summarize the text, in this case,
you are unable to request more information and you need to summarize the text with the information you have.
Your task is to summarize the following text into a short single sentence.
'''

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def summarize(text: str) -> str:
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=PROMPT_BEGIN + text
     )
    return response.text
