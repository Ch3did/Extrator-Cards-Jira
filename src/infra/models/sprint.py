from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional


@dataclass
class Sprint:
    sprint_id: int
    status: str
    self_url: str
    sprint_name: str
    origin_board: int
    start_date: Optional[datetime] = None
    resolution_date: Optional[datetime] = None
    created_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    collected_date: date = field(default_factory=date.today)

    def to_document(self) -> dict:
        return {
            "sprint_id": self.sprint_id,
            "status": self.status,
            "self_url": self.self_url,
            "sprint_name": self.sprint_name,
            "origin_board": self.origin_board,
            "start_date": self.start_date,
            "resolution_date": self.resolution_date,
            "created_date": self.created_date,
            "end_date": self.end_date,
            "collected_date": self.collected_date.isoformat(),
        }
