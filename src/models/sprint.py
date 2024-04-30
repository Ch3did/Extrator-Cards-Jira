from datetime import date, datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Sprint(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    sprint_id: int
    status: str
    self_url: str
    sprint_name: str
    origin_board: int
    start_date: Optional[datetime]  # Inicio
    resolution_date: Optional[datetime]  # resolução (sprint completa)
    created_date: Optional[datetime]  # criação
    end_date: Optional[datetime]  # fechamento
    colected_date: date = date.today()


def _run_sprint_model(engine):
    SQLModel.metadata.create_all(engine)
