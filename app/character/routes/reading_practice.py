from flask import render_template

from app.character import character
from app.character.services import lists_service


@character.route('/reading_practice/<int:list_id>')
def reading_practice(list_id):
    characters = lists_service.get_characters_by_list_id(list_id)
    return render_template('reading_practice.html',
                           title='Reading Practice', characters=characters)
