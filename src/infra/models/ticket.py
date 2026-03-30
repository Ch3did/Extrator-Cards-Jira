from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional


@dataclass
class ChangeHistory:
    change_id: int
    creator: str
    change_date: str
    change_timestamp: str
    change_field: str
    old_value: Optional[str] = None
    new_value: Optional[str] = None

    def to_document(self) -> dict:
        return {
            "change_id": self.change_id,
            "creator": self.creator,
            "change_date": self.change_date,
            "change_timestamp": self.change_timestamp,
            "change_field": self.change_field,
            "old_value": self.old_value,
            "new_value": self.new_value,
        }


@dataclass
class Ticket:
    issue_id: int
    board_id: int
    board_name: str
    board_url: str
    board_type: str
    status: str
    self_url: str
    key: str
    issue_type: str
    issue_type_id: str
    summary: str
    priority_name: str
    epic_key: Optional[str] = None
    epic_name: Optional[str] = None
    epic_summary: Optional[str] = None
    current_sprints: Optional[str] = None
    work_ratio: Optional[int] = None
    assignee_name: Optional[str] = None
    assignee_mail: Optional[str] = None
    reporter_name: Optional[str] = None
    reporter_mail: Optional[str] = None
    creators_name: Optional[str] = None
    creators_mail: Optional[str] = None
    progress: Optional[str] = None
    status_category_change_date: Optional[datetime] = None
    timespent: Optional[datetime] = None
    resolution_date: Optional[datetime] = None
    creation_date: Optional[datetime] = None
    belonged_sprint: Optional[str] = None
    deleted: bool = False
    collected_date: date = field(default_factory=date.today)
    changelog: list[ChangeHistory] = field(default_factory=list)

    def to_document(self) -> dict:
        return {
            "issue_id": self.issue_id,
            "board": {
                "id": self.board_id,
                "name": self.board_name,
                "url": self.board_url,
                "type": self.board_type,
            },
            "status": self.status,
            "self_url": self.self_url,
            "key": self.key,
            "issue_type": self.issue_type,
            "issue_type_id": self.issue_type_id,
            "summary": self.summary,
            "priority_name": self.priority_name,
            "epic": {
                "key": self.epic_key,
                "name": self.epic_name,
                "summary": self.epic_summary,
            },
            "current_sprints": self.current_sprints,
            "belonged_sprint": self.belonged_sprint,
            "work_ratio": self.work_ratio,
            "assignee": {
                "name": self.assignee_name,
                "mail": self.assignee_mail,
            },
            "reporter": {
                "name": self.reporter_name,
                "mail": self.reporter_mail,
            },
            "creator": {
                "name": self.creators_name,
                "mail": self.creators_mail,
            },
            "progress": self.progress,
            "status_category_change_date": self.status_category_change_date,
            "timespent": self.timespent,
            "resolution_date": self.resolution_date,
            "creation_date": self.creation_date,
            "deleted": self.deleted,
            "collected_date": self.collected_date.isoformat(),
            "changelog": [c.to_document() for c in self.changelog],
        }
