from datetime import datetime
from typing import Optional

from sqlmodel import TIMESTAMP, Column, Field, SQLModel, text


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


def _run_board_model(engine):
    SQLModel.metadata.create_all(engine)
