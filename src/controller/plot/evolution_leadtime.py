from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import numpy as np

from src.controller.database import DatabaseController


class EvolutionLeadtime:
    """classe responsável pelo controle da base de dados e geração de documentos"""

    def __init__(self):
        self.db = DatabaseController()
        self.today = datetime.now().date()
        self.medias = {}
        self.days = [
            (datetime.now() - timedelta(days=item)).date() for item in range(30)
        ]

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

    def make_plot(self, widget=3):
        """Gera e exibe um gráfico de barras horizontal.
        """
        dates = [datetime.strptime(item, "%Y-%m-%d") for item in self.medias.keys()]
        index = self.db.get_all_issue_types()

        plt.figure(figsize=(10, 6))

        for linha, tipo_linha in enumerate(index):
            pontos = [
                self.medias[item].get(tipo_linha, None) for item in self.medias.keys()
            ]
            plt.plot(
                dates,
                np.array(pontos),
                label=tipo_linha,
                linewidth=widget,
            )

        plt.title("Evolution Leadtime")
        plt.xlabel("Data")
        plt.ylabel("Tipo de leadtime")
        plt.xticks(rotation=45)
        plt.grid(True, linestyle="--", alpha=0.7)
        plt.legend()
        plt.tight_layout()
        plt.legend(loc="lower left")
        plt.show()

    def process(self):
        """Calcula o Evolution leadTime."""
        logger.info("Processing Evolution LeadTime...")
        for day in self.days:
            day_format = day.isoformat()

            types = self.db.get_all_issue_types()
            self.medias[day_format] = {tipo: 0 for tipo in types}

            for tipo in types:
                issues = self.db.get_done_issues_list_by_type(tipo)
                lenght = 0
                value = 0

                for issue in issues:
                    change_timestamp = self.db.get_changedate_from_issue_id_done(
                        issue.issue_id
                    )
                    if change_timestamp.date() <= day:
                        start_date = self.get_start_date_reference(issue)
                        days_comparisson = change_timestamp - start_date
                        count_days = days_comparisson.days + (
                            days_comparisson.seconds / 86400
                        )
                        lenght += 1
                        value += count_days

                if value:
                    self.medias[day_format].update({tipo: (value / lenght)})
