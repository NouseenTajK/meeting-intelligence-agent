from datetime import datetime

from src.database.connection import meetings_collection
from src.audio_recorder import record_meeting
from src.ai.gemini import analyze_meeting


def record_and_process():
    print("\n🎙️ STARTING MEETING RECORDING")
    print("=" * 50)

    audio_file = record_meeting()

    print("\n🧠 PROCESSING MEETING...")
    print("=" * 50)

    result = analyze_meeting(audio_file)

    meeting_document = {
        "created_at": datetime.now().isoformat(),
        "audio_file": audio_file,
        "transcript": result.get("transcript", ""),
        "summary": result.get("summary", ""),
        "discussion_points": result.get("discussion_points", []),
        "decisions": result.get("decisions", []),
        "promises": result.get("promises", []),
        "follow_ups": result.get("follow_ups", []),
        "action_items": result.get("action_items", [])
    }

    mongo_result = meetings_collection.insert_one(meeting_document)

    print("\n✅ MEETING SAVED TO MONGODB!")
    print("Meeting ID:", mongo_result.inserted_id)

    print("\n" + "=" * 50)
    print("📝 MEETING SUMMARY")
    print("=" * 50)

    print("\n📌 Summary:")
    print(result.get("summary", ""))

    print("\n💬 Discussion Points:")
    for item in result.get("discussion_points", []):
        print("•", item)

    print("\n✅ Decisions:")
    for item in result.get("decisions", []):
        print("•", item)

    print("\n🤝 Promises:")
    for item in result.get("promises", []):
        print("•", item)

    print("\n🔔 Follow-ups:")
    for item in result.get("follow_ups", []):
        print("•", item)

    print("\n📋 Action Items:")
    for item in result.get("action_items", []):
        if isinstance(item, dict):
            print(
                f"• {item.get('person', 'Unknown')}: "
                f"{item.get('task', '')} "
                f"({item.get('deadline', 'No deadline')})"
            )
        else:
            print("•", item)


def view_meetings():
    print("\n📋 PAST MEETINGS")
    print("=" * 50)

    meetings = meetings_collection.find()

    found = False

    for meeting in meetings:
        found = True

        print("\n🆔 Meeting ID:", meeting.get("_id"))
        print("📅 Created:", meeting.get("created_at"))
        print("🎙️ Audio:", meeting.get("audio_file"))

        print("\n📝 Summary:")
        print(meeting.get("summary", ""))

        print("\n💬 Discussion Points:")
        for item in meeting.get("discussion_points", []):
            print("•", item)

        print("\n✅ Decisions:")
        for item in meeting.get("decisions", []):
            print("•", item)

        print("\n🤝 Promises:")
        for item in meeting.get("promises", []):
            print("•", item)

        print("\n🔔 Follow-ups:")
        for item in meeting.get("follow_ups", []):
            print("•", item)

        print("\n📋 Action Items:")
        for item in meeting.get("action_items", []):
            if isinstance(item, dict):
                print(
                    f"• {item.get('person', 'Unknown')}: "
                    f"{item.get('task', '')} "
                    f"({item.get('deadline', 'No deadline')})"
                )
            else:
                print("•", item)

        print("\n" + "-" * 50)

    if not found:
        print("No meetings found.")


def main():
    while True:
        print("\n" + "=" * 55)
        print("🧠 MEETING INTELLIGENCE AGENT")
        print("=" * 55)

        print("1. 🎙️ Record & Analyze Meeting")
        print("2. 📋 View Past Meetings")
        print("3. 🚪 Exit")

        choice = input("\nChoose an option: ")

        if choice == "1":
            record_and_process()

        elif choice == "2":
            view_meetings()

        elif choice == "3":
            print("\nGoodbye! 👋")
            break

        else:
            print("\n❌ Invalid choice. Please try again.")


if __name__ == "__main__":
    main()