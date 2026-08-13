from pathlib import Path
import shutil
from datetime import datetime

from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from src.ai.gemini import analyze_meeting
from src.database.connection import meetings_collection


# --------------------------------------------------
# FastAPI Application
# --------------------------------------------------

app = FastAPI(
    title="Meeting Intelligence Agent",
    description="AI-powered meeting recording and intelligence system",
    version="2.0.0"
)


# --------------------------------------------------
# Folders
# --------------------------------------------------

RECORDINGS_DIR = Path("recordings")
RECORDINGS_DIR.mkdir(exist_ok=True)

STATIC_DIR = Path("static")
STATIC_DIR.mkdir(exist_ok=True)


# --------------------------------------------------
# Serve Frontend
# --------------------------------------------------

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


# --------------------------------------------------
# Home Page
# --------------------------------------------------

@app.get("/")
def home():
    return FileResponse("static/index.html")


# --------------------------------------------------
# Process Meeting Audio
# --------------------------------------------------

@app.post("/process-meeting")
async def process_meeting(file: UploadFile = File(...)):

    if not file.filename:
        return {
            "success": False,
            "error": "No audio file provided"
        }

    # Save uploaded audio
    file_path = RECORDINGS_DIR / file.filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    print(f"\n🎙️ Audio received: {file_path}")

    try:

        # ------------------------------------------
        # Send audio to Gemini
        # ------------------------------------------

        print("📤 Sending audio to Gemini...")

        analysis = analyze_meeting(str(file_path))

        print("✅ AI analysis completed!")

        # ------------------------------------------
        # Prepare MongoDB document
        # ------------------------------------------

        meeting_document = {
            "created_at": datetime.now().isoformat(),

            "audio_file": str(file_path),

            "transcript": analysis.get(
                "transcript",
                ""
            ),

            "summary": analysis.get(
                "summary",
                ""
            ),

            "discussion_points": analysis.get(
                "discussion_points",
                []
            ),

            "decisions": analysis.get(
                "decisions",
                []
            ),

            "promises": analysis.get(
                "promises",
                []
            ),

            "follow_ups": analysis.get(
                "follow_ups",
                []
            ),

            "action_items": analysis.get(
                "action_items",
                []
            )
        }

        # ------------------------------------------
        # Save to MongoDB
        # ------------------------------------------

        result = meetings_collection.insert_one(
            meeting_document
        )

        print("💾 Meeting saved to MongoDB!")

        return {
            "success": True,

            "meeting_id": str(
                result.inserted_id
            ),

            "analysis": analysis
        }

    except Exception as e:

        print("❌ Error:", e)

        return {
            "success": False,
            "error": str(e)
        }


# --------------------------------------------------
# Get Previous Meetings
# --------------------------------------------------

@app.get("/meetings")
def get_meetings():

    meetings = list(
        meetings_collection.find(
            {},
            {"_id": 0}
        ).sort(
            "created_at",
            -1
        )
    )

    return {
        "success": True,
        "count": len(meetings),
        "meetings": meetings
    }