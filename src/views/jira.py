from typing import List

from src.controller.jira_api import JiraAPI


class JiraView(JiraAPI):
    # TODO: adicionar paginação
    def get_boards_id(self) -> List:
        jira_boards = self._get_boards_info()
        boards = self.board.board_factory(jira_boards)
        return boards

    def get_issues_id(self, board: int)-> List:
        jira_issues = self._get_issues_info(board)
        issues = self.issue.issues_factory(jira_issues["issues"])
        return issues

    def process(self):
        boards_id_list = self.get_boards_id()
        for board in boards_id_list:
            issues_id_list = self.get_issues(board)
        return True if issues_id_list else False
