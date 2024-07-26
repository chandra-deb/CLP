from app import db
from app.models import UserCharacterStatus
from flask_login import current_user


class DashboardRepository:
    def get_mastered_chars_count(self) -> int:
        return db.session.execute(db.select(db.func.count()).select_from(UserCharacterStatus)
                                  .filter_by(user_id=current_user.id, status='mastered')).scalar()
