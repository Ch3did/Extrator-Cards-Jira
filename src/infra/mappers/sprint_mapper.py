from src.infra.models.sprint import Sprint


def to_sprint(data: dict, board_id: int) -> Sprint:
    return Sprint(
        sprint_id=data["id"],
        sprint_name=data["name"],
        status=data["state"],
        self_url=data["self"],
        origin_board=board_id,
        start_date=data.get("startDate"),
        end_date=data.get("endDate"),
        resolution_date=data.get("completeDate"),
        created_date=data.get("createdDate"),
    )
