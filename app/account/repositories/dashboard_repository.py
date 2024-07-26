from app import db
from app.models import UserCharacterStatus
from flask_login import current_user
from enum import Enum


class CharacterStatus(Enum):
    learning = 'learning'
    mastered = 'mastered'
    assumed = 'assumed'
    hard = 'hard'
    hidden = 'hidden'
    blocked = 'blocked'


class DashboardRepository:

    def __get_char_len_with_given_status(self, status: CharacterStatus) -> int:
        return db.session.execute(
            db.select(db.func.count()).select_from(UserCharacterStatus)
            .filter_by(user_id=current_user.id, status=status.value)).scalar()

    @property
    def learning_chars_len(self) -> int:
        return self.__get_char_len_with_given_status(CharacterStatus.learning)
    @property
    def mastered_chars_len(self) -> int:
        return self.__get_char_len_with_given_status(CharacterStatus.mastered)

    @property
    def assumed_chars_len(self) -> int:
        return self.__get_char_len_with_given_status(CharacterStatus.assumed)

    @property
    def blocked_chars_len(self) -> int:
        return self.__get_char_len_with_given_status(CharacterStatus.blocked)

    @property
    def hidden_chars_len(self) -> int:
        return self.__get_char_len_with_given_status(CharacterStatus.hidden)

    @property
    def hard_chars_len(self) -> int:
        return self.__get_char_len_with_given_status(CharacterStatus.hard)


