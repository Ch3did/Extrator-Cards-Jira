import base64

import requests


class BaseAPI:
    def __init__(self, domain, api_token, email):
        self.domain = domain
        self._board_request = "rest/agile/1.0/board"
        self.api_token = api_token
        self.email = email

    def _get_token(self):
        string = f"{self.email}:{self.api_token}"
        sample_string_bytes = string.encode("ascii")
        base64_bytes = base64.b64encode(sample_string_bytes)
        base64_string = base64_bytes.decode("ascii")
        return f"Basic {base64_string}"

    def _make_headers(self):
        return {"Authorization": f"{self._get_token()}"}

    def _get_boards_info(self) -> dict:
        url = f"{self.domain}rest/agile/1.0/board/"
        headers = self._make_headers()
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def _get_issues_info(self, board_id: int) -> dict:
        url = f"{self.domain}/rest/agile/1.0/board/{board_id}/issue"
        headers = self._make_headers()
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
