from datetime import datetime
from typing import Optional

from sqlmodel import TIMESTAMP, Column, Field, SQLModel, text


class Changelog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    issue_id: int
    change_id: int
    creator: str
    change_date: datetime
    change_field: str
    old_value: Optional[str]
    new_value: Optional[str]
    colected_time_stemp: Optional[datetime] = Field(
        sa_column=Column(
            TIMESTAMP(timezone=True),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
        )
    )


def _run_changelog_model(engine):
    SQLModel.metadata.create_all(engine)
