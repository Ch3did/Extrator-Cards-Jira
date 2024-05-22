from datetime import datetime

from loguru import logger

from src.controller.database import DatabaseController
from src.models.changelog import Changelog
from src.models.issue import Issue


class DeletedCards(DatabaseController):
    """Classe responsável pela criação e registro deletados"""

    def deleted_cards_factory(self) -> None:
        for issue_id in self.get_deleted_cards_register():
            last_issue = self.get_issue_yesterday_register(issue_id)

            logger.info(f"Creating deleted register for {last_issue.key}")

            deleted_issue = Issue(
                issue_id=issue_id,
                board_id=last_issue.board_id,
                status="Deleted",
                self_url=last_issue.self_url,
                key=last_issue.key,
                issue_type=last_issue.issue_type,
                issue_type_id=last_issue.issue_type_id,
                summary=last_issue.summary,
                priority_name=last_issue.priority_name,
                epic_key=last_issue.epic_key,
                epic_name=last_issue.epic_name,
                epic_summary=last_issue.epic_summary,
                current_sprints=last_issue.current_sprints,
                work_ratio=last_issue.work_ratio,
                assignee_name=last_issue.assignee_name,
                assignee_mail=last_issue.assignee_mail,
                reporter_name=last_issue.reporter_name,
                reportar_mail=last_issue.reportar_mail,
                creators_name=last_issue.creators_name,
                creators_mail=last_issue.creators_mail,
                progress=last_issue.progress,
                status_category_change_date=self.today,
                timespent=last_issue.timespent,
                resolution_date=last_issue.resolution_date,
                creation_date=last_issue.creation_date,
                belonged_sprint=last_issue.belonged_sprint,
            )

            deleted_changelog = Changelog(
                issue_id=issue_id,
                creator="animated_bassoon",
                change_date=self.today,
                change_timestamp=datetime.combine(self.today, datetime.min.time()),
                change_field="status",
                old_value=last_issue.status,
                new_value="deleted",
            )

            self.save_changelog(deleted_changelog)
            self.save_issue(deleted_issue)
