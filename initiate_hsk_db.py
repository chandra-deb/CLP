import hsk1
from app import app, db
from app.models import ChineseCharacter, CharacterListMapping

with app.app_context():
    db.create_all()

    for level in range(1, 2):
        if level == 1:
            words = hsk1.words
        # elif level == 2:
        #     words = hsk2.words
        # elif level == 3:
        #     words = hsk3.words
        # elif level == 4:
        #     word = hsk4.words
        # elif level == 5:
        #     words = hsk5.words
        # elif level == 6:
        #     words = hsk6.words

        for char in words:
            # print(char['id'])
            translations = ''
            for translation in char['translations']:
                translations += translation + ', '
            character = ChineseCharacter(
                id=char['id'],
                character=char['hanzi'],
                pinyin=char['pinyin'],
                meaning=translations[0],
            )
            clm = CharacterListMapping(character_list_id=3, character_id=char['id'])
            db.session.add(character)
            db.session.add(clm)


    db.session.commit()
