from enum import Enum

from app.account.repositories.dashboard_repository import DashboardRepository
from app.account.utils import CharacterStatus


class DashboardService:
    def __init__(self, dashboard_repository: DashboardRepository):
        self.dashboard_repository = dashboard_repository

    @property
    def vocabulary_len(self) -> int:
        vocabulary_size = (self.mastered_chars_len
                           + self.learning_chars_len
                           + self.assumed_chars_len
                           )
        return vocabulary_size

    @property
    def learning_chars_len(self) -> int:
        return self.dashboard_repository.get_chars_len_with_given_status(CharacterStatus.learning)

    @property
    def mastered_chars_len(self) -> int:
        return self.dashboard_repository.get_chars_len_with_given_status(CharacterStatus.mastered)

    @property
    def assumed_chars_len(self) -> int:
        return self.dashboard_repository.get_chars_len_with_given_status(CharacterStatus.assumed)

    @property
    def blocked_chars_len(self) -> int:
        return self.dashboard_repository.get_chars_len_with_given_status(CharacterStatus.blocked)

    @property
    def hidden_chars_len(self) -> int:
        return self.dashboard_repository.get_chars_len_with_given_status(CharacterStatus.hidden)

    @property
    def hard_chars_len(self) -> int:
        return self.dashboard_repository.get_chars_len_with_given_status(CharacterStatus.hard)

