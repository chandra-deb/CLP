from flask_sqlalchemy import SQLAlchemy
from app.account.utils import CharacterStatus
from app.models import UserCharacterStatus
from flask_login import current_user


class DashboardRepository:
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def get_char_len_with_given_status(self, status: CharacterStatus) -> int:
        return self.db.session.execute(
            self.db.select(self.db.func.count()).select_from(UserCharacterStatus)
            .filter_by(user_id=current_user.id, status=status.value)).scalar()



