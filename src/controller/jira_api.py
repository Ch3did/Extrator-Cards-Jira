import base64

import requests

from src.controller.factory.board import BoardController
from src.controller.factory.issue import IssueController
from src.controller.factory.sprint import SprintController


class JiraAPI:
    """classe responsável pelo controle da API do Jira"""

    def __init__(self, domain, api_token, email):
        self.domain = domain
        self.api_token = api_token
        self.email = email
        self.board = BoardController()
        self.issue = IssueController()
        self.sprint = SprintController()
        self._status = "In Progress"

    def _get_token(self) -> str:
        """Encode the email and apiToken to base 64 and return as token

        Returns:
            str: Authentication token string
        """
        string = f"{self.email}:{self.api_token}"
        sample_string_bytes = string.encode("ascii")
        base64_bytes = base64.b64encode(sample_string_bytes)
        base64_string = base64_bytes.decode("ascii")
        return f"Basic {base64_string}"

    def _make_headers(self) -> dict:
        return {"Authorization": f"{self._get_token()}"}

    def _make_params(self, page: int) -> dict:
        results = 100
        return {
            "startAt": f"{page*results}",
            "maxResults": f"{results}",
        }

    def _make_request(self, url: str, page: int) -> dict:
        headers = self._make_headers()
        params = self._make_params(page)
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()

    def _get_boards_info(self, page: int) -> dict:
        self._make_request(f"{self.domain}/board/", page)

    def _get_issues_info(self, board_id: int, page: int) -> dict:
        self._make_request(f"{self.domain}/board/{board_id}/issue", page)

    def _get_sprints_info(self, board_id, page: int) -> dict:
        self._make_request(f"{self.domain}/board/{board_id}/sprint", page)

    # def _get_epics_basic_info(self, board_id, page: int) -> dict:
    #     url = f"{self.domain}/rest/agile/1.0/board/{board_id}/epic"

    # def _get_epic_info(self, epic_id, page: int) -> dict:
    #     url = f"{self.domain}/rest//agile/1.0/epic/{epic_id}"
