from pydantic import BaseModel
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class LocationSchema(BaseModel):
    id: int
    displayName: str
    projectName: str
    projectKey: str
    projectTypeKey: str
    avatarURI: str
    name: str

    class Config:
        from_attributes = True


class BoardSchema(BaseModel):
    id: int
    name: str
    self_: str
    type_: str
    location: LocationSchema

    class Config:
        from_attributes = True


class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    displayName = Column(String(255), index=True)
    projectName = Column(String(255), index=True)
    projectKey = Column(String(255), index=True)
    projectTypeKey = Column(String(255), index=True)
    avatarURI = Column(String(255), index=True)
    name = Column(String(255), index=True)

    board = relationship("Board", back_populates="location")


class Board(Base):
    __tablename__ = "board"

    id = Column(String(255), primary_key=True, index=True)
    name = Column(String(255), index=True)
    self_ = Column(String(255), index=True)
    type_ = Column(String(255), index=True)
    location_id = Column(
        "location_id", Integer(), ForeignKey("locations.id"), nullable=False
    )

    location = relationship("Location", back_populates="board")


def _run_boar_model(engine):
    Base.metadata.create_all(engine)
