from src.controller.database import DatabaseController
from src.models.view.velocity import ViewVelocity


class VelocityController(DatabaseController):
    def velocity_factory(self, velocity_dict: dict) -> None:

        velocity = ViewVelocity(
            sprint_name=velocity_dict["sprint_name"],
            sprint_id=velocity_dict["sprint_id"],
            issue_key=velocity_dict["issue_key"],
            issue_type=velocity_dict["issue_type"],
            sprint_started_date=velocity_dict["sprint_started_date"],
            sprint_end_date=velocity_dict["sprint_end_date"],
        )
        self.save_average_velocity(velocity)
