from typing import List

from src.controller.jira_api import JiraAPI


class JiraView(JiraAPI):
    def get_boards(self) -> List:
        boards = []
        is_last_page = False
        while not is_last_page:
            jira_boards = self._get_boards_info()
            boards = boards + self.board.board_factory(jira_boards)
            is_last_page = jira_boards["isLast"]
        return boards

    def get_issues(self, board: int) -> None:
        issues = []
        is_last_page = False
        while not is_last_page:
            jira_issues = self._get_issues_info(board)
            self.issue.issues_factory(jira_issues)
            is_last_page = (
                True
                if jira_issues.get("isLast")
                or jira_issues["maxResults"] > jira_issues["total"]
                else False
            )

    def process(self):
        boards_id_list = self.get_boards()
        for board in boards_id_list:
            issues_id_list = self.get_issues(board)
        return True if issues_id_list else False
