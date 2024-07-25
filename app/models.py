from datetime import datetime
from typing import Optional, List
import sqlalchemy as sa
import sqlalchemy.orm as so
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from app import db, login

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))


class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    # New Added
    created_at: so.Mapped[datetime] = so.mapped_column(sa.DateTime, default=db.func.current_timestamp())
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    # Relationships
    character_statuses: so.Mapped[List['UserCharacterStatus']] = so.relationship('UserCharacterStatus',
                                                                                 back_populates='user')
    notes: so.Mapped[List['UserNote']] = so.relationship('UserNote', back_populates='user')
    character_lists: so.Mapped[List['CharacterList']] = so.relationship('CharacterList', back_populates='user')

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


class ChineseCharacter(db.Model):
    __tablename__ = 'chinese_character'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    character: so.Mapped[str] = so.mapped_column(sa.String(1), index=True, unique=True, nullable=False)
    pinyin: so.Mapped[str] = so.mapped_column(sa.String(64),index=True, nullable=False)

    # Relationships
    character_mappings: so.Mapped[List['CharacterListMapping']] = so.relationship('CharacterListMapping',
                                                                                  back_populates='character')
    notes: so.Mapped[List['UserNote']] = so.relationship('UserNote', back_populates='character')

    def __repr__(self):
        return f'<ChineseCharacter {self.character}>'


class UserCharacterStatus(db.Model):
    __tablename__ = 'user_character_status'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('user.id'))
    character_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('chinese_character.id'))
    status: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True, nullable=False)

    # Relationships
    user: so.Mapped['User'] = so.relationship('User', back_populates='character_statuses')
    character: so.Mapped['ChineseCharacter'] = so.relationship('ChineseCharacter')

    def __repr__(self):
        return f'<UserCharacterStatus {self.status}>'


class CharacterList(db.Model):
    __tablename__ = 'character_list'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=False, nullable=False)
    is_admin_created: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=False)
    user_id: so.Mapped[Optional[int]] = so.mapped_column(sa.ForeignKey('user.id'), nullable=True)
    parent_list_id: so.Mapped[Optional[int]] = so.mapped_column(sa.ForeignKey('character_list.id'), nullable=True)

    # Relationships
    character_mappings: so.Mapped[List['CharacterListMapping']] = so.relationship('CharacterListMapping',
                                                                                  back_populates='character_list')
    user: so.Mapped[Optional['User']] = so.relationship('User', back_populates='character_lists')
    parent_list: so.Mapped[Optional['CharacterList']] = so.relationship('CharacterList', remote_side=[id],
                                                                        back_populates='child_lists')
    child_lists: so.Mapped[List['CharacterList']] = so.relationship('CharacterList', back_populates='parent_list')
    characters: so.Mapped[List['ChineseCharacter']] = so.relationship('ChineseCharacter',
                                                                      secondary='character_list_mapping', viewonly=True)

    def __repr__(self):
        return f'<CharacterList {self.name}>'


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


