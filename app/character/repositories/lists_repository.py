import math
from datetime import datetime, timedelta
from typing import List

from flask_login import current_user
from flask_sqlalchemy import SQLAlchemy
from fsrs import FSRS, Card, Rating
from sqlalchemy import or_
from sqlalchemy.orm import selectinload
from sqlalchemy.future import select

from app.models import CharacterList, ChineseCharacter, User, UserRecognitionProgress, CharacterListMapping, \
    PinnedCharacterList


class ListsRepository:
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def get_list_by_id(self, list_id):
        stmt = select(CharacterList).filter_by(id=list_id)
        result = self.db.session.execute(stmt)
        result = result.scalars().one_or_none()
        return result

    # Little alternative approach but do the same thing.
    # def get_list_by_id(self, list_id: int):
    #     character_list = self.db.session.scalars(select(CharacterList).where(CharacterList.id == list_id)).first()
    #     return character_list

    def create_list(self, name: str, parent_id: int = None, user_id: int = None,
                    is_admin_created: bool = False) -> CharacterList:
        # character_list = CharacterList(name, is_admin_created, user_id,  parent_id)
        character_list = CharacterList(name=name, is_admin_created=is_admin_created,
                                       user_id=user_id, parent_list_id=parent_id)
        self.db.session.add(character_list)
        self.db.session.commit()
        return character_list

    def __delete_with_child_lists(self, character_list: CharacterList):
        """
         Delete this CharacterList and all its child lists.
         """
        # Delete child lists recursively
        for child_list in character_list.child_lists:
            self.__delete_with_child_lists(child_list)

        # Delete pinned character lists
        for pinned_list in character_list.pinned_character_lists:
            self.db.session.delete(pinned_list)

        # Delete character mappings
        for mapping in character_list.character_mappings:
            self.db.session.delete(mapping)

        # Finally, delete this character list
        self.db.session.delete(character_list)

    def delete_list(self, list_id: int):
        character_list = self.get_list_by_id(list_id)
        self.__delete_with_child_lists(character_list)
        self.db.session.commit()

    def update_list_name(self, list_id: int, name: str):
        self.db.session.query(CharacterList).filter_by(id=list_id).update(name)
        self.db.session.commit()

    def get_all_parent_lists(self, list_id):
        # Create a CTE to recursively get all parents
        parent_cte = (self.db.session.query(CharacterList)
                      .filter(CharacterList.id == list_id)
                      .cte(recursive=True))

        # Define the recursive query
        parent_cte = parent_cte.union_all(
            self.db.session.query(CharacterList)
            .filter(CharacterList.id == parent_cte.c.parent_list_id)
        )

        # Get all parents
        all_parents = self.db.session.query(parent_cte).all()

        # Return the parent list objects
        reversed_parents = all_parents[::-1]
        return reversed_parents[:-1]

    def get_top_level_user_lists(self):
        top_level_user_lists = self.db.session.scalars(
            select(CharacterList)
            .where(CharacterList.user_id == current_user.id)
            .where(CharacterList.parent_list == None)
        ).all()
        return top_level_user_lists

    def get_user_pinned_lists(self):
        pinned_lists = [char_list_ref.character_list for char_list_ref in current_user.pinned_character_lists]
        print('Pinned LIsts VAAA: ', pinned_lists)
        return pinned_lists

    def get_user_pinned_sub_lists(self, parent_list_id: int, user_id: int):
        stmt = (select(PinnedCharacterList)
                .where(
            PinnedCharacterList.character_list_id == CharacterList.id,
            CharacterList.parent_list_id == parent_list_id,
            PinnedCharacterList.user_id == user_id
        ).options(selectinload(PinnedCharacterList.character_list)))
        result = self.db.session.scalars(stmt)
        pinned_character_lists = result.all()
        pinned_lists = [char_list_ref.character_list for char_list_ref in pinned_character_lists]
        return pinned_lists

    def pin_list(self, list_id: int):
        new_pinned_list = PinnedCharacterList(character_list_id=list_id, user_id=current_user.id)
        self.db.session.add(new_pinned_list)
        self.db.session.commit()

    def unpin_list(self, list_id: int):
        pinned_lists_ref: List[PinnedCharacterList] = current_user.pinned_character_lists
        pinned_ref_id = None
        for ref in pinned_lists_ref:
            if ref.character_list.id == list_id:
                pinned_ref_id = ref.id
                self.db.session.query(PinnedCharacterList).filter_by(id=pinned_ref_id).delete()
                self.db.session.commit()
                break

    def get_top_level_premade_lists(self):
        top_level_premade_lists = self.db.session.scalars(
            select(CharacterList)
            .where(CharacterList.is_admin_created == True)
            .where(CharacterList.parent_list == None)
        ).all()
        return top_level_premade_lists

    def get_character_by_id(self, character_id: int) -> ChineseCharacter | None:
        return self.db.session.get(ChineseCharacter, character_id)

    # Even though this method use latest SqlAlchemy 2.x version
    # But for some weird reason it is just returning the ids of the lists not the lists object itself...
    # def get_all_parents(self, list_id):
    #     # Alias for the CharacterList table
    #     parent_alias = aliased(CharacterList)
    #
    #     # Create a CTE to recursively get all parents
    #     parent_cte = (
    #         select(CharacterList)
    #         .where(CharacterList.id == list_id)
    #         .cte(name="parent_cte", recursive=True)
    #     )
    #
    #     # Define the recursive query
    #     parent_cte = parent_cte.union_all(
    #         select(CharacterList)
    #         .where(CharacterList.id == parent_cte.c.parent_list_id)
    #     )
    #
    #     # Get all parents
    #     stmt = select(parent_cte)
    #     result = self.session.execute(stmt)
    #
    #     # Retrieve all parent CharacterList objects
    #     all_parents = result.scalars().all()
    #
    #     # Return the parent list objects in reverse order, excluding the last element
    #     reversed_parents = all_parents[::-1]
    #     return reversed_parents[:-1]

    def get_unstudied_chars(self, list_id: int, user_id: int, limit: int | None = None) -> List[ChineseCharacter]:
        """
        Get characters that have not been studied by the user in the given list.

        :param list_id: The ID of the character list
        :param user_id: The ID of the user
        :param limit: The maximum number of characters to return (default: 10)
        :return: A list of never studied ChineseCharacter objects
        """

        query = (
            self.db.session.query(ChineseCharacter)
            .join(CharacterListMapping, ChineseCharacter.id == CharacterListMapping.character_id)
            .join(CharacterList, CharacterListMapping.character_list_id == CharacterList.id)
            .outerjoin(UserRecognitionProgress, ChineseCharacter.id == UserRecognitionProgress.character_id)
            .filter(
                CharacterList.id == list_id,
                (UserRecognitionProgress.user_id == user_id) | (UserRecognitionProgress.user_id == None),
                # (UserRecognitionProgress.state == 1),
            )
            .order_by(ChineseCharacter.id)  # Add an order_by clause for consistent results
        )
        print('IIIIIIIIIIIIIIIIIIIIIIII')
        if limit is not None:
            query = query.limit(limit)
        unstudied_chars = query.all()
        return unstudied_chars

    def get_characters_with_memory_strength(self, user_id: int, list_id: int, limit: int | None = None) -> list[
        UserRecognitionProgress]:
        user: User = User.query.get(user_id)
        if user is None:
            print(f"User with ID {user_id} not found")
            return []

        character_list: CharacterList = CharacterList.query.get(list_id)
        if character_list is None:
            print(f"Character list with ID {list_id} not found")
            return []

        query = self.db.session.query(UserRecognitionProgress) \
            .join(CharacterListMapping, CharacterListMapping.character_id == UserRecognitionProgress.character_id) \
            .filter(UserRecognitionProgress.user_id == user.id, CharacterListMapping.character_list_id == list_id) \
            .options(selectinload(UserRecognitionProgress.character))

        if limit is not None:
            query = query.limit(limit)
        characters_with_memory_strength: List[UserRecognitionProgress] = query.all()

        return characters_with_memory_strength

    def update_recog_prog_on_char(self, resps):
        srs = FSRS()
        for resp in resps:
            char_id = resp['char_id']
            rating: int = resp['rating']
            rating_name = None
            if rating == 1:
                rating_name = Rating.Again
            elif rating == 2:
                rating_name = Rating.Hard
            elif rating == 3:
                rating_name = Rating.Good
            elif rating == 4:
                rating_name = Rating.Easy

            try:
                urp = self.db.session.scalar(select(UserRecognitionProgress)
                                             .filter_by(character_id=char_id).filter_by(user_id=current_user.id))
            except AttributeError:
                urp = None
            if urp:
                card = Card.from_dict(urp.to_dict_for_card())
                updated_card, review_log = srs.review_card(card=card, rating=rating_name)
                urp.update_recog_prog(card=updated_card)
            else:
                card = Card()
                new_urp = UserRecognitionProgress.create_from_card(char_id=char_id, card=card)
                self.db.session.add(new_urp)

        self.db.session.commit()

    # def get_searched_characters(self, query):
    #     char_results = [
    #         char.to_dict()
    #         for char in Character.query.filter(
    #             Character.character.like(f"%{query}%")
    #         ).limit(10)
    #     ]
    #
    #     if char_results == None:
    #         char_results = []
    #
    #     pinyin_results = [
    #         char.to_dict()
    #         for char in Character.query.filter(
    #             Character.no_tone_pinyin.like(f"%{query}%")
    #         ).limit(10)
    #     ]
    #     if pinyin_results == None:
    #         pinyin_results = []
    #
    #     meaning_results = [
    #         char.to_dict()
    #         for char in Character.query.filter(Character.meaning.like(f"%{query}%")).limit(
    #             10
    #         )
    #     ]
    #     if meaning_results == None:
    #         meaning_results = []
    #

    def add_characters_to_list(self, list_id: int, chars: List[str]) -> dict:
        character_list = CharacterList.query.get(list_id)
        if not character_list:
            raise ValueError("List not found")

        result = {
            "existing_characters": [],
            "added_characters": [],
            "not_found_characters": [],
            "multiple_matches": {}
        }

        for char in chars:
            matching_characters = ChineseCharacter.query.filter_by(simplified=char).all()
            if not matching_characters:
                result["not_found_characters"].append(char)
            else:
                if len(matching_characters) > 1:
                    result["multiple_matches"][char] = [
                        {"id": c.id, "character": c.simplified, "pinyin": c.pinyin, "meaning": c.definition} for c in
                        matching_characters]
                else:
                    character = matching_characters[0]
                    existing_mapping = CharacterListMapping.query.filter_by(character_list_id=list_id,
                                                                            character_id=character.id).first()
                    if existing_mapping:
                        result["existing_characters"].append({"id": character.id,
                                                              "character": character.simplified,
                                                              "pinyin": character.pinyin,
                                                              "meaning": character.definition})
                    else:
                        character_list_mapping = CharacterListMapping(character_list_id=list_id,
                                                                      character_id=character.id)
                        self.db.session.add(character_list_mapping)
                        result["added_characters"].append(
                            {"id": character.id, "character": character.simplified, "pinyin": character.pinyin,
                             "meaning": character.definition})

        self.db.session.commit()
        return result

    def add_chars_by_ids(self, list_id: int, char_ids: List[int]):
        for char_id in char_ids:
            existing_mapping = CharacterListMapping.query.filter_by(
                character_list_id=list_id,
                character_id=char_id).first()
            if not existing_mapping:
                self.db.session.add(
                    CharacterListMapping(character_list_id=list_id, character_id=char_id)
                )
        self.db.session.commit()

    def remove_chars(self, list_id: int, char_ids: List[int]):
        for char_id in char_ids:
            character_list_mapping = CharacterListMapping.query.filter_by(
                character_list_id=list_id,
                character_id=char_id).first()
            if character_list_mapping:
                self.db.session.delete(character_list_mapping)
        self.db.session.commit()
