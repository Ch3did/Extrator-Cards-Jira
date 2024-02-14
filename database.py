from sqlmodel import create_engine

from src.env import DATABASE_URL, DEBUG
from src.models.board import _run_board_model
from src.models.issue import _run_issue_model

engine = create_engine(DATABASE_URL, echo=bool(DEBUG))

if __name__ == "__main__":
    _run_board_model(engine)
    _run_issue_model(engine)
