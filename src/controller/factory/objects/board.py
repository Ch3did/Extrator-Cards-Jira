from src.controller.database import DatabaseController
from src.models.board import Board


class BoardController(DatabaseController):
    """Classe responsável pela criação e registro dos Boards"""

    def board_factory(self, api_response: dict):
        boad_id_list = []
        for board_dict in api_response["values"]:
            if board_dict["type"] == "scrum":
                board = Board(
                    board_id=board_dict.get("id"),
                    board_name=board_dict.get("name"),
                    board_url=board_dict.get("self"),
                    board_type=board_dict.get("type"),
                )
                boad_id_list.append(board.board_id)
                self.save_board(board)
        return boad_id_list
