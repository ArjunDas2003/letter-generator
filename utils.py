import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get API key
api_key = os.getenv("GEMINI_API_KEY")

# Configure Gemini with API key
genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-1.5-flash")

def generate_letter(data):
    prompt = f"""
You are an expert at writing formal college-use letters. Use the following input to write a formal letter:

From:
{data['from_name']}
{data['from_designation']}

Date: {data['date']}

To:
{data['to_name']}
{data['to_designation']}

Subject: {data['subject']}

Purpose: {data['purpose']}

Generate the letter in this format:

From:
{data['from_name']}
{data['from_designation']}

Date: {data['date']}

To:
{data['to_name']}
{data['to_designation']}

Subject: {data['subject']}

Respected Sir/Madam,

[3 short formal paragraphs based on purpose]

Yours sincerely,
{data['from_name']}
{data['from_designation']}
"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating letter: {str(e)}"
