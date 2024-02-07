from sqlalchemy import create_engine

from src.env import DATABASE_URL, DEBUG
from src.models import _run_boar_model, _run_issue_model

if __name__ == "__main__":
    engine = create_engine(DATABASE_URL)
    _run_boar_model(engine)
    _run_issue_model(engine)
