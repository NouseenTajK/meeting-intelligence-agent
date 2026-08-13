import os
import json
from pathlib import Path

from dotenv import load_dotenv
from google import genai


# Load .env from project root
BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set in the .env file")

client = genai.Client(api_key=GEMINI_API_KEY)


def analyze_meeting(audio_file_path):
    """
    Upload meeting audio to Gemini and return:
    - transcript
    - summary
    - discussion points
    - decisions
    - promises
    - follow-ups
    - action items
    """

    print("\n📤 Uploading meeting audio to Gemini...")

    audio_file = client.files.upload(file=audio_file_path)

    print("🧠 Gemini is analyzing the meeting...")

    prompt = """
You are a Meeting Intelligence Agent.

Listen to the uploaded meeting audio.

First create an accurate transcript of the conversation.

Then analyze the meeting and return ONLY valid JSON in exactly this structure:

{
  "transcript": "full transcript here",
  "summary": "short summary of the meeting",
  "discussion_points": [
    "point 1",
    "point 2"
  ],
  "decisions": [
    "decision 1"
  ],
  "promises": [
    "person will do something"
  ],
  "follow_ups": [
    "follow-up 1"
  ],
  "action_items": [
    {
      "person": "person name",
      "task": "task",
      "deadline": "deadline if mentioned"
    }
  ]
}

Rules:
- Do not invent information.
- If something was not discussed, use an empty list.
- Keep the transcript faithful to the audio.
- Identify speakers when possible.
- Return ONLY JSON.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=[audio_file, prompt]
    )

    text = response.text.strip()

    # Remove markdown code fences if Gemini adds them
    if text.startswith("```"):
        text = text.replace("```json", "")
        text = text.replace("```", "")
        text = text.strip()

    try:
        result = json.loads(text)
    except json.JSONDecodeError:
        print("\n⚠️ Gemini returned non-JSON output:")
        print(text)
        raise

    print("✅ Meeting analysis completed!")

    return result