from datetime import datetime
from typing import Optional

from sqlmodel import TIMESTAMP, Column, Field, SQLModel, text


class Issue(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    issue_id: int
    board_id: int
    expand: str
    status: str
    self_url: str
    key: str
    issue_type: str
    issue_type_id: str
    summary: str
    priority_name: str
    epic_id: Optional[int]
    epic_key: Optional[str]
    epic_name: Optional[str]
    epic_summary: Optional[str]
    sprint: Optional[str]
    work_ratio: Optional[int]
    reporter_name: Optional[str]
    reportar_mail: Optional[str]
    creators_name: Optional[str]
    creators_mail: Optional[str]
    progress: Optional[str]
    status_category_change_date: Optional[datetime]
    timespent: Optional[datetime]
    resolution_date: Optional[datetime]
    creation_date: Optional[datetime]
    closed_sprint: Optional[str]
    colected_time_stemp: Optional[datetime] = Field(
        sa_column=Column(
            TIMESTAMP(timezone=True),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
        )
    )


def _run_issue_model(engine):
    SQLModel.metadata.create_all(engine)
