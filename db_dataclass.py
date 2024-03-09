from dataclasses import dataclass
from datetime import datetime

@dataclass
class Poll:
    id: int
    name: str
    group_id: int
    created_by: int
    creator_name: str
    created_at: datetime
    closes_at: datetime
    description: str

@dataclass
class PollChoices:
    id: int
    name: str
    poll_id: int
    added_by: int
    votes: int
