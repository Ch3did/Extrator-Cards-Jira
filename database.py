import os

from sqlmodel import create_engine

from src.env import COMPANY_NAME, DATABASE_URL, DEBUG
from src.models.board import _run_board_model
from src.models.changelog import _run_changelog_model
from src.models.issue import _run_issue_model
from src.models.sprint import _run_sprint_model

if os.path.exists("/tmp/test_app.db"):
    os.rename("/tmp/test_app.db", f"./tmp/{COMPANY_NAME}.db")

engine = create_engine(DATABASE_URL, echo=bool(DEBUG))

if __name__ == "__main__":
    _run_board_model(engine)
    _run_issue_model(engine)
    _run_sprint_model(engine)
    _run_changelog_model(engine)
