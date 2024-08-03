from typing import List

from app.character.repositories.lists_repository import ListsRepository
from app.models import CharacterList, ChineseCharacter


class ListsService:
    def __init__(self, lists_repository: ListsRepository):
        self.repository = lists_repository

    def get_list_by_id(self, list_id: int) -> CharacterList:
        return self.repository.get_list_by_id(list_id)

    def get_characters_by_list_id(self, list_id: int) -> list[ChineseCharacter]:
        return self.get_list_by_id(list_id).characters

    def get_all_parent_lists(self, list_id: int) -> list[CharacterList]:
        return self.repository.get_all_parent_lists(list_id)

    def get_top_level_user_lists(self) -> list[CharacterList]:
        return self.repository.get_top_level_user_lists()

    def get_top_level_premade_lists(self) -> list[CharacterList]:
        return self.repository.get_top_level_premade_lists()

    def get_never_studied_chars_of_list(self, list_id: int):
        character_list = self.get_list_by_id(list_id)
        filtered_characters = [character for character in character_list.characters
                               if not character.recognition_progress]
        return filtered_characters

    __MEMORY_THRESHOLD = 0.5

    def get_strong_weak_chars(self, user_id: int, list_id: int):
        characters_with_memory_strength = self.repository.get_characters_with_memory_strength(user_id, list_id)
        memory_strengths = [(urp, urp.calculate_memory_strength()) for urp in characters_with_memory_strength]

        strong_characters = [urp.character for urp, strength in memory_strengths if
                             strength >= self.__MEMORY_THRESHOLD]

        weak_characters = [urp.character for urp, strength in memory_strengths if
                           strength < self.__MEMORY_THRESHOLD]

        return strong_characters, weak_characters
