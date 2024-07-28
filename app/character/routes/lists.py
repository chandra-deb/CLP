from flask import render_template

from app.character import character
from app.character.services import lists_service


# Revise 1
# !! This codes also works well
@character.route('/lists')
def lists():
    top_level_user_lists = lists_service.get_top_level_user_lists()
    top_level_premade_lists = lists_service.get_top_level_premade_lists()

    return render_template('lists.html', user_lists=top_level_user_lists, premade_lists=top_level_premade_lists)


