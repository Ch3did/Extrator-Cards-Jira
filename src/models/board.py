from datetime import date
from typing import Optional

from sqlmodel import Field, SQLModel


class Board(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    board_id: int
    board_name: str
    board_url: str
    board_type: str
    colected_date: date = date.today()


def _run_board_model(engine):
    SQLModel.metadata.create_all(engine)
