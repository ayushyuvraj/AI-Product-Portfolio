import google.generativeai as genai
import os

# Paste your key here temporarily just to test, or set env var
# os.environ['GOOGLE_API_KEY'] = "AIza..." 
genai.configure(api_key="AIzaSyCw2Wr9dkNIC_X-5suLQt8QbREfwGpYx4U")

print("Available Models:")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)