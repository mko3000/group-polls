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
class PollChoice:
    id: int
    name: str
    poll_id: int
    added_by: int
    added_at: datetime
    votes: int

@dataclass
class PollStats:
    poll_id: int
    total_votes: int
    max_votes: int
    avg_votes: float

