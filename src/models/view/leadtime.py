from datetime import date, datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class ViewLeadtime(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    issue_id: str
    average_days: float
    issue_type: str
    start_date: datetime
    end_date: datetime
    analyzed_day: date
    assignee: Optional[str]
    colected_date: date = date.today()


def _run_leadtime_model(engine):
    SQLModel.metadata.create_all(engine)
