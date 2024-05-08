import traceback

from loguru import logger

from src.controller.plot.evolution_leadtime import EvolutionLeadtime
from src.controller.plot.leadtime import LeadTimePoTipo
from src.env import API_TOKEN, DOMAIN, EMAIL
from src.views.jira import JiraView

if __name__ == "__main__":
    jira = JiraView(domain=DOMAIN, api_token=API_TOKEN, email=EMAIL)
    try:
        jira.process()
    except Exception as error:
        logger.error(error)
        msg = traceback.format_exc()
        logger.error(msg)
        jira._status = "Fail"
    finally:
        logger.info(f"Process has finished! Status: {jira._status}")
    
    evol = EvolutionLeadtime().process()
    lead = LeadTimePoTipo().process()
    lead.make_plot()
    evol.make_plot()
