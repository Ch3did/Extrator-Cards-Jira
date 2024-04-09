from loguru import logger
from sqlmodel import Session, select

from database import engine
from src.models.board import Board
from src.models.changelog import Changelog
from src.models.issue import Issue
from src.models.sprint import Sprint


class DatabaseController:
    """classe responsável pelo controle da base de dados e geração de documentos"""

    def __init__(self):
        self.engine = engine
        self.session = Session(engine)

    def _add_to_database(self, data):
        # TODO: Adicionar validação de dado duplicado com base no dia
        self.session.add(data)
        self.session.commit()

    def save_board(self, board_object: Board) -> str:
        data = select(Board).where(
            Board.board_name == board_object.board_name,
            Board.board_url == board_object.board_url,
            Board.board_type == board_object.board_type,
        )
        result = self.session.exec(data)
        if not bool(result.first()):
            logger.info(f"Saving board: {board_object.board_name}...")
            self._add_to_database(board_object)

    def save_issue(self, issue_object: Issue) -> str:
        data = select(Issue).where(
            Issue.issue_id == issue_object.issue_id,
            Issue.board_id == issue_object.board_id,
            Issue.self_url == issue_object.self_url,
            Issue.key == issue_object.key,
            Issue.creators_name == issue_object.creators_name,
        )
        result = self.session.exec(data)
        if not bool(result.first()):
            logger.info(f"Saving issue: {issue_object.key}...")
            self._add_to_database(issue_object)

    def save_sprint(self, sprint_object: Sprint) -> str:
        data = select(Sprint).where(
            Sprint.sprint_id == sprint_object.sprint_id,
            Sprint.self_url == sprint_object.self_url,
            Sprint.sprint_name == sprint_object.sprint_name,
        )
        result = self.session.exec(data)
        if not bool(result.first()):
            logger.info(f"Saving Sprint: {sprint_object.sprint_name}...")
            self._add_to_database(sprint_object)

    def save_changelog(self, changelog_object: Changelog) -> str:
        data = select(Changelog).where(
            Changelog.issue_id == changelog_object.issue_id,
            Changelog.creator == changelog_object.creator,
            Changelog.change_date == changelog_object.change_date,
            Changelog.change_field == changelog_object.change_field,
            Changelog.old_value == changelog_object.old_value,
            Changelog.new_value == changelog_object.new_value,
        )
        result = self.session.exec(data)
        if not bool(result.first()):
            logger.info(f"Saving Changelog: {changelog_object.issue_id}...")
            self._add_to_database(changelog_object)
