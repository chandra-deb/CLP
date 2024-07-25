# from app import app, db
# from app.models import User, ChineseCharacter, UserCharacterStatus, CharacterList, UserNote
#
# # Create the application instance
#
# with app.app_context():
#     # Dummy data for User
#     users = [
#         User(username=f'user{i}', email=f'user{i}@example.com', password_hash='hashedpassword')
#         for i in range(1, 11)
#     ]
#
#     # Dummy data for ChineseCharacter
#     characters = [
#         ChineseCharacter(character=chr(0x4E00 + i), pinyin=f'pinyin{i}')  # Using Unicode for Chinese characters
#         for i in range(10)
#     ]
#
#     # Dummy data for CharacterList
#     character_lists = [
#         CharacterList(name=f'List {i}', created_by_admin=(i % 2 == 0))  # Alternating between admin and user
#         for i in range(1, 11)
#     ]
#
#     # Dummy data for UserCharacterStatus
#     user_character_statuses = [
#         UserCharacterStatus(user_id=(i % 10) + 1, character_id=(i % 10) + 1, status='Learned')
#         for i in range(1, 11)
#     ]
#
#     # Dummy data for UserNote
#     user_notes = [
#         UserNote(user_id=(i % 10) + 1, note=f'Note for user {i}')
#         for i in range(1, 11)
#     ]
#
#     # Add data to the session
#     db.session.add_all(users)
#     db.session.add_all(characters)
#     db.session.add_all(character_lists)
#     # db.session.add_all(user_character_statuses)
#     db.session.add_all(user_notes)
#
#     # Commit the session
#     db.session.commit()
#
# print("Dummy data added successfully.")
#
#
# class CharacterList(db.Model):
#     __tablename__ = 'character_list'
#
#     id: so.Mapped[int] = so.mapped_column(primary_key=True)
#     name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=False, nullable=False)
#     is_admin_created: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=False)
#     user_id: so.Mapped[Optional[int]] = so.mapped_column(sa.ForeignKey('user.id'), nullable=True)
#     parent_list_id: so.Mapped[Optional[int]] = so.mapped_column(sa.ForeignKey('character_list.id'), nullable=True)
#
#     # Relationships
#     character_mappings: so.Mapped[List['CharacterListMapping']] = so.relationship('CharacterListMapping',
#                                                                                   back_populates='character_list')
#     user: so.Mapped[Optional['User']] = so.relationship('User', back_populates='character_lists')
#     parent_list: so.Mapped[Optional['CharacterList']] = so.relationship('CharacterList', remote_side=[id],
#                                                                         back_populates='child_lists')
#     child_lists: so.Mapped[List['CharacterList']] = so.relationship('CharacterList', back_populates='parent_list')
#     characters: so.Mapped[List['ChineseCharacter']] = so.relationship('ChineseCharacter',
#                                                                       secondary='character_list_mapping', viewonly=True)
#
#     def __repr__(self):
#         return f'<CharacterList {self.name}>'
#
#
#
#
#
class UserNote(db.Model):
    __tablename__ = 'user_note'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('user.id'))
    character_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('chinese_character.id'))
    note: so.Mapped[str] = so.mapped_column(sa.String(200), nullable=False)

    # Relationships
    user: so.Mapped['User'] = so.relationship('User', back_populates='notes')
    character: so.Mapped['ChineseCharacter'] = so.relationship('ChineseCharacter', back_populates='notes')

    def __repr__(self):
        return f'<UserNote {self.user_id}-{self.character_id}>'

