from datetime import datetime

import pytz

from src.controller.database import DatabaseController
from src.models.sprint import Sprint


class SprintController(DatabaseController):
    """Classe responsável pela criação e registro das sprint"""

    @staticmethod
    def _solve_time(sprint, reffs):
        fuso_horario_brasilia = pytz.timezone("America/Sao_Paulo")
        if date_value := sprint.get(reffs):
            resolution_date = datetime.strptime(
                date_value[:-5], "%Y-%m-%dT%H:%M:%S"
            ).replace(tzinfo=pytz.UTC)
            return resolution_date.astimezone(fuso_horario_brasilia)

    def sprint_factory(self, sprint_dict, board) -> Sprint:
        dates = {}
        for sprint in sprint_dict["values"]:

            # Resolution date
            dates["resolution_date"] = self._solve_time(sprint, "completeDate")

            # start date
            dates["start_date"] = self._solve_time(sprint, "startDate")

            # end date
            dates["end_date"] = self._solve_time(sprint, "endDate")

            # created date
            dates["created_date"] = self._solve_time(sprint, "createdDate")

            sprint = Sprint(
                sprint_id=sprint.get("id"),
                status=sprint.get("state"),
                self_url=sprint.get("self"),
                sprint_name=sprint.get("name"),
                origin_board=sprint.get("originBoardId"),
                resolution_date=dates.get("resolution_date"),
                start_date=dates.get("start_date"),
                end_date=dates.get("end_date"),
                created_date=dates.get("created_date"),
            )

            self.save_sprint(sprint)
