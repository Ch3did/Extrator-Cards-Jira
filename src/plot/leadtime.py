from datetime import datetime, timedelta

import matplotlib.pyplot as plt
from sqlmodel import Session, select

from database import engine
from src.models import Changelog, Issue, Sprint


class LeadTimePoTipo:
    """classe responsável pelo controle da base de dados e geração de documentos"""

    def __init__(self):
        self.engine = engine
        self.session = Session(engine)
        self.yesturday = (datetime.now() - timedelta(days=1)).date()
        self.today = datetime.now().date()

        self._y = {}
        self.dict = {}

    def get_startdate_reference(self, issue):
        """Retorna a data de início de referência para uma issue.

        Args:
            issue: Instância do objeto Issue.

        Returns:
            datetime: Data de início de referência.
        """
        if sprints := eval(issue.belonged_sprint):
            query = (
                select(Sprint.start_date)
                .where(Sprint.sprint_id.in_(sprints))
                .order_by(Sprint.start_date)
            )

            result = self.session.exec(query)
            return result.first()

        return issue.creation_date

    def get_changedate_from_done(self, issue: Issue):
        """Retorna a data da última mudança de status para 'Done' de uma issue.

        Args:
            issue: Instância do objeto Issue.

        Returns:
            datetime: Data da última mudança de status para 'Done'.
        """
        query = (
            select(Changelog.change_date)
            .filter(Changelog.issue_id == issue.issue_id)
            .filter(Changelog.change_field == "status")
            .filter(Changelog.new_value == "Done")
            .order_by(Changelog.change_date.desc())
        )
        result = self.session.exec(query)
        return result.first()

    def get_done_issues_list(self):
        """Retorna uma lista de issues que estão marcadas como 'Done'.

        Returns:
            list: Lista de objetos Issue.
        """
        card_filter = (
            select(Issue)
            .filter(Issue.status == "Done")
            .filter(Issue.issue_type != "Sub-task")
            .filter(Issue.colected_date == self.today)
        )

        cursor = self.session.exec(card_filter)
        return cursor.all()

    def make_plot(self, dados):
        """Gera e exibe um gráfico de barras horizontal.

        Args:
            dados: Dicionário contendo os dados a serem plotados.
        """
        barras = list(dados.keys())
        alturas = list(dados.values())

        plt.barh(barras, alturas, color="lightblue")
        plt.ylabel("Tipos")
        plt.xlabel("LeadTime (dias)")
        plt.title("LeadTime por Tipo")
        plt.xticks(range(0, int(max(alturas) + 2) + 1, 1))
        plt.show()
        pass

    def process(self):
        """Processa as issues 'Done' e calcula o LeadTime por tipo."""
        issues = self.get_done_issues_list()
        for count, issue in enumerate(issues):

            if issue.issue_type not in self._y:
                self._y[issue.issue_type] = []

            end_date = self.get_changedate_from_done(issue)
            start_date = self.get_startdate_reference(issue)

            count_of_days = end_date - start_date

            self._y[issue.issue_type].append(
                count_of_days.days + (count_of_days.seconds / 86400)
            )

        for item in self._y:
            self.dict[item] = sum(self._y[item]) / len(self._y[item])

        self.make_plot(self.dict)
