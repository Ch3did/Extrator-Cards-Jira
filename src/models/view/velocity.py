from datetime import date
from typing import Optional

from sqlmodel import Field, SQLModel


class ViewVelocity(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    sprint_name: str
    sprint_id: int
    issue_key: str
    issue_type: str
    sprint_started_date: date
    sprint_end_date: date


def _run_velocity_model(engine):
    SQLModel.metadata.create_all(engine)
