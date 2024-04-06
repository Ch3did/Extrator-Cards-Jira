from datetime import datetime

from src.controller.database import DatabaseController
from src.models.issue import Issue


class IssueController(DatabaseController):
    """Classe responsável pela criação e registro das Issues"""

    def issues_factory(self, issues_dict, board) -> Issue:
        for issue in issues_dict["issues"]:
            fields_dict = issue["fields"]

            timespent_value = (
                datetime.strptime(
                    fields_dict.get("timespent")[:-9], "%Y-%m-%dT%H:%M:%S"
                )
                if fields_dict.get("timespent")
                else None
            )
            creation_date_value = (
                datetime.strptime(fields_dict.get("created")[:-9], "%Y-%m-%dT%H:%M:%S")
                if fields_dict.get("created")
                else None
            )
            resolution_date_value = (
                datetime.strptime(
                    fields_dict.get("resolutiondate")[:-9], "%Y-%m-%dT%H:%M:%S"
                )
                if fields_dict.get("resolutiondate")
                else None
            )
            status_category_change_date_value = (
                datetime.strptime(
                    fields_dict.get("statuscategorychangedate")[:-9],
                    "%Y-%m-%dT%H:%M:%S",
                )
                if fields_dict.get("statuscategorychangedate")
                else None
            )

            closed_sprint = None
            if sprints := fields_dict.get("closedSprints"):
                closed_sprint = f"{[item['id'] for item in sprints]}"

            epic = fields_dict["epic"] if fields_dict.get("epic") else {}
            sprint = fields_dict["sprint"] if fields_dict.get("sprint") else {}
            creator = fields_dict["creator"] if fields_dict.get("creator") else {}
            priority = fields_dict["priority"] if fields_dict.get("priority") else {}
            reporter = fields_dict["reporter"] if fields_dict.get("reporter") else {}
            progress = fields_dict["progress"] if fields_dict.get("progress") else {}
            issue_type = (
                fields_dict["issuetype"] if fields_dict.get("issuetype") else {}
            )

            issue = Issue(
                issue_id = issue.get("id"),
                board_id=board,
                expand=issue.get("expand"),
                status=fields_dict["status"].get("name"),
                self_url=issue.get("self"),
                key=issue.get("key"),
                issue_type=issue_type.get("name"),
                issue_type_id=issue_type.get("id"),
                summary=fields_dict.get("summary"),
                epic_id=epic.get("id"),
                epic_key=epic.get("key"),
                epic_name=epic.get("name"),
                epic_summary=epic.get("summary"),
                priority_name=priority.get("name"),
                sprint=sprint.get("id"),
                work_ratio=fields_dict.get("workratio"),
                reporter_name=reporter.get("displayName"),
                reportar_mail=reporter.get("emailAddress"),
                creators_name=creator.get("displayName"),
                creators_mail=creator.get("emailAddress"),
                progress=progress.get("progress"),
                status_category_change_date=status_category_change_date_value,
                timespent=timespent_value,
                resolution_date=resolution_date_value,
                creation_date=creation_date_value,
                closed_sprint=closed_sprint,
            )

            self._add_to_database(issue)
