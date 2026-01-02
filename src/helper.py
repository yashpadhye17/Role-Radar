import fitz
import os
from dotenv import load_dotenv
import groq


load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
os.environ["GROQ_API_KEY"] = groq_api_key

client = groq.Client(api_key=groq_api_key)

## This function interacts with Groq's API to get a response based on the prompt provided.
def ask_groq(prompt,max_tokens=500):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=max_tokens,
        temperature=0.7,
        stream=False

    )
    return response.choices[0].message.content

## This function extracts text from an uploaded PDF file.
def extract_text_from_pdf(uploaded_file):
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    for page in doc:
        text = page.get_text()
    return text



