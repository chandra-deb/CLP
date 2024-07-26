class DashboardService:
    def __init__(self, dashboard_repository):
        self.dashboard_repository = dashboard_repository

    def get_mastered_chars_count(self) -> int:
        return self.dashboard_repository.get_mastered_chars_count()
