from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Fields(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    resolution: str
    work_ratio: int
    # customfield_10032: List[str] #TODO: Validar com o gui
    issue_type_id: int
    status_category_change_date: Optional[datetime]
    timespent: Optional[datetime]
    resolution_date: Optional[datetime]


class Issue(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    expand: str
    self_: str
    key: str
    fields_id: Optional[int] = Field(foreign_key="fields.id")


def _run_issue_model(engine):
    SQLModel.metadata.create_all(engine)
