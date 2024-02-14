import arrow

from src.controller.database import DatabaseController
from src.models.issue import Fields, Issue


class IssueController(DatabaseController):
    def _fields_factory(self, fields_dict):
        field = Fields(
            sprint=fields_dict.get("sprint")["id"],
            resolution=fields_dict.get("resolution")["id"],
            workratio=fields_dict.get("workratio"),
            customfield_10032=fields_dict.get("customfield_10032"),
            issuetype_id=fields_dict.get("issuetype")["id"],
            statuscategorychangedate=fields_dict.get("statuscategorychangedate"),
            timespent=(
                arrow.get(fields_dict.get("timespent"))
                if fields_dict.get("timespent")
                else None
            ),
            resolutiondate=(
                arrow.get(fields_dict.get("resolutiondate"))
                if fields_dict.get("resolutiondate")
                else None
            ),
        )
        self._add_to_database(field)
        return field

    def issues_factory(self, issues_dict) -> Issue:
        issue_id_list = []
        for issue in issues_dict["values"]:

            fields = self._fields_factory(issue.get("fields"))
            issue = Issue(
                expand=issue.get("expand"),
                id=issue.get("id"),
                self_=issue.get("self"),
                key=issue.get("key"),
                fields=fields.id,
            )
            self._add_to_database(issue)
            issue_id_list.append(issue)
        return issue_id_list
