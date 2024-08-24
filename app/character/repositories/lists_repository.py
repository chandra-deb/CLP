import math
from datetime import datetime, timedelta
from typing import List

from flask_login import current_user
from flask_sqlalchemy import SQLAlchemy
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

    def delete_list(self, list_id: int):
        self.unpin_list(list_id)
        self.db.session.query(CharacterList).filter_by(id=list_id).delete()
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
                (UserRecognitionProgress.status == "never_studied") | (UserRecognitionProgress.status == None),
            )
            .order_by(ChineseCharacter.id)  # Add an order_by clause for consistent results
        )
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

    def calculate_memory_strength(self, urp: UserRecognitionProgress) -> float:
        if urp:
            now = datetime.now()
            time_since_last_practice = (now - urp.last_practice).days
            new_memory_strength = urp.memory_strength
            # print(f'Prev Strength of {self.character.character} is {new_memory_strength}')

            # Decay Theory: memory strength decays over time
            decay_rate = 0.05  # adjust this value to control the decay rate
            # print('just print ',new_memory_strength * math.exp(-decay_rate * time_since_last_practice))
            new_memory_strength *= math.exp(-decay_rate * time_since_last_practice)
            # print('memory strength after decay: ', new_memory_strength)

            # Forgetting Curve: rapid decline in memory retention initially, then levels off
            forgetting_curve_rate = 0.2  # adjust this value to control the forgetting curve rate
            new_memory_strength *= math.pow(1 - forgetting_curve_rate, time_since_last_practice)

            new_memory_strength = max(0, min(1, new_memory_strength))

            # self.memory_strength = new_memory_strength
            # print(f'Now Strength of {self.character.character} is {self.memory_strength}')
            return new_memory_strength
        else:
            return 0

    def update_memory_strength(self, updated_char_details: list[{}]) -> None:
        for updated_char in updated_char_details:
            character_id = updated_char['character_id']
            is_correct = updated_char['is_correct']
            print(is_correct)
            try:
                urp = self.db.session.scalar(select(UserRecognitionProgress)
                                             .filter_by(character_id=character_id).filter_by(user_id=current_user.id))
            except AttributeError:
                urp = None
            if urp:
                now = datetime.now()
                latest_memory_strength = self.calculate_memory_strength(urp)
                if is_correct:
                    if latest_memory_strength < 0.5:
                        latest_memory_strength = 1.0
                    else:
                        latest_memory_strength += 0.1
                    urp.last_practice = now
                else:
                    if latest_memory_strength > 0.5:
                        latest_memory_strength -= 0.1
                    else:
                        latest_memory_strength = 0.0
                    urp.last_practice = now

                # Update the memory strength attribute
                urp.memory_strength = latest_memory_strength

                # Calculate the next practice date based on the memory strength
                if latest_memory_strength < 1.0:
                    urp.interval = 1
                elif latest_memory_strength < 2.0:
                    urp.interval = 3
                elif latest_memory_strength < 3.0:
                    urp.interval = 7
                elif latest_memory_strength < 4.0:
                    urp.interval = 14
                else:
                    urp.interval = 30

                urp.next_practice = urp.last_practice + timedelta(days=urp.interval)
            else:
                memory_strength = 0.0
                next_practice = datetime.now() + timedelta(days=1)
                if is_correct:
                    memory_strength = 1.0
                    next_practice = datetime.now() + timedelta(days=3)

                user_recog = UserRecognitionProgress(user_id=current_user.id, character_id=character_id,
                                                     memory_strength=memory_strength,
                                                     status='learning', last_practice=datetime.now(),
                                                     next_practice=next_practice,
                                                     interval=7)
                self.db.session.add(user_recog)

        self.db.session.commit()

    # def update_memory_strength(self, updated_char_details: list[{}]) -> None:
    #     for updated_char in updated_char_details:
    #         character_id = updated_char['character_id']
    #         is_correct = updated_char['is_correct']
    #         try:
    #             urp = self.db.session.scalar(select(UserRecognitionProgress)
    #                                          .filter_by(character_id=character_id).filter_by(
    #                 user_id=current_user.id))
    #         except AttributeError:
    #             urp = None
    #         if urp:
    #             now = datetime.now()
    #             latest_memory_strength = self.calculate_memory_strength(urp)
    #             if is_correct:
    #                 latest_memory_strength += 0.1
    #                 if urp.interval < 3:  # Initial phase (0-10 days)
    #                     urp.interval = min(urp.interval * 2, 3)  # cap at 3 days
    #                 elif urp.interval < 14:  # Short-term consolidation (10-30 days)
    #                     urp.interval = min(urp.interval * 2, 14)  # cap at 14 days
    #                 elif urp.interval < 30:  # Long-term retention (30-90 days)
    #                     urp.interval = min(urp.interval * 2, 30)  # cap at 30 days
    #                 else:  # Refresher phase (90+ days)
    #                     urp.interval = min(urp.interval * 2, 60)  # cap at 60 days
    #             else:
    #                 latest_memory_strength -= 0.1
    #                 urp.interval = 1  # reset the interval to 1 day
    #                 urp.next_practice = now + timedelta(days=1)  # update next practice date
    #             urp.last_practice = now
    #             urp.memory_strength = latest_memory_strength
    #             urp.next_practice = urp.last_practice + timedelta(days=urp.interval)
    #         else:
    #             memory_strength = 0.0
    #             next_practice = datetime.now() + timedelta(days=1)
    #             if is_correct:
    #                 memory_strength = 0.5
    #                 next_practice = datetime.now() + timedelta(days=3)
    #
    #             user_recog = UserRecognitionProgress(user_id=current_user.id, character_id=character_id,
    #                                                  memory_strength=memory_strength,
    #                                                  status='learning', last_practice=datetime.now(),
    #                                                  next_practice=next_practice,
    #                                                  interval=1)
    #             self.db.session.add(user_recog)
    #
    #     self.db.session.commit()
