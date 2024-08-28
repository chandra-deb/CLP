import math
from datetime import datetime
from typing import List

from flask_login import current_user

from app.character.repositories.lists_repository import ListsRepository
from app.models import CharacterList, ChineseCharacter, UserRecognitionProgress


class ListsService:
    def __init__(self, lists_repository: ListsRepository):
        self.repository = lists_repository

    def pin_list(self, list_id):
        self.repository.pin_list(list_id)

    def unpin_list(self, list_id):
        self.repository.unpin_list(list_id)

    def get_pinned_lists(self):
        return self.repository.get_user_pinned_lists()

    def get_pinned_sub_lists(self, parent_list_id: int):
        return self.repository.get_user_pinned_sub_lists(parent_list_id, user_id=current_user.id)

    def get_list_by_id(self, list_id: int) -> CharacterList:
        return self.repository.get_list_by_id(list_id)

    def create_list(self, name: str, parent_list_id: int = None) -> CharacterList:
        return self.repository.create_list(name=name, user_id=current_user.id, parent_id=parent_list_id)

    def delete_list(self, list_id: int):
        self.repository.delete_list(list_id)

    def update_list_name(self, list_id: int, name: str):
        self.repository.update_list_name(list_id, name)

    def get_characters_by_list_id(self, list_id: int) -> list[ChineseCharacter]:
        return self.get_list_by_id(list_id).characters

    def get_all_parent_lists(self, list_id: int) -> list[CharacterList]:
        return self.repository.get_all_parent_lists(list_id)

    def get_top_level_user_lists(self) -> list[CharacterList]:
        return self.repository.get_top_level_user_lists()

    def get_top_level_premade_lists(self) -> list[CharacterList]:
        return self.repository.get_top_level_premade_lists()

    def get_never_studied_chars_of_list(self, list_id: int, limit: int | None = None) -> list[ChineseCharacter]:
        return self.repository.get_unstudied_chars(list_id, current_user.id, limit=limit)
        # character_list = self.get_list_by_id(list_id)
        # filtered_characters = [character for character in character_list.characters
        #                        if not character.recognition_progress]
        # return filtered_characters

    __MEMORY_THRESHOLD = 0.5

    def get_strong_weak_chars(self, list_id: int):
        characters_with_memory_strength = self.repository.get_characters_with_memory_strength(current_user.id, list_id)
        memory_strengths = [(urp, urp.calculate_memory_strength()) for urp in characters_with_memory_strength]

        strong_characters = [urp.character for urp, strength in memory_strengths if
                             strength >= self.__MEMORY_THRESHOLD]

        weak_characters = [urp.character for urp, strength in memory_strengths if
                           strength < self.__MEMORY_THRESHOLD]

        return strong_characters, weak_characters

    def get_strong_chars_of_list(self, list_id: int, limit: int | None = None) -> list[ChineseCharacter]:
        characters_with_memory_strength = self.repository.get_characters_with_memory_strength(current_user.id, list_id)
        memory_strengths = [(urp, urp.calculate_memory_strength()) for urp in characters_with_memory_strength]
        strong_characters = [urp.character for urp, strength in memory_strengths if
                             strength >= self.__MEMORY_THRESHOLD]
        if limit is not None:
            return strong_characters[:int(limit)]
        return strong_characters

    def get_weak_chars_of_list(self, list_id: int, limit: int | None = None) -> list[ChineseCharacter]:
        characters_with_memory_strength = self.repository.get_characters_with_memory_strength(current_user.id, list_id)

        memory_strengths = [(urp, urp.calculate_memory_strength()) for urp in characters_with_memory_strength]
        weak_characters = [urp.character for urp, strength in memory_strengths if
                           strength < self.__MEMORY_THRESHOLD]
        if limit is not None:
            return weak_characters[:int(limit)]
        return weak_characters

    def get_ten_never_studied_chars(self, list_id: int):
        characters = self.get_never_studied_chars_of_list(list_id)
        return characters[:10]

    # def get_never_studied_chars(self, size: int,  list_id: int):

    def update_memory_strength(self, updated_char_details: list[{}]) -> None:
        self.repository.update_memory_strength(updated_char_details)

    def add_chars_by_ids(self, list_id: int, char_ids: List[int]):
        self.repository.add_chars_by_ids(list_id, char_ids)

    def add_chars_to_list(self, list_id: int, chars: List[str]) -> dict:
        return self.repository.add_characters_to_list(list_id=list_id, chars=chars)

    def remove_chars(self, list_id: int, char_ids: List[int]):
        self.repository.remove_chars(list_id, char_ids)
