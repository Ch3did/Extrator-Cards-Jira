from datetime import datetime

import matplotlib.pyplot as plt

from src.controller.database import DatabaseController


class LeadTimePoTipo:
    """classe responsável pelo controle da base de dados e geração de documentos"""

    def __init__(self):
        self.db = DatabaseController()

        self.today = datetime.now().date()

        self._y = {}
        self.medias = {}

    def get_start_date_reference(self, issue):
        """Retorna a data de início de referência para uma issue.

        Args:
            issue: Instância do objeto Issue.

        Returns:
            datetime: Data de início de referência.
        """
        if sprints := eval(issue.belonged_sprint):
            return self.db.get_start_date_from_older_sprint_on_list(sprints)

        return issue.creation_date

    def make_plot(self):
        """Gera e exibe um gráfico de barras horizontal.
        """
        barras = list(self.medias.keys())
        alturas = list(self.medias.values())

        plt.barh(barras, alturas, color="lightblue")
        plt.grid(True, axis="x", linestyle="--", alpha=0.7)
        plt.ylabel("Tipos")
        plt.xlabel("LeadTime (dias)")
        plt.title("LeadTime por Tipo")
        plt.xticks(range(0, int(max(alturas) + 2) + 1, 1))
        plt.show()
        pass

    def process(self):
        """Calcula o leadTime."""
        logger.info("Processing LeadTime...")
        issues = self.db.get_done_issues_list()
        for count, issue in enumerate(issues):

            if issue.issue_type not in self._y:
                self._y[issue.issue_type] = []

            end_date = self.db.get_changedate_from_issue_id_done(issue.issue_id)
            start_date = self.get_start_date_reference(issue)

            count_of_days = end_date - start_date

            self._y[issue.issue_type].append(
                count_of_days.days + (count_of_days.seconds / 86400)
            )

        for item in self._y:
            self.medias[item] = sum(self._y[item]) / len(self._y[item])
