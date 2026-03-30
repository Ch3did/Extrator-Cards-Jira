from typing import Callable, Generator

from loguru import logger

from src.infra.elastic_client import ElasticClient
from src.infra.mappers import sprint_mapper, ticket_mapper
from src.service.jira_api import JiraAPI


class ExtractView:
    def __init__(self, jira: JiraAPI, elastic: ElasticClient):
        self.jira = jira
        self.elastic = elastic

    def _paginate(self, fetch_fn: Callable, *args) -> Generator[dict, None, None]:
        """Gera uma página por vez sem acumular em memória."""
        page = 0
        while True:
            data = fetch_fn(*args, page)
            yield data

            if "isLast" in data:
                if data["isLast"]:
                    break
            else:
                start = data.get("startAt", 0)
                max_results = data.get("maxResults", 0)
                total = data.get("total", 0)
                if start + max_results >= total:
                    break

            page += 1

    def _get_boards(self) -> list[dict]:
        logger.info("Getting boards...")
        boards = [
            board
            for page in self._paginate(self.jira._get_boards_info)
            for board in page["values"]
        ]
        logger.info(f"Found {len(boards)} boards...")
        return boards

    def _get_sprints(self, board: dict) -> None:
        logger.info(f"Getting sprints for board {board.get("name")}...")
        board_id = board.get("id")
        for page in self._paginate(self.jira._get_sprints_info, board_id):
            for sprint_data in page["values"]:
                sprint = sprint_mapper.to_sprint(sprint_data, board_id)
                self.elastic.index_sprint(sprint)

    def _get_issues(self, board: dict) -> None:
        logger.info(f"Getting issues for board {board.get("name")}...")
        board_id = board.get("id")
        for page in self._paginate(self.jira._get_issues_info, board_id):
            changelogs = self._fetch_changelogs(page)
            for issue_data in page["issues"]:
                ticket = ticket_mapper.to_ticket(issue_data, board)
                ticket.changelog = changelogs.get(issue_data["id"], [])
                self.elastic.index_issue(ticket)

    def _fetch_changelogs(self, issue_dict: dict) -> dict:
        changelogs = {}
        for issue in issue_dict["issues"]:
            logger.info(f"Getting changelog for {issue.get("key")}...")
            issue_id = issue["id"]
            changelogs[issue_id] = [
                change
                for page in self._paginate(self.jira._get_changelog_info, issue_id)
                for event in page["values"]
                for change in ticket_mapper.to_change_history(event, issue_id)
            ]
        return changelogs

    def process(self) -> None:
        boards = self._get_boards()

        for board in boards:
            try:
                logger.info(f"Processing board {board.get('name')}...")
                self._get_sprints(board)
                self._get_issues(board)

            except Exception as e:
                logger.error(
                    f"Error processing board {board.get('id')} | {str(e)}"
                )
                continue

        logger.info("Finish data extract!")
