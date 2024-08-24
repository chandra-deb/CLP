from random import choice

from flask import render_template, session

from app.character import character
from app.character.services import lists_service

never_studied_ten_chars = 'never_studied_ten_chars'
has_chars = 'has_chars'


class NevSd:
    def __init__(self, id: int, char: str, pinyin: str, meaning: str):
        self.id = id
        self.character = char
        self.pinyin = pinyin
        self.meaning = meaning

    def to_dict(self):
        return {'id': self.id, 'character': self.character, 'pinyin': self.pinyin, 'meaning': self.meaning}

    @staticmethod
    def from_dict(data):
        return NevSd(data['id'], data['character'], data['pinyin'], data['meaning'])


@character.route('/study/new/<int:list_id>')
def sns(list_id):
    session.clear()
    if 'never_studied_ten_chars' not in session:
        session['never_studied_ten_chars'] = []
    if 'has_chars' not in session:
        session['has_chars'] = False

    if not session[has_chars]:
        chars = [NevSd(char.id, char.character, char.pinyin, char.meaning) for char in
                 lists_service.get_ten_never_studied_chars(list_id)]
        print(chars[0].to_dict())
    if len(session[never_studied_ten_chars]) == 0 and session[has_chars] == False:
        session[never_studied_ten_chars] = [char_detail.to_dict() for char_detail in chars]
        session[has_chars] = True
    try:
        chars_temp = session[never_studied_ten_chars]
        char = chars_temp.pop()
        print('Char')
        print(char)
        lists_service.update_memory_strength([{'character_id': char['id'], 'is_correct': True}])
        session['never_studied_ten_chars'] = chars_temp
        # print(session['never_studied_ten_chars'])
    except IndexError:
        session.clear()
        return render_template('study_report.html', title='Session Report')
    return render_template('study_never_studied.html', title='Practice Never Studied', character=char, list_id=list_id)


