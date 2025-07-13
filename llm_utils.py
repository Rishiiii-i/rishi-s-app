import os
import google.generativeai as genai

# Set your Gemini API key here, or use an environment variable
genai.configure(api_key=os.getenv("GEMINI_API_KEY", "AIzaSyDVA_R-xfyL5IkWVgasqJXJEeb_EBjm8MI"))

def ask_llm(question, context):
    model = genai.GenerativeModel("gemini-1.5-flash")  # or "gemini-1.5-pro" if available
    prompt = f"Context:\n{context}\n\nQuestion: {question}\nAnswer:"
    response = model.generate_content(prompt)
    return response.text.strip()
