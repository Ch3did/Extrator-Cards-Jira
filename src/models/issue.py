from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Fields(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    resolution: str
    workratio: int
    # customfield_10032: List[str] #TODO: Validar ocm o gui
    issuetype: int
    statuscategorychangedate: datetime
    timespent: Optional[datetime]
    resolutiondate: Optional[datetime]


class Issue(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    expand: str
    self_: str
    key: str
    fields_id: Optional[int] = Field(foreign_key="fields.id")


def _run_issue_model(engine):
    SQLModel.metadata.create_all(engine)
