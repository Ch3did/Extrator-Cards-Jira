from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
from loguru import logger


class Leadtime:
    """classe responsável pelo controle da base de dados e geração de documentos"""

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
        """Gera e exibe um gráfico de barras horizontal."""
        dates = [datetime.strptime(item, "%Y-%m-%d") for item in self.evolution.keys()]
        index = self.db.get_all_issue_types()

        plt.figure(figsize=(10, 6))

        for linha, tipo_linha in enumerate(index):
            pontos = [
                self.evolution[item].get(tipo_linha, None)
                for item in self.evolution.keys()
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
        """Detem a logica para montar gráficos relacionados ao leadTime."""
        for day in self.days:
            day_format = day.isoformat()
            logger.info(f"Searching for info on {day_format}")

            self.types = self.db.get_all_issue_types()
            self.evolution[day_format] = {tipo: 0 for tipo in self.types}

            for tipo in self.types:
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
                    self.evolution[day_format].update({tipo: (value / lenght)})
            if self.today == day:
                self.leadtime = self.evolution[day_format].copy()
