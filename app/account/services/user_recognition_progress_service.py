from app.account.repositories.user_recognition_progress_repository import UserRecognitionProgressRepository


class UserRecognitionProgressService:
    def __init__(self, repository: UserRecognitionProgressRepository):
        self.repository = repository

    def get_due_characters(self, user_id: int):
        return self.repository.get_due_characters(user_id)

    def count_due_characters(self, user_id: int) -> int:
        return self.repository.count_due_characters(user_id)

    def get_strong_memory_characters(self, user_id: int, limit: int = 10):
        return self.repository.get_strong_memory_characters(user_id, limit)

    def get_weak_memory_characters(self, user_id: int, limit: int = 10):
        return self.repository.get_weak_memory_characters(user_id, limit)

    def get_hard_characters(self, user_id: int, limit: int = 10):
        return self.repository.get_hard_characters(user_id, limit)

    def get_new_characters(self, user_id: int, limit: int = 10):
        return self.repository.get_new_characters(user_id, limit)




