from app.character.repositories.lists_repository import ListsRepository
from app.models import CharacterList


class ListsService:
    def __init__(self, lists_repository: ListsRepository):
        self.repository = lists_repository

    def get_list_by_id(self, list_id) -> CharacterList:
        return self.repository.get_list_by_id(list_id)

    def get_all_parent_lists(self, list_id) -> list[CharacterList]:
        return self.repository.get_all_parent_lists(list_id)

    def get_top_level_user_lists(self) -> list[CharacterList]:
        return self.repository.get_top_level_user_lists()

    def get_top_level_premade_lists(self) -> list[CharacterList]:
        return self.repository.get_top_level_premade_lists()