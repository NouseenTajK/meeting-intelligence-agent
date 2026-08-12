from dataclasses import dataclass
from typing import List


@dataclass
class Meeting:
    contact_name: str
    contact_email: str
    meeting_date: str
    discussion: str
    commitments: List[str]
    follow_ups: List[str]