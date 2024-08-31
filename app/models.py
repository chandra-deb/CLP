import math
from datetime import datetime, timedelta
from typing import Optional, List
import sqlalchemy as sa
import sqlalchemy.orm as so
from fsrs import Card, State
from sqlalchemy import DateTime, UniqueConstraint
from sqlalchemy.orm import remote, foreign
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, current_user

from app import db, login


@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))


class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(32), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    # New Added
    created_at: so.Mapped[datetime] = so.mapped_column(sa.DateTime, default=db.func.current_timestamp())
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    # Relationships
    # character_statuses: so.Mapped[List['UserCharacterStatus']] = so.relationship('UserCharacterStatus',
    #                                                                              back_populates='user')
    pinyin_progress: so.Mapped[List['UserPinyinProgress']] = so.relationship('UserPinyinProgress',
                                                                             back_populates='user')
    meaning_progress: so.Mapped[List['UserMeaningProgress']] = so.relationship('UserMeaningProgress',
                                                                               back_populates='user')
    recognition_progress: so.Mapped[List['UserRecognitionProgress']] = so.relationship('UserRecognitionProgress',
                                                                                       back_populates='user')
    writing_progress: so.Mapped[List['UserWritingProgress']] = so.relationship('UserWritingProgress',
                                                                               back_populates='user')
    notes: so.Mapped[List['UserNote']] = so.relationship('UserNote', back_populates='user')
    character_lists: so.Mapped[List['CharacterList']] = so.relationship('CharacterList', back_populates='user')
    pinned_character_lists: so.Mapped[List['PinnedCharacterList']] = so.relationship('PinnedCharacterList',
                                                                                     back_populates='user')

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


class ChineseCharacter(db.Model):
    __tablename__ = 'chinese_character'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    simplified: so.Mapped[str] = so.mapped_column(sa.String(8), index=True, nullable=False)
    traditional: so.Mapped[str] = so.mapped_column(sa.String(8), index=True, nullable=False)
    pinyin: so.Mapped[str] = so.mapped_column(sa.String(32), index=True, nullable=False)
    definition: so.Mapped[str] = so.mapped_column(sa.String(512), index=True, nullable=True)

    # Relationships
    character_mappings: so.Mapped[List['CharacterListMapping']] = so.relationship('CharacterListMapping',
                                                                                  back_populates='character')
    notes: so.Mapped[List['UserNote']] = so.relationship('UserNote', back_populates='character')
    recognition_progress: so.Mapped[List['UserRecognitionProgress']] = so.relationship('UserRecognitionProgress',
                                                                                       lazy='joined')

    def __repr__(self):
        return f'<ChineseCharacter {self.simplified.encode('utf-8')}>'

    def to_json(self):
        return {
            'id': self.id,
            'character': self.character,
            'pinyin': self.pinyin,
            'meaning': self.meaning,
        }


class UserRecognitionProgress(db.Model):
    __tablename__ = 'user_recognition_progress'
    __table_args__ = (UniqueConstraint('user_id', 'character_id', name='unique_user_recognition'),)

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('user.id'))
    character_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('chinese_character.id'))
    # status: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=False, nullable=False,
    #                                           default='never_studied')
    # To Implement SRS
    due: so.Mapped[datetime] = so.mapped_column()
    stability: so.Mapped[float] = so.mapped_column(default=0.0)
    difficulty: so.Mapped[float] = so.mapped_column(default=0.0)
    elapsed_days: so.Mapped[int] = so.mapped_column(default=0)
    scheduled_days: so.Mapped[int] = so.mapped_column(default=0)
    reps: so.Mapped[int] = so.mapped_column(default=0)
    lapses: so.Mapped[int] = so.mapped_column(default=0)
    state: so.Mapped[int] = so.mapped_column(default=0)
    last_review: so.Mapped[datetime] = so.mapped_column()

    # End

    # Relationships
    user: so.Mapped['User'] = so.relationship('User', back_populates='recognition_progress')
    character: so.Mapped['ChineseCharacter'] = so.relationship('ChineseCharacter')

    @classmethod
    def create_from_card(cls, char_id: int, card: Card):
        return UserRecognitionProgress(
            user_id=current_user.id,
            character_id=char_id,
            due=card.due,
            stability=card.stability,
            difficulty=card.difficulty,
            elapsed_days=card.elapsed_days,
            scheduled_days=card.scheduled_days,
            reps=card.reps,
            lapses=card.lapses,
            state=card.state,
            last_review=card.last_review,
        )

    def to_dict_for_card(self, ):
        due = self.due
        stability = self.stability
        difficulty = self.difficulty
        elapsed_days = self.elapsed_days
        scheduled_days = self.scheduled_days
        reps = self.reps
        lapses = self.lapses
        state = State(int(self.state))
        last_review = self.last_review,

        return {
            'due': due,
            'stability': stability,
            'difficulty': difficulty,
            'elapsed_days': elapsed_days,
            'scheduled_days': scheduled_days,
            'reps': reps,
            'lapses': lapses,
            'state': state,
            'last_review': last_review,
        }

    def update_recog_prog(self, card: Card):
        self.due = card.due
        self.stability = card.stability
        self.difficulty = card.difficulty
        self.elapsed_days = card.elapsed_days
        self.scheduled_days = card.scheduled_days
        self.reps = card.reps
        self.lapses = card.lapses
        self.state = card.state.value,
        self.last_review = card.last_review,


class UserPinyinProgress(db.Model):
    __tablename__ = 'user_pinyin_progress'
    __table_args__ = (UniqueConstraint('user_id', 'character_id', name='unique_user_pinyin'),)

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('user.id'))
    character_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('chinese_character.id'))
    status: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True, nullable=False,
                                              default='never_studied')
    memory_strength: so.Mapped[float] = so.mapped_column(default=0.0)
    last_practice: so.Mapped[datetime] = so.mapped_column(default=datetime.now())
    next_practice: so.Mapped[datetime] = so.mapped_column(default=datetime.now())
    interval: so.Mapped[int] = so.mapped_column(default=1)

    # Relationships
    user: so.Mapped['User'] = so.relationship('User', back_populates='pinyin_progress')
    character: so.Mapped['ChineseCharacter'] = so.relationship('ChineseCharacter')

    def update_memory_strength(self, correct: bool) -> None:
        """
        Update the memory strength based on the spaced repetition algorithm.

        :param correct: Whether the user answered correctly or not
        """
        now = datetime.now()
        if correct:
            if self.memory_strength < 0.5:
                self.memory_strength = 1.0
            else:
                self.memory_strength += 0.1
            self.last_practice = now
        else:
            if self.memory_strength > 0.5:
                self.memory_strength -= 0.1
            else:
                self.memory_strength = 0.0
            self.last_practice = now

        # Calculate the next practice date based on the memory strength
        if self.memory_strength < 1.0:
            self.interval = 1
        elif self.memory_strength < 2.0:
            self.interval = 3
        elif self.memory_strength < 3.0:
            self.interval = 7
        elif self.memory_strength < 4.0:
            self.interval = 14
        else:
            self.interval = 30

        self.next_practice = self.last_practice + timedelta(days=self.interval)

        db.session.commit()


class UserMeaningProgress(db.Model):
    __tablename__ = 'user_meaning_progress'
    __table_args__ = (UniqueConstraint('user_id', 'character_id', name='unique_user_meaning'),)

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('user.id'))
    character_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('chinese_character.id'))
    status: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True, nullable=False,
                                              default='never_studied')
    memory_strength: so.Mapped[float] = so.mapped_column(default=0.0)
    last_practice: so.Mapped[datetime] = so.mapped_column(default=datetime.now())
    next_practice: so.Mapped[datetime] = so.mapped_column(default=datetime.now())
    interval: so.Mapped[int] = so.mapped_column(default=1)

    # Relationships
    user: so.Mapped['User'] = so.relationship('User', back_populates='meaning_progress')
    character: so.Mapped['ChineseCharacter'] = so.relationship('ChineseCharacter')

    def update_memory_strength(self, correct: bool) -> None:
        """
        Update the memory strength based on the spaced repetition algorithm.

        :param correct: Whether the user answered correctly or not
        """
        now = datetime.now()
        if correct:
            if self.memory_strength < 0.5:
                self.memory_strength = 1.0
            else:
                self.memory_strength += 0.1
            self.last_practice = now
        else:
            if self.memory_strength > 0.5:
                self.memory_strength -= 0.1
            else:
                self.memory_strength = 0.0
            self.last_practice = now

        # Calculate the next practice date based on the memory strength
        if self.memory_strength < 1.0:
            self.interval = 1
        elif self.memory_strength < 2.0:
            self.interval = 3
        elif self.memory_strength < 3.0:
            self.interval = 7
        elif self.memory_strength < 4.0:
            self.interval = 14
        else:
            self.interval = 30

        self.next_practice = self.last_practice + timedelta(days=self.interval)

        db.session.commit()


class UserWritingProgress(db.Model):
    __tablename__ = 'user_writing_progress'
    __table_args__ = (UniqueConstraint('user_id', 'character_id', name='unique_user_writing'),)

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('user.id'))
    character_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('chinese_character.id'))
    status: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True, nullable=False,
                                              default='never_studied')
    memory_strength: so.Mapped[float] = so.mapped_column(default=0.0)
    last_practice: so.Mapped[datetime] = so.mapped_column(default=datetime.now())
    next_practice: so.Mapped[datetime] = so.mapped_column(default=datetime.now())
    interval: so.Mapped[int] = so.mapped_column(default=1)

    # Relationships
    user: so.Mapped['User'] = so.relationship('User', back_populates='writing_progress')
    character: so.Mapped['ChineseCharacter'] = so.relationship('ChineseCharacter')

    def update_memory_strength(self, correct: bool) -> None:
        """
        Update the memory strength based on the spaced repetition algorithm.

        :param correct: Whether the user answered correctly or not
        """
        now = datetime.now()
        if correct:
            if self.memory_strength < 0.5:
                self.memory_strength = 1.0
            else:
                self.memory_strength += 0.1
            self.last_practice = now
        else:
            if self.memory_strength > 0.5:
                self.memory_strength -= 0.1
            else:
                self.memory_strength = 0.0
            self.last_practice = now

        # Calculate the next practice date based on the memory strength
        if self.memory_strength < 1.0:
            self.interval = 1
        elif self.memory_strength < 2.0:
            self.interval = 3
        elif self.memory_strength < 3.0:
            self.interval = 7
        elif self.memory_strength < 4.0:
            self.interval = 14
        else:
            self.interval = 30

        self.next_practice = self.last_practice + timedelta(days=self.interval)

        db.session.commit()


# ----------End-----------#

class CharacterList(db.Model):
    __tablename__ = 'character_list'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=False, nullable=False)
    is_admin_created: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=False)
    user_id: so.Mapped[Optional[int]] = so.mapped_column(sa.ForeignKey('user.id'), nullable=True)
    parent_list_id: so.Mapped[Optional[int]] = so.mapped_column(sa.ForeignKey('character_list.id'), nullable=True)

    # Relationships
    character_mappings: so.Mapped[List['CharacterListMapping']] = so.relationship('CharacterListMapping',
                                                                                  back_populates='character_list',
                                                                                  cascade='all, delete-orphan')
    user: so.Mapped[Optional['User']] = so.relationship('User', back_populates='character_lists')

    parent_list: so.Mapped[Optional['CharacterList']] = so.relationship('CharacterList', remote_side=[id],
                                                                        back_populates='child_lists')
    child_lists: so.Mapped[List['CharacterList']] = so.relationship('CharacterList', back_populates='parent_list',
                                                                    cascade='all, delete', passive_deletes=True)
    characters: so.Mapped[List['ChineseCharacter']] = so.relationship('ChineseCharacter',
                                                                      secondary='character_list_mapping', viewonly=True)
    pinned_character_lists: so.Mapped[List['PinnedCharacterList']] = so.relationship('PinnedCharacterList',
                                                                                     back_populates='character_list',
                                                                                     cascade='all, delete-orphan')

    def __repr__(self):
        return f'<CharacterList {self.name}>'


class PinnedCharacterList(db.Model):
    __tablename__ = 'pinned_character_list'
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    character_list_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('character_list.id'))
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('user.id'))

    #     Relationships
    user: so.Mapped[Optional['User']] = so.relationship('User', back_populates='pinned_character_lists')
    character_list: so.Mapped[Optional['CharacterList']] = so.relationship('CharacterList',
                                                                           back_populates='pinned_character_lists',
                                                                           cascade='all, delete', passive_deletes=True)


class CharacterListMapping(db.Model):
    __tablename__ = 'character_list_mapping'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    character_list_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('character_list.id'))
    character_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('chinese_character.id'))

    # Relationships
    character_list: so.Mapped['CharacterList'] = so.relationship('CharacterList', back_populates='character_mappings')
    character: so.Mapped['ChineseCharacter'] = so.relationship('ChineseCharacter', back_populates='character_mappings')

    def __repr__(self):
        return f'<CharacterListMapping {self.character_list_id}-{self.character_id}>'


class UserNote(db.Model):
    __tablename__ = 'user_note'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('user.id'))
    character_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('chinese_character.id'))
    note: so.Mapped[str] = so.mapped_column(sa.String(200), index=True, nullable=False)

    # Relationships
    user: so.Mapped['User'] = so.relationship('User', back_populates='notes')
    character: so.Mapped['ChineseCharacter'] = so.relationship('ChineseCharacter', back_populates='notes')

    def __repr__(self):
        return f'<UserNote {self.user_id}-{self.character_id}>'

# def update_memory_strength(self, correct: bool) -> None:
#     """
#     Update the memory strength based on the spaced repetition algorithm.
#
#     :param correct: Whether the user answered correctly or not
#     """
#     now = datetime.now()
#     self.memory_strength = max(0.0, min(5.0, self.memory_strength + (0.1 if correct else -0.1)))
#     self.last_practice = now
#
#     intervals = [1, 3, 7, 14, 30]
#     self.interval = intervals[min(int(self.memory_strength), len(intervals) - 1)]
#     self.next_practice = self.last_practice + timedelta(days=self.interval)
#
#     try:
#         db.session.commit()
#     except Exception as e:
#         print(f"Error committing to the database: {e}")
