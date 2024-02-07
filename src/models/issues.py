from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class FieldsSchema(BaseModel):
    sprint: int  # id sprint
    resolution: str
    workratio: int
    customfield_10032: List
    issuetype: int
    statuscategorychangedate: datetime
    timespent: Optional[datetime]
    resolutiondate: Optional[datetime]

    class Config:
        from_attributes = True


class IssuesSchema(BaseModel):
    expand: str
    id: int
    self_: str
    key: str
    fields: FieldsSchema

    class Config:
        from_attributes = True


class Fields(Base):
    __tablename__ = "fields"

    id = Column(Integer, primary_key=True, autoincrement=True)
    sprint = Column(Integer)
    resolution = Column(String)
    workratio = Column(Integer)
    customfield_10032 = Column(String)
    issuetype = Column(Integer)
    statuscategorychangedate = Column(DateTime)
    timespent = Column(DateTime, nullable=True)
    resolutiondate = Column(DateTime, nullable=True)


class Issues(Base):
    __tablename__ = "issues"

    id = Column(Integer, primary_key=True, autoincrement=True)
    expand = Column(String)
    self_ = Column(String)
    key = Column(String)
    fields_id = Column(Integer, ForeignKey("fields.id"))

    fields = relationship("Fields", back_populates="issue")


def _run_issue_model(engine):
    Base.metadata.create_all(engine)
