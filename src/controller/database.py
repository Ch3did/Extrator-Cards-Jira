from sqlmodel import Session

from database import engine


class DatabaseController:
    """classe responsável pelo controle da base de dados"""

    def __init__(self):
        self.engine = engine
        self.session = Session(engine)

    def _add_to_database(self, data):
        # TODO: Adicionar validação de dado duplicado com base no dia
        self.session.add(data)
        self.session.commit()
