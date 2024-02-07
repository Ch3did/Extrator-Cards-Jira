from src.models import _run_boar_model, _run_issue_model
from src.env import DATABASE_URL, DEBUG
from sqlalchemy import create_engine


if __name__ == "__main__":
    engine = create_engine(DATABASE_URL)
    _run_boar_model(engine)
    _run_issue_model(engine)