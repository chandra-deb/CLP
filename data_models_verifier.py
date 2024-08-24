from app import app, db
from app.models import *
from sqlalchemy.sql import select

with app.app_context():
    # Create some users
    # user1 = User(username='katie', email='katie@example.com')
    # user1.set_password('password1')
    # db.session.add(user1)
    #
    # user2 = User(username='fasao', email='fasao@example.com')
    # user2.set_password('password2')
    # db.session.add(user2)
    #
    # # Create some Chinese characters
    # character1 = ChineseCharacter(character='PIng', pinyin='yi1')
    # db.session.add(character1)
    #
    # character2 = ChineseCharacter(character='Jingl', pinyin='er4')
    # db.session.add(character2)
    #
    # character3 = ChineseCharacter(character='NOdlj', pinyin='san1')
    # db.session.add(character3)
    #
    # # Create some character lists
    # list1 = CharacterList(name='last list', user=user1)
    # db.session.add(list1)
    #
    # list2 = CharacterList(name='mast list', user=user2)
    # db.session.add(list2)
    #
    # # Add characters to lists
    # mapping1 = CharacterListMapping(character_list=list1, character=character1)
    # db.session.add(mapping1)
    #
    # mapping2 = CharacterListMapping(character_list=list1, character=character2)
    # db.session.add(mapping2)
    #
    # mapping3 = CharacterListMapping(character_list=list2, character=character3)
    # db.session.add(mapping3)
    #
    # # Commit the changes
    # db.session.commit()

    lists = db.session.scalars(select(CharacterList).where(CharacterList.is_admin_created == True)).all()

    # Get the character lists for user1
    # lists = user.character_lists
    for list in lists:
        print(list.name)

    # Get the characters in list1
    # characters = list1.characters
    # for character in characters:
    #     print(character.character)
