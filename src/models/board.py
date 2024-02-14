from datetime import datetime
from typing import Optional

from sqlmodel import TIMESTAMP, Column, Field, SQLModel, text


class Location(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    location_id: int
    location_name: str
    display_name: str
    location_name: str
    location_key: str
    location_type_key: str
    avatar_URI: str
    colected_time_stemp: Optional[datetime] = Field(
        sa_column=Column(
            TIMESTAMP(timezone=True),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
        )
    )


class Board(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    board_id: int
    board_name: str
    board_url: str
    board_type: str
    colected_time_stemp: Optional[datetime] = Field(
        sa_column=Column(
            TIMESTAMP(timezone=True),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
        )
    )

    location_id: Optional[int] = Field(foreign_key="location.id")


def _run_board_model(engine):
    SQLModel.metadata.create_all(engine)
