import os

from dotenv import load_dotenv
from google import genai

from src.database.connection import save_meeting


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not set in the .env file")


client = genai.Client(api_key=api_key)


def analyze_meeting(meeting_text):
    """Analyze meeting notes with Gemini and save the result."""

    prompt = f"""
You are a Meeting Intelligence AI Agent.

Analyze the following meeting notes and extract:

1. A short summary
2. Discussion points
3. Promises or commitments
4. Follow-up actions

Meeting notes:
{meeting_text}

Return the result in exactly this format:

SUMMARY:
<summary>

DISCUSSION_POINTS:
- point 1
- point 2

PROMISES:
- promise 1
- promise 2

FOLLOW_UPS:
- follow-up 1
- follow-up 2
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )

    analysis = response.text

    save_meeting(
        meeting_text=meeting_text,
        analysis=analysis
    )

    return analysis