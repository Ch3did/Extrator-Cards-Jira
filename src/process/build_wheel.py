from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import numpy as np
from loguru import logger

from src.const import STATUS as ST
from src.controller.factory.analysis.leadtime import LeadTimeController
from src.controller.factory.objects.changelog import ChangelogController
from src.controller.factory.objects.issue import IssueController
from src.controller.factory.objects.sprint import SprintController


class BuildView:
    def __init__(self):
        self.issue = IssueController()
        self.sprint = SprintController()
        self.changelog = ChangelogController()
        self.leadtime = LeadTimeController()
        self.today = datetime.now().date()
        self.days = [
            (datetime.now() - timedelta(days=item)).date() for item in range(30)
        ]
        self._status = ST.ONGOING

    def get_start_date_reference(self, issue):
        """Retorna a data de início de referência para uma issue.

        Args:
            issue: Instância do objeto Issue.

        Returns:
            datetime: Data de início de referência.
        """
        if sprints := eval(issue.belonged_sprint):
            return self.sprint.get_start_date_from_older_sprint_on_list(sprints)

        return issue.creation_date

    def get_issues_from_changedate(self, isssus_dict, date):
        filtered_issues: list = {}
        for _, issue in isssus_dict.items():
            change_date = self.changelog.change_date_from_issue_done(issue.issue_id)
            if change_date.date() <= date:
                filtered_issues.update({issue.issue_id: change_date})
        return filtered_issues

    def get_issues_done_dict(self) -> dict:
        issue_dict = {}
        for issue in self.issue.get_done_issues_list():
            issue_dict.update({issue.issue_id: issue})
        return issue_dict

    def process_leadtime(self):
        """Detem a logica para montar gráficos relacionados ao leadTime."""

        done_issues = self.get_issues_done_dict()
        self.evolution = []
        for day in self.days:
            day_format = day.isoformat()
            logger.info(f"Searching for info on {day_format}")

            issues_from_date = self.get_issues_from_changedate(done_issues, day)

            for issue_id, change_timestamp in issues_from_date.items():
                start_date = self.get_start_date_reference(done_issues[issue_id])
                days_comparisson = change_timestamp - start_date
                count_days = days_comparisson.days + (days_comparisson.seconds / 86400)

                self.leadtime.leadtime_factory(
                    {
                        "issue_id": issue_id,
                        "average_days": count_days,
                        "issue_type": done_issues[issue_id].issue_type,
                        "start_date": start_date,
                        "end_date": change_timestamp,
                        "analyzed_day": day,
                        "assignee": done_issues[issue_id].assignee_name,
                    }
                )
        self._status = ST.SUCCESS