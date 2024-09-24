from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from fsrs import Card
from sqlalchemy import or_, and_, desc

from app.models import UserRecognitionProgress, PinnedCharacterList, CharacterListMapping, ChineseCharacter


class UserRecognitionProgressRepository:
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def get_due_characters(self, user_id: int):
        # Get the current date and time
        now = datetime.now()

        # Use db.session to query for characters that are due for review and sort by due date
        due_characters = self.db.session.query(UserRecognitionProgress).filter(
            UserRecognitionProgress.user_id == user_id,
            UserRecognitionProgress.due <= now
        ).order_by(UserRecognitionProgress.due).all()

        return due_characters

    def count_due_characters(self, user_id: int) -> int:
        # Get the current date and time
        now = datetime.now()

        # Count the number of due characters for the specified user
        due_count = self.db.session.query(UserRecognitionProgress).filter(
            UserRecognitionProgress.user_id == user_id,
            UserRecognitionProgress.due <= now
        ).count()

        return due_count

    def get_strong_memory_characters(self, user_id: int, limit: int = 10):
        # Query for characters with low stability (weak memory) and limit the results
        strong_memory_characters = self.db.session.query(UserRecognitionProgress).filter(
            UserRecognitionProgress.user_id == user_id,
            UserRecognitionProgress.stability > 0.5  # Adjust threshold as needed
        ).order_by(UserRecognitionProgress.stability).limit(limit).all()

        return strong_memory_characters

    def get_weak_memory_characters(self, user_id: int, limit: int = 10):
        # Query for characters with low stability (weak memory) and limit the results
        weak_memory_characters = self.db.session.query(UserRecognitionProgress).filter(
            UserRecognitionProgress.user_id == user_id,
            UserRecognitionProgress.stability <= 0.5  # Adjust threshold as needed
        ).order_by(UserRecognitionProgress.stability).limit(limit).all()

        return weak_memory_characters

    def get_hard_characters(self, user_id: int, limit: int = 10):
        # Query for characters that are hard based on difficulty and stability
        hard_characters = self.db.session.query(UserRecognitionProgress).filter(
            UserRecognitionProgress.user_id == user_id,
            or_(
                UserRecognitionProgress.difficulty > 0.5,  # High difficulty
                UserRecognitionProgress.stability < 0.5  # Low stability
            )
        ).order_by(
            desc(UserRecognitionProgress.difficulty),  # Sort by difficulty descending
            UserRecognitionProgress.stability  # Sort by stability ascending
        ).limit(limit).all()

        return hard_characters

    def get_new_characters(self, user_id: int, limit: int = 10):
        # Get the list of pinned character lists for the user
        pinned_lists = self.db.session.query(PinnedCharacterList).filter(
            PinnedCharacterList.user_id == user_id
        ).all()

        if not pinned_lists:
            return []  # Return empty if no pinned lists

        # Get the unique character IDs from the pinned character lists
        pinned_character_ids = self.db.session.query(CharacterListMapping.character_id).filter(
            CharacterListMapping.character_list_id.in_([pl.character_list_id for pl in pinned_lists])
        ).distinct().subquery()

        # Query for new characters that the user has never learned before
        new_characters = self.db.session.query(ChineseCharacter).filter(
            ChineseCharacter.id.notin_(
                self.db.session.query(UserRecognitionProgress.character_id).filter(
                    UserRecognitionProgress.user_id == user_id
                )
            ),
            ChineseCharacter.id.in_(pinned_character_ids)
        ).order_by(
            #!info: It is not quite right order. Check later
            CharacterListMapping.id
        ).limit(limit).all()

        return new_characters



    # def get_weak_memory_characters(self, user_id: int, limit: int = 10):
    #     # Get the current date and time
    #     now = datetime.now()
    #
    #     # Query for characters with weak memory based on multiple attributes
    #     weak_memory_characters = self.db.session.query(UserRecognitionProgress).filter(
    #         UserRecognitionProgress.user_id == user_id,
    #         or_(
    #             UserRecognitionProgress.stability < 0.5,  # Low stability
    #             and_(
    #                 UserRecognitionProgress.due <= now,  # Overdue
    #                 UserRecognitionProgress.elapsed_days > 7  # Not reviewed in a week
    #             ),
    #             UserRecognitionProgress.lapses > 2  # More than 2 lapses
    #         )
    #     ).order_by(
    #         UserRecognitionProgress.stability,  # Sort by stability
    #         UserRecognitionProgress.due,  # Sort by due date
    #         UserRecognitionProgress.lapses.desc()  # Sort by lapses descending
    #     ).limit(limit).all()

    # def get_strong_memory_characters(cls, user_id: int, limit: int = 10):
    #     # Get the current date and time
    #     now = datetime.now()
    #
    #     # Query for characters with strong memory based on multiple attributes
    #     strong_memory_characters = db.session.query(UserRecognitionProgress).filter(
    #         UserRecognitionProgress.user_id == user_id,
    #         and_(
    #             UserRecognitionProgress.stability > 0.8,  # High stability
    #             UserRecognitionProgress.due > now,  # Not due yet
    #             UserRecognitionProgress.lapses == 0  # No lapses
    #         )
    #     ).order_by(
    #         UserRecognitionProgress.stability.desc(),  # Sort by stability descending
    #         UserRecognitionProgress.due  # Sort by due date ascending
    #     ).limit(limit).all()
    #
    #     return strong_memory_characters
