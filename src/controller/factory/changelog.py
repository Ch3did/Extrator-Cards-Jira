from datetime import datetime

from src.controller.database import DatabaseController
from src.models.changelog import Changelog


class ChangelogController(DatabaseController):
    """Classe responsável pela criação e registro dos Changelogs"""

    def changelog_factory(self, changelog_dict) -> Changelog:
        for change in changelog_dict['values']:

            changelog = Changelog(
                issue_id=change['id'],
                creator=change["author"]["displayName"],
                change_date=datetime.strptime(change["created"][:-9], "%Y-%m-%dT%H:%M:%S"),
                change_field=change["items"][0]["field"],
                old_value=change["items"][0]["fromString"],
                new_value=change["items"][0]["toString"],
            )

            self._add_to_database(changelog)
