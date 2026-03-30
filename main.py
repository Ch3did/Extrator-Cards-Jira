import traceback

from loguru import logger

from src.controller.extract_view import ExtractView
from src.env import API_TOKEN, DOMAIN, ELASTIC_HOST, ELASTIC_PORT, EMAIL
from src.infra.elastic_client import ElasticClient
from src.service.jira_api import JiraAPI


def run():
    jira = JiraAPI(domain=DOMAIN, api_token=API_TOKEN, email=EMAIL)
    elastic = ElasticClient(host=ELASTIC_HOST, port=ELASTIC_PORT)
    extract = ExtractView(jira=jira, elastic=elastic)

    try:
        logger.info("Staring Extraction...")
        extract.process()

    except Exception as error:
        logger.error(f"Unexpected error: {error}")
        logger.error(traceback.format_exc())

    finally:
        logger.info("Extraction finished sucessfully!")


if __name__ == "__main__":
    run()
