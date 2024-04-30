from datetime import date, datetime
from typing import Optional

from sqlmodel import TIMESTAMP, Column, Field, SQLModel, text


class Changelog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    issue_id: Optional[int]
    change_id: Optional[int]
    creator: str
    change_date: datetime
    change_field: str
    old_value: Optional[str]
    new_value: Optional[str]
    colected_date: date = date.today()


def _run_changelog_model(engine):
    SQLModel.metadata.create_all(engine)
