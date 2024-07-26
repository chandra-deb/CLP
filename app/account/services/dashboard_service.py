from app.account.repositories.dashboard_repository import DashboardRepository


class DashboardService:
    def __init__(self, dashboard_repository: DashboardRepository):
        self.dashboard_repository = dashboard_repository

    @property
    def mastered_chars_len(self) -> int:
        return self.dashboard_repository.mastered_chars_len

    @property
    def vocabulary_len(self) -> int:
        vocabulary_size = (self.dashboard_repository.mastered_chars_len
                           + self.dashboard_repository.learning_chars_len
                           + self.dashboard_repository.assumed_chars_len)
        return vocabulary_size
