from datetime import datetime

from src.controller.database import DatabaseController
from src.models.sprint import Sprint


class SprintController(DatabaseController):
    """Classe responsável pela criação e registro das sprint"""

    def sprint_factory(self, sprint_dict, board) -> Sprint:
        for sprint in sprint_dict["values"]:

            resolution_date = (
                datetime.strptime(sprint.get("completeDate")[:-5], "%Y-%m-%dT%H:%M:%S")
                if sprint.get("completeDate")
                else None
            )
            start_date = (
                datetime.strptime(sprint.get("start_date")[:-9], "%Y-%m-%dT%H:%M:%S")
                if sprint.get("start_date")
                else None
            )
            end_date = (
                datetime.strptime(sprint.get("endDate")[:-5], "%Y-%m-%dT%H:%M:%S")
                if sprint.get("endDate")
                else None
            )
            created_date = (
                datetime.strptime(sprint.get("createdDate")[:-5], "%Y-%m-%dT%H:%M:%S")
                if sprint.get("createdDate")
                else None
            )

            sprint = Sprint(
                sprint_id=sprint.get("id"),
                status=sprint.get("state"),
                self_url=sprint.get("self"),
                sprint_name=sprint.get("name"),
                origin_board=sprint.get("originBoardId"),
                start_date=start_date,
                resolution_date=resolution_date,
                created_date=created_date,
                end_date=end_date,
            )

            self._add_to_database(sprint)
