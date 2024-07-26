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
    def get_mastered_chars_count(self) -> int:
        return db.session.execute(db.select(db.func.count()).select_from(UserCharacterStatus)
                                  .filter_by(user_id=current_user.id, status='mastered')).scalar()
