from elasticsearch import Elasticsearch

from src.infra.models.sprint import Sprint
from src.infra.models.ticket import Ticket


class ElasticClient:
    ISSUES_INDEX = "jira_issues"
    SPRINTS_INDEX = "jira_sprints"

    def __init__(self, host: str, port: int = 9200):
        self._client = Elasticsearch(f"http://{host}:{port}")

    def index_issue(self, document: Ticket) -> None:
        self._client.update(
            index=self.ISSUES_INDEX,
            id=document.issue_id,
            body={"doc": document.to_document(), "doc_as_upsert": True},
        )

    def index_sprint(self, document: Sprint) -> None:
        self._client.update(
            index=self.SPRINTS_INDEX,
            id=document.sprint_id,
            body={"doc": document.to_document(), "doc_as_upsert": True},
        )
