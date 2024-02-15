from datetime import datetime

from src.controller.database import DatabaseController
from src.models.issue import Fields, Issue


class IssueController(DatabaseController):
    """Classe responsável pela criação e registro das Issues"""

    def _fields_factory(self, fields_dict):
        timespent_value = fields_dict.get("timespent")
        resolution_date_value = fields_dict.get("resolutiondate")
        status_category_change_date_value = fields_dict.get("statuscategorychangedate")
        sprint = fields_dict["sprint"].get("id") if fields_dict.get("sprint") else None
        resolution = (
            fields_dict["resolution"].get("id")
            if fields_dict.get("resolution")
            else None
        )
        issue_type_id = (
            fields_dict["issuetypeid"].get("id")
            if fields_dict.get("issuetypeid")
            else None
        )
        field = Fields(
            sprint=sprint,
            resolution=resolution,
            work_ratio=fields_dict.get("workratio"),
            issue_type_id=issue_type_id,
            status_category_change_date=(
                datetime.strptime(
                    status_category_change_date_value[:-9], "%Y-%m-%dT%H:%M:%S"
                )
                if timespent_value
                else None
            ),
            timespent=(
                datetime.strptime(timespent_value[:-9], "%Y-%m-%dT%H:%M:%S")
                if timespent_value
                else None
            ),
            resolution_date=(
                datetime.strptime(resolution_date_value[:-9], "%Y-%m-%dT%H:%M:%S")
                if resolution_date_value
                else None
            ),
        )

        self._add_to_database(field)
        return field

    def issues_factory(self, issues_dict) -> Issue:
        issue_id_list = []
        for issue in issues_dict["issues"]:

            fields = self._fields_factory(issue.get("fields"))
            issue = Issue(
                expand=issue.get("expand"),
                id=issue.get("id"),
                self_=issue.get("self"),
                key=issue.get("key"),
                fields_id=fields.id,
            )
            self._add_to_database(issue)
            issue_id_list.append(issue)
        return issue_id_list
