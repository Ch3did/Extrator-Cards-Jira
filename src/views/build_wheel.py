from datetime import datetime, timedelta
from io import BytesIO

import boto3
import matplotlib.pyplot as plt
import numpy as np
from loguru import logger

from src.controller.database import DatabaseController
from src.controller.plot.leadtime import Leadtime


class BuildView(Leadtime):
    """Cria os dados para montar os gráficos e os envia para o serviço nescessario"""

    def __init__(self, access_key_id, secret_access_key, bucket, show=False):
        logger.info("Starting Data Analyzes...")
        self.show = show
        self.today = datetime.now().date()
        self.evolution = {}
        self.leadtime = {}
        self.db = DatabaseController()
        self.access_key_id = access_key_id
        self.secret_access_key = secret_access_key
        self.bucket = bucket
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=self.access_key_id,
            aws_secret_access_key=self.secret_access_key,
        )
        self.days = [
            (datetime.now() - timedelta(days=item)).date() for item in range(30)
        ]

    def send_to_s3(self, plt, file_name, acl="public-read") -> BytesIO:
        imagem_buffer = BytesIO()
        plt.savefig(imagem_buffer, format="png")
        imagem_buffer.seek(0)
        imagem_buffer
        logger.info(f"Sending {file_name} to S3!")

        self.s3.upload_fileobj(
            imagem_buffer, self.bucket, file_name, ExtraArgs={"ACL": acl}
        )

        url = self.s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": self.bucket, "Key": file_name},
            ExpiresIn=3600,
        )
        logger.info(f"File with key: {file_name} saved succesfully!")
        logger.info(f"\nURL for {file_name}: {url}")

    def plot_leadtime_graff(self) -> None:
        logger.info("Creating leadtime graffic")
        dados = self.leadtime

        barras = list(dados.keys())
        alturas = list(dados.values())

        plt.barh(barras, alturas, color="lightblue")
        plt.ylabel("Tipos")
        plt.xlabel("LeadTime (dias)")
        plt.title(f"LeadTime por Tipo ({self.today})")
        plt.xticks(range(0, int(max(alturas) + 2) + 1, 1))
        plt.grid(True, axis="x", linestyle="--", alpha=0.7)
        plt.show()
        self.send_to_s3(plt, f"{self.today.isoformat()}-leadtime.png")

    def plot_evolution_graff(self, thickness: int = 3) -> None:
        logger.info("Creating elovution leadtime graffic")
        index = self.types
        dados = self.evolution
        datas = [datetime.strptime(data, "%Y-%m-%d") for data in dados.keys()]

        plt.figure(figsize=(10, 6))
        plt.title("Evolution Leadtime")
        plt.xlabel("Data")
        plt.ylabel("Tipo de leadtime")

        for linha, tipo_linha in enumerate(index):
            pontos = [dados[data].get(tipo_linha, None) for data in dados.keys()]
            plt.plot(
                datas,
                np.array(pontos),
                label=tipo_linha,
                linewidth=thickness,
            )
        plt.xticks(rotation=45)
        plt.grid(True, linestyle="--", alpha=0.7)
        plt.legend()
        plt.tight_layout()
        plt.legend(loc="lower left")
        plt.show()
        self.send_to_s3(plt, f"{self.today.isoformat()}-evolution.png")
