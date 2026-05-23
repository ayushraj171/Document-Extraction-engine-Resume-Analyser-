import os
import json
import re
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")


def extract_structured_data(text):

    prompt = f"""
Extract resume data and return ONLY valid JSON.

{{
    "name": "",
    "email": "",
    "phone": "",
    "skills": [],
    "education": [],
    "projects": [],
    "experience": [],
    "ats_score": 85,
    "summary": "",
    "missing_skills": []
}}

Rules:
- Return ONLY JSON
- No markdown
- ats_score must be 1–100

Resume:
{text}
"""

    try:
        response = model.generate_content(prompt)

        if not response or not response.text:
            return {"error": "Empty response from Gemini"}

        cleaned = response.text.replace("```json", "").replace("```", "").strip()

        match = re.search(r'\{.*\}', cleaned, re.DOTALL)

        if not match:
            return {"error": "No JSON found", "raw": cleaned}

        return json.loads(match.group())

    except Exception as e:
        return {"error": str(e)}
        }
