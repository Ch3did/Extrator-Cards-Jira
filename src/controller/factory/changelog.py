from datetime import datetime

from src.controller.database import DatabaseController
from src.models.changelog import Changelog


class ChangelogController(DatabaseController):
    """Classe responsável pela criação e registro dos Changelogs"""

    def changelog_factory(self, changelog_dict: dict, issue_id: int) -> Changelog:
        for change in changelog_dict["values"]:

            for item in change["items"]:

                changelog = Changelog(
                    issue_id=issue_id,
                    change_id=change["id"],
                    creator=change["author"]["displayName"],
                    change_date=datetime.strptime(change["created"][:-17], "%Y-%m-%dT"),
                    change_timestamp=datetime.strptime(
                        change["created"][:-9], "%Y-%m-%dT%H:%M:%S"
                    ),
                    change_field=item["field"],
                    old_value=item["fromString"],
                    new_value=item["toString"],
                )

                self.save_changelog(changelog)
