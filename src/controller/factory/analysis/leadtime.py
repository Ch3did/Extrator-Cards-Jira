from src.controller.database import DatabaseController
from src.models.view.leadtime import ViewLeadtime


class LeadTimeController(DatabaseController):
    def leadtime_factory(self, leadtime_dict: dict) -> None:

        leadtime = ViewLeadtime(
            issue_id=leadtime_dict["issue_id"],
            average_days=leadtime_dict["average_days"],
            issue_type=leadtime_dict["issue_type"],
            start_date=leadtime_dict["start_date"],
            end_date=leadtime_dict["end_date"],
            analyzed_day=leadtime_dict["analyzed_day"],
            assignee=leadtime_dict["assignee"],
        )

        self.save_average_leadtime(leadtime)
