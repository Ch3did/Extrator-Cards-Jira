from typing import List

from loguru import logger

from src.controller.jira_api import JiraAPI
from src.models.board import Board


class JiraView(JiraAPI):
    def get_boards(self) -> List[Board]:
        """Handle the logic for get boards and pagination"""
        logger.info("Getting boards...")
        boards = []
        is_last_page = False
        page = 0
        while not is_last_page:
            jira_boards = self._get_boards_info(page)
            boards += self.board.board_factory(jira_boards)
            is_last_page = jira_boards["isLast"]
            page += 1
        logger.info(f"Found {len(boards)} boards...")
        return boards

    def get_issues(self, board: int) -> None:
        """Handle the logic for get Issues and pagination"""
        logger.info("Getting Issues...")
        is_last_page = False
        page = 0
        while not is_last_page:
            jira_issues = self._get_issues_info(board, page)
            self.issue.issues_factory(jira_issues, board)
            self.get_changelog(jira_issues)
            is_last_page = (
                True
                if jira_issues.get("startAt") + jira_issues.get("maxResults")
                >= jira_issues.get("total")
                else False
            )
            page += 1

    def get_sprints(self, board: int) -> None:
        """Handle the logic for get Issues and pagination"""
        logger.info("Getting Sprints...")
        is_last_page = False
        page = 0
        while not is_last_page:
            jira_sprints = self._get_sprints_info(board, page)
            self.sprint.sprint_factory(jira_sprints, board)
            is_last_page = (
                True
                if jira_sprints.get("isLast")
                or jira_sprints["maxResults"] > jira_sprints["total"]
                else False
            )
            page += 1

    def get_changelog(self, issue_dict: dict):
        is_last_page = False
        page = 0
        while not is_last_page:
            for issue in issue_dict["issues"]:
                jira_changelog = self._get_changelog_info(issue["id"], page)
                self.changelog.changelog_factory(jira_changelog, issue["id"])
                is_last_page = (
                    True
                    if jira_changelog.get("isLast")
                    or jira_changelog["maxResults"] > jira_changelog["total"]
                    else False
                )
            page += 1

    def process(self) -> None:
        boards_id_list = self.get_boards()
        for board in boards_id_list:
            logger.info(f"Running JiraAPI for board {board}")
            self.get_sprints(board)
            self.get_issues(board)
            self._status = "Success"
