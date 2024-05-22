from datetime import datetime, timedelta

from loguru import logger

from src.const import STATUS as ST
from src.controller.factory.analysis.leadtime import LeadTimeController
from src.controller.factory.analysis.velocity import VelocityController
from src.controller.factory.objects.changelog import ChangelogController
from src.controller.factory.objects.issue import IssueController
from src.controller.factory.objects.sprint import SprintController


class BuildView:
    def __init__(self):
        # Models
        self.issue = IssueController()
        self.sprint = SprintController()
        self.changelog = ChangelogController()
        # Analytics
        self.leadtime = LeadTimeController()
        self.velocity = VelocityController()
        # Variables
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

    def get_sprints(self) -> dict:
        sprint_dict = {}
        for sprint in self.sprint.get_all_sprints():
            sprint_dict.update(
                {
                    sprint.id: {
                        "sprint_name": sprint.sprint_name,
                        "start_date": sprint.start_date,
                        "end_date": sprint.end_date,
                    }
                }
            )
        return sprint_dict

    def get_changelog_from_sprints_cards(self, sprint_info):
        changelogs = self.changelog.get_all_changelog_from_sprint_before_date(
            sprint_info["sprint_name"], sprint_info["start_date"]
        )
        return changelogs

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

    def process_velocity(self):
        """Detem a logica para montar gráficos relacionados ao velocity."""
        sprints = self.get_sprints()
        for sprint_id, sprint_info in sprints.items():
            self.get_changelog_from_sprints_cards(sprint_info)

        self.velocity.velocity_factory(
            {
                "sprint_name": "",
                "issue_type": "",
                "count_of_cards": "",
                "sprint_started_date": "",
                "sprint_end_date": "",
            }
        )
