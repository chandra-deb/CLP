from flask import render_template

from app.character import character
from app.character.services import lists_service


# Revise 1
# !! This codes also works well
@character.route('/add_chars_to_list/<int:list_id>', methods=['GET'])
def add_chars_to_list(list_id):
    return render_template('add_characters_to_list.html', list_id=list_id)
