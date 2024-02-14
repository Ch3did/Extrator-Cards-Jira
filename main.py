from src.env import API_TOKEN, DOMAIN, EMAIL
from src.views.jira import JiraView

if __name__ == "__main__":
    jira = JiraView(domain=DOMAIN, api_token=API_TOKEN, email=EMAIL)
    try:
        jira.process()
    except Exception as error:
        print(error)
