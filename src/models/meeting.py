from datetime import datetime


def create_meeting(
    contact_name,
    meeting_date,
    summary,
    discussion_points=None,
    promises=None,
    follow_ups=None
):
    return {
        "contact_name": contact_name,
        "meeting_date": meeting_date,
        "summary": summary,
        "discussion_points": discussion_points or [],
        "promises": promises or [],
        "follow_ups": follow_ups or [],
        "created_at": datetime.utcnow()
    }