import os
import json
import re

from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Gemini
genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

# Gemini model
model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


def extract_structured_data(text):

    prompt = f"""
Extract resume data and return ONLY valid JSON.

Format:
{{
    "name": "",
    "email": "",
    "phone": "",
    "skills": [],
    "education": [],
    "projects": [],
    "experience": [],
    "ats_score": "85",
    "summary": "",
    "missing_skills": []
}}

Instructions:
- ats_score MUST be a number between 1 and 100
- Return ONLY JSON
- No markdown
- missing_skills should contain important missing industry skills

Resume:
{text}
"""

    try:

        response = model.generate_content(prompt)

        raw_text = response.text

        # Remove markdown formatting
        cleaned = raw_text.replace(
            "```json",
            ""
        ).replace(
            "```",
            ""
        ).strip()

        # Extract JSON
        match = re.search(
            r'\{.*\}',
            cleaned,
            re.DOTALL
        )

        if match:

            json_text = match.group()

            data = json.loads(json_text)

            return data

        else:

            return {
                "error": "No JSON found",
                "raw_response": cleaned
            }

    except Exception as e:

        return {
            "error": str(e)
        }

    except Exception as e:
        return {"error": str(e)}
