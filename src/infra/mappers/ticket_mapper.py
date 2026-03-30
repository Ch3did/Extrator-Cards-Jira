from src.infra.models.ticket import ChangeHistory, Ticket


def to_ticket(issue: dict, board: dict) -> Ticket:
    fields = issue.get("fields", {})
    assignee = fields.get("assignee") or {}
    reporter = fields.get("reporter") or {}
    creator = fields.get("creator") or {}
    epic = fields.get("epic") or {}
    priority = fields.get("priority") or {}
    issue_type = fields.get("issuetype") or {}
    progress = fields.get("progress") or {}

    return Ticket(
        issue_id=issue["id"],
        self_url=issue["self"],
        key=issue["key"],
        board_id=board["id"],
        board_name=board["name"],
        board_url=board["self"],
        board_type=board["type"],
        status=fields.get("status", {}).get("name", ""),
        summary=fields.get("summary", ""),
        issue_type=issue_type.get("name", ""),
        issue_type_id=issue_type.get("id", ""),
        priority_name=priority.get("name", ""),
        epic_key=epic.get("key"),
        epic_name=epic.get("name"),
        epic_summary=epic.get("summary"),
        current_sprints=(
            fields.get("sprint", {}).get("name") if fields.get("sprint") else None
        ),
        belonged_sprint=(
            fields.get("closedSprints", [{}])[-1].get("name")
            if fields.get("closedSprints")
            else None
        ),
        work_ratio=fields.get("workratio"),
        assignee_name=assignee.get("displayName"),
        assignee_mail=assignee.get("emailAddress"),
        reporter_name=reporter.get("displayName"),
        reporter_mail=reporter.get("emailAddress"),
        creators_name=creator.get("displayName"),
        creators_mail=creator.get("emailAddress"),
        progress=(
            str(progress.get("percent"))
            if progress.get("percent") is not None
            else None
        ),
        status_category_change_date=fields.get("statuscategorychangedate"),
        timespent=fields.get("timespent"),
        resolution_date=fields.get("resolutiondate"),
        creation_date=fields.get("created"),
    )


def to_change_history(event: dict, issue_id: str) -> list[ChangeHistory]:
    return [
        ChangeHistory(
            change_id=event["id"],
            creator=event.get("author", {}).get("displayName", ""),
            change_date=event["created"][:10],
            change_timestamp=event["created"],
            change_field=item["field"],
            old_value=item.get("fromString"),
            new_value=item.get("toString"),
        )
        for item in event.get("items", [])
    ]
