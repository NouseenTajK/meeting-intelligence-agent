from src.agent.meeting_agent import analyze_meeting


meeting_text = """
Meeting with John Doe to discuss project requirements
and the development timeline.

John Doe will send the complete requirements by Friday.

The project team will prepare the project plan.

Both parties agreed to schedule another meeting next week.

Discussion points:
- Project requirements
- Development timeline
- Responsibilities

Promises:
- John Doe will send the requirements by Friday
- I will prepare the project plan

Follow-ups:
- Send project plan
- Schedule next meeting
"""


print("\n" + "=" * 60)
print("AI MEETING ANALYSIS")
print("=" * 60)

try:
    result = analyze_meeting(meeting_text)

    print("\n" + result)

    print("\n" + "=" * 60)
    print("Meeting saved to MongoDB successfully 🚀")
    print("=" * 60)

except Exception as e:
    print("\nERROR:")
    print(e)