from datetime import datetime, timedelta
from typing import List

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
        self.yesturday = (datetime.now() - timedelta(days=1)).date()
        self.today = datetime.now().date()

    def _add_to_database(self, data: object) -> None:
        "Save and commit objects on the database"
        self.session.add(data)
        self.session.commit()

    def save_board(self, board_object: Board) -> None:
        """Usa o Objeto Board recem criado para validar duplicidade
            antes de salvar o dado

        Args:
            board_object (Board): Objeto Board para validação

        campos usados para comparação:
        - Board.board_name
        - Board.board_url
        - Board.board_type

        """
        data = select(Board).where(
            Board.board_name == board_object.board_name,
            Board.board_url == board_object.board_url,
            Board.board_type == board_object.board_type,
        )
        result = self.session.exec(data)
        if not bool(result.first()):
            logger.info(f"Saving board: {board_object.board_name}...")
            self._add_to_database(board_object)

    def save_issue(self, issue_object: Issue) -> None:
        """Usa o Objeto Issue recem criado para validar duplicidade
            antes de salvar o dado

        Args:
            issue_object (Issue): Objeto Issue para validação


        """
        logger.info(f"Saving issue: {issue_object.key}...")
        self._add_to_database(issue_object)

        # OUTDATED Filter:
        # campos usados para comparação:
        # - Issue.issue_id
        # - Issue.board_id
        # - Issue.self_url
        # - Issue.key
        # - Issue.creators_name

        # data = select(Issue).where(
        #     Issue.issue_id == issue_object.issue_id,
        #     Issue.board_id == issue_object.board_id,
        #     Issue.self_url == issue_object.self_url,
        #     Issue.status == issue_object.status,
        #     Issue.key == issue_object.key,
        #     Issue.creators_name == issue_object.creators_name,
        # )
        # result = self.session.exec(data)
        # if not bool(result.first()):

    def save_sprint(self, sprint_object: Sprint) -> None:
        """Usa o Objeto Sprint recem criado para validar duplicidade
            antes de salvar o dado

        Args:
            sprint_object (Sprint): Objeto Sprint para validação

        campos usados para comparação:
        - Sprint.sprint_id
        - Sprint.self_url
        - Sprint.sprint_name
        - Sprint.status
        - Sprint.start_date
        - Sprint.resolution_date
        - Sprint.created_date
        - Sprint.end_date

        """
        data = select(Sprint).where(
            Sprint.sprint_id == sprint_object.sprint_id,
            Sprint.self_url == sprint_object.self_url,
            Sprint.sprint_name == sprint_object.sprint_name,
            Sprint.status == sprint_object.status,
            Sprint.start_date == sprint_object.start_date,
            Sprint.resolution_date == sprint_object.resolution_date,
            Sprint.created_date == sprint_object.created_date,
            Sprint.end_date == sprint_object.end_date,
        )
        result = self.session.exec(data)
        if not bool(result.first()):
            logger.info(f"Saving Sprint: {sprint_object.sprint_name}...")
            self._add_to_database(sprint_object)

    def save_changelog(self, changelog_object: Changelog) -> None:
        """Usa o Objeto Changelog recem criado para validar duplicidade
            antes de salvar o dado

        Args:
            changelog_object (Changelog): Objeto Changelog para validação

        campos usados para comparação:
            - Changelog.issue_id
            - Changelog.creator
            - Changelog.change_date
            - Changelog.change_field
            - Changelog.old_value
            - Changelog.new_value

        """
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

    def get_issue_last_register(self, issue_id: str) -> Issue:
        """Use issue_id to get the last card inside the database
        Args:
            issue_id (str): reference for issue

        Returns:
            Issue
        """
        card_filter = (
            select(Issue)
            .filter(Issue.colected_date == self.today)
            .filter(Issue.issue_id == issue_id)
        )
        return self.session.exec(card_filter).first()

    def get_deleted_cards_register(self) -> List[str]:
        """Cross-reference the data extracted yesterday with today's to search for deleted cards.

        Returns:
            List[str]: list of issue_id from deleted cards
        """
        cards_ontem = select(Issue.issue_id).where(
            Issue.colected_date == self.yesturday
        )
        chaves_ontem = self.session.exec(cards_ontem).all()

        cards_hoje = select(Issue.issue_id).filter(Issue.colected_date == self.today)
        chaves_hoje = self.session.exec(cards_hoje).all()

        return [chave for chave in chaves_ontem if chave not in chaves_hoje]
