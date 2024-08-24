from random import choice

from sqlalchemy import select

from app import app, db
from app.models import User, ChineseCharacter, UserCharacterStatus, CharacterList, UserNote

# Create the application instance

with app.app_context():

    list_id = 80  # Replace with the ID of the list you want to get characters from
    list_characters = db.session.scalars(
        select(ChineseCharacter).join(CharacterList.characters).where(CharacterList.id == list_id)).all()

    for character in list_characters:
        print(f"Character: {character.character}, Pinyin: {character.pinyin}")
    # Create some Chinese characters
    # char1 = ChineseCharacter(character="好", pinyin="hao3")
    # char2 = ChineseCharacter(character="人", pinyin="ren2")
    # char3 = ChineseCharacter(character="大", pinyin="da4")
    # char4 = ChineseCharacter(character="小", pinyin="xiao3")
    # char5 = ChineseCharacter(character="水", pinyin="shui3")
    #
    # db.session.add(char1)
    # db.session.add(char2)
    # db.session.add(char3)
    # db.session.add(char4)
    # db.session.add(char5)

    # Create premade lists
    # list1 = CharacterList(name="HSK 4", is_admin_created=True)
    # list2 = CharacterList(name="HSK 5", is_admin_created=True)
    # list3 = CharacterList(name="HSK 6", is_admin_created=True)
    #
    # all_characters = db.session.scalars(select(ChineseCharacter)).all()
    #
    # # Add characters to lists
    # list1.characters.append(choice(all_characters))
    # list1.characters.append(choice(all_characters))
    #
    # list2.characters.append(choice(all_characters))
    # list2.characters.append(choice(all_characters))
    #
    # list3.characters.append(choice(all_characters))
    # list3.characters.append(choice(all_characters))
    # list3.characters.append(choice(all_characters))
    #
    # # Add lists to the session
    # db.session.add(list1)
    # db.session.add(list2)
    # db.session.add(list3)
    #
    # # Commit the changes
    # db.session.commit()
    #
    # print("Done")

    # Dummy data for User
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
#         CharacterList(name=f'List {i}', is_admin_created=(i % 2 == 0))  # Alternating between admin and user
#         for i in range(1, 11)
#     ]
#
#     # Dummy data for UserCharacterStatus
#     s = ['mastered', 'assumed', 'learning']
#     user_character_statuses = [
#         UserCharacterStatus(user_id=(i % 10) + 1, character_id=(i % 10) + 1, status=choice(s))
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
# Create some Chinese characters
# char1 = ChineseCharacter(character="", pinyin="hao3")
# char2 = ChineseCharacter(character="", pinyin="ren2")
# char3 = ChineseCharacter(character="", pinyin="da4")
# char4 = ChineseCharacter(character="", pinyin="xiao3")
# char5 = ChineseCharacter(character="", pinyin="shui3")
#
# # Create premade lists
# list1 = CharacterList(name="List 1", is_admin_created=True)
# list2 = CharacterList(name="List 2", is_admin_created=True)
# list3 = CharacterList(name="List 3", is_admin_created=True)
#
# # Add characters to lists
# list1.characters.append(char1)
# list1.characters.append(char2)
#
# list2.characters.append(char2)
# list2.characters.append(char3)
#
# list3.characters.append(char1)
# list3.characters.append(char4)
# list3.characters.append(char5)
#
# # Add lists to the session
# db.session.add(list1)
# db.session.add(list2)
# db.session.add(list3)
#
# # Commit the changes
# db.session.commit()
