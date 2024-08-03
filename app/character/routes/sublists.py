from flask import render_template
from flask_login import current_user

from app.character import character
from app.character.services import lists_service


@character.route('/lists/<int:list_id>')
def sublists(list_id):
    # Parent lists
    parents = lists_service.get_all_parent_lists(list_id)
    current_list = lists_service.get_list_by_id(list_id)
    never_learned_chars = lists_service.get_never_studied_chars_of_list(list_id)
    strong_chars, weak_chars = lists_service.get_strong_weak_chars(current_user.id, list_id)
    if current_list is None:
        return 'List not found', 404
    child_lists = current_list.child_lists
    characters = current_list.characters
    return render_template('sublists.html', list=current_list, child_lists=child_lists,
                           characters=characters, parents=parents,
                           never_learned_chars=never_learned_chars,
                           strong_chars=strong_chars,
                           weak_chars=weak_chars)
