import json
from typing import List

import arrow
import requests

from src.controller.base_api import BaseAPI
from src.models.board import Board, Location
from src.models.issues import Fields, Issues


class JiraView(BaseAPI):
    def fields_factory(self, fields_dict):
        return Fields(
            sprint=fields_dict.get("sprint")["id"],
            resolution=fields_dict.get("resolution")["id"],
            workratio=fields_dict.get("workratio"),
            customfield_10032=fields_dict.get("customfield_10032"),
            issuetype_id=fields_dict.get("issuetype")["id"],
            statuscategorychangedate=fields_dict.get("statuscategorychangedate"),
            timespent=arrow.get(fields_dict.get("timespent"))
            if fields_dict.get("timespent")
            else None,
            resolutiondate=arrow.get(fields_dict.get("resolutiondate"))
            if fields_dict.get("resolutiondate")
            else None,
        )

    def issues_factory(self, issues_dict) -> Issues:
        data = []
        for issue in issues_dict:
            data.append(
                Issues(
                    expand=issue.get("expand"),
                    id=issue.get("id"),
                    self_=issue.get("self"),
                    key=issue.get("key"),
                    fields=self.fields_factory(issue.get("fields")),
                )
            )
        return data

    def location_factory(self, location_data: dict) -> Location:
        return Location(
            projectId=location_data.get("projectId"),
            displayName=location_data.get("displayName"),
            projectName=location_data.get("projectName"),
            projectKey=location_data.get("projectKey"),
            projectTypeKey=location_data.get("projectTypeKey"),
            avatarURI=location_data.get("avatarURI"),
            name=location_data.get("name"),
        )

    def board_factory(self, api_response: dict):
        # TODO: adicionar lógica de páginação
        data = []
        for board_dict in api_response["values"]:
            b = Board(
                id=board_dict.get("id"),
                name=board_dict.get("name"),
                self_=board_dict.get("self"),
                type_=board_dict.get("type"),
                location=self.location_factory(board_dict.get("location")),
            )
            data.append(b)
        return data

    def get_boards(self) -> List:
        boards = self.board_factory(self._get_boards_info())
        return boards

    def get_issues(self, board: Board):
        issues_info = self._get_issues_info(board.id)
        issues_list = self.issues_factory(issues_info["issues"])

        for _ in range(0, response.json()["total"]):
            issue = response.json()["issues"][issue_number]
            issue["id"] = int(issue["id"])
            if issue["fields"]["resolutiondate"]:
                resolution_date = issue["fields"]["resolutiondate"]
                resolution_date = issue["fields"]["resolutiondate"]
                issue["fields"]["resolutiondate"] = arrow.get(resolution_date).format(
                    "YYYY-MM-DD"
                )
            lista.append(issue)
            issue_number += 1
            if issue_number >= response.json()["maxResults"]:
                position += issue_number
                response = requests.get(
                    url, headers=headers, params={"startAt": position}
                )
                issue_number = 0

    def get_sprint(self, board_id, position=0):
        isLast = False
        sprint_list = []
        while not isLast:
            url = f"{self.domain}/rest/agile/1.0/board/{board_id}/sprint"
            headers = self._make_headers()
            response = requests.get(url, headers=headers, params={"startAt": position})
            if response.status_code < 400:
                isLast = response.json()["isLast"]
                sprint_list += response.json()["values"]
                position += len(response.json()["values"])
            else:
                isLast = True

    def _write(self):
        pass

    def process(self, boards=None):
        boards_list = self.get_boards()
        for board in boards_list:
            self.get_issues(board)
            self.get_sprint(board_id)
            print(f"finish board {board_id}")
