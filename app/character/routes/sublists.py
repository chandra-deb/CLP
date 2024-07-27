from flask import render_template
from flask_login import current_user

from app.character import character
from app.models import CharacterList


@character.route('/lists/<path:list_path>')
def sublists(list_path):
    print(list_path)
    list_path_parts = list_path.split('/')
    current_list = CharacterList.query.filter_by(name=list_path_parts[0], parent_list=None,
                                                 # user_id=current_user.id
                                                 ).first()
    if current_list is None:
        return 'List not found', 404
    list_path_so_far = [list_path_parts[0]]
    print(list_path_so_far)
    for part in list_path_parts[1:]:
        current_list = CharacterList.query.filter_by(name=part, parent_list=current_list,
                                                     # user_id=current_user.id
                                                     ).first()
        if current_list is None:
            return 'List not found', 404

        list_path_so_far.append(part)
    sublists = current_list.child_lists
    list_path_so_far.pop(len(list_path_so_far) - 1)
    print(list_path_so_far)
    characters = current_list.characters
    return render_template('sublists.html', list=current_list, sublists=sublists, characters=characters,
                           list_path=list_path, list_path_so_far=list_path_so_far)