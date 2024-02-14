from src.controller.database import DatabaseController
from src.models.board import Board, Location


class BoardController(DatabaseController):
    """Classe responsável pela criação e registro dos Boards"""
    def _location_factory(self, location_data: dict) -> Location:
        location = Location(
            location_id=location_data.get("projectId"),
            location_name=location_data.get("projectName"),
            display_name=location_data.get("displayName"),
            location_key=location_data.get("projectKey"),
            location_type_key=location_data.get("projectTypeKey"),
            avatar_URI=location_data.get("avatarURI"),
        )
        self._add_to_database(location)
        return location

    def board_factory(self, api_response: dict):
        boad_id_list = []
        for board_dict in api_response["values"]:

            location = self._location_factory(board_dict.get("location"))
            board = Board(
                board_id=board_dict.get("id"),
                board_name=board_dict.get("name"),
                board_url=board_dict.get("self"),
                board_type=board_dict.get("type"),
                location_id=location.id,
            )
            boad_id_list.append(board.board_id)
            self._add_to_database(board)
        return boad_id_list
