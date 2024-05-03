from datetime import datetime

import pytz

from src.controller.database import DatabaseController
from src.models.sprint import Sprint


class SprintController(DatabaseController):
    """Classe responsável pela criação e registro das sprint"""

    def sprint_factory(self, sprint_dict, board) -> Sprint:
        fuso_horario_brasilia = pytz.timezone("America/Sao_Paulo")
        dates = {}
        for sprint in sprint_dict["values"]:

            # Resolution date
            if resolution_date_value := sprint.get("completeDate"):
                resolution_date = datetime.strptime(
                    resolution_date_value[:-5], "%Y-%m-%dT%H:%M:%S"
                ).replace(tzinfo=pytz.UTC)
                dates["resolution_date"] = resolution_date.astimezone(
                    fuso_horario_brasilia
                )

            # start date
            if start_date_value := sprint.get("startDate"):
                start_date = datetime.strptime(
                    start_date_value[:-5], "%Y-%m-%dT%H:%M:%S"
                ).replace(tzinfo=pytz.UTC)
                dates["start_date"] = start_date.astimezone(fuso_horario_brasilia)

            # end date
            if end_date_value := sprint.get("startDate"):
                end_date = datetime.strptime(
                    end_date_value[:-5], "%Y-%m-%dT%H:%M:%S"
                ).replace(tzinfo=pytz.UTC)
                dates["end_date"] = end_date.astimezone(fuso_horario_brasilia)

            # created date
            if created_date_value := sprint.get("startDate"):
                created_date = datetime.strptime(
                    created_date_value[:-5], "%Y-%m-%dT%H:%M:%S"
                ).replace(tzinfo=pytz.UTC)
                dates["created_date"] = created_date.astimezone(fuso_horario_brasilia)

            sprint = Sprint(
                sprint_id=sprint.get("id"),
                status=sprint.get("state"),
                self_url=sprint.get("self"),
                sprint_name=sprint.get("name"),
                origin_board=sprint.get("originBoardId"),
                start_date=dates.get("start_date"),
                resolution_date=dates.get("resolution_date"),
                created_date=dates.get("created_date"),
                end_date=dates.get("end_date"),
            )

            self.save_sprint(sprint)
