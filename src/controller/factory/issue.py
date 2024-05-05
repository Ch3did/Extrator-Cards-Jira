from datetime import datetime

from src.controller.database import DatabaseController
from src.models.issue import Issue


class IssueController(DatabaseController):
    """Classe responsável pela criação e registro das Issues"""

    @staticmethod
    def _solve_time(fields_dict, reffs):
        time_value = (
            datetime.strptime(fields_dict.get(reffs)[:-9], "%Y-%m-%dT%H:%M:%S")
            if fields_dict.get(reffs)
            else None
        )
        return time_value

    @staticmethod
    def _solve_sprint(sprints_list):
        sprints = []
        if isinstance(sprints_list, list):
            for sprint in sprints_list:
                sprints.append(sprint["id"])
        else:
            if current_sprint_id := sprints_list.get("id"):
                sprints.append(current_sprint_id)

    @staticmethod
    def _solve_belonged_sprint(belonged_sprint_list, sprints=[]):
        sprints = sprints if sprints else []
        if belonged_sprint_list:
            for item in belonged_sprint_list:
                sprints.append(item["id"])
        return sprints

    def issues_factory(self, issues_dict, board) -> Issue:
        for issue in issues_dict["issues"]:
            fields_dict = issue["fields"]

            # Data reesolution
            timespent_value = self._solve_time(fields_dict, "timespent")
            creation_date_value = self._solve_time(fields_dict, "created")
            resolution_date_value = self._solve_time(fields_dict, "resolutiondate")
            status_category_change_date_value = self._solve_time(
                fields_dict, "statuscategorychangedate"
            )

            # Sprint Resolution
            sprints_list = fields_dict["sprint"] if fields_dict.get("sprint") else {}
            sprints = self._solve_sprint(sprints_list)
            belonged_sprint = self._solve_belonged_sprint(
                fields_dict.get("closedSprints"), sprints
            )

            epic = fields_dict["epic"] if fields_dict.get("epic") else {}
            creator = fields_dict["creator"] if fields_dict.get("creator") else {}
            priority = fields_dict["priority"] if fields_dict.get("priority") else {}
            reporter = fields_dict["reporter"] if fields_dict.get("reporter") else {}
            progress = fields_dict["progress"] if fields_dict.get("progress") else {}
            issue_type = (
                fields_dict["issuetype"] if fields_dict.get("issuetype") else {}
            )

            issue = Issue(
                issue_id=issue.get("id"),
                board_id=board,
                status=fields_dict["status"].get("name"),
                self_url=issue.get("self"),
                key=issue.get("key"),
                issue_type=issue_type.get("name"),
                issue_type_id=issue_type.get("id"),
                summary=fields_dict.get("summary"),
                epic_key=epic.get("key"),
                epic_name=epic.get("name"),
                epic_summary=epic.get("summary"),
                priority_name=priority.get("name"),
                current_sprints=f"{sprints}",
                belonged_sprint=f"{belonged_sprint}",
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
            )

            self.save_issue(issue)
